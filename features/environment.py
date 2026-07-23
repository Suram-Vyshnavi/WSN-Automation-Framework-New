from playwright.sync_api import sync_playwright
import os
from pages.login_page import LoginPage
from utils.config import Config

def before_all(context):
    """Setup browser and login once before all scenarios"""
    persona = Config.get_persona()
    context.persona = persona

    slow_mo_ms = int(os.getenv("SLOW_MO", "0"))
    headless = os.getenv("HEADLESS", "false").lower() in ("1", "true", "yes")

    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(
        headless=headless, slow_mo=slow_mo_ms,
        args=[
            '--start-maximized',
            '--use-fake-ui-for-media-stream',  # Auto-deny camera/mic prompts
            '--use-fake-device-for-media-stream'  # Use fake device instead of prompting
        ]
    )
    context.context = context.browser.new_context(
        no_viewport=True,
        permissions=[]  # Deny all permissions (camera, microphone, notifications, etc.)
    )
    # Check if tracing should be enabled
    context._trace_on = os.getenv("TRACE_ON", "false").lower() in ("1", "true", "yes")
    
    context.page = context.context.new_page()

    username, password = Config.get_credentials(persona)

    # Login as precondition - happens once for all scenarios.
    # Keep student persona on the existing student login page object flow.
    if persona == "student":
        login_page = LoginPage(context.page)
        login_page.open(Config.BASE_URL)
        login_page.dismiss_popup_if_present()
        login_page.click_get_started()
        login_page.click_continue_with_email()
        login_page.login(username, password)
        login_page.wait_for_home_page()
    else:
        from locators.Common_locators.common_login_locators import CommonLoginLocators
        from pages.Common_pages.Login_page import CommonLoginPage

        context.login_locators = CommonLoginLocators
        login_page = CommonLoginPage(context.page, login_locators=context.login_locators)
        login_page.open(Config.BASE_URL)
        login_page.dismiss_popup_if_present()
        login_page.click_get_started()
        login_page.click_continue_with_email()
        login_page.login(username, password)
        context.page.wait_for_load_state("networkidle", timeout=15000)
        # Wait until browser navigates away from the login page
        context.page.wait_for_function(
            "() => !window.location.href.includes('login')",
            timeout=20000
        )

    print(f"Login completed for persona '{persona}' - ready to run scenarios")

def _ensure_live_page(context):
    """Guarantee context.page points at a usable page.

    A scenario can crash the Chromium tab (or the whole context), after which
    every later scenario would fail with 'Target page, context or browser has
    been closed' because re-login kept reusing the dead page. Recreate the page
    — and the context if that is gone too — so one crash no longer cascades into
    the rest of the run.
    """
    try:
        if getattr(context, "page", None) is not None and not context.page.is_closed():
            return True
    except Exception:
        pass

    # Page is dead: try a fresh page in the existing context first.
    try:
        context.page = context.context.new_page()
        return True
    except Exception:
        pass

    # Context/browser is gone too: rebuild the context (and a page) from scratch.
    try:
        context.context = context.browser.new_context(no_viewport=True, permissions=[])
        context.page = context.context.new_page()
        return True
    except Exception as e:
        print(f"Could not recreate a live page after crash: {e}")
        return False


def _re_login(context):
    """Re-login after session loss (e.g. after logout step) or a tab crash."""
    persona = getattr(context, 'persona', 'student')
    username, password = Config.get_credentials(persona)
    if not _ensure_live_page(context):
        print("Re-login aborted: no live page/browser available")
        return
    try:
        from locators.student_locators.login_locators import LoginLocators
        login_page = LoginPage(context.page)
        login_page.open(Config.BASE_URL)
        login_page.dismiss_popup_if_present()

        # If the session is still authenticated, opening the guest URL just
        # redirects to the home dashboard and there is no "Get Started" button —
        # don't waste 20s waiting for it (and don't log a spurious failure).
        # Treat that as already-logged-in and return.
        try:
            context.page.locator(LoginLocators.GET_STARTED_BUTTON).wait_for(state="visible", timeout=5000)
        except Exception:
            print(f"Session still authenticated (persona={persona}) — skipping full re-login")
            return

        login_page.click_get_started()
        login_page.click_continue_with_email()
        login_page.login(username, password)
        login_page.wait_for_home_page()
        print(f"Re-login successful for scenario (persona={persona})")
    except Exception as e:
        print(f"Re-login failed: {e}")


