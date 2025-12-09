# executor/executor_core.py

from .playwright_actions import PlaywrightExecutor

# ------------------------------
# Standard Response Builder
# ------------------------------
def build_executor_response(html=None, screenshot=None, intent=None):
    return {
        "status": "ok",
        "html": html,
        "screenshot": screenshot,
        "intent": intent
    }


class ExecutorCore:
    def __init__(self):
        self.executor = PlaywrightExecutor()

    async def start(self):
        await self.executor.start()

    async def run(self, planner_action: dict):
        """
        planner_action example:
        {
            "action": "goto",
            "url": "https://example.com",
            "intent": {...}
        }
        """

        action = planner_action.get("action")
        intent = planner_action.get("intent")

        html = None
        screenshot_path = None

        # ---------------------------
        # Action Routing
        # ---------------------------

        if action == "goto":
            url = planner_action.get("url")
            html = await self.executor.goto_page(url)

        elif action == "click":
            selector = planner_action.get("selector")
            html = await self.executor.click_element(selector)

        elif action == "extract_dom":
            html = await self.executor.extract_dom()

        elif action == "screenshot":
            screenshot_path = await self.executor.screenshot()

        else:
            return { "status": "error", "message": f"Unknown action: {action}" }

        # ---------------------------
        # Build Executor → Perceptor response
        # ---------------------------
        return build_executor_response(
            html=html,
            screenshot=screenshot_path,
            intent=intent
        )

    async def stop(self):
        await self.executor.close()
