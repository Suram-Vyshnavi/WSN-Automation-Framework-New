from locators.student_persona_locators.courses_locators import CoursesLocators
from pages.base_page import LONG_TIMEOUT
from pages.student_persona.student_persona_page import CARD_TIMEOUT, StudentPersonaPage
from utils.logger import log


class CoursesPage(StudentPersonaPage):
    """The courses half of the merged 'Programs & Courses' screen.

    The application merged the old separate Courses and Programs screens into
    one (/en/course-program-list) and redesigned the course detail page: the
    Overview / Course Content / Performance tabs and the "View Details" button
    are gone, replaced by a certificate-progress panel and lesson accordions.
    This page object drives the new UI; `ProgramsPage` covers the programs half
    of the same screen.
    """

    def _navigate_to_courses(self):
        """Open the merged Programs & Courses screen from the dashboard."""
        self.open_card_from_dashboard(
            CoursesLocators.COURSES_CARD, "Programs & Courses card",
            ready_locator=CoursesLocators.VALIDATE_INPROGRESS_TAB)

    # ------------------------------------------------------------------
    # List screen
    # ------------------------------------------------------------------
    def validate_inprogress_and_completed_tabs(self):
        self._navigate_to_courses()
        self.validate_visible(CoursesLocators.VALIDATE_INPROGRESS_TAB, "In Progress tab")
        self.validate_visible(CoursesLocators.VALIDATE_COMPLETED_TAB, "Completed tab")

    def click_inprogress_tab(self):
        self.click(CoursesLocators.VALIDATE_INPROGRESS_TAB, "In Progress tab", timeout=CARD_TIMEOUT)

    def click_completed_tab(self):
        self.click(CoursesLocators.VALIDATE_COMPLETED_TAB, "Completed tab", timeout=CARD_TIMEOUT)

    def validate_enrolled_course_card(self):
        """An enrolled course card is listed under the active tab."""
        self.validate_visible(CoursesLocators.ENROLLED_COURSE_CARD, "Enrolled course card",
                              timeout=CARD_TIMEOUT)

    def open_first_course(self):
        """Open the first listed course by its title."""
        title = self.get_text(CoursesLocators.COURSE_CARD_TITLE, timeout=CARD_TIMEOUT)
        self.click(CoursesLocators.COURSE_CARD_TITLE, f"course '{title}'", timeout=CARD_TIMEOUT)
        self.validate_visible(CoursesLocators.COURSE_TITLE, "course detail title",
                              timeout=LONG_TIMEOUT)
        log.info("Opened course '%s'", title)

    # ------------------------------------------------------------------
    # Course detail screen
    # ------------------------------------------------------------------
    def validate_course_detail_sections(self):
        """The detail page shows its title, certificate progress and lessons."""
        self.validate_visible(CoursesLocators.COURSE_TITLE, "course title", timeout=CARD_TIMEOUT)
        self.validate_visible(CoursesLocators.CERTIFICATE_PROGRESS, "Certificate Progress panel")
        self.validate_visible(CoursesLocators.EARNED_MICRO_CERTIFICATES,
                              "Earned Micro Certificates panel")
        self.validate_visible(CoursesLocators.LESSON_ACCORDION, "lesson accordion")

    def expand_first_lesson_section(self):
        section = self.get_text(CoursesLocators.LESSON_ACCORDION, timeout=CARD_TIMEOUT)
        self.click(CoursesLocators.LESSON_ACCORDION, f"lesson section '{section}'",
                   timeout=CARD_TIMEOUT)

    def validate_assessment_score(self):
        """Assert the assessment score is shown, and that it reads as a percentage."""
        self.validate_visible(CoursesLocators.ASSESSMENT_SCORE_LABEL, "Assessment Score label",
                              timeout=CARD_TIMEOUT)
        score = self.get_text(CoursesLocators.ASSESSMENT_SCORE_VALUE)
        assert "%" in score, f"Assessment score '{score}' is not shown as a percentage"
        log.info("Assessment score is %s", score)

    def go_back_to_course_list(self):
        self.click(CoursesLocators.BACK_BUTTON, "back to the Programs & Courses list",
                   timeout=CARD_TIMEOUT)
        self.validate_visible(CoursesLocators.VALIDATE_INPROGRESS_TAB, "In Progress tab",
                              timeout=CARD_TIMEOUT)

    # ------------------------------------------------------------------
    # Recommendation sections
    # ------------------------------------------------------------------
    def validate_courses_recommended_by_institute(self):
        self.scroll_to_bottom()
        self.validate_visible(CoursesLocators.COURSES_RECOMMENDED_BY_INSTITUTE,
                              "Programs & Courses recommended by your institute",
                              timeout=LONG_TIMEOUT)

    def validate_recommended_course_card(self):
        self.validate_visible(CoursesLocators.VALIDATE_RECOMMENDED_COURSE_CARD,
                              "recommended course card", timeout=CARD_TIMEOUT)

    def validate_courses_offered_by_wadhwani_foundation(self):
        self.scroll_to_bottom()
        self.validate_visible(CoursesLocators.COURSES_OFFERED_BY_WADHWANI_FOUNDATION,
                              "Programs & Courses recommended by Wadhwani Foundation",
                              timeout=LONG_TIMEOUT)
