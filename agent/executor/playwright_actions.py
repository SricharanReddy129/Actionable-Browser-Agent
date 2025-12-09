# executor/executor_core.py

from executor.playwright_actions import PlaywrightExecutor


class ExecutorCore:
    """
    Executor receives ACTIONS from the Planner:
    {
        "action": "goto" | "click" | "extract_dom" | "screenshot",
        "url": "...",
        "selector": "...",
        "intent": {...}
    }

    The Executor performs actions using Playwright
    and returns raw observation to Perceptor:
    {
        "status": "ok",
        "html": "...",
        "screenshot": null,
        "intent": {...}
    }
    """

    def __init__(self):
        self.engine = PlaywrightExecutor()

    async def start(self):
        await self.engine.start()

    async def run(self, planner_action: dict):
        action = planner_action.get("action")
        intent = planner_action.get("intent")

        html = None
        screenshot = None

        # -------------------------
        # Action Routing
        # -------------------------
        if action == "goto":
            url = planner_action.get("url")
            html = await self.engine.goto_page(url)

        elif action == "click":
            selector = planner_action.get("selector")
            html = await self.engine.click_element(selector)

        elif action == "extract_dom":
            html = await self.engine.extract_dom()

        elif action == "screenshot":
            screenshot = await self.engine.screenshot()

        else:
            return {
                "status": "error",
                "message": f"Unknown action '{action}'",
                "intent": intent
            }

        # -------------------------
        # Standard Raw Output
        # -------------------------
        return {
            "status": "ok",
            "html": html,
            "screenshot": screenshot,
            "intent": intent
        }

    async def stop(self):
        await self.engine.stop()
