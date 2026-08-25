from pages.base_page import BasePage
from locators.faculty_locators.batch_details_scorecard_locators import BatchDetailsScorecardLocators
from utils.logger import log
from locators.xpath import UPPER


class BatchDetailsScorecardPage(BasePage):
    DEFAULT_TIMEOUT = 5000


    def _scroll_assessment_container_fully(self, container):
        try:
            container.scroll_into_view_if_needed()
        except Exception as _ignored:
            log.debug("Optional step in _scroll_assessment_container_fully() did not apply: %s", _ignored)

        try:
            self.pause(80)
            self.page.evaluate("""
                (el) => {
                    el.scrollIntoView({ behavior: 'instant', block: 'center', inline: 'nearest' });
                    if (el.scrollHeight > el.clientHeight) {
                        el.scrollTop = el.scrollHeight;
                        el.dispatchEvent(new Event('scroll', { bubbles: true }));
                        el.scrollTop = 0;
                        el.dispatchEvent(new Event('scroll', { bubbles: true }));
                    }
                }
            """, container)
            self.pause(80)
        except Exception as _ignored:
            log.debug("Optional step in _scroll_assessment_container_fully() did not apply: %s", _ignored)

    def validate_scorecard_tab_and_click(self):
        self.validate_any_visible([
            BatchDetailsScorecardLocators.SCORECARD_TAB,
            f"//p[contains({UPPER}, 'SCORECARD')]",
            f"//*[contains(@class,'tab') and contains({UPPER}, 'SCORECARD')]",
        ], "Scorecard tab", timeout=10000)

        self.click_required([
            BatchDetailsScorecardLocators.SCORECARD_TAB,
            f"//p[contains({UPPER}, 'SCORECARD')]",
        ], "Scorecard tab", timeout=8000)

        try:
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception as _ignored:
            log.debug("Optional step in validate_scorecard_tab_and_click() did not apply: %s", _ignored)
        try:
            self.pause(120)
        except Exception as _ignored:
            log.debug("Optional step in validate_scorecard_tab_and_click() did not apply: %s", _ignored)

    def validate_assessment_schedule_title_and_container(self):
        title = self.first_visible([
            BatchDetailsScorecardLocators.ASSESSMENT_SCHEDULE_TITLE,
            f"//*[contains({UPPER}, 'ASSESSMENT SCHEDULE')]",
        ], timeout=4000)
        if not title:
            log.warning("[Info] Assessment Schedule title not visible for this batch; skipping scorecard schedule validation.")
            return

        container = self.first_visible([
            BatchDetailsScorecardLocators.COURSE_ASSESSMENTS_CONTAINER,
            "//div[contains(@class,'course-assessments-container')]",
        ], timeout=4000)
        if not container:
            log.warning("[Info] Assessment Schedule container not visible for this batch; skipping scorecard schedule validation.")
            return
        self._scroll_assessment_container_fully(container)
        self.show_element(container, duration=700)
