from typing import List, Dict
from playwright.sync_api import sync_playwright

from .base_scraper import BaseScraper
from .utils import get_random_user_agent

class Browse(BaseScraper):
    def __init__(self, url):
        super().__init__(url)
        self.browser = None
        self.page = None
        self.headless_actions: List[Dict] = []

    def get_html(self) -> str:
        if self.html is None:
            self.html = self.headless_scrape()
        return self.html

    def headless_scrape(self) -> str:
        with sync_playwright() as p:
            print("Starting headless Chromium browser...")
            self.browser = p.chromium.launch(
                headless=False,
                args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage', '--disable-blink-features=AutomationControlled'],
            )
            context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent=get_random_user_agent(),
                locale='en-US',
                timezone_id='America/New_York',
                geolocation={'latitude': 40.7128, 'longitude': -74.0060},
                permissions=['geolocation'],
            )

            try:
                self.page = context.new_page()

                # Apply resource blocking
                # self.page.route("**/*", self.block_resources)

                self.page.goto(self.url, wait_until="networkidle", timeout=100000)

                for action in self.headless_actions:
                    self.perform_action(action)

                self.page.wait_for_timeout(1000)

                try:
                    self.page.click(".sc-gFqAkR")
                except:
                    pass

                # wait for networkidle
                self.page.wait_for_timeout(20000)

                # Scroll to the bottom of the page in a human-like manner
                last_height = self.page.evaluate('document.body.scrollHeight')
                scroll_count = 0
                while True:
                    # Scroll down to bottom
                    self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                    # Wait to load page
                    self.page.wait_for_timeout(2000)
                    # Calculate new scroll height and compare with last scroll height
                    new_height = self.page.evaluate('document.body.scrollHeight')
                    if new_height == last_height:
                        break
                    last_height = new_height
                    # Save the page as PDF after each scroll
                    self.page.screenshot(path=f'scroll_{scroll_count}.png')
                    scroll_count += 1
                    # Add some randomness to scrolling behavior
                    self.page.wait_for_timeout(1000 + (scroll_count * 500))

                content = self.page.content()
                return content
            except Exception as e:
                print(f"An error occurred during headless scraping: {str(e)}")
                raise
            finally:
                if self.browser:
                    self.browser.close()

    def block_resources(self, route):
        if route.request.resource_type in ["stylesheet", "image", "media", "font"]:
            route.abort()
        else:
            route.continue_()

    def perform_action(self, action: Dict):
        if action["action"] == "entering":
            self.page.press(action["selector"], "Tab")
            self.page.press(action["selector"], "Enter")
        elif action["action"] == "typing":
            self.page.type(action["selector"], action["text"], delay=10)
        elif action["action"] == "click":
            self.page.click(action["selector"])
        self.page.wait_for_timeout(500)

    def entering(self, selector: str):
        self.headless_actions.append({"action": "entering", "selector": selector})
        return self

    def typing(self, selector: str, text: str):
        self.headless_actions.append({"action": "typing", "selector": selector, "text": text})
        return self

    def click(self, selector: str):
        self.headless_actions.append({"action": "click", "selector": selector})
        return self