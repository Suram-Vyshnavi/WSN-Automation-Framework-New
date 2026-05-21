from pages.base_page import BasePage
from locators.student_persona_locators.Jobsconnect_locators import jobsconnectLocators
from utils.helpers import attach_screenshot, highlight_element


class JobsConnectPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def _navigate_to_jobsconnect(self):
        """Navigate from dashboard to the Jobs Connect page."""
        from pages.studentpersona.home_dashboard_page import HomeDashboardPage
        if HomeDashboardPage._shared_dashboard_url:
            self.page.goto(HomeDashboardPage._shared_dashboard_url, wait_until="domcontentloaded", timeout=60000)
        self.page.locator(jobsconnectLocators.JOBS_CONNECT_CARD).wait_for(state="visible", timeout=15000)
        self.page.locator(jobsconnectLocators.JOBS_CONNECT_CARD).click()
        self.page.locator(jobsconnectLocators.VALIDATE_ALL_FILTERS).wait_for(state="visible", timeout=20000)

    def click_jobsconnect_card(self):
        self._navigate_to_jobsconnect()
        print("Clicked Jobs Connect card and navigated to Jobs Connect page")

    def click_jobtype_and_select_full_time(self):
        self.page.locator(jobsconnectLocators.JOB_TYPE_FILTER).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, jobsconnectLocators.JOB_TYPE_FILTER)
        self.page.locator(jobsconnectLocators.JOB_TYPE_FILTER).click()
        self.page.locator(jobsconnectLocators.FULL_TIME_OPTION).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, jobsconnectLocators.FULL_TIME_OPTION)
        self.page.locator(jobsconnectLocators.FULL_TIME_OPTION).click()
        print("Selected Full Time from Job Type filter")

    def click_workmode_and_select_office(self):
        self.page.locator(jobsconnectLocators.WORK_MODE_FILTER).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, jobsconnectLocators.WORK_MODE_FILTER)
        self.page.locator(jobsconnectLocators.WORK_MODE_FILTER).click()
        self.page.locator(jobsconnectLocators.OFFICE_OPTION).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, jobsconnectLocators.OFFICE_OPTION)
        self.page.locator(jobsconnectLocators.OFFICE_OPTION).click()
        print("Selected Office from Work Mode filter")

    def click_industry_sector_and_select_automotive(self):
        self.page.locator(jobsconnectLocators.INDUSTRY_SECTOR_FILTER).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, jobsconnectLocators.INDUSTRY_SECTOR_FILTER)
        self.page.locator(jobsconnectLocators.INDUSTRY_SECTOR_FILTER).click()
        self.page.locator(jobsconnectLocators.AUTOMOTIVE_OPTION).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, jobsconnectLocators.AUTOMOTIVE_OPTION)
        self.page.locator(jobsconnectLocators.AUTOMOTIVE_OPTION).click()
        print("Selected Automotive from Industry/Sector filter")

    def click_education_level_and_select_graduate(self):
        self.page.locator(jobsconnectLocators.EDUCATION_LEVEL_FILTER).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, jobsconnectLocators.EDUCATION_LEVEL_FILTER)
        self.page.locator(jobsconnectLocators.EDUCATION_LEVEL_FILTER).click()
        self.page.locator(jobsconnectLocators.GRADUATE_OPTION).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, jobsconnectLocators.GRADUATE_OPTION)
        self.page.locator(jobsconnectLocators.GRADUATE_OPTION).click()
        print("Selected Graduate from Education Level filter")

    def click_preferred_companies_and_select_diatoz(self):
        self.page.locator(jobsconnectLocators.PREFERRED_COMPANIES_FILTER).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, jobsconnectLocators.PREFERRED_COMPANIES_FILTER)
        self.page.locator(jobsconnectLocators.PREFERRED_COMPANIES_FILTER).click()
        self.page.wait_for_timeout(1000)
        # Type in search box within the dropdown if available (handles long company lists)
        search_input = self.page.locator("//div[text()='Preferred Companies']/parent::div/parent::div//input")
        if search_input.count() > 0:
            search_input.first.fill("Diatoz")
            self.page.wait_for_timeout(1000)
        # Scroll the option into view in case it is below the visible area
        try:
            self.page.locator(jobsconnectLocators.DIATOZ_OPTION).scroll_into_view_if_needed(timeout=10000)
        except Exception:
            pass
        self.page.locator(jobsconnectLocators.DIATOZ_OPTION).wait_for(state="visible", timeout=20000)
        highlight_element(self.page, jobsconnectLocators.DIATOZ_OPTION)
        self.page.locator(jobsconnectLocators.DIATOZ_OPTION).click()
        print("Selected DIATOZ from Preferred Companies filter")

    def search_by_role_title_and_find_jobs(self):
        self.page.locator(jobsconnectLocators.SEARCH_BY_JOB_TITLE).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, jobsconnectLocators.SEARCH_BY_JOB_TITLE)
        self.page.locator(jobsconnectLocators.SEARCH_BY_JOB_TITLE).fill("Product Manager")
        self.page.locator(jobsconnectLocators.FIND_JOBS_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, jobsconnectLocators.FIND_JOBS_BUTTON)
        try:
            with self.page.context.expect_page(timeout=5000) as new_page_info:
                self.page.locator(jobsconnectLocators.FIND_JOBS_BUTTON).click()
            new_page = new_page_info.value
            new_page.wait_for_load_state("domcontentloaded", timeout=30000)
            self.page = new_page
            print("Searched for 'Product Manager', clicked Find Jobs - switched to new tab")
            return new_page
        except Exception:
            # No new tab; results load in the same page
            self.page.wait_for_load_state("domcontentloaded", timeout=30000)
            print("Searched for 'Product Manager' and clicked Find Jobs")
            return None

    def click_first_job_card(self):
        self.page.locator(jobsconnectLocators.FIRST_JOB_CARD).wait_for(state="visible", timeout=40000)
        highlight_element(self.page, jobsconnectLocators.FIRST_JOB_CARD)
        self.page.locator(jobsconnectLocators.FIRST_JOB_CARD).click()
        self.page.wait_for_load_state("domcontentloaded", timeout=30000)
        print("Clicked on the first job card")

    def validate_about_job_and_company_sections(self):
        self.page.locator(jobsconnectLocators.VALIDATE_ABOUT_THE_JOB_BUTTON).wait_for(state="visible", timeout=30000)
        highlight_element(self.page, jobsconnectLocators.VALIDATE_ABOUT_THE_JOB_BUTTON)
        assert self.page.locator(jobsconnectLocators.VALIDATE_ABOUT_THE_JOB_BUTTON).count() > 0, "'About the job' button not found"
        self.page.locator(jobsconnectLocators.VALIDATE_ABOUT_THE_COMPANY_BUTTON).wait_for(state="visible", timeout=30000)
        highlight_element(self.page, jobsconnectLocators.VALIDATE_ABOUT_THE_COMPANY_BUTTON)
        assert self.page.locator(jobsconnectLocators.VALIDATE_ABOUT_THE_COMPANY_BUTTON).count() > 0, "'About the company' button not found"
        print("'About the job' and 'About the company' sections validated")

    def validate_apply_button_and_navigate_back(self):
        self.page.locator(jobsconnectLocators.VALIDATE_APPLY_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, jobsconnectLocators.VALIDATE_APPLY_BUTTON)
        assert self.page.locator(jobsconnectLocators.VALIDATE_APPLY_BUTTON).count() > 0, "Apply button not found"
        print("Apply button validated")
        self.page.go_back(wait_until="domcontentloaded", timeout=30000)
        self.page.locator(jobsconnectLocators.VALIDATE_ALL_FILTERS).wait_for(state="visible", timeout=20000)
        print("Closed job detail and navigated back to Jobs Connect page")

    def click_reset_button(self):
        self.page.locator(jobsconnectLocators.RESET_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, jobsconnectLocators.RESET_BUTTON)
        self.page.locator(jobsconnectLocators.RESET_BUTTON).click()
        print("Clicked Reset button")
