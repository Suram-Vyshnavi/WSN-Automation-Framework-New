from pages.base_page import BasePage
from locators.student_locators import PlacementLocators, CareerBuddyLocators, InterviewPrepLocators

class PlacementPage(BasePage):
    def click_placement_prep(self):
        self.page.locator(PlacementLocators.PLACEMENT_PREP_MENU).wait_for(state="visible", timeout=20000)
        self.page.click(PlacementLocators.PLACEMENT_PREP_MENU)
        self.page.wait_for_load_state("networkidle")

    def verify_personal_pitch_tile(self):
        self.page.locator(PlacementLocators.PERSONAL_PITCH_TILE).wait_for(state="visible", timeout=10000)
        assert self.page.locator(PlacementLocators.PERSONAL_PITCH_TILE).is_visible()

    def click_explore(self):
        self.page.locator(PlacementLocators.EXPLORE_BTN).first.wait_for(state="visible", timeout=10000)
        self.page.locator(PlacementLocators.EXPLORE_BTN).first.click()

    def verify_header(self):
        self.page.locator(PlacementLocators.PERSONAL_PITCH_HEADER).wait_for(state="visible", timeout=10000)
        assert self.page.locator(PlacementLocators.PERSONAL_PITCH_HEADER).is_visible()

    def click_create_pitch(self):
        self.page.locator(PlacementLocators.CREATE_PITCH_BTN).wait_for(state="visible", timeout=10000)
        self.page.click(PlacementLocators.CREATE_PITCH_BTN, force=True)
        self.page.wait_for_load_state("networkidle")

    def handle_resume_modal(self):
        try:
            self.page.locator(PlacementLocators.RESUME_PITCH_MODAL).wait_for(state="visible", timeout=5000)
            self.page.locator(PlacementLocators.START_NEW_PITCH_BTN).wait_for(state="visible", timeout=5000)
            self.page.click(PlacementLocators.START_NEW_PITCH_BTN)
            self.page.wait_for_load_state("networkidle")
        except:
            # Modal might not appear if it's a fresh start
            pass

    def verify_step_1(self):
        self.page.locator(PlacementLocators.STEP_1_INDICATOR).wait_for(state="visible", timeout=10000)
        self.page.locator(PlacementLocators.TARGET_JOB_HEADER).wait_for(state="visible", timeout=10000)
        assert self.page.locator(PlacementLocators.TARGET_JOB_HEADER).is_visible()

    def enter_job_role(self, role):
        # Click container to focus
        self.page.locator(PlacementLocators.JOB_ROLE_CONTAINER).first.click(force=True)
        
        # Type the role
        self.page.keyboard.type(role, delay=100)
        
        # Wait for and click the validation/submit button
        self.page.locator(PlacementLocators.JOB_ROLE_SUBMIT_BTN).wait_for(state="visible", timeout=5000)
        self.page.locator(PlacementLocators.JOB_ROLE_SUBMIT_BTN).click()
        
        # Wait for button to disappear or next state

    def handle_understand_popup(self):
        try:
            if self.page.locator(PlacementLocators.UNDERSTAND_BTN).is_visible(timeout=5000):
                self.page.click(PlacementLocators.UNDERSTAND_BTN)
                self.page.wait_for_load_state("networkidle")
        except:
            pass

    def verify_step_2(self):
        self.page.locator(PlacementLocators.STEP_2_INDICATOR).wait_for(state="visible", timeout=10000)
        assert self.page.locator(PlacementLocators.STEP_2_INDICATOR).is_visible()
        self.page.locator(PlacementLocators.RECORD_PITCH_HEADER).wait_for(state="visible", timeout=10000)
        assert self.page.locator(PlacementLocators.RECORD_PITCH_HEADER).is_visible()

    def handle_leaving_modal(self):
        try:
            self.page.locator(PlacementLocators.LEAVING_PITCH_MODAL).wait_for(state="visible", timeout=5000)
            self.page.click(PlacementLocators.SAVE_EXIT_BTN)
        except:
            pass

    def handle_language_alert(self):
        try:
            if self.page.locator(PlacementLocators.LANGUAGE_ALERT_HEADER).is_visible(timeout=5000):
                 self.page.click(PlacementLocators.LANGUAGE_ALERT_CONTINUE_BTN, force=True)
                 self.page.wait_for_load_state("networkidle")
        except:
            pass

    # Career Buddy Methods
    def click_career_buddy_explore(self):
        self.page.locator(CareerBuddyLocators.EXPLORE_BTN).wait_for(state="visible", timeout=10000)
        self.page.click(CareerBuddyLocators.EXPLORE_BTN, force=True)
        self.page.wait_for_load_state("networkidle")

    def search_mentor(self, name):
        self.page.locator(CareerBuddyLocators.SEARCH_INPUT).wait_for(state="visible", timeout=10000)
        self.page.fill(CareerBuddyLocators.SEARCH_INPUT, name)
        self.page.locator(CareerBuddyLocators.MENTOR_NAME).wait_for(state="visible", timeout=10000)

    def book_session_flow(self):
        # Click Book Session on Mentor Card
        self.page.locator(CareerBuddyLocators.BOOK_SESSION_BTN).first.click()
        self.page.wait_for_load_state("networkidle")
        
        # Select Date with Slots
        # Wait for calendar to be visible
        self.page.locator(CareerBuddyLocators.AVAILABLE_DATE).first.wait_for(state="visible", timeout=10000)
        
        # Get all available dates
        available_dates = self.page.locator(CareerBuddyLocators.AVAILABLE_DATE).all()
        
        slots_found = False
        for i in range(len(available_dates)):
            # Re-query elements to avoid stale element errors if DOM refreshes
            dates = self.page.locator(CareerBuddyLocators.AVAILABLE_DATE).all()
            if i >= len(dates): break
            
            date = dates[i]
            date.click()
            # Wait a bit for slots to load or 'no slots' message
            try:
                # Expect either slots or no slots message
                self.page.wait_for_selector(f"{CareerBuddyLocators.TIME_SLOT} | {CareerBuddyLocators.NO_SLOTS_MSG}", timeout=3000)
                
                if self.page.locator(CareerBuddyLocators.TIME_SLOT).count() > 0:
                    slots_found = True
                    break
            except:
                continue
                
        if not slots_found:
            print("No time slots available for any of the visible dates. Skipping booking flow.")
            return False  # Return False to indicate no slots available

        # Select Time Slot (First one)
        self.page.locator(CareerBuddyLocators.TIME_SLOT).first.click()
        return True  # Return True to indicate slot was selected successfully

    def fill_booking_details(self):
        # Select Purpose (assuming Dropdown)
        # Try clicking the selector using JS to bypass viewport issues
        dropdown = self.page.locator(CareerBuddyLocators.SESSION_PURPOSE_DROPDOWN).first
        dropdown.wait_for(state="attached", timeout=10000)
        # Force click via JS
        dropdown.evaluate("element => element.click()")
        
        self.page.locator(CareerBuddyLocators.SESSION_PURPOSE_OPTION).wait_for(state="visible", timeout=5000)
        self.page.locator(CareerBuddyLocators.SESSION_PURPOSE_OPTION).click()

        # Enter Outcome
        # Click container to expand if needed
        container = self.page.locator("//div[contains(@class, 'meeting_outcome_textarea')]")
        if container.is_visible():
            container.click()
            
        self.page.fill(CareerBuddyLocators.OUTCOME_TEXTAREA, "I need help with my resume.")

        # Check Checkbox
        self.page.locator(CareerBuddyLocators.CHECKBOX).check()

        # Click Book
        book_btn = self.page.locator(CareerBuddyLocators.BOOK_CONFIRM_BTN).first
        book_btn.evaluate("element => element.click()")
        self.page.wait_for_load_state("networkidle")

    def verify_meeting_details(self):
        self.page.locator(CareerBuddyLocators.MEETING_HEADER).wait_for(state="visible", timeout=20000)
        assert self.page.locator(CareerBuddyLocators.MEETING_HEADER).is_visible()

    # Interview Coach Methods
    def verify_interview_coach_tile(self):
        """Verify Interview Coach tile is visible"""
        self.page.locator(InterviewPrepLocators.INTERVIEW_COACH_CARD).wait_for(state="visible", timeout=10000)
        assert self.page.locator(InterviewPrepLocators.INTERVIEW_COACH_CARD).is_visible()
        print("Interview Coach tile verified")

    def click_interview_coach_explore(self):
        """Click Explore button for Interview Coach"""
        self.page.locator(InterviewPrepLocators.INTERVIEW_COACH_EXPLORE_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.click(InterviewPrepLocators.INTERVIEW_COACH_EXPLORE_BUTTON)
        self.page.wait_for_load_state("networkidle")
        print("Clicked Interview Coach Explore button")

    def validate_textbox_and_mic(self):
        """Validate textbox and mic button are visible"""
        self.page.locator(InterviewPrepLocators.INTERVIEW_PREP_TEXTBOX).wait_for(state="visible", timeout=10000)
        assert self.page.locator(InterviewPrepLocators.INTERVIEW_PREP_TEXTBOX).is_visible()
        print("Textbox is visible")
        
        self.page.locator(InterviewPrepLocators.VALIDATE_INTERVIEW_PREP_MICBUTTON).wait_for(state="visible", timeout=10000)
        assert self.page.locator(InterviewPrepLocators.VALIDATE_INTERVIEW_PREP_MICBUTTON).is_visible()
        print("Mic button is visible")

    def send_interview_details(self, role1="Product Manager", role2="E-commerce"):
        """Send interview coaching details - two roles"""
        # Send first role
        self.page.locator(InterviewPrepLocators.INTERVIEW_PREP_TEXTBOX).wait_for(state="visible", timeout=10000)
        self.page.fill(InterviewPrepLocators.INTERVIEW_PREP_TEXTBOX, role1)
        self.page.locator(InterviewPrepLocators.INTERVIEW_COACH_SEND_ICON).click()
        print(f"Sent first role: {role1}")
        
        # Send second role
        self.page.locator(InterviewPrepLocators.INTERVIEW_PREP_TEXTBOX).wait_for(state="visible", timeout=10000)
        self.page.fill(InterviewPrepLocators.INTERVIEW_PREP_TEXTBOX, role2)
        self.page.locator(InterviewPrepLocators.INTERVIEW_COACH_SEND_ICON).click()
        print(f"Sent second role: {role2}")

    def click_practice_interviewing(self):
        """Click on 'Practise Interviewing for the role'"""
        self.page.locator(InterviewPrepLocators.PRACTISE_INTERVIEWING_FOR_ROLE).wait_for(state="visible", timeout=10000)
        self.page.click(InterviewPrepLocators.PRACTISE_INTERVIEWING_FOR_ROLE)
        print("Clicked 'Practise Interviewing for the role'")

    def validate_start_button(self):
        """Validate Start button is visible and clickable"""
        self.page.locator(InterviewPrepLocators.VALIDATE_START_BUTTON).wait_for(state="visible", timeout=10000)
        assert self.page.locator(InterviewPrepLocators.VALIDATE_START_BUTTON).is_visible()
        print("Start button is visible")

    def navigate_back_and_delete(self):
        """Navigate back from questions page and delete the created interview coaching"""
        # Click back icon
        self.page.locator(InterviewPrepLocators.BACK_ICON).wait_for(state="visible", timeout=10000)
        self.page.click(InterviewPrepLocators.BACK_ICON)
        print("Navigated back from questions page")
        
        # Click more details icon
        current_roles_locator = self.page.locator(InterviewPrepLocators.YOUR_RECENT_ROLES)
        current_roles_locator.scroll_into_view_if_needed()
        More_details_locator = self.page.locator(InterviewPrepLocators.MORE_DETAILS_ICON)
        More_details_locator.scroll_into_view_if_needed()
        More_details_locator.click()
        print("Clicked more details icon")
        
        # Click Delete this role
        self.page.locator(InterviewPrepLocators.DELETE_ROLE).wait_for(state="visible", timeout=10000)
        self.page.click(InterviewPrepLocators.DELETE_ROLE)
        print("Clicked 'Delete this role'")
        
        # Confirm deletion
        self.page.locator(InterviewPrepLocators.DELETE_ROLE_CONFIRM_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.click(InterviewPrepLocators.DELETE_ROLE_CONFIRM_BUTTON)
        print("Confirmed deletion")
