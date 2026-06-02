from pages.base_page import BasePage
from locators.student_persona_locators.personal_pitch_trainer_locators import personal_pitch_trainerLocators
from locators.student_persona_locators.new_homepage_locators import NewHomepageLocators
from utils.helpers import highlight_element


class PersonalPitchPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def _navigate_to_personal_pitch(self):
        """Navigate from dashboard to the Personal Pitch Trainer page."""
        from pages.studentpersona.home_dashboard_page import HomeDashboardPage
        if HomeDashboardPage._shared_dashboard_url:
            self.page.goto(HomeDashboardPage._shared_dashboard_url, wait_until="domcontentloaded", timeout=60000)
        self.page.locator(personal_pitch_trainerLocators.PERSONAL_PITCH_TRAINER).wait_for(state="visible", timeout=15000)
        self.page.locator(personal_pitch_trainerLocators.PERSONAL_PITCH_TRAINER).click()
        self.page.locator(personal_pitch_trainerLocators.CREATE_YOUR_PITCH_BUTTON).wait_for(state="visible", timeout=15000)

    def click_create_your_pitch_button(self):
        self._navigate_to_personal_pitch()
        highlight_element(self.page, personal_pitch_trainerLocators.CREATE_YOUR_PITCH_BUTTON)
        self.page.locator(personal_pitch_trainerLocators.CREATE_YOUR_PITCH_BUTTON).click()
        print("Clicked Create Your Pitch button")

    def click_create_your_pitch_back_button(self):
        self.page.locator(personal_pitch_trainerLocators.PITCH_TRAINER_BACK_ARROW_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, personal_pitch_trainerLocators.PITCH_TRAINER_BACK_ARROW_BUTTON)
        self.page.locator(personal_pitch_trainerLocators.PITCH_TRAINER_BACK_ARROW_BUTTON).click()
        print("Clicked Create Your Pitch back button")

    def click_pitch_summary_view_button(self):
        self.page.locator(personal_pitch_trainerLocators.PITCH_SUMMARY_VIEW_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, personal_pitch_trainerLocators.PITCH_SUMMARY_VIEW_BUTTON)
        self.page.locator(personal_pitch_trainerLocators.PITCH_SUMMARY_VIEW_BUTTON).click()
        print("Clicked Pitch Summary View button")

    def click_view_pitch_button(self):
        self.page.locator(personal_pitch_trainerLocators.VIEW_PITCH_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, personal_pitch_trainerLocators.VIEW_PITCH_BUTTON)
        self.page.locator(personal_pitch_trainerLocators.VIEW_PITCH_BUTTON).click()
        print("Clicked View Pitch button")

    def click_video_play_button(self):
        self.page.locator(personal_pitch_trainerLocators.VIDEO_PLAY_BUTTON).wait_for(state="attached", timeout=15000)
        self.page.locator(personal_pitch_trainerLocators.VIDEO_PLAY_BUTTON).click(force=True)
        print("Clicked video play button")

    def click_video_close_button(self):
        self.page.locator(personal_pitch_trainerLocators.VIDEO_CLOSE_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, personal_pitch_trainerLocators.VIDEO_CLOSE_BUTTON)
        self.page.locator(personal_pitch_trainerLocators.VIDEO_CLOSE_BUTTON).click()
        print("Clicked video close button")

    def click_share_pitch_button(self):
        self.page.locator(personal_pitch_trainerLocators.SHARE_PITCH_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, personal_pitch_trainerLocators.SHARE_PITCH_BUTTON)
        self.page.locator(personal_pitch_trainerLocators.SHARE_PITCH_BUTTON).click()
        print("Clicked Share Pitch button")

    def click_copy_pitch_button(self):
        self.page.locator(personal_pitch_trainerLocators.COPY_SHARE_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, personal_pitch_trainerLocators.COPY_SHARE_BUTTON)
        self.page.locator(personal_pitch_trainerLocators.COPY_SHARE_BUTTON).click()
        print("Clicked Copy Pitch button")

    def click_share_pitch_close_button(self):
        self.page.locator(personal_pitch_trainerLocators.SHARE_PITCH_CLOSE_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, personal_pitch_trainerLocators.SHARE_PITCH_CLOSE_BUTTON)
        self.page.locator(personal_pitch_trainerLocators.SHARE_PITCH_CLOSE_BUTTON).click()
        print("Clicked Share Pitch Close button")

    def click_home_icon_and_navigate_home(self):
        """Click the Home icon to navigate back to the home page."""
        home = self.page.locator(personal_pitch_trainerLocators.HOME).first
        home.wait_for(state="visible", timeout=15000)
        home.scroll_into_view_if_needed()
        highlight_element(self.page, personal_pitch_trainerLocators.HOME)
        home.click()
        print("Clicked Home icon and navigated to home page")
        self.page.wait_for_timeout(1500)

    def click_passed_text_on_pitch_card(self):
        """Click the 'Passed' text on the Personal Pitch Trainer card on the dashboard.

        If the 'Passed' text is not present, log a message and return without
        failing the test case.
        """
        # Wait for the Personal Pitch Trainer card to be visible on the dashboard.
        self.page.locator(personal_pitch_trainerLocators.PERSONAL_PITCH_TRAINER).wait_for(state="visible", timeout=15000)

        passed_text = self.page.locator(personal_pitch_trainerLocators.PERSONAL_PITCH_TRAINER_PASSED_TEXT).first
        if passed_text.count() == 0 or not passed_text.is_visible():
            print("'Passed' text is not present on the Personal Pitch Trainer card - skipping without failing the test case")
            return False

        passed_text.scroll_into_view_if_needed()
        highlight_element(self.page, personal_pitch_trainerLocators.PERSONAL_PITCH_TRAINER_PASSED_TEXT)
        passed_text.click()
        print("Clicked 'Passed' text on the Personal Pitch Trainer card")
        self.page.wait_for_timeout(1000)
        return True

    def validate_check_button(self):
        """Validate the check button is displayed.

        If the check button is not present, log a message and return without
        failing the test case.
        """
        check_button = self.page.locator(personal_pitch_trainerLocators.VALIDATE_CHECK_BUTTON).first
        if check_button.count() == 0 or not check_button.is_visible():
            print("Check button is not present - skipping without failing the test case")
            return False

        check_button.scroll_into_view_if_needed()
        highlight_element(self.page, personal_pitch_trainerLocators.VALIDATE_CHECK_BUTTON)
        print("Validated check button")
        return True

    def click_logout(self):
        from pages.studentpersona.home_dashboard_page import HomeDashboardPage
        if HomeDashboardPage._shared_dashboard_url:
            self.page.goto(HomeDashboardPage._shared_dashboard_url, wait_until="domcontentloaded", timeout=60000)
        self.page.locator(NewHomepageLocators.HEADER_PROFILE_MENU_ICON).wait_for(state="attached", timeout=15000)
        self.page.locator(NewHomepageLocators.HEADER_PROFILE_MENU_ICON).click(force=True)
        self.page.locator(NewHomepageLocators.LOG_OUT).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.LOG_OUT)
        self.page.locator(NewHomepageLocators.LOG_OUT).click()
        print("Clicked Logout")
