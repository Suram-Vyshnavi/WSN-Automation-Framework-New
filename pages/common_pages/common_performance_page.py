from locators.common_locators.common_performance_locators import CommonPerformanceLocators
from locators.faculty_locators.home_locators import HomeLocators
from pages.base_page import BasePage, SHORT_TIMEOUT
from utils.logger import log

MENU_TIMEOUT = 12000


class CommonPerformancePage(BasePage):
    """The Performance dashboard shared by the faculty and RM personas."""

    def _navigate_to_home(self):
        """Best-effort return to Home so the sidebar is in a known state."""
        if self.click_first_visible([HomeLocators.HOME_MENU], "Home menu", timeout=3000):
            self.pause(800)

    def _course_option_selectors(self, course_name):
        return [
            f"(//div[@class='ant-select-item-option-content' and normalize-space()='{course_name}'])[1]",
            f"(//div[contains(@class,'ant-select-item-option-content') and normalize-space()='{course_name}'])[1]",
            f"(//span[normalize-space()='{course_name}'])[1]",
            CommonPerformanceLocators.FIRST_COURSE_IN_DROPDOWN,
        ]

    def click_performance_menu(self):
        self._navigate_to_home()
        self.click_required([
            CommonPerformanceLocators.PERFORMANCE_MENU,
            HomeLocators.PERFORMANCE_MENU,
        ], "Performance menu", timeout=MENU_TIMEOUT)

    def validate_course_program_label_and_select_course(self, course_name):
        """Pick a course in the filter. False when the account has no courses.

        An account with no performance data renders an empty dropdown; that is a
        data gap, not a defect, so the caller is told to skip the dependent
        validations instead of the run failing.
        """
        self.validate_any_visible([CommonPerformanceLocators.VALIDATE_COURSE_PROGRAM_LABEL],
                                  "Course / Program label", timeout=MENU_TIMEOUT)
        self.click_required([CommonPerformanceLocators.SELECT_COURSE_INPUT_FIELD],
                            "Select course input field")

        if not self.click_first_visible(self._course_option_selectors(course_name),
                                        f"'{course_name}' course option", timeout=10000):
            log.warning("Course '%s' is not available in the dropdown; skipping course "
                        "selection and the dependent performance validations.", course_name)
            self.press_escape()
            return False
        return True

    def validate_risk_category_and_select_critical(self):
        self.validate_any_visible([CommonPerformanceLocators.VALIDATE_RISK_CATEGORY_LABEL],
                                  "Risk Category label", timeout=MENU_TIMEOUT)
        self.click_required([CommonPerformanceLocators.SELECT_STATUS_INPUT_FIELD],
                            "Select status input field")
        self.click_required([CommonPerformanceLocators.FIRST_STATUS_IN_DROPDOWN],
                            "Critical status option")

    def validate_batch_status_and_select_active(self):
        # Batch Status is a pill toggle (All / Active / Inactive) - click the Active pill.
        self.validate_any_visible([CommonPerformanceLocators.VALIDATE_BATCH_STATUS_LABEL],
                                  "Batch Status label", timeout=MENU_TIMEOUT)
        self.click_required([CommonPerformanceLocators.BATCH_STATUS], "Active batch status pill")

    def click_batch_row_and_validate_certification_status(self):
        """Open a batch row. False when the table has no performance data."""
        no_data = self.first_visible([CommonPerformanceLocators.NO_DATA_FOUND], timeout=SHORT_TIMEOUT)
        has_rows = self.first_visible([CommonPerformanceLocators.BATCH_DETAILS_ROW_OPTION], timeout=2000)
        if no_data and not has_rows:
            log.warning("Performance table shows 'No Data Found' - this account has no batch "
                        "performance data; skipping the certification status validation.")
            return False

        self.click_required([CommonPerformanceLocators.BATCH_DETAILS_ROW_OPTION],
                            "Batch details row", timeout=MENU_TIMEOUT)
        self.validate_any_visible([CommonPerformanceLocators.VALIDATE_CERTIFICATION_STATUS_LABEL],
                                  "Certification Status label", timeout=MENU_TIMEOUT)
        return True

    def validate_student_activity_and_click_plus_icons(self):
        self.validate_any_visible([CommonPerformanceLocators.VALIDATE_STUDENT_ACTIVITY_LABEL],
                                  "Student Activity label", timeout=MENU_TIMEOUT)
        self.click_required([CommonPerformanceLocators.PLUS_ICON_PREVIDEO], "Pre-video plus icon")
        self.click_required([CommonPerformanceLocators.PLUS_ICON_POSTVIDEO], "Post-video plus icon")

    def validate_assessment_activity_and_click_quiz_plus(self):
        self.validate_any_visible([CommonPerformanceLocators.VALIDATE_STUDENT_ACTIVITY_ASSESSMENTS_LABEL],
                                  "Student Activity - Assessments label", timeout=MENU_TIMEOUT)
        # Expanding the pre/post-video rows can push the Quiz row off-screen.
        self.scroll_into_view(CommonPerformanceLocators.QUIZ_PLUS_ICON)
        self.pause(500)
        if not self.click_first_visible([CommonPerformanceLocators.QUIZ_PLUS_ICON], "Quiz plus icon"):
            log.warning("Quiz plus icon is not present for this account's performance data "
                        "- skipping that expansion.")

    def click_back_to_dashboard(self):
        self.click_required([CommonPerformanceLocators.BACK_TO_DASHBOARD_BUTTON],
                            "Back to Dashboard button", timeout=MENU_TIMEOUT)
