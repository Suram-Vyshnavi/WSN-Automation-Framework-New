from locators.student_locators.settings_delete_account_locators import SettingsDeleteAccountLocators
from locators.student_persona_locators.learning_progress_locators import LearningProgressLocators
from locators.student_persona_locators.messages_locators import MessagesAndDiscussionsLocators
from locators.student_persona_locators.new_homepage_locators import NewHomepageLocators
from pages.base_page import SHORT_TIMEOUT
from pages.student_persona.student_persona_page import CARD_TIMEOUT, StudentPersonaPage
from utils.helpers import attach_screenshot
from utils.logger import log

GENIE_TIMEOUT = 25000


class HomeDashboardPage(StudentPersonaPage):
    """The authenticated student home dashboard: feature cards + account menu."""

    def _return_to_dashboard(self):
        """Go back to the dashboard and wait until the cards have rendered."""
        self.capture_dashboard_url()
        self.open_dashboard(ready_locator=NewHomepageLocators.PROGRAMS_AND_COURSES_CARD)

    def _open_card_and_return(self, locator, description):
        """Open a dashboard feature card, then come back to the dashboard."""
        self.capture_dashboard_url()
        self.click(locator, description, timeout=CARD_TIMEOUT)
        self._return_to_dashboard()

    def _open_account_menu(self):
        """Open the header account (profile) menu, if it is not already open.

        The trigger is a toggle: clicking it while the dropdown is open closes
        it again. A step that runs straight after another menu step would
        otherwise silently shut the menu it needs.

        The trigger is only 'attached' - not 'visible' - until the header
        finishes animating, so it is waited for in that state and force-clicked.
        """
        if self.is_visible(NewHomepageLocators.ACCOUNT_MENU_ITEM, timeout=SHORT_TIMEOUT):
            log.info("Account menu is already open")
            return
        self.click(NewHomepageLocators.HEADER_PROFILE_MENU_ICON, "account menu",
                   timeout=CARD_TIMEOUT, state="attached", force=True)

    def _open_account_menu_item(self, locator, description, ready_locator, screenshot_name):
        """Open one entry of the account menu and confirm its page rendered."""
        self._return_to_dashboard()
        self._open_account_menu()
        self.click(locator, description, timeout=CARD_TIMEOUT)
        self.validate_visible(ready_locator, f"{description} page", timeout=CARD_TIMEOUT)
        attach_screenshot(self.page, screenshot_name)

    # ------------------------------------------------------------------
    # Dashboard validations
    # ------------------------------------------------------------------
    def validate_home_icon(self):
        self.validate_visible(NewHomepageLocators.HOME, "Home icon on the dashboard",
                              timeout=CARD_TIMEOUT)
        self.capture_dashboard_url()

    def validate_genie_ai(self):
        """Walk the Genie AI assistant: ask a question, rate it, browse history."""
        self.capture_dashboard_url()
        self.validate_visible(NewHomepageLocators.VALIDATE_GENIE_AI_BANNER, "Genie AI banner",
                              timeout=CARD_TIMEOUT)
        self.enter_text(NewHomepageLocators.GENIE_AI_SEARCH_INPUT, "Help me choose a career",
                        "Genie AI search box")
        self.click(NewHomepageLocators.SEND_ICON_ARROW, "Genie send arrow", timeout=GENIE_TIMEOUT)

        self.click(NewHomepageLocators.SPEAKER_SECTION, "Genie speaker section", timeout=GENIE_TIMEOUT)
        attach_screenshot(self.page, "Speaker Section Page")

        self.click(NewHomepageLocators.GENIE_RATING_BUTTON, "Genie rating button", timeout=GENIE_TIMEOUT)
        self.enter_text(NewHomepageLocators.ASK_YOUR_QUESTIONS_HERE_TEXTAREA,
                        "How to prepare for an interview?", "Genie question box")
        self.click(NewHomepageLocators.SEND_MSG_ICON, "Genie send message icon", timeout=GENIE_TIMEOUT)

        # Opening a conversation collapses the history sidebar, so expand it
        # before asserting on its contents.
        self.click(NewHomepageLocators.GENIE_SIDEBAR_TOGGLE, "Genie sidebar toggle",
                   timeout=GENIE_TIMEOUT)
        self.validate_visible(NewHomepageLocators.PREVIOUS_CHATS_HEADER, "Previous Chats header",
                              timeout=GENIE_TIMEOUT)
        self.validate_visible(NewHomepageLocators.GENIE_CHAT_HISTORY_ITEM,
                              "a previous chat in the history")
        attach_screenshot(self.page, "New Chat Page")

        self.click(NewHomepageLocators.SUBPAGE_BACK_BUTTON, "Genie back button", timeout=GENIE_TIMEOUT)
        attach_screenshot(self.page, "Back to Dashboard")
        self._return_to_dashboard()

    # ------------------------------------------------------------------
    # Feature cards
    # ------------------------------------------------------------------
    def click_programs_and_courses_card(self):
        self._open_card_and_return(NewHomepageLocators.PROGRAMS_AND_COURSES_CARD,
                                   "Programs & Courses card")

    def click_personal_pitch_trainer_card(self):
        self._open_card_and_return(NewHomepageLocators.PERSONAL_PITCH_TRAINER,
                                   "Personal Pitch Trainer card")

    def click_interview_coach_card(self):
        self._open_card_and_return(NewHomepageLocators.INTERVIEW_COACH, "Interview Coach card")

    def click_forums_card(self):
        self._open_card_and_return(NewHomepageLocators.FORUMS_CARD, "Forums card")

    def click_my_career_advisor_card(self):
        self._open_card_and_return(NewHomepageLocators.MY_CAREER_ADVISOR_CARD,
                                   "My Career Advisor card")

    def click_career_buddy_card(self):
        self._open_card_and_return(NewHomepageLocators.CARRER_BUDDY_CARD, "Career Buddy card")

    def click_jobs_connect_card(self):
        self._open_card_and_return(NewHomepageLocators.JOBS_CONNECT_CARD, "Jobs Connect card")

    # ------------------------------------------------------------------
    # Header icons
    # ------------------------------------------------------------------
    def click_menu_help_icon(self):
        """Help opens the support site in a new tab; close it and come back."""
        self.open_in_new_tab_and_close(NewHomepageLocators.MENU_HELP_ICON, "Menu Help icon",
                                       timeout=CARD_TIMEOUT)

    def click_notification_icon(self):
        self.click(NewHomepageLocators.NOTIFICATION_ICON, "Notification icon", timeout=CARD_TIMEOUT)
        # The profile icon re-rendering is the signal that the panel finished opening.
        self.wait_for_visible(NewHomepageLocators.HEADER_PROFILE_MENU_ICON, timeout=CARD_TIMEOUT)

    def click_profile_icon(self):
        self.click(NewHomepageLocators.PROFILE_ICON, "Profile icon", timeout=CARD_TIMEOUT)

    def click_header_profile_menu_icon(self):
        self._open_account_menu()

    def click_calendar(self):
        self._open_account_menu()
        self.click(NewHomepageLocators.CALENDAR, "Calendar", timeout=CARD_TIMEOUT)

    # ------------------------------------------------------------------
    # Account menu entries
    # ------------------------------------------------------------------
    def click_messages_and_discussions(self):
        self._open_account_menu_item(
            NewHomepageLocators.MESSAGES_AND_DISCUSSIONS, "Messages & Discussions",
            MessagesAndDiscussionsLocators.SEND_MESSAGE_BUTTON, "Messages and Discussions Page")
        self._return_to_dashboard()

    def click_learning_progress(self):
        # Deliberately stays on the Learning Progress page: the "Learning
        # progress validation" scenario continues from here. The dashboard smoke
        # test is unaffected because every other menu method returns home first.
        self._open_account_menu_item(
            NewHomepageLocators.LEARNING_PROGRESS, "Learning Progress",
            LearningProgressLocators.VALIDATE_LEARNING_PROGRESS, "Learning Progress Page")

    def click_settings(self):
        self._open_account_menu_item(
            NewHomepageLocators.SETTINGS, "Settings",
            SettingsDeleteAccountLocators.DELETE_ACCOUNT, "Settings Page")
        self._return_to_dashboard()

