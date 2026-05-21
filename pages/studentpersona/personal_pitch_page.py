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
