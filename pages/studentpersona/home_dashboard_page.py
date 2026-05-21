from pages.base_page import BasePage
from locators.student_persona_locators.new_homepage_locators import NewHomepageLocators
from utils.helpers import attach_screenshot, highlight_element


class HomeDashboardPage(BasePage):

    _shared_dashboard_url = None  # class-level: survives across step instances

    def __init__(self, page):
        super().__init__(page)

    def _capture_dashboard_url(self):
        """Store current URL as the shared dashboard URL if not already set."""
        if not HomeDashboardPage._shared_dashboard_url:
            HomeDashboardPage._shared_dashboard_url = self.page.url

    def _return_to_dashboard(self):
        """Navigate back to the stored dashboard URL and wait for cards to render."""
        self.page.goto(HomeDashboardPage._shared_dashboard_url, wait_until="domcontentloaded", timeout=60000)
        self.page.locator(NewHomepageLocators.COURSES_CARD).wait_for(state="visible", timeout=20000)

    def validate_home_icon(self):
        locator = self.page.locator(NewHomepageLocators.HOME)
        locator.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.HOME)
        assert locator.count() > 0, "Home icon not found on the dashboard"
        self._capture_dashboard_url()
        print("Home icon validated")

    def validate_welcome_and_wadhwani_header(self):
        welcome = self.page.locator(NewHomepageLocators.VALIDATE_WELCOME_HEADER)
        welcome.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.VALIDATE_WELCOME_HEADER)
        assert welcome.count() > 0, "Welcome header not found"

        wadhwani = self.page.locator(NewHomepageLocators.VALIDATE_WADHWANI_SKILLING_HEADER)
        wadhwani.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.VALIDATE_WADHWANI_SKILLING_HEADER)
        assert wadhwani.count() > 0, "Wadhwani Skilling header not found"
        print("Welcome and Wadhwani Skilling headers validated")

    def click_courses_card(self):
        self._capture_dashboard_url()
        self.page.locator(NewHomepageLocators.COURSES_CARD).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.COURSES_CARD)
        self.page.locator(NewHomepageLocators.COURSES_CARD).click()
        print("Clicked Courses card")
        self._return_to_dashboard()

    def click_programs_card(self):
        self._capture_dashboard_url()
        self.page.locator(NewHomepageLocators.PROGRAMS_CARD).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.PROGRAMS_CARD)
        self.page.locator(NewHomepageLocators.PROGRAMS_CARD).click()
        print("Clicked Programs card")
        self._return_to_dashboard()

    def click_personal_pitch_trainer_card(self):
        self._capture_dashboard_url()
        self.page.locator(NewHomepageLocators.PERSONAL_PITCH_TRAINER).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.PERSONAL_PITCH_TRAINER)
        self.page.locator(NewHomepageLocators.PERSONAL_PITCH_TRAINER).click()
        print("Clicked Personal Pitch Trainer card")
        self._return_to_dashboard()

    def click_interview_coach_card(self):
        self._capture_dashboard_url()
        self.page.locator(NewHomepageLocators.INTERVIEW_COACH).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.INTERVIEW_COACH)
        self.page.locator(NewHomepageLocators.INTERVIEW_COACH).click()
        print("Clicked Interview Coach card")
        self._return_to_dashboard()

    def click_forums_card(self):
        self._capture_dashboard_url()
        self.page.locator(NewHomepageLocators.FORUMS_CARD).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.FORUMS_CARD)
        self.page.locator(NewHomepageLocators.FORUMS_CARD).click()
        print("Clicked Forums card")
        self._return_to_dashboard()

    def click_my_career_advisor_card(self):
        self._capture_dashboard_url()
        self.page.locator(NewHomepageLocators.MY_CAREER_ADVISOR_CARD).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.MY_CAREER_ADVISOR_CARD)
        self.page.locator(NewHomepageLocators.MY_CAREER_ADVISOR_CARD).click()
        print("Clicked My Career Advisor card")
        self._return_to_dashboard()

    def click_career_buddy_card(self):
        self._capture_dashboard_url()
        self.page.locator(NewHomepageLocators.CARRER_BUDDY_CARD).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.CARRER_BUDDY_CARD)
        self.page.locator(NewHomepageLocators.CARRER_BUDDY_CARD).click()
        print("Clicked Career Buddy card")
        self._return_to_dashboard()

    def click_jobs_connect_card(self):
        self._capture_dashboard_url()
        self.page.locator(NewHomepageLocators.JOBS_CONNECT_CARD).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.JOBS_CONNECT_CARD)
        self.page.locator(NewHomepageLocators.JOBS_CONNECT_CARD).click()
        print("Clicked Jobs Connect card")
        self._return_to_dashboard()

    def click_menu_help_icon(self):
        parent_page = self.page
        self.page.locator(NewHomepageLocators.MENU_HELP_ICON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.MENU_HELP_ICON)
        with self.page.expect_popup() as popup_info:
         self.page.locator(NewHomepageLocators.MENU_HELP_ICON).click()

        child_page = popup_info.value
        child_page.wait_for_load_state()
        print("Clicked Menu Help icon")
        # Close new tab
        child_page.close()
        # Switch back to original tab
        parent_page.bring_to_front()

    def click_notification_icon(self):
        self.page.locator(NewHomepageLocators.NOTIFICATION_ICON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.NOTIFICATION_ICON)
        self.page.locator(NewHomepageLocators.NOTIFICATION_ICON).click()
        self.page.locator(NewHomepageLocators.HEADER_PROFILE_MENU_ICON).wait_for(state="visible", timeout=15000)  # Wait for profile icon to ensure notification panel is loaded
        print("Clicked Notification icon")

    def click_profile_icon(self):
        self.page.locator(NewHomepageLocators.PROFILE_ICON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.PROFILE_ICON)
        self.page.locator(NewHomepageLocators.PROFILE_ICON).click()
        print("Clicked Profile icon")

    def click_header_profile_menu_icon(self):
        self.page.locator(NewHomepageLocators.HEADER_PROFILE_MENU_ICON).wait_for(state="attached", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.HEADER_PROFILE_MENU_ICON)
        self.page.locator(NewHomepageLocators.HEADER_PROFILE_MENU_ICON).click(force=True)
        print("Clicked Header Profile Menu icon")

    def click_calendar(self):
        self.page.locator(NewHomepageLocators.HEADER_PROFILE_MENU_ICON).wait_for(state="attached", timeout=15000)
        self.page.locator(NewHomepageLocators.HEADER_PROFILE_MENU_ICON).click(force=True)
        self.page.locator(NewHomepageLocators.CALENDAR).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.CALENDAR)
        self.page.locator(NewHomepageLocators.CALENDAR).click()
        print("Clicked Calendar")

    def click_messages_and_discussions(self):
        self._return_to_dashboard()
        self.page.locator(NewHomepageLocators.HEADER_PROFILE_MENU_ICON).wait_for(state="attached", timeout=15000)
        self.page.locator(NewHomepageLocators.HEADER_PROFILE_MENU_ICON).click(force=True)
        self.page.locator(NewHomepageLocators.MESSAGES_AND_DISCUSSIONS).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.MESSAGES_AND_DISCUSSIONS)
        self.page.locator(NewHomepageLocators.MESSAGES_AND_DISCUSSIONS).click()
        print("Clicked Messages & Discussions")

    def click_learning_progress(self):
        self._return_to_dashboard()
        self.page.locator(NewHomepageLocators.HEADER_PROFILE_MENU_ICON).wait_for(state="attached", timeout=15000)
        self.page.locator(NewHomepageLocators.HEADER_PROFILE_MENU_ICON).click(force=True)
        self.page.locator(NewHomepageLocators.LEARNING_PROGRESS).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.LEARNING_PROGRESS)
        self.page.locator(NewHomepageLocators.LEARNING_PROGRESS).click()
        print("Clicked Learning Progress")

    def click_settings(self):
        self._return_to_dashboard()
        self.page.locator(NewHomepageLocators.HEADER_PROFILE_MENU_ICON).wait_for(state="attached", timeout=15000)
        self.page.locator(NewHomepageLocators.HEADER_PROFILE_MENU_ICON).click(force=True)
        self.page.locator(NewHomepageLocators.SETTINGS).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.SETTINGS)
        self.page.locator(NewHomepageLocators.SETTINGS).click()
        print("Clicked Settings")

    def click_log_out(self):
        self._return_to_dashboard()
        self.page.locator(NewHomepageLocators.HEADER_PROFILE_MENU_ICON).wait_for(state="attached", timeout=15000)
        self.page.locator(NewHomepageLocators.HEADER_PROFILE_MENU_ICON).click(force=True)
        self.page.locator(NewHomepageLocators.LOG_OUT).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.LOG_OUT)
        self.page.locator(NewHomepageLocators.LOG_OUT).click()
        print("Clicked Logout")
