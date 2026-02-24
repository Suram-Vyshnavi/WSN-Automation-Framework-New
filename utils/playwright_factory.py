from playwright.sync_api import sync_playwright
from config.env_config import HEADLESS

class PlaywrightFactory:
    def start(self):
        pw = sync_playwright().start()
        browser = pw.chromium.launch(
            headless=HEADLESS,
            args=[
                '--use-fake-ui-for-media-stream',
                '--use-fake-device-for-media-stream'
            ]
        )
        context = browser.new_context(permissions=[])
        page = context.new_page()
        
        return pw, browser, context, page
