from playwright.sync_api import sync_playwright
import os
from pages.login_page import LoginPage
from utils.config import Config

def before_all(context):
    """Setup browser and login once before all scenarios"""
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(
        headless=False, slow_mo=1500,
        args=['--start-maximized']
    )
    context.context = context.browser.new_context(no_viewport=True)
    
    # Check if tracing should be enabled
    context._trace_on = os.getenv("TRACE_ON", "false").lower() in ("1", "true", "yes")
    
    context.page = context.context.new_page()
    
    # Login as precondition - happens once for all scenarios
    login_page = LoginPage(context.page)
    login_page.open(Config.BASE_URL)
    login_page.dismiss_popup_if_present()
    login_page.click_get_started()
    login_page.click_continue_with_email()
    login_page.login(Config.USERNAME_INPUT, Config.PASSWORD_INPUT)
    login_page.wait_for_home_page()
    print("Login completed - ready to run scenarios")

def before_scenario(context, scenario):
    """Start tracing for each scenario if enabled"""
    try:
        if context._trace_on:
            context.context.tracing.start(screenshots=True, snapshots=True, sources=True)
            context._trace_enabled = True
        else:
            context._trace_enabled = False
    except Exception:
        context._trace_enabled = False

def after_scenario(context, scenario):
    """Stop tracing and save trace file for each scenario"""
    try:
        if getattr(context, "_trace_enabled", False):
            traces_dir = os.path.join(os.getcwd(), "reports", "traces")
            os.makedirs(traces_dir, exist_ok=True)
            # sanitize scenario name for filename
            name = "".join(c if c.isalnum() or c in (" ","-","_") else "_" for c in scenario.name).strip().replace(" ","_")
            trace_file = os.path.join(traces_dir, f"{name}.zip")
            context.context.tracing.stop(path=trace_file)
    except Exception:
        pass

def after_all(context):
    """Logout and cleanup browser once after all scenarios"""
    try:
        login_page = LoginPage(context.page)
        login_page.logout()
        print("Logout completed")
    except Exception as e:
        print(f"Logout failed: {e}")
    
    try:
        context.context.close()
        context.browser.close()
        context.playwright.stop()
    except Exception as e:
        print(f"Browser cleanup failed: {e}")
