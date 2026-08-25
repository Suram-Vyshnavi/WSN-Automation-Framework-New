from config.env_config import IS_PROD
from locators.student_persona_locators.interview_coach_locators import InterviewCoachLocators
from pages.student_persona.student_persona_page import CARD_TIMEOUT, PROD_PROBE_TIMEOUT, StudentPersonaPage
from utils.logger import log

MAX_ROLES_TO_DELETE = 20


class InterviewCoachPage(StudentPersonaPage):
    """The Interview Coach: create a role, practise it, then clean it up.

    Dev and prod behave differently here. On dev the card opens the create-role
    flow; on prod the account already has roles, so the card opens an existing
    role's question page and the create-only steps are skipped.
    """

    # Class-level so it survives the per-step page-object instances. The
    # create-role flow is only reachable when the account has no journey open.
    create_role_flow_available = True

    def _create_flow_skipped(self, step_name):
        """True (and logged) when the create-role flow is not reachable."""
        if InterviewCoachPage.create_role_flow_available:
            return False
        log.warning("Create-role flow is not available on this account - skipping '%s'", step_name)
        return True

    def _navigate_to_interview_coach(self):
        InterviewCoachPage.create_role_flow_available = True
        self.open_card_from_dashboard(InterviewCoachLocators.INTERVIEW_COACH_CARD,
                                      "Interview Coach card")

    def _on_question_page(self):
        """True when the card opened an existing role's question page."""
        return self.is_visible(InterviewCoachLocators.PITCH_TRAINER_BACK_ICON,
                               timeout=PROD_PROBE_TIMEOUT)

    def _go_back_to_roles_list(self):
        """Click back until the Recent Roles list is showing."""
        self.click(InterviewCoachLocators.PITCH_TRAINER_BACK_ICON, "Interview Coach back icon")
        self.pause(2000)

    def _fill_textbox_and_send(self, text):
        self.enter_text(InterviewCoachLocators.INTERVIEW_SEARCH_INPUT, text,
                        "Interview Coach textbox", timeout=CARD_TIMEOUT)
        self.click(InterviewCoachLocators.INTERVIEW_COACH_SEND_ICON, "send icon",
                   timeout=CARD_TIMEOUT)

    # ------------------------------------------------------------------
    # Create-role flow (dev only)
    # ------------------------------------------------------------------
    def click_audio_button_image(self):
        """Start a new practice role, or step back out of one already running.

        The card opens the create-role flow only when the account has no
        journey in progress. When one is already open - a leftover from an
        earlier run, or the normal state on prod - the flow is unreachable, so
        we return to the Recent Roles list instead. That is decided from the
        page, not from the environment.
        """
        if self._on_question_page():
            self._go_back_to_roles_list()
            log.info("A practice journey was already open - returned to the Recent Roles list")
            InterviewCoachPage.create_role_flow_available = False
            return
        InterviewCoachPage.create_role_flow_available = not IS_PROD
        if not InterviewCoachPage.create_role_flow_available:
            log.info("Prod flow: already on the Recent Roles list")
            return
        self.click(InterviewCoachLocators.AUDIO_BUTTON_IMAGE, "audio button image",
                   timeout=CARD_TIMEOUT)

    def validate_textbox_and_mic_button(self):
        if self._create_flow_skipped("create-role textbox/mic validation"):
            return
        self.validate_visible(InterviewCoachLocators.INTERVIEW_SEARCH_INPUT,
                              "Interview Coach textbox", timeout=CARD_TIMEOUT)
        self.validate_visible(InterviewCoachLocators.VALIDATE_MIC_BUTTON, "Mic button",
                              timeout=CARD_TIMEOUT)

    def fill_textbox_and_click_send(self):
        """Send the role, then the sector, as two separate messages."""
        if self._create_flow_skipped("create-role textbox send"):
            return
        self._fill_textbox_and_send("Product Manager")
        self._fill_textbox_and_send("healthcare")

    def click_practise_interviewing_for_role(self):
        if self._create_flow_skipped("Practise Interviewing"):
            return
        self.click(InterviewCoachLocators.PRACTISE_INTERVIEW_BUTTON,
                   "Practise Interviewing for the role", timeout=20000)

    def validate_start_button(self):
        if self._create_flow_skipped("Start button validation"):
            return
        self.validate_visible(InterviewCoachLocators.START_BUTTON, "Start button",
                              timeout=CARD_TIMEOUT)

    # ------------------------------------------------------------------
    # Recent Roles list
    # ------------------------------------------------------------------
    MAX_BACK_CLICKS = 4

    def click_pitch_trainer_back_icon(self):
        """Walk back out of the practice journey to the Recent Roles list.

        A single back click only leaves the current step of the journey, so it
        is repeated until the Recent Roles list is on screen.
        """
        for attempt in range(self.MAX_BACK_CLICKS):
            if self.is_visible(InterviewCoachLocators.VALIDATE_YOUR_RECENT_ROLES_HEADER,
                               timeout=PROD_PROBE_TIMEOUT):
                log.info("Reached the Recent Roles list after %d back click(s)", attempt)
                return
            if not self.click_first_visible([InterviewCoachLocators.PITCH_TRAINER_BACK_ICON],
                                            "Interview Coach back icon", timeout=CARD_TIMEOUT):
                break
            self.pause(2000)
        assert self.is_visible(InterviewCoachLocators.VALIDATE_YOUR_RECENT_ROLES_HEADER,
                               timeout=CARD_TIMEOUT),             "Could not get back to the Recent Roles list from the practice journey"

    def validate_your_recent_roles_header(self):
        self.validate_visible(InterviewCoachLocators.VALIDATE_YOUR_RECENT_ROLES_HEADER,
                              "Your Recent Roles header", timeout=CARD_TIMEOUT)

    def validate_ongoing_and_completed_headers(self):
        self.validate_visible(InterviewCoachLocators.VALIDATE_ONGOING_HEADER, "Ongoing header",
                              timeout=CARD_TIMEOUT)
        self.validate_visible(InterviewCoachLocators.VALIDATE_COMPLETED_HEADER, "Completed header",
                              timeout=CARD_TIMEOUT)

    def click_threedots_icon(self):
        """Make the Ongoing tab active, ready for the delete step.

        The delete step opens each role's own three-dots menu, so nothing is
        opened here - that kept the two environments on one code path.
        """
        self.click_first_visible([InterviewCoachLocators.VALIDATE_ONGOING_HEADER],
                                 "Ongoing tab", timeout=PROD_PROBE_TIMEOUT)
        self.pause(1000)

    def click_delete_role_and_confirm(self):
        """Delete every ongoing role, so the scenario leaves no residue.

        This used to delete all roles on prod but only one on dev, which is why
        a half-finished dev run left a journey behind and broke the next run's
        create-role flow. Cleaning up fully on both environments makes the
        scenario repeatable.
        """
        self._delete_all_ongoing_roles()

    def _delete_all_ongoing_roles(self):
        """Delete every ongoing role.

        The three-dots menu is re-queried each iteration because the list
        shrinks after every deletion.
        """
        deleted = 0
        for _ in range(MAX_ROLES_TO_DELETE):
            if self.count(InterviewCoachLocators.THREEDOTS_MORE_DETAILS_ICON) == 0:
                break
            try:
                self.click(InterviewCoachLocators.THREEDOTS_MORE_DETAILS_ICON, "three dots icon")
                self.click(InterviewCoachLocators.DELETE_ROLE_BUTTON, "Delete this role")
                self.click(InterviewCoachLocators.DELETE_ROLE_CONFIRM_BUTTON, "delete confirmation")
                self.pause(2000)
                deleted += 1
            except Exception as error:
                log.warning("Stopped deleting ongoing roles after %d: %s", deleted, error)
                break
        log.info("Deleted %d ongoing role(s)", deleted)
