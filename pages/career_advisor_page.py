from pages.base_page import BasePage
from utils.locators import CareerAdvisorLocators

class CareerAdvisorPage(BasePage):
    def navigate_to_career_advisor(self):
        """Navigate to Career Advisor section"""
        self.page.locator(CareerAdvisorLocators.CARRER_ADVISOR).wait_for(state="visible", timeout=20000)
        self.page.click(CareerAdvisorLocators.CARRER_ADVISOR)
        print("Clicked on Career Advisor")
        
        # Handle Got It popup if present
        self.handle_got_it_popup()

    def handle_got_it_popup(self):
        """Handle 'Got It' popup if it appears"""
        try:
            got_it = self.page.locator(CareerAdvisorLocators.GOT_IT)
            if got_it.count() > 0:
                got_it.wait_for(state="visible", timeout=10000)
                got_it.click()
                print("Handled 'Got It' popup")
        except Exception as e:
            print(f"Got It popup not found: {e}")

    def select_passions_preferences(self):
        """Click on Passions section to expand it"""
        
        print("Looking for Passions section header...")
        # Try multiple possible locators for Passions header
        passions_header = None
        locators_to_try = [
            "//h4[text()='Passions']",
            "//h4[contains(text(),'Passions')]",
            "//div[contains(@class, 'passion')]//h4",
            "text=Passions"
        ]
        
        for locator in locators_to_try:
            if self.page.locator(locator).count() > 0:
                passions_header = self.page.locator(locator).first
                print(f"Found Passions header using locator: {locator}")
                break
        
        if passions_header is None:
            print("ERROR: Could not find Passions header with any locator")
            raise Exception("Passions header not found")
        
        # Click on Passions section header to expand it
        passions_header.wait_for(state="visible", timeout=10000)
        passions_header.scroll_into_view_if_needed()
        passions_header.click()
        print("✓ Clicked on 'Passions' section to expand")

    def select_review_passions(self):
        """Click on Review button in Passions section"""
        print("Looking for Review button in Passions section...")
        
        # Try multiple possible locators for Review button
        review_button = None
        locators_to_try = [
            CareerAdvisorLocators.PASSIONS_REVIEW,
            "//span[text()='Review']",
            "//button[contains(., 'Review')]",
            "text=Review"
        ]
        
        for locator in locators_to_try:
            count = self.page.locator(locator).count()
            print(f"Trying locator '{locator}': found {count} element(s)")
            if count > 0:
                review_button = self.page.locator(locator).first
                print(f"✓ Found Review button using locator: {locator}")
                break
        
        if review_button is None:
            print("ERROR: Could not find Review button with any locator")
            page_text = self.page.locator("body").inner_text()
            print(f"Page text preview: {page_text[:500]}")
            raise Exception("Review button not found in Passions section")
        
        # Click on Review button
        review_button.wait_for(state="visible", timeout=10000)
        review_button.scroll_into_view_if_needed()
        review_button.click()
        print("✓ Clicked on 'Review' button in Passions section")

    def validate_passions_review(self):
        """Validate selected items in passions review section"""
        selected_items = self.page.locator(CareerAdvisorLocators.PASSIONS_SELECTED_ITEMS).first
        selected_items.wait_for(state="visible", timeout=15000)
        
        items_text = selected_items.text_content().strip()
        print(f"Selected passions items: {items_text}")
        
        assert len(items_text) > 0, "No passions selected items found"

    def click_submit_passions(self):
        """Click Submit button in passions section"""
        submit_button = self.page.locator(CareerAdvisorLocators.SUBMIT)
        submit_button.wait_for(state="visible", timeout=15000)
        submit_button.click()
        print("Clicked 'Submit' button in Passions section")

    def click_questionnaires_section(self):
        """Click on Questionnaires section"""
        questionnaires = self.page.locator(CareerAdvisorLocators.QUESTIONNAIRES)
        questionnaires.wait_for(state="visible", timeout=15000)
        questionnaires.click()
        print("Clicked on 'Questionnaires' section")

    def click_aptitudes_review(self):
        """Click on Review button in Aptitudes section"""
        aptitudes_review = self.page.locator(CareerAdvisorLocators.APTITUDES_REVIEW)
        aptitudes_review.wait_for(state="visible", timeout=15000)
        aptitudes_review.click()
        print("Clicked on 'Review' button in Aptitudes section")

    def click_reattempt(self):
        """Click on Reattempt button"""
        reattempt_button = self.page.locator(CareerAdvisorLocators.APTITUDES_REATTEMPT)
        reattempt_button.wait_for(state="visible", timeout=15000)
        reattempt_button.click()
        print("Clicked on 'Reattempt' button")

    def choose_slider_option(self):
        """Click on Slider option in Aptitudes"""
        slider_choose = self.page.locator(CareerAdvisorLocators.APTITUDES_SLIDER_CHOOSE)
        slider_choose.wait_for(state="visible", timeout=15000)
        slider_choose.click()
        print("Clicked 'Choose' for Slider option in Aptitudes")

    def change_slider_value_and_update(self):
        """Change slider value to 9 or 10 and click update"""
        
        slider_10 = self.page.locator(CareerAdvisorLocators.SLIDER_10)
        slider_9 = self.page.locator(CareerAdvisorLocators.SLIDER_9)
        
        try:
            # Check if slider 10 is currently selected
            slider_10_parent = self.page.locator(f"{CareerAdvisorLocators.SLIDER_10}/..")
            parent_classes = slider_10_parent.get_attribute("class") if slider_10_parent.count() > 0 else ""
            
            if parent_classes and ("selected" in parent_classes.lower() or "active" in parent_classes.lower()):
                # Current value is 10, change to 9
                slider_9.wait_for(state="visible", timeout=5000)
                slider_9.click()
                print("Current value was 10, changed to 9")
            else:
                # Current value is 9 (or other), change to 10
                slider_10.wait_for(state="visible", timeout=5000)
                slider_10.click()
                print("Current value was 9, changed to 10")
        except Exception as e:
            print(f"Could not determine current state: {e}")
            # Fallback: try to click slider 9
            slider_9.wait_for(state="visible", timeout=5000)
            slider_9.click()
            print("Fallback: Changed slider to 9")
        
        
        # Click Update button
        update_button = self.page.locator(CareerAdvisorLocators.APTITUDES_REATTEMPT_UPDATE)
        update_button.wait_for(state="visible", timeout=10000)
        update_button.click()
        print("Clicked 'Update' button")

    def click_go_to_matched_roles(self):
        """Click on 'Go to Matched Roles' button"""
        go_to_roles = self.page.locator(CareerAdvisorLocators.GO_TO_MATCHED_ROLES)
        go_to_roles.wait_for(state="visible", timeout=15000)
        go_to_roles.click()
        print("Clicked 'Go to Matched Roles' button")

    def click_search_roles(self):
        """Click on Search Roles section"""
        search_roles = self.page.locator(CareerAdvisorLocators.SEARCH_ROLES)
        search_roles.wait_for(state="visible", timeout=15000)
        search_roles.click()
        print("Clicked on 'Search Roles' section")

    def enter_jobrole_and_add_favourite(self, job_role="Project manager"):
        """Enter job role in search and add first job to favourites"""
        # Enter job role in search input
        search_input = self.page.locator(CareerAdvisorLocators.SEARCH_FOR_JOB_ROLE)
        search_input.wait_for(state="visible", timeout=15000)
        search_input.fill(job_role)
        print(f"Entered '{job_role}' in job role search")
        
        # Validate search results
        results = self.page.locator(CareerAdvisorLocators.RESULTS_SEARCH)
        if results.count() > 0:
            results_text = results.first.text_content().strip()
            print(f"Search results: {results_text}")
        
        # Add first job to favourites
        add_favourite = self.page.locator(CareerAdvisorLocators.ADD_FAVOURITE_JOB).first
        add_favourite.wait_for(state="visible", timeout=30000)
        add_favourite.first.click()
        print("Added first job to favourites")
        
        return job_role

    def click_favourites_and_validate(self):
        """Click on Favourites section and validate job is present"""
        favourites = self.page.locator(CareerAdvisorLocators.FAVOURITES)
        favourites.wait_for(state="visible", timeout=15000)
        favourites.first.click()
        print("Clicked on 'Favourites' section")
        
        checkfavorites = self.page.locator(CareerAdvisorLocators.REMOVE_FAVOURITE_JOB)
        checkfavorites.wait_for(state="visible", timeout=15000)
        print("Validated that the added job is in favourites")

    def click_share_report_and_validate(self):
        """Click on Share report button and validate share options"""
        # Click on Share button
        share_report_button = self.page.locator(CareerAdvisorLocators.SHARE_REPORT)
        share_report_button.wait_for(state="visible", timeout=30000)
        share_report_button.click()
        print("Clicked 'Share report' button")
        
        share_button = self.page.locator(CareerAdvisorLocators.SHARE_BUTTON)
        share_button.wait_for(state="visible", timeout=30000)
        share_button.click()
        print("Clicked 'Share' button")
        
        # Validate "Link copied" message
        link_copied = self.page.locator(CareerAdvisorLocators.LINK_COPIED_VALIDATION)
        link_copied.wait_for(state="visible", timeout=10000)
        link_copied_text = link_copied.text_content().strip()
        print(f"Share validation: {link_copied_text}")
        
        assert "Link copied" in link_copied_text or "copied" in link_copied_text.lower(), "Link copied message not displayed"

    def remove_job_from_favourites(self):
        """Navigate to Favourites and remove the job"""
        # Navigate back to Favourites section
        favourites = self.page.locator(CareerAdvisorLocators.FAVOURITES)
        favourites.wait_for(state="visible", timeout=15000)
        favourites.first.click()
        print("Clicked on 'Favourites' section")
        
        # Remove job from favourites
        remove_favourite = self.page.locator(CareerAdvisorLocators.REMOVE_FAVOURITE_JOB)
        remove_favourite.wait_for(state="visible", timeout=15000)
        remove_favourite.first.click()
        print("Removed job from favourites")
