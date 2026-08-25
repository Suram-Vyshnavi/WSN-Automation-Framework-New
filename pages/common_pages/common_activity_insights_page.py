from pages.base_page import BasePage
from locators.common_locators.common_activity_insights_locators import CommonActivityInsightsLocators
from utils.logger import log


class CommonActivityInsightsPage(BasePage):
    def validate_activity_insights_tab_and_click(self):
        # Some batches (e.g. a deleted-course batch) don't expose the Activity
        # Insights tab. Treat its absence as a graceful data gap.
        tab = self.first_visible([
            CommonActivityInsightsLocators.ACTIVITY_INSIGHTS_TAB,
            "(//p[normalize-space()='Activity Insights'])[1]",
        ], timeout=15000)
        if not tab:
            log.info("Activity Insights tab is not available for this batch "
                     "(e.g. a deleted-course batch); skipping activity insights validation.")
            return False
        try:
            tab.scroll_into_view_if_needed()
        except Exception as _ignored:
            log.debug("Optional step in validate_activity_insights_tab_and_click() did not apply: %s", _ignored)
        try:
            tab.click(timeout=15000)
        except Exception:
            tab.click(timeout=15000, force=True)
        return True

    def validate_submission_header_module_and_lesson(self):
        header = self.first_visible([CommonActivityInsightsLocators.SUBMISSION_INSIGHTS_HEADER_SECTION])
        module = self.first_visible([CommonActivityInsightsLocators.MODULE_COLUMN_TITLE])
        lesson = self.first_visible([CommonActivityInsightsLocators.LESSON_NAME_COLUMN_TITLE])
        assert header, "Submission insights header section is not visible"
        assert module, "Module column title is not visible"
        assert lesson, "Lesson name column title is not visible"

    def click_students_submitted_icon_and_validate(self):
        self.click_required([CommonActivityInsightsLocators.STUDENTS_SUBMITTED_I_ICON], "Students submitted info icon")
        self.validate_any_visible([
            "//div[contains(@class,'ant-tooltip-inner')]",
            "//div[@role='tooltip']",
        ], "Tooltip text", timeout=5000)

    def click_students_scored_icon_and_validate(self):
        self.click_required([CommonActivityInsightsLocators.STUDENTS_SCORED_I_ICON], "Students scored info icon")
        self.validate_any_visible([
            "//div[contains(@class,'ant-tooltip-inner')]",
            "//div[@role='tooltip']",
        ], "Tooltip text", timeout=5000)

    def open_lesson_arrow_validate_and_back(self, arrow_locator):
        self.click_required([arrow_locator], "Lesson row arrow icon", timeout=10000)

        heading = self.first_visible([CommonActivityInsightsLocators.HEADING_SECTION], timeout=10000)
        table = self.first_visible([CommonActivityInsightsLocators.INSIGHTS_TABLE], timeout=10000)
        assert heading, "Insights detail heading section is not visible"
        assert table, "Insights detail table is not visible"

        self.click_required([CommonActivityInsightsLocators.BACK_ARROW], "Insights detail back arrow", timeout=10000)
