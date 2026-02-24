import sys
import pathlib
import os
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from utils.playwright_factory import PlaywrightFactory
from utils.config import Config

factory = PlaywrightFactory()
pw, browser, context, page = factory.start()
try:
    page.goto(Config.BASE_URL)
    page.wait_for_load_state("networkidle")
    html = page.content()
    pathlib.Path("debug_page.html").write_text(html, encoding="utf-8")
    page.screenshot(path="debug_page.png", full_page=True)
    print("Saved debug_page.html and debug_page.png")
finally:
    context.close()
    browser.close()
    pw.stop()
