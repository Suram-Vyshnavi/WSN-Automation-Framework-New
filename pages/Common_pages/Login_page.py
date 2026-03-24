from pages.base_page import BasePage
from locators.Common_locators.common_login_locators import CommonLoginLocators


class CommonLoginPage(BasePage):
    """Common login actions shared across personas."""

    def __init__(self, page, login_locators=None):
        super().__init__(page)
        self.login_locators = login_locators or CommonLoginLocators

    def use_login_locators(self, login_locators):
        """Switch login locator class when a persona needs specific locators."""
        self.login_locators = login_locators or CommonLoginLocators

    def open(self, url):
        """Navigate to the login page"""
        self.page.goto(url)

    def dismiss_popup_if_present(self):
        """Dismiss notification popup if present"""
        try:
            later_btn = self.page.locator("//button[normalize-space()=\"I'll do it later\"]")
            later_btn.wait_for(state="attached", timeout=2500)
            later_btn.click(force=True)
            print("Popup dismissed")
        except Exception:
            print("Popup not found / already dismissed")

    def click_get_started(self):
        """Click Get Started button"""
        self.page.locator(self.login_locators.GET_STARTED_BUTTON).wait_for(state="visible", timeout=20000)
        self.validate_using_inner_text(self.login_locators.GET_STARTED_BUTTON, "get started")
        self.page.click(self.login_locators.GET_STARTED_BUTTON)
        

    def click_continue_with_email(self):
        """Click Continue with Email/Login button"""
        self.page.locator(self.login_locators.LOGIN_BUTTON).wait_for(state="visible", timeout=20000)
        self.validate_using_inner_text(self.login_locators.LOGIN_BUTTON, "continue with email")
        self.page.click(self.login_locators.LOGIN_BUTTON)

    def login(self, username, password):
        """Enter username and password and submit login form"""
        self.page.locator(self.login_locators.USERNAME).wait_for(state="visible", timeout=20000)
        self.page.fill(self.login_locators.USERNAME, username)

        next_clicked = False
        next_selectors = [
            self.login_locators.NEXT_BUTTON,
            "//button[.//span[normalize-space()='Next'] or normalize-space()='Next']",
            "//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NEXT')]",
            "//button[@type='submit']",
        ]
        for selector in next_selectors:
            locator = self.page.locator(selector).first
            try:
                locator.wait_for(state="visible", timeout=7000)
                locator.click()
                next_clicked = True
                break
            except Exception:
                continue

        if not next_clicked:
            raise AssertionError("Unable to click Next button in login flow")

        password_filled = False
        password_selectors = [
            self.login_locators.PASSWORD,
            "//input[@type='password']",
            "//input[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'password')]",
            "//input[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'password')]",
        ]

        for selector in password_selectors:
            locator = self.page.locator(selector).first
            try:
                locator.wait_for(state="visible", timeout=7000)
                locator.fill(password)
                password_filled = True
                break
            except Exception:
                continue

        if not password_filled:
            raise AssertionError("Password input is not visible/editable in login flow")

        submit_clicked = False
        submit_selectors = [
            self.login_locators.SUBMIT_BUTTON,
            "//button[.//span[normalize-space()='Submit'] or normalize-space()='Submit']",
            "//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SIGN IN')]",
            "//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'LOGIN')]",
            "//button[@type='submit']",
        ]
        for selector in submit_selectors:
            locator = self.page.locator(selector).first
            try:
                locator.wait_for(state="visible", timeout=7000)
                locator.click()
                submit_clicked = True
                break
            except Exception:
                continue

        if not submit_clicked:
            raise AssertionError("Unable to click Submit/Sign in button in login flow")


# Backward-compatible alias if callers still import LoginPage from this module.
class LoginPage(CommonLoginPage):
    pass
