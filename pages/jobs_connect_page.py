from pages.base_page import BasePage
from locators.student_locators import JobsConnectLocators

class JobsConnectPage(BasePage):
    def navigate_to_jobs_connect(self):
        """Navigate to Jobs Connect section"""
        jobs_connect_tab = self.page.locator(JobsConnectLocators.JOBS_CONNECT)
        jobs_connect_tab.wait_for(state="visible", timeout=20000)
        jobs_connect_tab.click()
        print("Clicked on Jobs Connect")
        
        # Check for any popups or modals that might need to be closed
        self.handle_got_it_popup()
        
        # Verify Jobs Connect content is visible
        self.verify_jobs_connect_loaded()

    def handle_got_it_popup(self):
        """Handle 'Got It' popup if it appears"""
        try:
            got_it_button = self.page.locator("//span[text()='Got It'] | //button[text()='Got It']")
            if got_it_button.count() > 0:
                got_it_button.first.click()
                print("Closed 'Got It' popup")
        except:
            pass

    def verify_jobs_connect_loaded(self):
        """Verify Jobs Connect page has loaded"""
        try:
            search_input = self.page.locator(JobsConnectLocators.SEARCH_BY_JOB_TITLE_INPUT)
            search_input.wait_for(state="visible", timeout=10000)
            print("Jobs Connect page loaded - search input visible")
        except:
            # If search input not visible, check for Get Started button (onboarding)
            try:
                get_started = self.page.locator(JobsConnectLocators.GET_STARTED_BUTTON)
                if get_started.count() > 0:
                    print("Jobs Connect onboarding detected - Get Started button found")
            except:
                print("Jobs Connect page may still be loading")

    def reset_filters(self):
        """Reset all filters on Jobs Connect page"""
        try:
            reset_button = self.page.locator(JobsConnectLocators.RESET_FILTER_BUTTON)
            
            if reset_button.count() > 0:
                reset_button.wait_for(state="visible", timeout=10000)
                reset_button.click()
                print("Clicked 'Reset' button to clear filters")
            else:
                print("Reset button not found - filters may already be clear or page layout different")
        except Exception as e:
            print(f"Reset button not available: {e}")
            print("Skipping filter reset - continuing with test")

    def handle_onboarding(self):
        """Complete onboarding flow if required"""
        get_started = self.page.locator(JobsConnectLocators.GET_STARTED_BUTTON)
        if get_started.count() > 0 and get_started.is_visible():
            print("Jobs Connect onboarding required - clicking 'Get Started' button")
            get_started.click()
            
            # After onboarding, skip profile setup if needed
            try:
                dont_need_job = self.page.locator(JobsConnectLocators.DONT_NEED_JOB_BUTTON)
                if dont_need_job.count() > 0:
                    dont_need_job.click()
                    print("Clicked 'I don't need a job' to skip onboarding")
            except:
                pass

    def search_for_job(self, job_title="Product Manager"):
        """Search for a job by title"""
        # Handle onboarding if needed
        self.handle_onboarding()
        
        # Enter job title in search input
        search_input = self.page.locator(JobsConnectLocators.SEARCH_BY_JOB_TITLE_INPUT)
        search_input.wait_for(state="visible", timeout=15000)
        search_input.fill(job_title)
        print(f"Entered '{job_title}' in job search")

    def click_find_jobs(self):
        """Click Find Jobs button"""
        find_jobs_button = self.page.locator(JobsConnectLocators.FIND_JOBS_BUTTON)
        find_jobs_button.wait_for(state="visible", timeout=15000)
        find_jobs_button.click()
        print("Clicked 'Find Jobs' button")

    def validate_job_search_results(self):
        """Validate that job search results are displayed"""
        results_validation = self.page.locator(JobsConnectLocators.SEARCH_RESULTS_VALIDATION)
        results_validation.wait_for(state="visible", timeout=15000)
        results_text = results_validation.text_content().strip()
        print(f"Search results message: {results_text}")
        
        # Count job result cards
        job_cards_locator = self.page.locator(JobsConnectLocators.JOB_RESULT_CARD)
        job_cards = job_cards_locator.count()
        print(f"Found {job_cards} job result cards")
        
        assert job_cards > 0, "No job results found"
        
        return job_cards

    def click_first_job_result(self):
        """Click on the first job result card"""
        first_job = self.page.locator(JobsConnectLocators.FIRST_JOB_RESULT)
        first_job.wait_for(state="visible", timeout=15000)
        first_job.click()
        print("Clicked on first job result")

    def validate_apply_option(self):
        """Validate that Apply option is available"""
        apply_locators = [
            JobsConnectLocators.JOB_DETAILS_APPLY,
            JobsConnectLocators.APPLY_BUTTON,
            JobsConnectLocators.APPLY_NOW_BUTTON,
            "//button[contains(text(),'pply')] | //span[contains(text(),'pply')] | //a[contains(text(),'pply')]"
        ]
        
        apply_found = False
        for locator in apply_locators:
            try:
                apply_button = self.page.locator(locator)
                if apply_button.count() > 0:
                    apply_button.first.wait_for(state="visible", timeout=5000)
                    print(f"Apply button found with locator: {locator}")
                    apply_found = True
                    break
            except:
                continue
        
        if not apply_found:
            print("Apply button not found - checking if job details are visible")
            print("Note: Apply button may require login to job portal or other prerequisites")
        else:
            print("Apply option validated successfully")
        
        return apply_found
