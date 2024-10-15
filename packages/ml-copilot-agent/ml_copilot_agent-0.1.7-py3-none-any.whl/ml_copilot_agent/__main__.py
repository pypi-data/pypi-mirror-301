# ml_copilot_agent/__main__.py

import asyncio
import sys

from .workflow import MLWorkflow
from . import initialize
from llama_index.utils.workflow import draw_all_possible_flows

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m ml_copilot_agent <OPENAI_API_KEY>")
        sys.exit(1)
    api_key = sys.argv[1]
    initialize(api_key)

    async def run_workflow():
        workflow = MLWorkflow(timeout=600, verbose=True)
        draw_all_possible_flows(workflow, filename="MLCopilot_workflow.html")
        await workflow.run()
    
    asyncio.run(run_workflow())

if __name__ == "__main__":
    main()