def _student_go_home(context):
    """Return the student to the home dashboard in the SAME tab — no logout/login.

    The student new-dashboard scenarios keep a valid session across scenarios, so
    re-logging in is both unnecessary and flaky. Navigating to the stored home URL
    (or BASE_URL, which redirects to /home when authenticated) reliably lands on
    home so menu-based scenarios (Learning Progress, Settings) find the Accounts
    menu — all within one tab.
    """
    try:
        from pages.studentpersona.home_dashboard_page import HomeDashboardPage
        url = HomeDashboardPage._shared_dashboard_url
        if not url:
            base = Config.BASE_URL or ""
            # BASE_URL is the /guest landing; the authenticated dashboard is /home.
            url = base.replace("/guest", "/home") if "/guest" in base else base

        # A prior scenario can leave a stray tab open (courses/pitch/certificate
        # open in a new tab). Close them so context.page is the only/front tab and
        # the next scenario doesn't act on a background page.
        try:
            for pg in list(context.context.pages):
                if pg is not context.page and not pg.is_closed():
                    pg.close()
        except Exception:
            pass

        # Navigate home, then confirm the header actually rendered before handing
        # the page to the next scenario. A bare goto used to be enough, but when a
        # previous scenario left a modal/drawer open (e.g. notifications panel) or
        # got stuck mid-SPA, that overlay intercepts the next scenario's first
        # click on the Accounts menu / notification icon — cascading a single
        # broken scenario into a run of "menu is not visible/clickable" failures.
        # Reload once, then re-login as a last resort, so the corruption can't leak.
        accounts_menu = "//button[@aria-label='Accounts menu']"
        # The "Help us personalize your journey" popup re-appears whenever the
        # dashboard is (re)loaded and overlays the header, intercepting the next
        # scenario's first click. Dismiss it after every navigation.
        personalize_popup = (
            "//*[contains(normalize-space(),'personalize your journey') "
            "or contains(normalize-space(),'personalise your journey')]"
        )
        for _ in range(2):
            context.page.goto(url, wait_until="domcontentloaded", timeout=60000)
            context.page.wait_for_timeout(1000)
            # Dismiss any leftover modal/drawer that would intercept header clicks.
            try:
                context.page.keyboard.press("Escape")
            except Exception:
                pass
            # Explicitly close the personalize-journey popup if it rendered.
            popup_visible = False
            try:
                popup_visible = context.page.locator(personalize_popup).first.is_visible()
                if popup_visible:
                    for close_sel in [
                        "//div[contains(@class,'ant-modal')]//button[contains(@class,'ant-modal-close')]",
                        "//button[normalize-space()='Skip' or normalize-space()='Maybe Later' or normalize-space()='Close' or normalize-space()='No, Thanks']",
                    ]:
                        try:
                            context.page.locator(close_sel).first.click(timeout=1500)
                            break
                        except Exception:
                            continue
                    context.page.wait_for_timeout(500)
                    popup_visible = context.page.locator(personalize_popup).first.is_visible()
            except Exception:
                pass

            # Only hand off once the header is reachable AND the popup is no longer
            # overlaying it; otherwise reload (a refresh reliably clears the popup).
            try:
                context.page.locator(accounts_menu).first.wait_for(state="visible", timeout=8000)
                if not popup_visible:
                    return  # Home is ready with a reachable, unobstructed header.
            except Exception:
                pass
            # Retry with a fresh navigation (also clears a stuck popup).

        # Header never appeared after navigate + reload — the session is likely
        # logged out or the view crashed. Re-login for a guaranteed clean state.
        print("Student home header not reachable after reload — re-logging in")
        _re_login(context)
    except Exception as e:
        print(f"Student home navigation issue: {e}")


def before_scenario(context, scenario):
    """Navigate back to home dashboard before each scenario, then start tracing if enabled"""
    # Step 0: If a prior scenario crashed the tab/context, rebuild it and
    # re-login immediately so the rest of the run is not lost to a cascade of
    # 'Target page, context or browser has been closed' errors.
    page_dead = True
    try:
        page_dead = getattr(context, 'page', None) is None or context.page.is_closed()
    except Exception:
        page_dead = True
    if page_dead:
        if _ensure_live_page(context):
            _re_login(context)
        # Skip the home-navigation block below: a fresh login already lands home.
        try:
            if context._trace_on:
                context.context.tracing.start(screenshots=True, snapshots=True, sources=True)
                context._trace_enabled = True
            else:
                context._trace_enabled = False
        except Exception:
            context._trace_enabled = False
        return

    if getattr(context, 'page', None) is not None:
        # Step 1: Dismiss any open modal/dialog by pressing Escape
        try:
            context.page.keyboard.press("Escape")
        except Exception:
            pass

        # Student new-dashboard: never logout/login between scenarios. Just return
        # to the home dashboard in the same tab so the menu-based scenarios work.
        if getattr(context, 'persona', 'student') == 'student':
            _student_go_home(context)
        else:
            _before_scenario_other_personas(context)

    try:
        if context._trace_on:
            context.context.tracing.start(screenshots=True, snapshots=True, sources=True)
            context._trace_enabled = True
        else:
            context._trace_enabled = False
    except Exception:
        context._trace_enabled = False


def _before_scenario_other_personas(context):
    """Home-reset + re-login recovery for non-student personas (faculty/rm/…)."""
    # Check if we've been logged out (e.g. by a logout step)
    try:
        current_url = context.page.url
    except Exception:
        current_url = ""

    logged_out = any(x in current_url for x in ('login', '/guest', 'sign-in', 'signin'))
    if logged_out:
        _re_login(context)
        return

    # Navigate to home dashboard via the HOME nav button
    try:
        from locators.student_locators.login_locators import LoginLocators
        home_btn = context.page.locator(LoginLocators.HOME_BUTTON)
        home_btn.wait_for(state="visible", timeout=8000)
        home_btn.click()
        context.page.wait_for_load_state("domcontentloaded", timeout=10000)
    except Exception:
        pass

    # Verify the home dashboard actually rendered. A prior scenario that died
    # deep in a sub-view can leave the Home button unreachable, so confirm the
    # Accounts-menu entry point is present; if not, re-login for a clean state.
    try:
        context.page.locator(
            "//button[@aria-label='Accounts menu']"
        ).first.wait_for(state="visible", timeout=8000)
    except Exception:
        _re_login(context)


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
    """Cleanup browser once after all scenarios"""
    try:
        context.context.close()
        context.browser.close()
        context.playwright.stop()
    except Exception:
        pass
