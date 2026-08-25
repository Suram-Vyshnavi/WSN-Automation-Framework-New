from pages.base_page import BasePage, LONG_TIMEOUT
from locators.common_locators.common_login_locators import CommonLoginLocators
from utils.logger import log
from locators.xpath import UPPER


class CommonLoginPage(BasePage):
    """Login actions shared by every persona.

    The login screen renders slightly differently per environment/persona, so
    each control is resolved through a small ordered list of selectors: the
    persona's own locator first, then generic fallbacks.
    """

    DEFAULT_TIMEOUT = LONG_TIMEOUT

    DISMISS_POPUP_SELECTORS = ["//button[normalize-space()=\"I'll do it later\"]"]

    _UPPER = f"{UPPER}"
    LOGIN_ERROR_SELECTORS = [
        f"//*[contains({_UPPER}, 'INVALID') or contains({_UPPER}, 'INCORRECT') "
        f"or contains({_UPPER}, 'EXPIRED') or contains({_UPPER}, 'LOCKED')]",
        "//div[contains(@class,'error') or contains(@class,'alert')]",
    ]

    def __init__(self, page, login_locators=None):
        super().__init__(page)
        self.login_locators = login_locators or CommonLoginLocators

    def _next_button_selectors(self):
        return [
            self.login_locators.NEXT_BUTTON,
            "//button[.//span[normalize-space()='Next'] or normalize-space()='Next']",
            f"//button[contains({UPPER}, 'NEXT')]",
            "//button[@type='submit']",
        ]

    def _password_selectors(self):
        return [
            self.login_locators.PASSWORD,
            "//input[@type='password']",
            "//input[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'password')]",
            "//input[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'password')]",
        ]

    def _submit_selectors(self):
        return [
            self.login_locators.SUBMIT_BUTTON,
            "//button[.//span[normalize-space()='Submit'] or normalize-space()='Submit']",
            f"//button[contains({UPPER}, 'SIGN IN')]",
            f"//button[contains({UPPER}, 'LOGIN')]",
            "//button[@type='submit']",
        ]

    def open(self, url):
        """Navigate to the application landing page."""
        self.open_url(url)

    def dismiss_popup_if_present(self):
        """Close the optional 'enable notifications' prompt."""
        self.dismiss_if_present(self.DISMISS_POPUP_SELECTORS, "Login notification popup", timeout=2500)

    def click_get_started(self):
        """Click the Get Started button on the guest landing page."""
        self.validate_text(self.login_locators.GET_STARTED_BUTTON, "get started")
        self.click(self.login_locators.GET_STARTED_BUTTON, "Get Started button")

    def click_continue_with_email(self):
        """Choose the email login option."""
        self.validate_text(self.login_locators.LOGIN_BUTTON, "continue with email")
        self.click(self.login_locators.LOGIN_BUTTON, "Continue with Email button")

    def login(self, username, password):
        """Enter the credentials and submit the login form.

        Credentials are never logged - only the outcome of each stage is.
        """
        self.enter_text(self.login_locators.USERNAME, username, "email address")
        self.click_required(self._next_button_selectors(), "Next button", timeout=7000)

        password_field = self.first_visible(self._password_selectors(), timeout=7000)
        assert password_field is not None, "Password input is not visible/editable in login flow"
        password_field.fill(password)
        log.info("Entered *** in password field")

        self.click_required(self._submit_selectors(), "Submit button", timeout=7000)

    def validate_login_successful(self, timeout=15000):
        """Assert the login flow navigated away from the login page.

        When it did not, the visible login error is read first so the failure
        message says *why* (invalid/expired/locked account) instead of only
        reporting the URL.
        """
        try:
            self.page.wait_for_function(
                "() => !window.location.href.toLowerCase().includes('login')", timeout=timeout)
        except Exception as _ignored:
            log.debug("Optional step in validate_login_successful() did not apply: %s", _ignored)

        if "login" not in self.current_url().lower():
            log.info("Login successful - navigated away from the login page")
            return

        error_element = self.first_visible(self.LOGIN_ERROR_SELECTORS, timeout=1500)
        error_message = error_element.inner_text().strip() if error_element else ""
        detail = f" Login page error: {error_message}" if error_message else ""
        raise AssertionError(
            f"Login appears unsuccessful. Current URL: {self.current_url()}.{detail}")
