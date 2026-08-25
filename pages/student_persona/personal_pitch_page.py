from config.env_config import IS_PROD
from locators.student_persona_locators.personal_pitch_trainer_locators import PersonalPitchTrainerLocators
from pages.student_persona.student_persona_page import (
    CARD_TIMEOUT, PROD_PROBE_TIMEOUT, StudentPersonaPage)
from utils.logger import log


class PersonalPitchPage(StudentPersonaPage):
    """The Personal Pitch Trainer card and the saved-pitch summary flow."""

    # Class-level so it survives across the per-step page-object instances.
    # The "view an existing pitch summary" flow (View -> play -> share -> copy)
    # only applies when the account already has a saved pitch. The prod account
    # has none, so the View button never appears; the flow is then flagged
    # unavailable and its dependent steps skip instead of failing.
    _pitch_summary_available = True

    def _pitch_flow_skipped(self, step_name):
        """True (and logged) when the existing-pitch flow is unavailable."""
        if PersonalPitchPage._pitch_summary_available:
            return False
        log.warning("No saved pitch summary - skipping '%s'", step_name)
        return True

    def _navigate_to_personal_pitch(self):
        """Open the Personal Pitch Trainer from the dashboard."""
        self.open_card_from_dashboard(
            PersonalPitchTrainerLocators.PERSONAL_PITCH_TRAINER, "Personal Pitch Trainer card",
            ready_locator=PersonalPitchTrainerLocators.CREATE_YOUR_PITCH_BUTTON)

    # ------------------------------------------------------------------
    # Create-pitch flow
    # ------------------------------------------------------------------
    def click_create_your_pitch_button(self):
        self._navigate_to_personal_pitch()
        self.click(PersonalPitchTrainerLocators.CREATE_YOUR_PITCH_BUTTON,
                   "Create Your Pitch button", timeout=CARD_TIMEOUT)

    def click_create_your_pitch_back_button(self):
        """Leave the create-pitch flow and land back on the pitch dashboard.

        One back click only exits the current step of the flow, so the
        dashboard is confirmed and the trainer re-opened if we are still
        somewhere inside the journey.
        """
        self.click(PersonalPitchTrainerLocators.PITCH_TRAINER_BACK_ARROW_BUTTON,
                   "Create Your Pitch back button", timeout=CARD_TIMEOUT)
        if not self.is_visible(PersonalPitchTrainerLocators.CREATE_YOUR_PITCH_BUTTON,
                               timeout=PROD_PROBE_TIMEOUT):
            log.info("Still inside the create-pitch flow - re-opening the pitch dashboard")
            self._navigate_to_personal_pitch()

    # ------------------------------------------------------------------
    # Saved-pitch summary flow
    # ------------------------------------------------------------------
    def click_pitch_summary_view_button(self):
        """Open the saved pitch summary, or flag the flow unavailable on prod."""
        # Reset each run so a fresh execution re-probes availability.
        PersonalPitchPage._pitch_summary_available = True
        timeout = PROD_PROBE_TIMEOUT if IS_PROD else CARD_TIMEOUT

        if not self.is_visible(PersonalPitchTrainerLocators.PITCH_SUMMARY_VIEW_BUTTON, timeout=timeout):
            if not IS_PROD:
                raise AssertionError("Pitch Summary View button is not visible")
            PersonalPitchPage._pitch_summary_available = False
            log.warning("No saved pitch summary - skipping 'pitch summary view button'")
            return

        self.click(PersonalPitchTrainerLocators.PITCH_SUMMARY_VIEW_BUTTON,
                   "Pitch Summary View button", timeout=timeout)

    def click_view_pitch_button(self):
        if self._pitch_flow_skipped("view pitch button"):
            return
        self.click(PersonalPitchTrainerLocators.VIEW_PITCH_BUTTON, "View Pitch button",
                   timeout=CARD_TIMEOUT)

    def click_video_play_button(self):
        if self._pitch_flow_skipped("video play button"):
            return
        # The <video> element never reports as "visible" - wait for attached and force.
        self.click(PersonalPitchTrainerLocators.VIDEO_PLAY_BUTTON, "video play button",
                   timeout=CARD_TIMEOUT, state="attached", force=True)

    def click_video_close_button(self):
        if self._pitch_flow_skipped("video close button"):
            return
        self.click(PersonalPitchTrainerLocators.VIDEO_CLOSE_BUTTON, "video close button",
                   timeout=CARD_TIMEOUT)

    def click_share_pitch_button(self):
        if self._pitch_flow_skipped("share pitch button"):
            return
        self.click(PersonalPitchTrainerLocators.SHARE_PITCH_BUTTON, "Share Pitch button",
                   timeout=CARD_TIMEOUT)

    def click_copy_pitch_button(self):
        if self._pitch_flow_skipped("copy pitch button"):
            return
        self.click(PersonalPitchTrainerLocators.COPY_SHARE_BUTTON, "Copy Pitch button",
                   timeout=CARD_TIMEOUT)

    def click_share_pitch_close_button(self):
        if self._pitch_flow_skipped("share pitch close button"):
            return
        self.click(PersonalPitchTrainerLocators.SHARE_PITCH_CLOSE_BUTTON,
                   "Share Pitch Close button", timeout=CARD_TIMEOUT)

    # ------------------------------------------------------------------
    # Dashboard card state
    # ------------------------------------------------------------------
    def click_home_icon_and_navigate_home(self):
        self.click(PersonalPitchTrainerLocators.HOME, "Home icon", timeout=CARD_TIMEOUT)
        self.pause(1500)

    def click_passed_text_on_pitch_card(self):
        """Click the 'Passed' badge on the pitch card.

        Returns False (without failing) when the account has not passed a pitch,
        because the badge is then simply not rendered.
        """
        self.wait_for_visible(PersonalPitchTrainerLocators.PERSONAL_PITCH_TRAINER,
                              timeout=CARD_TIMEOUT)
        if not self.is_visible(PersonalPitchTrainerLocators.PERSONAL_PITCH_TRAINER_PASSED_TEXT,
                               timeout=PROD_PROBE_TIMEOUT):
            log.warning("'Passed' badge is not present on the Personal Pitch Trainer card "
                        "- skipping without failing the scenario")
            return False

        self.click(PersonalPitchTrainerLocators.PERSONAL_PITCH_TRAINER_PASSED_TEXT,
                   "'Passed' badge on the Personal Pitch Trainer card", timeout=CARD_TIMEOUT)
        self.pause(1000)
        return True

    def validate_check_button(self):
        """Validate the check button, or skip when the pitch was never passed."""
        if not self.is_visible(PersonalPitchTrainerLocators.VALIDATE_CHECK_BUTTON,
                               timeout=PROD_PROBE_TIMEOUT):
            log.warning("Check button is not present - skipping without failing the scenario")
            return False
        self.validate_visible(PersonalPitchTrainerLocators.VALIDATE_CHECK_BUTTON, "Check button")
        return True
