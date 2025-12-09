from playwright.async_api import async_playwright

class PlaywrightExecutor:
    def __init__(self):
        self.browser = None
        self.page = None
        self.pw = None

    async def start(self, headless=True):
        """Start Playwright browser instance."""
        self.pw = await async_playwright().start()
        self.browser = await self.pw.chromium.launch(headless=headless)
        self.page = await self.browser.new_page()

    async def goto_page(self, url: str):
        """Navigate to a URL and return the DOM."""
        await self.page.goto(url)
        return await self.page.content()

    async def click_element(self, selector: str):
        """Click an element and return updated DOM."""
        await self.page.click(selector)
        return await self.page.content()

    async def extract_dom(self):
        """Return current DOM content."""
        return await self.page.content()

    async def screenshot(self, path="page.png"):
        """Take a screenshot and return the file path."""
        await self.page.screenshot(path=path)
        return path

    async def stop(self):
        if self.browser:
            await self.browser.close()
        if self.pw:
            await self.pw.stop()