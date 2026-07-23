import os
from pages.base_page import BasePage
from locators.student_persona_locators.interview_coach_locators import interviewCoachLocators
from locators.student_persona_locators.new_homepage_locators import NewHomepageLocators
from utils.helpers import highlight_element


def _is_prod():
    return os.getenv("ENV", "").strip().lower() == "prod"


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

    def _on_question_page(self):
        """True when the IC card opened an existing role's question/journey page."""
        try:
            return self.page.locator(interviewCoachLocators.PITCH_TRAINER_BACK_ICON).first.is_visible()
        except Exception:
            return False

    def _go_back_to_roles_list(self):
        """Click the interview-coach back button to reach the Recent Roles list."""
        back = self.page.locator(interviewCoachLocators.PITCH_TRAINER_BACK_ICON).first
        back.wait_for(state="visible", timeout=10000)
        highlight_element(self.page, interviewCoachLocators.PITCH_TRAINER_BACK_ICON)
        back.click()
        self.page.wait_for_timeout(2000)

    def click_audio_button_image(self):
        # Prod opens an existing role's question page (no create flow). Go back
        # to the Recent Roles list instead of starting a new practice session.
        if _is_prod():
            if self._on_question_page():
                self._go_back_to_roles_list()
                print("Prod flow: question page detected, clicked back to Recent Roles list")
            else:
                print("Prod flow: already on Recent Roles list")
            return
        self.page.locator(interviewCoachLocators.AUDIO_BUTTON_IMAGE).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.AUDIO_BUTTON_IMAGE)
        self.page.locator(interviewCoachLocators.AUDIO_BUTTON_IMAGE).click()
        print("Clicked audio button image")

    def validate_textbox_and_mic_button(self):
        if _is_prod():
            print("Prod flow: skipping create-role textbox/mic validation")
            return
        textbox = self.page.locator(interviewCoachLocators.INTERVIEW_SEARCH_INPUT)
        textbox.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.INTERVIEW_SEARCH_INPUT)
        assert textbox.is_visible(), "Interview Coach textbox not visible"

        mic = self.page.locator(interviewCoachLocators.VALIDATE_MIC_BUTTON)
        mic.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.VALIDATE_MIC_BUTTON)
        assert mic.is_visible(), "Mic button not visible"
        print("Validated textbox and mic button in Interview Coach page")

    def _fill_textbox_and_send(self, text):
        textbox = self.page.locator(interviewCoachLocators.INTERVIEW_SEARCH_INPUT)
        textbox.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.INTERVIEW_SEARCH_INPUT)
        textbox.fill(text)
        send_icon = self.page.locator(interviewCoachLocators.INTERVIEW_COACH_SEND_ICON)
        send_icon.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.INTERVIEW_COACH_SEND_ICON)
        send_icon.click()
        print(f"Filled textbox with '{text}' and clicked send icon")

    def fill_textbox_and_click_send(self):
        if _is_prod():
            print("Prod flow: skipping create-role textbox send")
            return
        # First fill 'Product Manager' and send, then fill 'healthcare' and send
        self._fill_textbox_and_send("Product Manager")
        self._fill_textbox_and_send("healthcare")

    def click_practise_interviewing_for_role(self):
        if _is_prod():
            print("Prod flow: skipping Practise Interviewing")
            return
        self.page.locator(interviewCoachLocators.PRACTISE_INTERVIEW_BUTTON).wait_for(state="visible", timeout=20000)
        highlight_element(self.page, interviewCoachLocators.PRACTISE_INTERVIEW_BUTTON)
        self.page.locator(interviewCoachLocators.PRACTISE_INTERVIEW_BUTTON).click()
        print("Clicked Practise Interviewing for the role")

    def validate_start_button(self):
        if _is_prod():
            print("Prod flow: skipping Start button validation")
            return
        start = self.page.locator(interviewCoachLocators.START_BUTTON)
        start.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.START_BUTTON)
        assert start.is_visible(), "Start button not visible"
        print("Validated Start button")

    def click_pitch_trainer_back_icon(self):
        # On prod we already returned to the Recent Roles list in the audio step.
        # Only click back if we are somehow still on a question page.
        if _is_prod():
            try:
                recent_visible = self.page.locator(interviewCoachLocators.VALIDATE_YOUR_RECENT_ROLES_HEADER).first.is_visible()
            except Exception:
                recent_visible = False
            if not recent_visible and self._on_question_page():
                self._go_back_to_roles_list()
                print("Prod flow: clicked back to Recent Roles list")
            else:
                print("Prod flow: already on Recent Roles list, no back needed")
            return
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
        # On prod the delete step deletes every ongoing role (it opens each
        # role's three-dots menu itself), so make sure the Ongoing tab is active
        # here instead of opening a single menu.
        if _is_prod():
            try:
                ongoing_tab = self.page.locator(interviewCoachLocators.VALIDATE_ONGOING_HEADER).first
                if ongoing_tab.count() > 0:
                    ongoing_tab.click()
                    self.page.wait_for_timeout(1000)
                    print("Prod flow: selected Ongoing tab")
            except Exception as e:
                print(f"Prod flow: could not select Ongoing tab: {e}")
            return
        self.page.locator(interviewCoachLocators.THREEDOTS_MORE_DETAILS_ICON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.THREEDOTS_MORE_DETAILS_ICON)
        self.page.locator(interviewCoachLocators.THREEDOTS_MORE_DETAILS_ICON).click()
        print("Clicked three dots icon")

    def click_delete_role_and_confirm(self):
        if _is_prod():
            # Delete EVERY ongoing role so the run is repeatable. All actions stay
            # in the same tab. Re-query the three-dots each iteration since the
            # list shrinks after every deletion.
            deleted = 0
            for _ in range(20):  # safety cap against an infinite loop
                dots = self.page.locator(interviewCoachLocators.THREEDOTS_MORE_DETAILS_ICON)
                if dots.count() == 0:
                    break
                try:
                    dots.first.click()
                    delete_btn = self.page.locator(interviewCoachLocators.DELETE_ROLE_BUTTON).first
                    delete_btn.wait_for(state="visible", timeout=10000)
                    delete_btn.click()
                    confirm_btn = self.page.locator(interviewCoachLocators.DELETE_ROLE_CONFIRM_BUTTON).first
                    confirm_btn.wait_for(state="visible", timeout=10000)
                    confirm_btn.click()
                    self.page.wait_for_timeout(2000)
                    deleted += 1
                except Exception as e:
                    print(f"Stopped deleting ongoing roles after {deleted}: {e}")
                    break
            print(f"Prod flow: deleted {deleted} ongoing role(s)")
            return
        self.page.locator(interviewCoachLocators.DELETE_ROLE_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.DELETE_ROLE_BUTTON)
        self.page.locator(interviewCoachLocators.DELETE_ROLE_BUTTON).click()
        self.page.locator(interviewCoachLocators.DELETE_ROLE_CONFIRM_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, interviewCoachLocators.DELETE_ROLE_CONFIRM_BUTTON)
        self.page.locator(interviewCoachLocators.DELETE_ROLE_CONFIRM_BUTTON).click()
        print("Clicked Delete this role and confirmed")
