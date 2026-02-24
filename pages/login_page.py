from pages.base_page import BasePage
from utils.locators import LoginLocators, CareerAdvisorLocators, DashboardLocators
from utils.helpers import highlight_element, attach_screenshot


class LoginPage(BasePage):
    def open(self, url):
        """Navigate to the login page"""
        self.page.goto(url)

    def dismiss_popup_if_present(self):
        """Dismiss notification popup if present"""
        try:
            later_btn = self.page.locator("//button[normalize-space()=\"I'll do it later\"]")
            later_btn.wait_for(state="attached", timeout=20000)
            later_btn.click(force=True)
            print("Popup dismissed")
        except Exception:
            print("Popup not found / already dismissed")

    def click_get_started(self):
        """Click Get Started button"""
        self.page.locator(LoginLocators.GET_STARTED_BUTTON).wait_for(state="visible", timeout=20000)
        self.validate_using_inner_text(LoginLocators.GET_STARTED_BUTTON, "get started")
        self.page.click(LoginLocators.GET_STARTED_BUTTON)
        

    def click_continue_with_email(self):
        """Click Continue with Email/Login button"""
        self.page.locator(LoginLocators.LOGIN_BUTTON).wait_for(state="visible", timeout=10000)
        self.validate_using_inner_text(LoginLocators.LOGIN_BUTTON, "continue with email")   
        self.page.click(LoginLocators.LOGIN_BUTTON)

    def login(self, username, password):
        """Enter username and password and submit login form"""
        self.page.locator(LoginLocators.USERNAME_INPUT).wait_for(state="visible", timeout=10000)
        self.page.fill(LoginLocators.USERNAME_INPUT, username)
        self.page.click(LoginLocators.NEXT_BUTTON)

        self.page.locator(LoginLocators.PASSWORD_INPUT).wait_for(state="visible", timeout=10000)
        self.page.fill(LoginLocators.PASSWORD_INPUT, password)
        self.page.click(LoginLocators.SUBMIT_BUTTON)

    def wait_for_home_page(self):
        """Wait for home page to load after login"""
        Wadhwani_logo=self.page.locator(LoginLocators.WADHWANI_LOGO)
        Wadhwani_logo.wait_for(state="visible", timeout=20000)
        highlight_element(self.page, LoginLocators.WADHWANI_LOGO)
        assert Wadhwani_logo.count() > 0 , "Login may have failed - Wadhwani logo not visible on home page"
        print("Login successful - home page loaded")

    def navigate_to_dashboard(self):
        """Navigate through dashboard"""
        self.page.locator(LoginLocators.HOME_BUTTON).wait_for(state="visible", timeout=20000)
        self.validate_using_inner_text(LoginLocators.HOME_BUTTON, "home")
        self.page.click(LoginLocators.HOME_BUTTON)
        self.page.locator(LoginLocators.CARD).first.wait_for(state="visible", timeout=20000)
        self.page.locator(LoginLocators.CARD).first.click()

    def click_career_advisor(self):
        """Click on Career Advisor menu item"""
        self.page.locator(LoginLocators.CARRER_ADVISOR).wait_for(state="visible", timeout=20000)
        self.validate_using_inner_text(LoginLocators.CARRER_ADVISOR, "career advisor")
        self.page.click(LoginLocators.CARRER_ADVISOR)
        
        # Handle Got It popup after clicking Career Advisor
        try:
            self.page.locator(CareerAdvisorLocators.GOT_IT).wait_for(state="visible", timeout=10000)
            self.page.click(CareerAdvisorLocators.GOT_IT)
            print("Career Advisor - Got It popup clicked")
        except Exception as e:
            print(f"Got It popup not found in Career Advisor: {e}")

    def click_placement_prep(self):
        """Click on Placement Prep menu item"""
        self.page.locator(LoginLocators.PLACEMENT_PREP).wait_for(state="visible", timeout=20000)
        self.validate_using_inner_text(LoginLocators.PLACEMENT_PREP, "placement prep")
        self.page.click(LoginLocators.PLACEMENT_PREP)

    def click_jobs_connect(self):
        """Click on Jobs Connect menu item"""
        self.page.locator(LoginLocators.JOBS_CONNECT).wait_for(state="visible", timeout=20000)
        self.validate_using_inner_text(LoginLocators.JOBS_CONNECT, "jobs connect")
        self.page.click(LoginLocators.JOBS_CONNECT)

    def click_calendar(self):
        """Click on Calendar menu item"""
        self.page.locator(LoginLocators.CALENDER).wait_for(state="visible", timeout=20000)
        self.page.click(LoginLocators.CALENDER)

    def navigate_support(self):
        """Navigate to support page and return"""
        self.page.locator(LoginLocators.SUPPORT_ICON).wait_for(state="visible", timeout=20000)

        # Capture new tab
        with self.page.context.expect_page() as new_page_info:
            self.page.click(LoginLocators.SUPPORT_ICON)
        support_page = new_page_info.value
        support_page.wait_for_load_state()

        # Close support tab
        support_page.close()

        # Back to main page
        self.page.bring_to_front()

        # Click chat icon
        self.page.locator(LoginLocators.CHAT_ICON).click()

    def check_notifications_and_chat(self):
        """Check notifications and chat icons"""
        self.page.locator(LoginLocators.CHAT_ICON).wait_for(state="visible", timeout=20000)
        self.page.click(LoginLocators.CHAT_ICON)
        self.page.locator(LoginLocators.NOTIFICATIONS_ICON).wait_for(state="visible", timeout=20000)
        self.page.click(LoginLocators.NOTIFICATIONS_ICON)
        self.page.locator(LoginLocators.CLOSE_NOTIFICATION).wait_for(state="visible", timeout=20000)
        self.page.click(LoginLocators.CLOSE_NOTIFICATION)

    def click_profile_icon(self):
        """Click on profile icon"""
        self.page.locator(LoginLocators.PROFILE_ICON).wait_for(state="visible", timeout=20000)
        self.page.click(LoginLocators.PROFILE_ICON)


    def verify_profile_fields_visible(self):
        """Verify profile fields are visible"""
        fields = [
            LoginLocators.FIRST_NAME,
            LoginLocators.LAST_NAME,
            LoginLocators.SELECT_COUNTRY,
            LoginLocators.SELECT_CITY,
            LoginLocators.UPDATE_PROFILE,
        ]

        # Sometimes the profile menu requires clicking 'My Profile' first.
        try:
            self.page.locator(LoginLocators.FIRST_NAME).wait_for(state="visible", timeout=3000)
        except Exception:
            # Open My Profile view if fields not already visible
            try:
                self.page.locator(LoginLocators.MY_PROFILE).wait_for(state="visible", timeout=8000)
                self.validate_using_inner_text(LoginLocators.MY_PROFILE, "my profile")
                self.page.click(LoginLocators.MY_PROFILE)
                # Click Edit to reveal the fields
                self.page.locator(LoginLocators.EDIT_PROFILE).wait_for(state="visible", timeout=8000)
                self.validate_using_inner_text(LoginLocators.EDIT_PROFILE, "edit")
                self.page.click(LoginLocators.EDIT_PROFILE)
            except Exception:
                # If MY_PROFILE isn't present, try opening profile icon again and then Edit
                try:
                    self.page.click(LoginLocators.PROFILE_ICON)
                    self.page.locator(LoginLocators.MY_PROFILE).wait_for(state="visible", timeout=8000)
                    self.validate_using_inner_text(LoginLocators.MY_PROFILE, "my profilee")
                    self.page.click(LoginLocators.MY_PROFILE)
                    self.page.locator(LoginLocators.EDIT_PROFILE).wait_for(state="visible", timeout=8000)
                    self.validate_using_inner_text(LoginLocators.EDIT_PROFILE, "editt")
                    self.page.click(LoginLocators.EDIT_PROFILE)
                except Exception:
                    pass

        for locator in fields:
            self.page.locator(locator).wait_for(state="visible", timeout=15000)
            assert self.page.locator(locator).is_visible(), f"Profile field {locator} not visible"

    def edit_profile_details(self, first_name="Wadhwani12", last_name="Foundation12", country="India", city="Bangalore, Bangalore, Karnataka, India", whatsapp_number="9182269382"):
        """Edit profile details"""
        # If fields already visible, proceed to fill. Otherwise open My Profile -> Edit
        try:
            self.page.locator(LoginLocators.FIRST_NAME).wait_for(state="visible", timeout=3000)
        except Exception:
            try:
                self.page.locator(LoginLocators.MY_PROFILE).wait_for(state="visible", timeout=8000)
                self.validate_using_inner_text(LoginLocators.MY_PROFILE, "my profile")
                self.page.click(LoginLocators.MY_PROFILE)
                self.page.locator(LoginLocators.EDIT_PROFILE).wait_for(state="visible", timeout=8000)
                self.validate_using_inner_text(LoginLocators.EDIT_PROFILE, "edit")
                self.page.click(LoginLocators.EDIT_PROFILE)
            except Exception:
                # Fallback: try opening profile icon then my profile and edit
                try:
                    self.page.click(LoginLocators.PROFILE_ICON)
                    self.page.locator(LoginLocators.MY_PROFILE).wait_for(state="visible", timeout=8000)
                    self.validate_using_inner_text(LoginLocators.MY_PROFILE, "my profile")
                    self.page.click(LoginLocators.MY_PROFILE)
                    self.page.locator(LoginLocators.EDIT_PROFILE).wait_for(state="visible", timeout=8000)
                    self.validate_using_inner_text(LoginLocators.EDIT_PROFILE, "edit")
                    self.page.click(LoginLocators.EDIT_PROFILE)
                except Exception:
                    pass

        self.page.fill(LoginLocators.FIRST_NAME, first_name)
        self.page.fill(LoginLocators.LAST_NAME, last_name)
        self.page.locator(LoginLocators.SELECT_COUNTRY).scroll_into_view_if_needed()
        self.page.locator(f"text={country}").first.click()
        self.page.locator(LoginLocators.SELECT_CITY).scroll_into_view_if_needed()
        self.page.locator(f"text={city}").first.click()
        self.page.locator(LoginLocators.UPDATE_PROFILE).scroll_into_view_if_needed()
        self.page.locator(".container-content").evaluate("el => el.scrollTop = el.scrollHeight")
        self.page.click(LoginLocators.UPDATE_PROFILE)

    def click_logout(self):
        """Click logout button"""
        # Wait for logout button to be visible in the dropdown
        self.page.locator(LoginLocators.LOGOUT_BUTTON).wait_for(state="visible", timeout=15000)
        self.page.click(LoginLocators.LOGOUT_BUTTON)

    def logout(self):
        """Complete logout flow (click profile icon then logout)"""
        # Wait to ensure any previous dropdowns are fully closed
        # Click profile icon to open dropdown menu
        self.click_profile_icon()
        # Wait for dropdown animation to complete
        # Click logout button
        self.click_logout()

    def navigate_to_home(self):
        """Navigate to home page"""
        self.page.locator(LoginLocators.HOME_BUTTON).wait_for(state="visible", timeout=20000)
        self.validate_using_inner_text(LoginLocators.HOME_BUTTON, "home")
        self.page.click(LoginLocators.HOME_BUTTON)

    # Dashboard Section Validations
    
    def validate_recommended_activities_section(self):
        """Validate recommended activities section on dashboard"""
        self.navigate_to_home()
        
        try:
            # Locate and scroll to recommended activities section
            section_locator = self.page.locator(DashboardLocators.RECOMMENDED_ACTIVITIES_SECTION).first
            section_locator.scroll_into_view_if_needed()
            
            section_locator.wait_for(state="visible", timeout=10000)
            section_visible = section_locator.is_visible()
            self.validate_using_inner_text(DashboardLocators.RECOMMENDED_ACTIVITIES_SECTION, "Recommended Activities")
            assert section_visible, "Recommended Activities section not visible"
            
            # Highlight the section
            print("Highlighting Recommended Activities Section Heading...")
            highlight_element(self.page, section_locator, duration=2000)
            
            # Check for activity/forum cards
            activity_cards = self.page.locator(DashboardLocators.RECOMMENDED_ACTIVITY_CARD).count()
            print(f"Found {activity_cards} recommended activity/forum cards")
            
            # Check for forum badges within cards
            forum_cards = self.page.locator(DashboardLocators.FORUM_CARD).count()
            print(f"Found {forum_cards} forum badges")
            
            # Highlight each card
            if activity_cards > 0:
                for i in range(min(activity_cards, 5)):  # Highlight first 5 cards
                    try:
                        print(f"Highlighting card {i+1}...")
                        card = self.page.locator(DashboardLocators.RECOMMENDED_ACTIVITY_CARD).nth(i)
                        highlight_element(self.page, card, duration=1500)
                    except Exception as e:
                        print(f"Could not highlight card {i+1}: {e}")
            
            attach_screenshot(self.page, f"Recommended Activities - {activity_cards} cards ({forum_cards} forums)")
        except Exception as e:
            print(f"Recommended Activities section not found or not visible: {e}")
            attach_screenshot(self.page, "Recommended Activities - Section not found")

    def validate_ongoing_course_section(self):
        """Validate ongoing course section on dashboard"""
        try:
            # Locate and scroll to ongoing course section
            ongoing_locator = self.page.locator(DashboardLocators.ONGOING_COURSE_SECTION).first
            ongoing_locator.scroll_into_view_if_needed()
            
            ongoing_locator.wait_for(state="visible", timeout=10000)
            section_visible = ongoing_locator.is_visible()
            assert section_visible, "Ongoing Course section not visible"
            print("Highlighting Ongoing Course Section Heading...")
            highlight_element(self.page, ongoing_locator, duration=2000)
            
            # Check for course cards
            progress_cards = self.page.locator(DashboardLocators.LEARNING_PROGRESS_CARD).count()
            print(f"Found {progress_cards} ongoing course cards")
            
            # Highlight course cards
            if progress_cards > 0:
                for i in range(min(progress_cards, 3)):
                    try:
                        print(f"Highlighting course card {i+1}...")
                        card = self.page.locator(DashboardLocators.LEARNING_PROGRESS_CARD).nth(i)
                        highlight_element(self.page, card, duration=1500)
                    except Exception as e:
                        print(f"Could not highlight course card {i+1}: {e}")
            
            # Check for progress bars
            progress_bars = self.page.locator(DashboardLocators.COURSE_PROGRESS_BAR).count()
            print(f"Found {progress_bars} course progress bars")
            
            # Highlight first progress bar
            if progress_bars > 0:
                try:
                    print("Highlighting progress bar...")
                    first_bar = self.page.locator(DashboardLocators.COURSE_PROGRESS_BAR).first
                    highlight_element(self.page, first_bar, duration=1500)
                except Exception as e:
                    print(f"Could not highlight progress bar: {e}")
            
            attach_screenshot(self.page, f"Ongoing Courses - {progress_cards} cards with {progress_bars} progress bars")
        except Exception as e:
            print(f"Ongoing Course section not found: {e}")
            attach_screenshot(self.page, "Ongoing Course - Section not found")

    def validate_institute_specific_courses(self):
        """Validate institute specific courses section on dashboard"""
        try:
            # Locate and scroll to institute courses section
            institute_locator = self.page.locator(DashboardLocators.INSTITUTE_COURSES_SECTION)
            institute_locator.scroll_into_view_if_needed()
            
            # Validate section heading
            institute_locator.wait_for(state="visible", timeout=10000)
            section_visible = institute_locator.is_visible()
            assert section_visible, "Institute Courses section not visible"
            print("Highlighting Institute Courses Section Heading...")
            highlight_element(self.page, institute_locator, duration=2000)
            
            # Validate Programs subheading and program cards
            programs_heading = self.page.locator(DashboardLocators.INSTITUTE_PROGRAMS_SUBHEADING).first
            program_cards = 0
            if programs_heading.is_visible():
                print("Highlighting Programs Subheading...")
                highlight_element(self.page, programs_heading, duration=1500)
                program_cards = self.page.locator(DashboardLocators.INSTITUTE_PROGRAM_CARD).count()
                print(f"Found {program_cards} institute program cards")
                
                # Highlight first 3 program cards
                if program_cards > 0:
                    for i in range(min(program_cards, 3)):
                        try:
                            print(f"Highlighting program card {i+1}...")
                            card = self.page.locator(DashboardLocators.INSTITUTE_PROGRAM_CARD).nth(i)
                            highlight_element(self.page, card, duration=1500)
                        except Exception as e:
                            print(f"Could not highlight program card {i+1}: {e}")
            
            # Validate Courses subheading and course cards
            courses_heading = self.page.locator(DashboardLocators.INSTITUTE_COURSES_SUBHEADING).first
            course_cards = 0
            if courses_heading.is_visible():
                print("Highlighting Courses Subheading...")
                highlight_element(self.page, courses_heading, duration=1500)
                course_cards = self.page.locator(DashboardLocators.INSTITUTE_COURSE_CARD).count()
                print(f"Found {course_cards} institute course cards")
                
                # Highlight first 3 course cards
                if course_cards > 0:
                    for i in range(min(course_cards, 3)):
                        try:
                            print(f"Highlighting course card {i+1}...")
                            card = self.page.locator(DashboardLocators.INSTITUTE_COURSE_CARD).nth(i)
                            highlight_element(self.page, card, duration=1500)
                        except Exception as e:
                            print(f"Could not highlight course card {i+1}: {e}")
            
            attach_screenshot(self.page, f"Institute Section - {program_cards} programs, {course_cards} courses")
        except Exception as e:
            print(f"Institute Courses section not found: {e}")
            attach_screenshot(self.page, "Institute Courses - Section not found")

    def validate_wadhwani_courses_and_programs(self):
        """Validate Wadhwani courses and programs section on dashboard"""
        try:
            # Locate and scroll to Wadhwani courses section
            wadhwani_locator = self.page.locator(DashboardLocators.WADHWANI_COURSES_SECTION)
            wadhwani_locator.scroll_into_view_if_needed()
            
            # Validate section heading
            wadhwani_locator.wait_for(state="visible", timeout=10000)
            section_visible = wadhwani_locator.is_visible()
            assert section_visible, "Wadhwani Courses section not visible"
            print("Highlighting Wadhwani Courses Section Heading...")
            highlight_element(self.page, wadhwani_locator, duration=2000)
            
            # Validate Programs subheading and program cards
            programs_heading = self.page.locator(DashboardLocators.WADHWANI_PROGRAMS_SUBHEADING).first
            program_cards = 0
            if programs_heading.is_visible():
                print("Highlighting Programs Subheading...")
                highlight_element(self.page, programs_heading, duration=1500)
                program_cards = self.page.locator(DashboardLocators.WADHWANI_PROGRAM_CARD).count()
                print(f"Found {program_cards} Wadhwani program cards")
                
                # Highlight first 3 program cards
                if program_cards > 0:
                    for i in range(min(program_cards, 3)):
                        try:
                            print(f"Highlighting program card {i+1}...")
                            card = self.page.locator(DashboardLocators.WADHWANI_PROGRAM_CARD).nth(i)
                            highlight_element(self.page, card, duration=1500)
                        except Exception as e:
                            print(f"Could not highlight program card {i+1}: {e}")
            
            # Validate Courses subheading and course cards
            courses_heading = self.page.locator(DashboardLocators.WADHWANI_COURSES_SUBHEADING).first
            course_cards = 0
            if courses_heading.is_visible():
                print("Highlighting Courses Subheading...")
                highlight_element(self.page, courses_heading, duration=1500)
                course_cards = self.page.locator(DashboardLocators.WADHWANI_COURSE_CARD).count()
                print(f"Found {course_cards} Wadhwani course cards")
                
                # Highlight first 3 course cards
                if course_cards > 0:
                    for i in range(min(course_cards, 3)):
                        try:
                            print(f"Highlighting course card {i+1}...")
                            card = self.page.locator(DashboardLocators.WADHWANI_COURSE_CARD).nth(i)
                            highlight_element(self.page, card, duration=1500)
                        except Exception as e:
                            print(f"Could not highlight course card {i+1}: {e}")
            
            attach_screenshot(self.page, f"Wadhwani Section - {program_cards} programs, {course_cards} courses")
        except Exception as e:
            print(f"Wadhwani Courses section not found: {e}")
            attach_screenshot(self.page, "Wadhwani Courses - Section not found")

    def validate_enrol_batch_card(self):
        """Validate enrol batch card section on dashboard"""
        try:
            # Locate and scroll to enrol batch section
            enrol_locator = self.page.locator(DashboardLocators.ENROL_BATCH_SECTION)
            enrol_locator.scroll_into_view_if_needed()
            
            enrol_locator.wait_for(state="visible", timeout=10000)
            section_visible = enrol_locator.is_visible()
            assert section_visible, "Enrol Batch section not visible"
            print("Highlighting Enrol Batch Card Container...")
            highlight_element(self.page, enrol_locator, duration=2000)
            
            # Validate batch title
            title_locator = self.page.locator(DashboardLocators.ENROL_BATCH_TITLE)
            if title_locator.is_visible():
                print("Highlighting 'Join a batch' Title...")
                highlight_element(self.page, title_locator, duration=1500)
            
            # Validate description
            description_locator = self.page.locator(DashboardLocators.ENROL_BATCH_DESCRIPTION)
            if description_locator.is_visible():
                print("Highlighting batch description...")
                highlight_element(self.page, description_locator, duration=1500)
            
            # Validate input field
            input_locator = self.page.locator(DashboardLocators.ENROL_BATCH_INPUT)
            if input_locator.is_visible():
                print("Highlighting code input field...")
                highlight_element(self.page, input_locator, duration=1500)
            
            # Check for enrol button
            enrol_buttons = self.page.locator(DashboardLocators.ENROL_BUTTON).count()
            print(f"Found {enrol_buttons} enroll buttons")
            if enrol_buttons > 0:
                print("Highlighting Enroll button...")
                highlight_element(self.page, self.page.locator(DashboardLocators.ENROL_BUTTON).first, duration=1500)
            
            attach_screenshot(self.page, f"Enrol Batch Card - {enrol_buttons} buttons")
        except Exception as e:
            print(f"Enrol Batch section not found: {e}")
            attach_screenshot(self.page, "Enrol Batch - Section not found")

    def validate_footer_section(self):
        """Validate footer section on dashboard"""
        try:
            # Locate and scroll to footer section
            footer_locator = self.page.locator(DashboardLocators.FOOTER_SECTION)
            footer_locator.scroll_into_view_if_needed()
            
            footer_locator.wait_for(state="visible", timeout=10000)
            footer_visible = footer_locator.is_visible()
            assert footer_visible, "Footer section not visible"
            print("Highlighting Footer Container...")
            highlight_element(self.page, footer_locator, duration=2000)
            
            # Validate "For more information" section
            info_locator = self.page.locator(DashboardLocators.FOOTER_INFO)
            if info_locator.is_visible():
                print("Highlighting 'For more information' text...")
                highlight_element(self.page, info_locator, duration=1500)
                
                # Highlight website link
                website_link = self.page.locator(DashboardLocators.FOOTER_WEBSITE_LINK)
                if website_link.is_visible():
                    print("Highlighting website link...")
                    highlight_element(self.page, website_link, duration=1500)
            
            # Validate social media section
            social_locator = self.page.locator(DashboardLocators.FOOTER_SOCIAL_MEDIA)
            if social_locator.is_visible():
                print("Highlighting 'Follow us on social media' text...")
                highlight_element(self.page, social_locator, duration=1500)
                
                # Count and highlight social icons
                social_icons = self.page.locator(DashboardLocators.FOOTER_SOCIAL_ICONS).count()
                print(f"Found {social_icons} social media icons")
            
            # Validate footer legal links
            footer_links = [
                (DashboardLocators.FOOTER_PRIVACY, "Privacy policy"),
                (DashboardLocators.FOOTER_TERMS, "Terms"),
                (DashboardLocators.FOOTER_COOKIE, "Cookie policy")
            ]
            
            found_links = []
            for locator, name in footer_links:
                try:
                    if self.page.locator(locator).count() > 0:
                        found_links.append(name)
                        print(f"Highlighting {name} link...")
                        highlight_element(self.page, self.page.locator(locator).first, duration=1500)
                except Exception as e:
                    print(f"Could not highlight {name}: {e}")
            
            # Validate version and copyright
            version_locator = self.page.locator(DashboardLocators.FOOTER_VERSION)
            if version_locator.is_visible():
                print("Highlighting version text...")
                highlight_element(self.page, version_locator, duration=1500)
            
            copyright_locator = self.page.locator(DashboardLocators.FOOTER_COPYRIGHT)
            if copyright_locator.is_visible():
                print("Highlighting copyright text...")
                highlight_element(self.page, copyright_locator, duration=1500)
            
            print(f"Footer links found: {', '.join(found_links) if found_links else 'None'}")
            attach_screenshot(self.page, f"Footer Section - {len(found_links)} legal links")
        except Exception as e:
            print(f"Footer section not found: {e}")
            attach_screenshot(self.page, "Footer - Section not found")
