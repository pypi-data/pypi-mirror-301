from archytas.react import ReActAgent, FailedTaskError
from archytas.tools import PythonTool
from easyrepl import REPL
from .tool import AdhocApi

import pdb

def main():
    python = PythonTool()
    adhoc_api = AdhocApi(run_code=python.run)

    tools = [adhoc_api, python]
    agent = ReActAgent(model='gpt-4o', tools=tools, verbose=True)
    print(agent.prompt)

    # REPL to interact with agent
    for query in REPL(history_file='.chat'):
        try:
            answer = agent.react(query)
            print(answer)
        except FailedTaskError as e:
            print(f"Error: {e}")




if __name__ == "__main__":
    main()

