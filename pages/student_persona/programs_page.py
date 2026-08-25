from locators.student_persona_locators.programs_locators import ProgramsLocators
from pages.base_page import LONG_TIMEOUT
from pages.student_persona.student_persona_page import CARD_TIMEOUT, StudentPersonaPage


class ProgramsPage(StudentPersonaPage):
    """The programs half of the merged 'Programs & Courses' screen.

    The application merged the old separate Courses and Programs screens into
    one (/en/course-program-list). Programs now appear as
    `learning-item-card--program` cards alongside courses, and the old
    Enroll -> Confirm/Cancel modal has been replaced by opening the program
    directly. `CoursesPage` covers the courses half of the same screen.
    """

    def _navigate_to_programs(self):
        """Open the merged Programs & Courses screen from the dashboard."""
        self.open_card_from_dashboard(
            ProgramsLocators.PROGRAMS_CARD, "Programs & Courses card",
            ready_locator=ProgramsLocators.VALIDATE_INPROGRESS_TAB)

    # ------------------------------------------------------------------
    # List screen
    # ------------------------------------------------------------------
    def validate_inprogress_and_completed_tabs(self):
        self._navigate_to_programs()
        self.validate_visible(ProgramsLocators.VALIDATE_INPROGRESS_TAB, "In Progress tab")
        self.validate_visible(ProgramsLocators.VALIDATE_COMPLETED_TAB, "Completed tab")

    def click_inprogress_tab(self):
        self.click(ProgramsLocators.VALIDATE_INPROGRESS_TAB, "In Progress tab", timeout=CARD_TIMEOUT)

    def click_completed_tab(self):
        self.click(ProgramsLocators.VALIDATE_COMPLETED_TAB, "Completed tab", timeout=CARD_TIMEOUT)

    def validate_program_card(self):
        """At least one program card is listed on the merged screen."""
        self.scroll_to_bottom()
        self.validate_visible(ProgramsLocators.PROGRAM_CARD, "program card", timeout=CARD_TIMEOUT)

    # ------------------------------------------------------------------
    # Recommendation sections
    # ------------------------------------------------------------------
    def validate_recommended_by_institute_header(self):
        self.scroll_to_bottom()
        self.validate_visible(ProgramsLocators.VALIDATE_RECOMMENDED_BY_INSTITUTE,
                              "Programs & Courses recommended by your institute",
                              timeout=LONG_TIMEOUT)

    def validate_recommended_program_card(self):
        self.validate_visible(ProgramsLocators.RECOMMENDED_PROGRAM_CARD,
                              "recommended program card", timeout=CARD_TIMEOUT)

    def validate_offered_by_wadhwani_foundation_header(self):
        self.scroll_to_bottom()
        self.validate_visible(ProgramsLocators.VALIDATE_OFFERED_BY_WADHWANI_FOUNDATION,
                              "Programs & Courses recommended by Wadhwani Foundation",
                              timeout=LONG_TIMEOUT)

    def validate_join_a_batch_section(self):
        self.scroll_to_bottom()
        self.validate_visible(ProgramsLocators.JOIN_A_BATCH, "Join a batch section",
                              timeout=CARD_TIMEOUT)
