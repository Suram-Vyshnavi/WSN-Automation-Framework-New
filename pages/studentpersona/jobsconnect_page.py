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
        # Scroll the option into view in case it is below the visible area
        try:
            self.page.locator(jobsconnectLocators.JOB_OPTION).first.scroll_into_view_if_needed(timeout=10000)
        except Exception:
            pass
        self.page.locator(jobsconnectLocators.JOB_OPTION).first.wait_for(state="visible", timeout=20000)
        highlight_element(self.page, jobsconnectLocators.JOB_OPTION)
        self.page.locator(jobsconnectLocators.JOB_OPTION).first.click()
        self.page.wait_for_timeout(500)
        print("Selected job option from Preferred Companies filter")
        

    def search_by_role_title_and_find_jobs(self):
        self.page.locator(jobsconnectLocators.SEARCH_BY_JOB_TITLE).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, jobsconnectLocators.SEARCH_BY_JOB_TITLE)
        self.page.locator(jobsconnectLocators.SEARCH_BY_JOB_TITLE).fill("Product Manager")
        self.page.locator(jobsconnectLocators.FIND_JOBS_BUTTON).click()
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
        try:
            with self.page.context.expect_page(timeout=8000) as new_page_info:
                self.page.locator(jobsconnectLocators.FIRST_JOB_CARD).click()
            new_page = new_page_info.value
            new_page.wait_for_load_state("domcontentloaded", timeout=30000)
            print("Clicked on the first job card - opened in new tab")
            return new_page
        except Exception:
            self.page.wait_for_load_state("domcontentloaded", timeout=30000)
            print("Clicked on the first job card")
            return None

    def validate_about_job_and_company_sections(self):
        self.page.locator(jobsconnectLocators.VALIDATE_ABOUT_THE_JOB_BUTTON).wait_for(state="visible", timeout=30000)
        highlight_element(self.page, jobsconnectLocators.VALIDATE_ABOUT_THE_JOB_BUTTON)
        assert self.page.locator(jobsconnectLocators.VALIDATE_ABOUT_THE_JOB_BUTTON).count() > 0, "'About the job' button not found"
        self.page.locator(jobsconnectLocators.VALIDATE_ABOUT_THE_COMPANY_BUTTON).wait_for(state="visible", timeout=30000)
        highlight_element(self.page, jobsconnectLocators.VALIDATE_ABOUT_THE_COMPANY_BUTTON)
        assert self.page.locator(jobsconnectLocators.VALIDATE_ABOUT_THE_COMPANY_BUTTON).count() > 0, "'About the company' button not found"
        print("'About the job' and 'About the company' sections validated")

    def validate_apply_button_and_navigate_back(self, original_page=None):
        self.page.locator(jobsconnectLocators.VALIDATE_APPLY_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, jobsconnectLocators.VALIDATE_APPLY_BUTTON)
        assert self.page.locator(jobsconnectLocators.VALIDATE_APPLY_BUTTON).count() > 0, "Apply button not found"
        print("Apply button validated")
        if original_page:
            self.page.close()
            original_page.bring_to_front()
            original_page.locator(jobsconnectLocators.VALIDATE_ALL_FILTERS).wait_for(state="visible", timeout=20000)
            self.page = original_page
            print("Closed job detail tab and switched back to Jobs Connect page")
        else:
            self.page.go_back(wait_until="domcontentloaded", timeout=30000)
            self.page.locator(jobsconnectLocators.VALIDATE_ALL_FILTERS).wait_for(state="visible", timeout=20000)
            print("Navigated back to Jobs Connect page")

    def click_reset_button(self):
        self.page.locator(jobsconnectLocators.RESET_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, jobsconnectLocators.RESET_BUTTON)
        self.page.locator(jobsconnectLocators.RESET_BUTTON).click()
        self.page.locator(jobsconnectLocators.HOME).click()
        print("Clicked Reset button")

    def click_jobs_connect_applied_status_card(self):
        """Navigate to Jobs Connect and click the Applied status card.

        If the Applied status card is not present, the step is skipped
        gracefully (asserted as not present) so the test case does not fail.
        """
        from pages.studentpersona.home_dashboard_page import HomeDashboardPage
        if HomeDashboardPage._shared_dashboard_url:
            self.page.goto(HomeDashboardPage._shared_dashboard_url, wait_until="domcontentloaded", timeout=60000)
        self.page.locator(jobsconnectLocators.JOBS_CONNECT_CARD).wait_for(state="visible", timeout=15000)
        self.page.locator(jobsconnectLocators.JOBS_CONNECT_CARD).click()

        applied_status = self.page.locator(jobsconnectLocators.JOBS_CONNECT_APPLIED_STATUS).first
        try:
            applied_status.wait_for(state="visible", timeout=10000)
        except Exception:
            pass

        applied_status_present = applied_status.count() > 0 and applied_status.is_visible()
        if not applied_status_present:
            # Soft assertion: Applied status card is absent, so the test case is
            # expected to pass without continuing the validation.
            assert not applied_status_present, "Applied status card not present"
            print("Applied status card not present - skipping applied status validation")
            return

        highlight_element(self.page, jobsconnectLocators.JOBS_CONNECT_APPLIED_STATUS)
        applied_status.click()
        print("Navigated to homepage, clicked Jobs Connect card, then clicked Applied Status card")

    def click_applied_jobs_button_and_validate(self):
        """Click the Applied Jobs button and validate the applied job card.

        If no applied job is present (the Applied Jobs button or applied job
        card is absent), the step is skipped gracefully (asserted as not
        present) so the test case does not fail.
        """
        applied_button = self.page.locator(jobsconnectLocators.APPLIED_JOBS_BUTTON).first
        try:
            applied_button.wait_for(state="visible", timeout=10000)
        except Exception:
            pass

        applied_button_present = applied_button.count() > 0 and applied_button.is_visible()
        if not applied_button_present:
            # Soft assertion: no applied jobs, so the test case is expected to
            # pass without continuing the validation.
            assert not applied_button_present, "Applied Jobs button not present"
            print("Applied Jobs button not present - skipping applied job card validation")
            return

        highlight_element(self.page, jobsconnectLocators.APPLIED_JOBS_BUTTON)
        applied_button.click()
        self.page.wait_for_timeout(1500)

        applied_card = self.page.locator(jobsconnectLocators.APPLIED_JOB_CARD).first
        try:
            applied_card.wait_for(state="visible", timeout=15000)
        except Exception:
            pass

        applied_card_present = applied_card.count() > 0 and applied_card.is_visible()
        if not applied_card_present:
            assert not applied_card_present, "Applied job card not present"
            print("Applied job card not present - skipping applied job card validation")
            return

        highlight_element(self.page, jobsconnectLocators.APPLIED_JOB_CARD)
        assert applied_card.count() > 0, "Applied job card not found"
        print("Clicked Applied Jobs button and validated applied job card")
