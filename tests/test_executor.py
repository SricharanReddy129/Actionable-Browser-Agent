import asyncio
import sys

# Fix Playwright subprocess issue on Windows
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import asyncio
from agent.executor.extractData_executor import ExecutorCore

async def test_executor():
    executor = ExecutorCore()

    # Start browser
    await executor.start()

    # Simulated planner instruction
    planner_action = {
        "action": "goto",
        "url": "https://gateway.fm/blog/tokenisation-of-deposits",
        "intent": {
            "goal": "test_fetch",
            "keywords": ["ai", "machine learning", 'distributed ledger systems', 'cryptocurrency']
        }
    }

    # Run executor
    result = await executor.run(planner_action)

    print("\n=== EXECUTOR OUTPUT ===")
    print(result)

    # Stop browser
    await executor.stop()


# Run test
asyncio.run(test_executor())
