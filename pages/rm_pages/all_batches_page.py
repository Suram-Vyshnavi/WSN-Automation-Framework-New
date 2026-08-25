from pages.base_page import BasePage
from locators.rm_locators.all_batches_locators import AllBatchesLocators
from locators.xpath import UPPER
from utils.logger import log


class RMAllBatchesPage(BasePage):
    DEFAULT_TIMEOUT = 8000


    def _go_to_home_menu(self):
        self.click_first_visible([
            "//div[@id='Home']",
            f"//div[@role='menuitem' and contains({UPPER}, 'HOME')]",
        ], timeout=7000)
        self.pause(700)

    def click_first_assigned_batch(self):
        # RM dashboard uses Assigned Batches on Home screen (not Active Batches tab).
        self._go_to_home_menu()

        self.validate_any_visible([
            "(//h2[normalize-space()='Assigned Batches'])[1]",
            f"//*[self::h2 or self::h3][contains({UPPER}, 'ASSIGNED BATCH')]",
        ], "Assigned Batches section", timeout=12000)

        clicked_assigned = self.click_first_visible([
            "(//tr[not(contains(normalize-space(td[3]), 'dont use')) and number(normalize-space(td[6])) > 0])[1]",
            "(//tbody//tr[1]//td[contains(@class,'batch-list-content')])[1]",
            "(//tbody//tr[1]//td)[1]",
            "(//div[contains(@class,'ant-table-tbody')]//tr[1]//td[1])[1]",
        ], timeout=10000)

        if clicked_assigned:
            return

        # Fallback: if Assigned Batches row is not interactable, use All Batches list.
        self.click_required([
            "//div[@id='All']",
            f"//div[@role='menuitem' and contains({UPPER}, 'ALL BATCH')]",
        ], "Unable to open All Batches menu from RM flow", timeout=10000)

        self.validate_any_visible([
            AllBatchesLocators.ALL_BATCHES_TITLE,
            f"//*[self::h2 or self::h3][contains({UPPER}, 'ALL BATCH')]",
        ], "All Batches page did not load", timeout=15000)

        self.click_required([
            "(//tbody//tr[1]//td[contains(@class,'batch-list-content-bold')])[1]",
            "(//tbody//tr[1]//td[contains(@class,'batch-list-content')])[1]",
            "(//tbody//tr[1]//td)[1]",
        ], "First batch row", timeout=10000)

    def click_first_active_batch(self):
        # Backward-compatible alias for existing step text.
        self.click_first_assigned_batch()

    def click_all_batches_menu(self):
        self.click_required([
            "(//div[@id='All'])[1]",
            "//div[@id='All']",
            f"//div[@role='menuitem' and contains({UPPER}, 'ALL BATCH')]",
        ], "All Batches menu", timeout=12000)

    def validate_all_batches_title_and_search(self, batch_name):
        self.validate_any_visible([
            AllBatchesLocators.ALL_BATCHES_TITLE,
            f"//*[self::h2 or self::h3][contains({UPPER}, 'ALL BATCH')]",
        ], "All Batches title", timeout=15000)

        search = self.first_visible([
            AllBatchesLocators.SEARCHBAR,
            "(//input[contains(@placeholder,'Search')])[1]",
        ], timeout=10000)
        assert search, "All Batches search bar is not visible"
        search.click(timeout=3000)
        search.fill(batch_name, timeout=4000)
        try:
            search.press("Enter")
        except Exception as _ignored:
            log.debug("Optional step in validate_all_batches_title_and_search() did not apply: %s", _ignored)
        self.pause(800)

    def validate_status_title(self):
        self.validate_any_visible([
            AllBatchesLocators.STATUS_TITLE,
            f"//*[contains({UPPER}, 'STATUS')]",
        ], "Status title", timeout=10000)

    def select_status_option(self, option_text):
        dropdown = self.first_visible([
            AllBatchesLocators.STATUS_DROPDOWN,
            "(//button[contains(@class,'dropdown-btn')])[1]",
            f"(//button[contains(@class,'ant-btn') and .//*[contains({UPPER}, 'STATUS')]])[1]",
        ], timeout=10000)
        assert dropdown, "Status dropdown is not visible/clickable"
        try:
            dropdown.click(timeout=4000)
        except Exception:
            dropdown.click(timeout=4000, force=True)

        if option_text.strip().lower() == "active":
            option_locators = [
                AllBatchesLocators.ACTIVE_OPTION_IN_DROPDOWN,
                "//div[contains(@class,'ant-dropdown')]//span[normalize-space(text())='Active']",
            ]
        else:
            option_locators = [
                AllBatchesLocators.INACTIVE_OPTION_IN_DROPDOWN,
                "//div[contains(@class,'ant-dropdown')]//span[normalize-space(text())='Inactive']",
            ]

        selected = self.click_first_visible(option_locators, "option locators", timeout=8000)
        assert selected, f"Unable to select '{option_text}' option from Status dropdown"
        self.pause(900)

    def validate_batches_section(self):
        self.validate_any_visible([
            AllBatchesLocators.ALL_BATCHES_CONTAINER,
            "(//div[contains(@class,'site-content')])[1]",
            "(//table[contains(@class,'ant-table')])[1]",
        ], "All Batches section/container", timeout=12000)

