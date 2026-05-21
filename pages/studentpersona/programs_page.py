from pages.base_page import BasePage
from locators.student_persona_locators.programs_locators import programsLocators
from utils.helpers import attach_screenshot, highlight_element


class ProgramsPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def _navigate_to_programs(self):
        """Navigate from dashboard to the Programs page."""
        from pages.studentpersona.home_dashboard_page import HomeDashboardPage
        if HomeDashboardPage._shared_dashboard_url:
            self.page.goto(HomeDashboardPage._shared_dashboard_url, wait_until="domcontentloaded", timeout=60000)
        self.page.locator(programsLocators.PROGRAMS_CARD).wait_for(state="visible", timeout=15000)
        self.page.locator(programsLocators.PROGRAMS_CARD).click()
        self.page.locator(programsLocators.VALIDATE_INPROGRESS_TAB).wait_for(state="visible", timeout=15000)

    def validate_inprogress_and_completed_tabs(self):
        self._navigate_to_programs()
        highlight_element(self.page, programsLocators.VALIDATE_INPROGRESS_TAB)
        assert self.page.locator(programsLocators.VALIDATE_INPROGRESS_TAB).count() > 0, "In Progress tab not found"
        highlight_element(self.page, programsLocators.VALIDATE_COMPLETED_TAB)
        assert self.page.locator(programsLocators.VALIDATE_COMPLETED_TAB).count() > 0, "Completed tab not found"
        print("In Progress and Completed tabs validated")

    def click_inprogress_tab(self):
        self.page.locator(programsLocators.VALIDATE_INPROGRESS_TAB).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, programsLocators.VALIDATE_INPROGRESS_TAB)
        self.page.locator(programsLocators.VALIDATE_INPROGRESS_TAB).click()
        print("Clicked In Progress tab")

    def click_completed_tab(self):
        self.page.locator(programsLocators.VALIDATE_COMPLETED_TAB).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, programsLocators.VALIDATE_COMPLETED_TAB)
        self.page.locator(programsLocators.VALIDATE_COMPLETED_TAB).click()
        print("Clicked Completed tab")

    def validate_recommended_by_institute_header(self):
        self.page.locator(programsLocators.VALIDATE_RECOMMENDED_BY_INSTITUTE).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, programsLocators.VALIDATE_RECOMMENDED_BY_INSTITUTE)
        assert self.page.locator(programsLocators.VALIDATE_RECOMMENDED_BY_INSTITUTE).count() > 0, "Recommended by Institute header not found"
        print("Recommended by Institute header validated")

    def click_recommended_by_institute_tab(self):
        self.page.locator(programsLocators.RECOMMENDED_PROGRAM_CARD_ARROW_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, programsLocators.RECOMMENDED_PROGRAM_CARD_ARROW_BUTTON)
        self.page.locator(programsLocators.RECOMMENDED_PROGRAM_CARD_ARROW_BUTTON).click()
        print("Clicked Recommended by Institute tab arrow")

    def click_enroll_button(self):
        self.page.locator(programsLocators.ENROLL_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, programsLocators.ENROLL_BUTTON)
        self.page.locator(programsLocators.ENROLL_BUTTON).click()
        print("Clicked Enroll button")

    def validate_confirm_and_cancel_buttons(self):
        self.page.locator(programsLocators.VALIDATE_CONFIRM_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, programsLocators.VALIDATE_CONFIRM_BUTTON)
        assert self.page.locator(programsLocators.VALIDATE_CONFIRM_BUTTON).count() > 0, "Confirm button not found"
        highlight_element(self.page, programsLocators.VALIDATE_CANCEL_BUTTON)
        assert self.page.locator(programsLocators.VALIDATE_CANCEL_BUTTON).count() > 0, "Cancel button not found"
        print("Confirm and Cancel buttons validated")

    def click_close_modal_button(self):
        self.page.locator(programsLocators.CLOSE_MODAL_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, programsLocators.CLOSE_MODAL_BUTTON)
        self.page.locator(programsLocators.CLOSE_MODAL_BUTTON).click()
        print("Clicked Close Modal button")

    def validate_offered_by_wadhwani_foundation_header(self):
        self._navigate_to_programs()
        self.page.locator(programsLocators.VALIDATE_OFFERED_BY_WADHWANI_FOUNDATION).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, programsLocators.VALIDATE_OFFERED_BY_WADHWANI_FOUNDATION)
        assert self.page.locator(programsLocators.VALIDATE_OFFERED_BY_WADHWANI_FOUNDATION).count() > 0, "Offered by Wadhwani Foundation header not found"
        print("Offered by Wadhwani Foundation header validated")

    def click_offered_by_wadhwani_foundation_tab(self):
        from locators.student_persona_locators.new_homepage_locators import NewHomepageLocators
        # Click Offered by Wadhwani Foundation card arrow
        self.page.locator(programsLocators.RECOMMENDED_PROGRAM_CARD_8_ARROW_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, programsLocators.RECOMMENDED_PROGRAM_CARD_8_ARROW_BUTTON)
        self.page.locator(programsLocators.RECOMMENDED_PROGRAM_CARD_8_ARROW_BUTTON).click()
        print("Clicked Offered by Wadhwani Foundation tab arrow")
        # Enroll
        self.page.locator(programsLocators.ENROLL_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, programsLocators.ENROLL_BUTTON)
        self.page.locator(programsLocators.ENROLL_BUTTON).click()
        print("Clicked Enroll button")
        # Validate Confirm and Cancel
        self.page.locator(programsLocators.VALIDATE_CONFIRM_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, programsLocators.VALIDATE_CONFIRM_BUTTON)
        assert self.page.locator(programsLocators.VALIDATE_CONFIRM_BUTTON).count() > 0, "Confirm button not found"
        highlight_element(self.page, programsLocators.VALIDATE_CANCEL_BUTTON)
        assert self.page.locator(programsLocators.VALIDATE_CANCEL_BUTTON).count() > 0, "Cancel button not found"
        print("Confirm and Cancel buttons validated")
        # Close modal
        self.page.locator(programsLocators.CLOSE_MODAL_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, programsLocators.CLOSE_MODAL_BUTTON)
        self.page.locator(programsLocators.CLOSE_MODAL_BUTTON).click()
        print("Closed modal")
        # Navigate back to programs listing
        self._navigate_to_programs()
        # Open header profile menu and logout
        self.page.locator(NewHomepageLocators.HEADER_PROFILE_MENU_ICON).wait_for(state="attached", timeout=15000)
        self.page.locator(NewHomepageLocators.HEADER_PROFILE_MENU_ICON).click(force=True)
        print("Clicked Header Profile Menu icon")
        self.page.locator(NewHomepageLocators.LOG_OUT).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, NewHomepageLocators.LOG_OUT)
        self.page.locator(NewHomepageLocators.LOG_OUT).click()
        print("Clicked Logout")
