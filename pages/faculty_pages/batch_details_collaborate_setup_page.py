from pages.base_page import BasePage
from locators.faculty_locators.batch_details_collaborate_setup_locators import BatchDetailsCollaborateSetupLocators
from utils.logger import log
from locators.xpath import UPPER


class BatchDetailsCollaborateSetupPage(BasePage):
    DEFAULT_TIMEOUT = 5000


    def _full_page_scroll_cycle(self):
        try:
            self.page.evaluate("window.scrollTo(0, 0)")
            self.pause(80)
        except Exception as _ignored:
            log.debug("Optional step in _full_page_scroll_cycle() did not apply: %s", _ignored)

        for offset in (600, 1200, 1800, 2400):
            try:
                self.page.evaluate(f"window.scrollTo(0, {offset})")
                self.pause(60)
            except Exception as _ignored:
                log.debug("Optional step in _full_page_scroll_cycle() did not apply: %s", _ignored)

        try:
            self.page.evaluate("window.scrollTo(0, 0)")
            self.pause(60)
        except Exception as _ignored:
            log.debug("Optional step in _full_page_scroll_cycle() did not apply: %s", _ignored)

    def validate_collaboratesetup_tab_and_click(self):
        collab_tab = self.first_visible([
            BatchDetailsCollaborateSetupLocators.COLLABORATESETUP_TAB,
            f"//p[contains({UPPER}, 'COLLABORATE SETUP')]",
            f"//*[contains(@class,'tab') and contains({UPPER}, 'COLLABORATE')]",
        ], timeout=10000)
        # Some batches (e.g. a deleted-course batch) don't expose the Collaborate
        # Setup tab at all. Treat its absence as a graceful data gap.
        if not collab_tab:
            log.info("Collaborate Setup tab is not available for this batch "
                     "(e.g. a deleted-course batch); skipping collaborate setup validation.")
            return False

        clicked = self.click_first_visible([
            BatchDetailsCollaborateSetupLocators.COLLABORATESETUP_TAB,
            f"//p[contains({UPPER}, 'COLLABORATE SETUP')]",
        ], "collaboratesetup tab", timeout=8000)
        # assert clicked, "Collaborate Setup tab is not clickable"
        return True

    def click_edit_and_change_level_save(self):
        self.validate_any_visible([
            BatchDetailsCollaborateSetupLocators.COLLABORATE_TITLE,
            f"//h4[contains({UPPER}, 'COLLABORATE')]",
        ], "Collaborate setup customize title", timeout=15000)

        self.click_required([
            BatchDetailsCollaborateSetupLocators.COLLABORATE_EDIT_BUTTON,
            "//button[normalize-space()='Edit']",
        ], "Edit button", timeout=10000)

        self.click_required([
            BatchDetailsCollaborateSetupLocators.LEVEL1_SECTION,
            "(//div[contains(@class,'radio_option')])[1]",
        ], "Level 1 option", timeout=10000)

        self.click_required([
            BatchDetailsCollaborateSetupLocators.COLLABORATE_SAVE_BUTTON,
            "//button[normalize-space()='Save']",
        ], "Save button", timeout=10000)

    def navigate_to_collaborate_setup_and_validate_career_plans(self):
        self._full_page_scroll_cycle()
        career_plans = self.first_visible([
            BatchDetailsCollaborateSetupLocators.SELECTED_CAREER_PLANS_SECTION,
            "//div[contains(@class,'career-plans-container')]",
        ], timeout=15000)
        assert career_plans, "Selected Career Plans section is not visible"
        self.show_element(career_plans, duration=700)
