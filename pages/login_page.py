from pages.common_pages.common_login_page import CommonLoginPage
from pages.base_page import LONG_TIMEOUT
from locators.student_locators.login_locators import LoginLocators
from locators.student_persona_locators.new_homepage_locators import NewHomepageLocators


class LoginPage(CommonLoginPage):
    """Student login flow.

    Shares the whole login sequence with `CommonLoginPage` and only adds the
    student-specific post-login checks and the logout entry point.
    """

    def __init__(self, page):
        super().__init__(page, login_locators=LoginLocators)

    def wait_for_home_page(self):
        """Confirm login landed on the authenticated home page."""
        self.validate_visible(LoginLocators.WADHWANI_LOGO, "Wadhwani logo on the home page",
                              timeout=LONG_TIMEOUT)

    def logout(self):
        """Open the header profile menu on the dashboard and log out."""
        from pages.student_persona.student_persona_page import StudentPersonaPage

        StudentPersonaPage(self.page).open_dashboard()
        self.click(NewHomepageLocators.HEADER_PROFILE_MENU_ICON, "header profile menu",
                   state="attached", force=True)
        self.click(NewHomepageLocators.LOG_OUT, "Logout")
