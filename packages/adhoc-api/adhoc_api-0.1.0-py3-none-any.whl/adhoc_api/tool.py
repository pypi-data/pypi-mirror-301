# import asyncio

from archytas.tool_utils import AgentRef, LoopControllerRef, ReactContextRef, tool
from .agent import GeminiDrafter, GPTCodeFinalizer
from pathlib import Path
from typing import Callable, Any

here = Path(__file__).resolve().parent


def simple_info(info: dict):
    print('INFO', info)

def simple_error(error: dict):
    print('ERROR', error)




class AdhocApi:
    def __init__(self, *, run_code: Callable[[str], Any]|None=None, info: Callable[[dict], None]=simple_info, error: Callable[[dict], None]=simple_error):
        self.info = info
        self.error = error
        self.run_code = run_code

        self.drafter = GeminiDrafter(info, error)
        self.finalizer = GPTCodeFinalizer(info, error)

    @tool
    async def list_apis(self) -> str:
        """
        This tool lists all the APIs available to you.

        Returns:
            str: A list of the APIs and descriptions
        """
        return self.drafter.cache.available_api_context()
    
    @tool
    async def use_api(self, api: str, goal: str, agent: AgentRef) -> str:#, loop: LoopControllerRef, react_context: ReactContextRef) -> str:
        """
        This tool provides interaction with external APIs with a second agent.
        You will query external APIs through this tool.
        Based on what that code returns and the user's goal, continue to interact with the API to get to that goal.

        The output will either be a summary of the code output or an error. 
        If it is an error, see if you can modify the code to get it to work, and try running it again.

        Consult the APIs available to you when specifying which to use.

        Args:
            api (str): The API to query. Must be one of the available APIs.
            goal (str): The task given to the second agent. If the user states the API is unauthenticated, relay that information here.
        Returns:
            str: A summary of the current step being run, along with the collected stdout, stderr, returned result, display_data items, and any
                 errors that may have occurred, or just an error.
              
        """
        draft_code = self.drafter.draft_request(api, goal)
        fixed_code = await self.finalizer.proofread_code(api, draft_code, agent)
        
        if self.run_code is None:
            return fixed_code

        try:
            evaluation = self.run_code(fixed_code)
        except Exception as e:
            self.error({'error': str(e)})
            return f"""
                The second agent failed to create valid code. Instruct it to rerun. The error was {str(e)}. The code will be provided for fixes or retry.
                """
        return evaluation