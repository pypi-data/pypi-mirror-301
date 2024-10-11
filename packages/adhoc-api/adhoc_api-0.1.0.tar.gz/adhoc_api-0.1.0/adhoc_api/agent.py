import copy
import yaml
from google import generativeai as genai
from google.generativeai import caching
import pathlib
import datetime
from archytas.agent import Agent

import os
from pathlib import Path
from typing import Callable


import pdb

here = Path(__file__).resolve().parent



def simple_info(info: dict):
    print('INFO', info)

def simple_error(error: dict):
    print('ERROR', error)




class GeminiDrafter:
    def __init__(self, info: Callable[[dict], None]=simple_info, error: Callable[[dict], None]=simple_error):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.cache = APICache(f'{here}/api_agent.yaml')
        self.info = info
        self.error = error

    def draft_request(self, api: str, query: str) -> str:
        """Using Gemini, draft source code to make a request to the specified API that fulfills the query."""
        self.info({'api': api, 'goal': query})

        if api not in self.cache.loaded_apis():
            self.info({'cache': f'api is not loaded: {api}'})
            if api not in self.cache.available_apis():
                self.info({'cache': f'api does not exist: {api}'})
                return f"The selected API was not in the following list: {self.cache.available_apis()}. Please use one of those."
            self.info({'cache': f'loading api: {api}'})
            self.cache.load_api(api)
        
        try:
            agent_response = self.cache.chats[api].send_message(query).text
            prefixes = ['```python', '```']
            suffixes = ['```', '```\n']
            for prefix in prefixes:
                if agent_response.startswith(prefix):
                    agent_response = agent_response[len(prefix):]
            for suffix in suffixes:
                if agent_response.endswith(suffix):
                    agent_response = agent_response[:-len(suffix)]
            agent_response = '\n'.join([
                'import pandas as pd',
                'import os',
                'import json',
                'import requests',
                agent_response
            ])
        except Exception as e:
            self.error({'error': str(e)})
            return f"The agent failed to produce valid code: {str(e)}"
        
        return agent_response



class GPTCodeFinalizer:
    def __init__(self, info: Callable[[dict], None]=simple_info, error: Callable[[dict], None]=simple_error):
        self.cache = APICache(f'{here}/api_agent.yaml')
        self.info = info
        self.error = error

    async def proofread_code(self, api: str, code: str, agent: Agent) -> str:
        """Proofreads the code, making syntax corrections, and adjusting according to specific notes about the API"""
        transformed_code = code
        syntax_check_prompt: str = self.cache.config.get('syntax_check_prompt','')
        
        if syntax_check_prompt != '':
            transformed_code = await agent.query(syntax_check_prompt.format(code=transformed_code))
            if transformed_code.strip() != code.strip():
                self.info({
                    "message": "GPT has changed the code output from Gemini in the syntax fix step.", 
                    "gpt": transformed_code, 
                    "gemini": code}
                )

        additional_pass_prompt: str = self.cache.cache[api].get('gpt_additional_pass', '')
        if additional_pass_prompt != '':
            prior_code = transformed_code
            transformed_code = await agent.query(
                additional_pass_prompt.format(code=transformed_code)
                                      .format_map(self.cache.cache[api])
            )
            if transformed_code.strip() != prior_code.strip():
                self.info({
                    "message": "GPT has changed the code output from Gemini or the syntax check in the additional pass step.", 
                    "gpt": transformed_code, 
                    "prior": prior_code}
                )
        return transformed_code

# requires gemini API key initialization done beforehand
class APICache:

    def __init__(self, api_definition_filepath: str, info: Callable[[dict], None]=simple_info, error: Callable[[dict], None]=simple_error):
        self.cache: dict[str, dict] = {}
        self.chats: dict[str, genai.ChatSession] = {}
        self.models: dict[str, genai.GenerativeModel] = {}
        self.config: dict[str, dict] = {}
        self.info = info
        self.error = error

        with open(api_definition_filepath, 'r') as f:
            try:
                contents = yaml.safe_load(f)
                self.config = contents['config']
                api_definitions = contents['apis']
            except Exception as e:
                print(f"failed to load API definitions file properly. check filepath and/or format: {str(e)}")
                return
        self.cache['default'] = dict(api_definitions['default'])
        for api_name, definition in api_definitions.items():
            if api_name == 'default':
                continue
            
            # merge w/ overwriting defaults
            self.cache[api_name] = copy.deepcopy(self.cache['default'])
            for key, value in definition.items():
                if isinstance(value, str | int | list | bool):
                    self.cache[api_name][key] = value
                elif isinstance(value, dict):
                    self.cache[api_name][key] |= value
            
            if self.cache[api_name]['disabled']:
                del self.cache[api_name]
                continue 

            # fill docs body
            try:
                root_folder = pathlib.Path(__file__).resolve().parent
                filepath = '/'.join([
                    str(root_folder),
                    self.config["documentation_root"],
                    self.cache[api_name]["documentation_file"]
                ])
                with open(filepath, 'r') as f:
                    self.cache[api_name]['docs'] = f.read()
            except Exception as e:
                raise ValueError(f"failed to open docs for api {api_name}: file path {self.cache[api_name]['documentation_file']}: {str(e)}")
            
            # formatting interpolations - don't format API docs though.
            self.cache[api_name] = {
                k: v.format_map(self.cache[api_name]) 
                    if isinstance(v, str) else v
                for k, v in self.cache[api_name].items() 
                    if k not in self.config['deferred_formatting_fields'] 
            }
        del self.cache['default']

    def available_apis(self) -> dict[str, str]:
        """Returns a mapping of available APIs to their descriptions and full, human readable names."""
        return {key: f"{self.cache[key]['name']}: {self.cache[key]['description']}" for key in self.cache.keys()}

    def available_api_context(self) -> str:
        """Nicer formatting for a system prompt of APIs and their descriptions."""
        return "\n".join([f'    - {k}: {v}' for k, v in self.available_apis().items()])

    def loaded_apis(self):
        """Returns a list of loaded APIs."""
        return self.chats.keys()

    def load_api(self, api_name: str):
        if api_name not in self.available_apis():
            raise ValueError("requested API is not in available APIs - check definitions file and API name")
        content = caching.CachedContent.list()
        is_cached = False
        for cache_object in content: 
            if cache_object.display_name == self.cache[api_name]['cache']['key']:
                is_cached = True
                self.info({'cache': f'found cached content for {api_name}'})
                break
        if not is_cached:
            cache_object = self.build_cache(api_name)
        self.models[api_name] = genai.GenerativeModel.from_cached_content(cached_content=cache_object)
        self.chats[api_name] = self.models[api_name].start_chat()

    def build_cache(self, api_name):
        if api_name not in self.available_apis():
            raise ValueError("requested API is not in available APIs - check definitions file and API name")
        self.info({'cache': f'building cache for {api_name}'})
        api = self.cache[api_name]
        cache = caching.CachedContent.create(
            model=api['cache']['model'],
            display_name=api['cache']['key'],
            contents=[api['cache_body']],
            ttl=datetime.timedelta(minutes=api['cache']['ttl']),
            system_instruction=api['system_prompt']
        )
        return cache