from pages.base_page import BasePage
from locators.student_persona_locators.interview_coach_locators import interviewCoachLocators
from locators.student_persona_locators.new_homepage_locators import NewHomepageLocators
from utils.helpers import highlight_element


class InterviewCoachPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def _navigate_to_interview_coach(self):
        """Navigate from dashboard to the Interview Coach page."""
        from pages.studentpersona.home_dashboard_page import HomeDashboardPage
        if HomeDashboardPage._shared_dashboard_url:
            self.page.goto(HomeDashboardPage._shared_dashboard_url, wait_until="domcontentloaded", timeout=60000)
        self.page.locator(interviewCoachLocators.INTERVIEW_COACH_CARD).wait_for(state="visible", timeout=15000)
        self.page.locator(interviewCoachLocators.INTERVIEW_COACH_CARD).click()
        print("Clicked Interview Coach card")

    def click_audio_button_image(self):
        self.page.locator(interviewCoachLocators.AUDIO_BUTTON_IMAGE).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.AUDIO_BUTTON_IMAGE)
        self.page.locator(interviewCoachLocators.AUDIO_BUTTON_IMAGE).click()
        print("Clicked audio button image")

    def validate_textbox_and_mic_button(self):
        textbox = self.page.locator(interviewCoachLocators.INTERVIEW_SEARCH_INPUT)
        textbox.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.INTERVIEW_SEARCH_INPUT)
        assert textbox.is_visible(), "Interview Coach textbox not visible"

        mic = self.page.locator(interviewCoachLocators.VALIDATE_MIC_BUTTON)
        mic.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.VALIDATE_MIC_BUTTON)
        assert mic.is_visible(), "Mic button not visible"
        print("Validated textbox and mic button in Interview Coach page")

    def fill_textbox_and_click_send(self):
        self.page.locator(interviewCoachLocators.INTERVIEW_SEARCH_INPUT).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.INTERVIEW_SEARCH_INPUT)
        self.page.locator(interviewCoachLocators.INTERVIEW_SEARCH_INPUT).fill("Product Manager")
        self.page.locator(interviewCoachLocators.INTERVIEW_COACH_SEND_ICON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.INTERVIEW_COACH_SEND_ICON)
        self.page.locator(interviewCoachLocators.INTERVIEW_COACH_SEND_ICON).click()
        print("Filled textbox with 'Product Manager' and clicked send icon")

    def click_practise_interviewing_for_role(self):
        self.page.locator(interviewCoachLocators.PRACTISE_INTERVIEW_BUTTON).wait_for(state="visible", timeout=20000)
        highlight_element(self.page, interviewCoachLocators.PRACTISE_INTERVIEW_BUTTON)
        self.page.locator(interviewCoachLocators.PRACTISE_INTERVIEW_BUTTON).click()
        print("Clicked Practise Interviewing for the role")

    def validate_start_button(self):
        start = self.page.locator(interviewCoachLocators.START_BUTTON)
        start.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.START_BUTTON)
        assert start.is_visible(), "Start button not visible"
        print("Validated Start button")

    def click_pitch_trainer_back_icon(self):
        self.page.locator(interviewCoachLocators.PITCH_TRAINER_BACK_ICON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.PITCH_TRAINER_BACK_ICON)
        self.page.locator(interviewCoachLocators.PITCH_TRAINER_BACK_ICON).click()
        print("Clicked pitch trainer back icon")

    def validate_your_recent_roles_header(self):
        header = self.page.locator(interviewCoachLocators.VALIDATE_YOUR_RECENT_ROLES_HEADER)
        header.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.VALIDATE_YOUR_RECENT_ROLES_HEADER)
        assert header.is_visible(), "Your Recent Roles header not visible"
        print("Validated Your Recent Roles header")

    def validate_ongoing_and_completed_headers(self):
        ongoing = self.page.locator(interviewCoachLocators.VALIDATE_ONGOING_HEADER)
        ongoing.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.VALIDATE_ONGOING_HEADER)
        assert ongoing.is_visible(), "Ongoing header not visible"

        completed = self.page.locator(interviewCoachLocators.VALIDATE_COMPLETED_HEADER)
        completed.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.VALIDATE_COMPLETED_HEADER)
        assert completed.is_visible(), "Completed header not visible"
        print("Validated Ongoing and Completed headers")

    def click_threedots_icon(self):
        self.page.locator(interviewCoachLocators.THREEDOTS_MORE_DETAILS_ICON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.THREEDOTS_MORE_DETAILS_ICON)
        self.page.locator(interviewCoachLocators.THREEDOTS_MORE_DETAILS_ICON).click()
        print("Clicked three dots icon")

    def click_delete_role_and_confirm(self):
        self.page.locator(interviewCoachLocators.DELETE_ROLE_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.DELETE_ROLE_BUTTON)
        self.page.locator(interviewCoachLocators.DELETE_ROLE_BUTTON).click()
        self.page.locator(interviewCoachLocators.DELETE_ROLE_CONFIRM_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.DELETE_ROLE_CONFIRM_BUTTON)
        self.page.locator(interviewCoachLocators.DELETE_ROLE_CONFIRM_BUTTON).click()
        print("Clicked Delete this role and confirmed")
