# Ad-Hoc API
An [Archytas](https://github.com/jataware/archytas) tool that eses LLMs to interact with APIs given documentation. User explains what they want in plain english, and then the agent (using the APIs docs for context) writes python code to complete the task.

## Installation
```bash
pip install adhoc-api
```

## Usage

This is designed to be paired with an Archytas agent. You may omit the python tool, and the agent should instead return the source code to you rather than running it.

```python
from adhoc_api import AdHocAPI
from archytas.react import ReActAgent, FailedTaskError
from archytas.tools import PythonTool
from easyrepl import REPL

def main():
    python = PythonTool()
    adhoc_api = AdhocApi(run_code=python.run)
    tools = [adhoc_api, python]
    agent = ReActAgent(model='gpt-4o', tools=tools, verbose=True)

    # REPL to interact with agent
    for query in REPL(history_file='.chat'):
        try:
            answer = agent.react(query)
            print(answer)
        except FailedTaskError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
```