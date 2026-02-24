from playwright.sync_api import sync_playwright
from config.env_config import HEADLESS
class PlaywrightFactory:
    def start(self):
        pw=sync_playwright().start()
        browser=pw.chromium.launch(headless=HEADLESS)
        context=browser.new_context()
        page=context.new_page()
        
        return pw,browser,context,page
