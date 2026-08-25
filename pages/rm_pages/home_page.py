from pages.base_page import BasePage
from locators.rm_locators.home_locators import HomeLocators
from locators.xpath import UPPER


class RMHomePage(BasePage):

    def click_all_batches_menu(self):
        self.click_required([
            HomeLocators.ALL_BATCHES_MENU,
            "//div[@id='All']",
            f"//div[@role='menuitem' and contains({UPPER}, 'ALL BATCH')]",
        ], "All Batches menu")

    def validate_assigned_batches_section(self):
        self.validate_any_visible([
            HomeLocators.ASSIGNED_BATCHES_TITLE,
            f"//*[self::h2 or self::h3][contains({UPPER}, 'ASSIGNED BATCH')]",
        ], "Assigned Batches section", timeout=15000)

    def validate_assigned_batches_table_headers(self):
        expected_headers = [
            ("Batch Name", HomeLocators.BATCH_NAME_TITLE),
            ("Institute Name", HomeLocators.INSTITUTE_NAME_TITLE),
            ("Course Name", HomeLocators.COURSE_NAME_TITLE),
            ("Start Date", HomeLocators.START_DATE_TITLE),
            ("End Date", HomeLocators.END_DATE_TITLE),
            ("No. of Students", HomeLocators.NO_OF_STUDENTS_TITLE),
            ("Action", HomeLocators.ACTION_TITLE),
        ]

        for header_name, locator in expected_headers:
            header = self.first_visible([
                locator,
                f"//*[contains(@class,'ant-table') and contains({UPPER}, '{header_name.upper()}')]",
            ], timeout=10000)
            assert header, f"'{header_name}' column title is not visible in Assigned Batches section"

    def click_assigned_batches_next_arrow_button(self):
        next_arrow = self.first_visible([
            HomeLocators.ASSIGNED_BATCHES_NEXT_BUTTON,
            "//li[contains(@class,'ant-pagination-next')]/button[not(@disabled)]",
        ], timeout=5000)
        assert next_arrow, "Assigned Batches next arrow is not visible/clickable"
        try:
            next_arrow.click(timeout=4000)
        except Exception:
            next_arrow.click(timeout=4000, force=True)

