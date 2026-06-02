from pages.base_page import BasePage
from locators.student_persona_locators.Careerbuddy_locators import careerbuddy_locators
from utils.helpers import attach_screenshot, highlight_element


class CareerBuddyPage(BasePage):

    def click_career_buddy_card(self):
        self.page.locator(careerbuddy_locators.CAREER_BUDDY_CARD).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, careerbuddy_locators.CAREER_BUDDY_CARD)
        self.page.locator(careerbuddy_locators.CAREER_BUDDY_CARD).click()
        print("Clicked Career Buddy card")

    def click_language_dropdown_and_apply(self):
        self.page.locator(careerbuddy_locators.LANGUAGE_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, careerbuddy_locators.LANGUAGE_BUTTON)
        self.page.locator(careerbuddy_locators.LANGUAGE_BUTTON).click()
        self.page.locator(careerbuddy_locators.LANGUAGE_OPTION_ENGLISH).wait_for(state="visible", timeout=10000)
        highlight_element(self.page, careerbuddy_locators.LANGUAGE_OPTION_ENGLISH)
        self.page.locator(careerbuddy_locators.LANGUAGE_OPTION_ENGLISH).click()
        self.page.locator(careerbuddy_locators.APPLY_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.locator(careerbuddy_locators.APPLY_BUTTON).click()
        print("Language dropdown selected and Apply clicked")

    def click_language_close_button(self):
        self.page.locator(careerbuddy_locators.LANGUAGE_CLOSE_BUTTON).wait_for(state="visible", timeout=10000)
        highlight_element(self.page, careerbuddy_locators.LANGUAGE_CLOSE_BUTTON)
        self.page.locator(careerbuddy_locators.LANGUAGE_CLOSE_BUTTON).click()
        print("Language close button clicked")

    def click_sector_dropdown_and_apply(self):
        self.page.locator(careerbuddy_locators.SECTOR_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, careerbuddy_locators.SECTOR_BUTTON)
        self.page.locator(careerbuddy_locators.SECTOR_BUTTON).click()
        self.page.locator(careerbuddy_locators.SECTOR_OPTION_HEALTHCARE).wait_for(state="visible", timeout=10000)
        highlight_element(self.page, careerbuddy_locators.SECTOR_OPTION_HEALTHCARE)
        self.page.locator(careerbuddy_locators.SECTOR_OPTION_HEALTHCARE).click()
        self.page.locator(careerbuddy_locators.APPLY_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.locator(careerbuddy_locators.APPLY_BUTTON).click()
        print("Sector dropdown selected and Apply clicked")

    def click_sector_close_button(self):
        self.page.locator(careerbuddy_locators.SECTOR_CLOSE_BUTTON).wait_for(state="visible", timeout=10000)
        highlight_element(self.page, careerbuddy_locators.SECTOR_CLOSE_BUTTON)
        self.page.locator(careerbuddy_locators.SECTOR_CLOSE_BUTTON).click()
        print("Sector close button clicked")

    def click_location_dropdown_and_apply(self):
        self.page.locator(careerbuddy_locators.LOCATION_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, careerbuddy_locators.LOCATION_BUTTON)
        self.page.locator(careerbuddy_locators.LOCATION_BUTTON).click()
        self.page.locator(careerbuddy_locators.LOCATION_OPTION_BENGALURU).wait_for(state="visible", timeout=10000)
        highlight_element(self.page, careerbuddy_locators.LOCATION_OPTION_BENGALURU)
        self.page.locator(careerbuddy_locators.LOCATION_OPTION_BENGALURU).click()
        self.page.locator(careerbuddy_locators.APPLY_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.locator(careerbuddy_locators.APPLY_BUTTON).click()
        print("Location dropdown selected and Apply clicked")

    def click_location_close_button(self):
        self.page.locator(careerbuddy_locators.LOCATION_CLOSE_BUTTON).wait_for(state="visible", timeout=10000)
        highlight_element(self.page, careerbuddy_locators.LOCATION_CLOSE_BUTTON)
        self.page.locator(careerbuddy_locators.LOCATION_CLOSE_BUTTON).click()
        print("Location close button clicked")

    def click_job_role_dropdown_and_apply(self):
        self.page.locator(careerbuddy_locators.JOBROLE_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, careerbuddy_locators.JOBROLE_BUTTON)
        self.page.locator(careerbuddy_locators.JOBROLE_BUTTON).click()
        self.page.locator(careerbuddy_locators.JOBROLE_OPTION_SALES_ASSOCIATE).wait_for(state="visible", timeout=10000)
        highlight_element(self.page, careerbuddy_locators.JOBROLE_OPTION_SALES_ASSOCIATE)
        self.page.locator(careerbuddy_locators.JOBROLE_OPTION_SALES_ASSOCIATE).click()
        self.page.locator(careerbuddy_locators.APPLY_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.locator(careerbuddy_locators.APPLY_BUTTON).click()
        print("Job Role dropdown selected and Apply clicked")

    def click_job_role_close_button(self):
        self.page.locator(careerbuddy_locators.JOB_ROLE_CLOSE_BUTTON).wait_for(state="visible", timeout=10000)
        highlight_element(self.page, careerbuddy_locators.JOB_ROLE_CLOSE_BUTTON)
        self.page.locator(careerbuddy_locators.JOB_ROLE_CLOSE_BUTTON).click()
        print("Job Role close button clicked")

    def search_mentor_and_fill_details(self):
        self.page.locator(careerbuddy_locators.SEARCH_MENTORS_INPUT).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, careerbuddy_locators.SEARCH_MENTORS_INPUT)
        self.page.locator(careerbuddy_locators.SEARCH_MENTORS_INPUT).fill("leela b")
        print("Mentor search filled with details")

    def click_recommended_mentor_card(self):
        self.page.locator(careerbuddy_locators.RECOMMENDED_MENTOR_CARD).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, careerbuddy_locators.RECOMMENDED_MENTOR_CARD)
        self.page.locator(careerbuddy_locators.RECOMMENDED_MENTOR_CARD).click()
        print("Clicked on recommended mentor card")

    def validate_sector_jobrole_language_details(self):
        sectors = self.page.locator(careerbuddy_locators.VALIDATE_SECTORS_HEADER)
        sectors.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, careerbuddy_locators.VALIDATE_SECTORS_HEADER)
        assert sectors.count() > 0, "Sectors header not found on mentor profile"

        job_roles = self.page.locator(careerbuddy_locators.VALIDATE_JOB_ROLES_HEADER)
        job_roles.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, careerbuddy_locators.VALIDATE_JOB_ROLES_HEADER)
        assert job_roles.count() > 0, "Job Roles header not found on mentor profile"

        language = self.page.locator(careerbuddy_locators.VALIDATE_LANGUAGE_HEADER)
        language.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, careerbuddy_locators.VALIDATE_LANGUAGE_HEADER)
        assert language.count() > 0, "Language header not found on mentor profile"

        print("Sector, Job Role, and Language details validated on mentor profile")

    def click_book_session_button(self):
        self.page.locator(careerbuddy_locators.BOOK_SESSION_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, careerbuddy_locators.BOOK_SESSION_BUTTON)
        self.page.locator(careerbuddy_locators.BOOK_SESSION_BUTTON).click()
        print("Clicked Book Session button")

    def select_available_date_and_slot(self):
        self.page.locator(careerbuddy_locators.AVAILABLE_SELECT_DATE).first.wait_for(state="visible", timeout=15000)
        dates = self.page.locator(careerbuddy_locators.AVAILABLE_SELECT_DATE)
        count = dates.count()
        slot_found = False
        for i in range(count):
            dates.nth(i).click(force=True)
            try:
                self.page.locator(careerbuddy_locators.SLOT_BUTTON).first.wait_for(state="visible", timeout=5000)
                slot_found = True
                print(f"Slots found on date index {i}")
                break
            except Exception:
                print(f"No slots on date index {i}, trying next date...")
                continue
        assert slot_found, "No available slots found on any date in the calendar"
        highlight_element(self.page, careerbuddy_locators.SLOT_BUTTON)
        self.page.locator(careerbuddy_locators.SLOT_BUTTON).first.click()
        print("Available date selected and slot button clicked")

    def click_session_purpose_and_select_job_search_strategy(self):
        self.page.locator(careerbuddy_locators.SESSION_PURPOSE_LABEL).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, careerbuddy_locators.SESSION_PURPOSE_LABEL)
        # ant-select-selector is hidden by ant-design CSS — use force click via JS on its parent ant-select container
        purpose_select = "//label[contains(text(),'purpose of this session')]/following::div[contains(@class,'ant-select')][1]"
        self.page.locator(purpose_select).wait_for(state="attached", timeout=10000)
        self.page.locator(purpose_select).evaluate("el => el.querySelector('.ant-select-selector').click()")
        # Wait for the option and click it
        self.page.locator(careerbuddy_locators.JOB_SEARCH_STRATEGY_OPTION).wait_for(state="visible", timeout=10000)
        highlight_element(self.page, careerbuddy_locators.JOB_SEARCH_STRATEGY_OPTION)
        self.page.locator(careerbuddy_locators.JOB_SEARCH_STRATEGY_OPTION).click()
        print("Session purpose dropdown clicked and Job Search Strategy selected")

    def fill_specific_outcome_and_book(self):
        self.page.locator(careerbuddy_locators.SPECIFIC_OUTCOME_LABEL).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, careerbuddy_locators.SPECIFIC_OUTCOME_LABEL)
        # ant-input-borderless textarea is hidden to Playwright — use specific id + force fill
        outcome_textarea = "//textarea[@id='Outcome']"
        self.page.locator(outcome_textarea).wait_for(state="attached", timeout=10000)
        self.page.locator(outcome_textarea).fill("I need help in identifying right path", force=True)
        print("Specific outcome filled")
        self.page.locator(careerbuddy_locators.CHECKBOX_OPTION).wait_for(state="attached", timeout=10000)
        self.page.locator(careerbuddy_locators.CHECKBOX_OPTION).click(force=True)
        self.page.locator(careerbuddy_locators.BOOK_BUTTON).wait_for(state="visible", timeout=10000)
        highlight_element(self.page, careerbuddy_locators.BOOK_BUTTON)
        self.page.locator(careerbuddy_locators.BOOK_BUTTON).click()
        print("Checkbox selected and Book button clicked")

    def fill_session_details_and_book(self):
        self.page.locator(careerbuddy_locators.SESSION_PURPOSE_LABEL).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, careerbuddy_locators.SESSION_PURPOSE_LABEL)
        # Click the ant-select inside the booking modal to open the session purpose dropdown
        self.page.locator("//div[contains(@class,'ant-modal-content')]//div[contains(@class,'ant-select-selector')]").wait_for(state="visible", timeout=10000)
        self.page.locator("//div[contains(@class,'ant-modal-content')]//div[contains(@class,'ant-select-selector')]").click()
        # Wait for the dropdown panel to appear
        self.page.locator(careerbuddy_locators.SESSION_PURPOSE_DROPDOWN).wait_for(state="visible", timeout=10000)
        self.page.locator(careerbuddy_locators.JOB_SEARCH_STRATEGY_OPTION).wait_for(state="visible", timeout=10000)
        highlight_element(self.page, careerbuddy_locators.JOB_SEARCH_STRATEGY_OPTION)
        self.page.locator(careerbuddy_locators.JOB_SEARCH_STRATEGY_OPTION).click()

        self.page.locator(careerbuddy_locators.SPECIFIC_OUTCOME_LABEL).wait_for(state="visible", timeout=10000)
        highlight_element(self.page, careerbuddy_locators.SPECIFIC_OUTCOME_LABEL)
        self.page.locator(careerbuddy_locators.SPECIFIC_OUTCOME_LABEL).click()
        self.page.locator(careerbuddy_locators.SPECIFIC_OUTCOME_TEXTAREA).wait_for(state="visible", timeout=10000)
        self.page.locator(careerbuddy_locators.SPECIFIC_OUTCOME_TEXTAREA).fill("I need help in identifying the right path")
        self.page.locator(careerbuddy_locators.CHECKBOX_OPTION).wait_for(state="visible", timeout=10000)
        highlight_element(self.page, careerbuddy_locators.CHECKBOX_OPTION)
        self.page.locator(careerbuddy_locators.CHECKBOX_OPTION).click()

        self.page.locator(careerbuddy_locators.BOOK_BUTTON).wait_for(state="visible", timeout=10000)
        highlight_element(self.page, careerbuddy_locators.BOOK_BUTTON)
        self.page.locator(careerbuddy_locators.BOOK_BUTTON).click()
        print("Session details filled and Book button clicked")

    def click_copy_link_and_validate(self):
        self.page.locator(careerbuddy_locators.COPY_LINK_OPTION).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, careerbuddy_locators.COPY_LINK_OPTION)
        self.page.locator(careerbuddy_locators.COPY_LINK_OPTION).click()
        print("Copy Link option clicked and link validated")
