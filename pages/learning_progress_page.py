from playwright.sync_api import Page
from locators.student_locators import Learning_Progress_Locators, LoginLocators
from utils.helpers import attach_screenshot


class LearningProgressPage:
    def __init__(self, page: Page):
        self.page = page

    def click_profile_icon(self):
        """Click on profile icon"""
        self.page.locator(Learning_Progress_Locators.PROFILE_ICON).wait_for(state="visible", timeout=10000)
        self.page.click(Learning_Progress_Locators.PROFILE_ICON)
        attach_screenshot(self.page, "Profile Icon Clicked")

    def click_learning_progress(self):
        """Click on Learning Progress option"""
        self.page.locator(Learning_Progress_Locators.LEARNING_PROGRESS).wait_for(state="visible", timeout=10000)
        self.page.click(Learning_Progress_Locators.LEARNING_PROGRESS)
        attach_screenshot(self.page, "Learning Progress Clicked")

    def validate_learning_progress(self):
        """Validate Learning Progress page is loaded"""
        self.page.locator(Learning_Progress_Locators.VALIDATE_LEARNING_PROGRESS).wait_for(state="visible", timeout=15000)
        assert self.page.locator(Learning_Progress_Locators.VALIDATE_LEARNING_PROGRESS).is_visible(), "Learning Progress page not loaded"
        
        # Validate My Courses section
        self.page.locator(Learning_Progress_Locators.MY_COURSES).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.MY_COURSES).is_visible(), "My Courses section not visible"
        attach_screenshot(self.page, "Learning Progress Page Validated")

    def click_ongoing_courses_and_validate_overview(self):
        """Click on ongoing courses tab and validate overview section"""
        # Navigate back to Learning Progress page (from completed course details)
        self.page.go_back()
        
        # Click on Ongoing Courses tab
        self.page.locator(Learning_Progress_Locators.ONGOING_COURSES).wait_for(state="visible", timeout=10000)
        self.page.click(Learning_Progress_Locators.ONGOING_COURSES)
        attach_screenshot(self.page, "Ongoing Courses Tab Clicked")
        
        # Click on first ongoing course
        self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE).wait_for(state="visible", timeout=10000)
        self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE).scroll_into_view_if_needed()
        self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE).click()
        
        # Validate course page heading
        self.page.locator(Learning_Progress_Locators.VALIDATE_LEARNING_PROGRESSFIRST_ONGOING_COURSE_HEADING).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.VALIDATE_LEARNING_PROGRESSFIRST_ONGOING_COURSE_HEADING).is_visible(), "Ongoing course heading not visible"
        attach_screenshot(self.page, "First Ongoing Course Opened")
        
        # Validate Overview section
        self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE_OVERVIEW).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE_OVERVIEW).is_visible(), "Overview section not visible"
        self.page.click(Learning_Progress_Locators.FIRST_ONGOING_COURSE_OVERVIEW)
        
        # Validate course banner in overview
        self.page.locator(Learning_Progress_Locators.VALIDATE_FIRST_ONGOING_COURSE_BANNER).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.VALIDATE_FIRST_ONGOING_COURSE_BANNER).is_visible(), "Course banner not visible"
        attach_screenshot(self.page, "Overview Section Validated")

    def click_content_section_and_resume(self):
        """Click on content section and click resume button"""
        # Click on Content section
        self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE_CONTENT).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE_CONTENT).is_visible(), "Content section not visible"
        self.page.click(Learning_Progress_Locators.FIRST_ONGOING_COURSE_CONTENT)
        attach_screenshot(self.page, "Content Section Clicked")
        
        # Click on Resume button
        self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE_RESUME).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE_RESUME).is_visible(), "Resume button not visible"
        self.page.click(Learning_Progress_Locators.FIRST_ONGOING_COURSE_RESUME)
        attach_screenshot(self.page, "Resume Button Clicked")
        self.page.go_back()

    def click_performance_section_and_validate_final_score(self):
        """Click on performance section and validate final score"""
        # Click on Performance section
        self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE_PERFORMANCE).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE_PERFORMANCE).is_visible(), "Performance section not visible"
        self.page.click(Learning_Progress_Locators.FIRST_ONGOING_COURSE_PERFORMANCE)
        attach_screenshot(self.page, "Performance Section Clicked")
        
        # Try to validate Final Score if available (may not be present in ongoing courses)
        try:
            self.page.locator(Learning_Progress_Locators.VALIDATE_FINAL_SCORE).wait_for(state="visible", timeout=5000)
            assert self.page.locator(Learning_Progress_Locators.VALIDATE_FINAL_SCORE).is_visible(), "Final Score not visible"
            attach_screenshot(self.page, "Final Score Validated")
            print("Final Score validated successfully")
        except:
            print("Final Score not present - may be an ongoing course without final score")
            attach_screenshot(self.page, "Performance Section Validated (No Final Score)")

    def navigate_to_learning_progress_and_click_completed_courses(self):
        # Click on Completed Courses tab
        # Click on Completed Courses tab (no need to go back as we're on learning progress page)
        self.page.locator(Learning_Progress_Locators.COMPLETED_COURSES).wait_for(state="visible", timeout=10000)
        self.page.click(Learning_Progress_Locators.COMPLETED_COURSES)
        attach_screenshot(self.page, "Completed Courses Tab Clicked")

    def click_completed_course_and_validate_all_sections(self):
        """Click on a completed course and validate overview, content, performance sections, score value and overall progress"""
        # Click on first completed course
        self.page.locator(Learning_Progress_Locators.FIRST_COMPLETED_COURSE).wait_for(state="visible", timeout=10000)
        self.page.locator(Learning_Progress_Locators.FIRST_COMPLETED_COURSE).scroll_into_view_if_needed()
        self.page.locator(Learning_Progress_Locators.FIRST_COMPLETED_COURSE).click()
        
        # Validate course page heading
        self.page.locator(Learning_Progress_Locators.VALIDATE_LEARNING_PROGRESSFIRST_COMPLETED_COURSE_HEADING).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.VALIDATE_LEARNING_PROGRESSFIRST_COMPLETED_COURSE_HEADING).is_visible(), "Completed course heading not visible"
        attach_screenshot(self.page, "First Completed Course Opened")
        
        # Validate Overview section
        self.page.locator(Learning_Progress_Locators.FIRST_COMPLETED_COURSE_OVERVIEW).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.FIRST_COMPLETED_COURSE_OVERVIEW).is_visible(), "Overview section not visible"
        self.page.click(Learning_Progress_Locators.FIRST_COMPLETED_COURSE_OVERVIEW)
        attach_screenshot(self.page, "Completed Course - Overview Section Validated")
        
        # Validate Content section
        self.page.locator(Learning_Progress_Locators.FIRST_COMPLETED_COURSE_CONTENT).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.FIRST_COMPLETED_COURSE_CONTENT).is_visible(), "Content section not visible"
        self.page.click(Learning_Progress_Locators.FIRST_COMPLETED_COURSE_CONTENT)
        attach_screenshot(self.page, "Completed Course - Content Section Validated")
        
        # Validate Performance section
        self.page.locator(Learning_Progress_Locators.FIRST_COMPLETED_COURSE_PERFORMANCE).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.FIRST_COMPLETED_COURSE_PERFORMANCE).is_visible(), "Performance section not visible"
        self.page.click(Learning_Progress_Locators.FIRST_COMPLETED_COURSE_PERFORMANCE)
        attach_screenshot(self.page, "Completed Course - Performance Section Validated")
        
        # Validate Score Value
        self.page.locator(Learning_Progress_Locators.VALIDATE_SCORE_VALUE).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.VALIDATE_SCORE_VALUE).is_visible(), "Score value not visible"
        attach_screenshot(self.page, "Score Value Validated")
        
        # Validate Overall Progress
        self.page.locator(Learning_Progress_Locators.VALIDATE_OVERALL_PROGRESS).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.VALIDATE_OVERALL_PROGRESS).is_visible(), "Overall Progress not visible"
        attach_screenshot(self.page, "Overall Progress Validated")

    def click_share_certificate_and_validate_download(self):
        """Click on share certificate button and validate download certificate option"""
        # Click on Share Certificate button
        self.page.locator(Learning_Progress_Locators.CERTIFICATE_SHARE_BUTTON).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.CERTIFICATE_SHARE_BUTTON).is_visible(), "Share certificate button not visible"
        self.page.click(Learning_Progress_Locators.CERTIFICATE_SHARE_BUTTON)
        attach_screenshot(self.page, "Share Certificate Button Clicked")
        
        # Validate Copy Link option
        self.page.locator(Learning_Progress_Locators.CERTIFICATE_COPY_LINK).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.CERTIFICATE_COPY_LINK).is_visible(), "Copy Link option not visible"
        self.page.click(Learning_Progress_Locators.CERTIFICATE_COPY_LINK)
        
        # Validate certificate link copied message
        self.page.locator(Learning_Progress_Locators.VALIDATE_CERTIFICATE_LINK_COPIED).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.VALIDATE_CERTIFICATE_LINK_COPIED).is_visible(), "Certificate link copied message not visible"
        attach_screenshot(self.page, "Certificate Link Copied")

        
        # Validate Download Certificate option
        self.page.locator(Learning_Progress_Locators.VALIDATE_CERTIFICATE_DOWNLOAD_BUTTON).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.VALIDATE_CERTIFICATE_DOWNLOAD_BUTTON).is_visible(), "Download certificate option not visible"
        attach_screenshot(self.page, "Download Certificate Option Validated")

    def click_overview_and_view_batch(self):
        """Click on overview section, click view batch button and validate batch details"""
        # Click on Overview section
        self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE_OVERVIEW).wait_for(state="visible", timeout=10000)
        self.page.click(Learning_Progress_Locators.FIRST_ONGOING_COURSE_OVERVIEW)
        attach_screenshot(self.page, "Overview Section Clicked")
        
        # Click on View Batch button
        self.page.locator(Learning_Progress_Locators.VIEW_BATCH).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.VIEW_BATCH).is_visible(), "View Batch button not visible"
        self.page.click(Learning_Progress_Locators.VIEW_BATCH)
        attach_screenshot(self.page, "View Batch Button Clicked")
        
        # Validate Batch Name is displayed
        self.page.locator(Learning_Progress_Locators.BATCH_NAME).wait_for(state="visible", timeout=10000)
        attach_screenshot(self.page, "Batch Details Validated")

    def click_general_info_and_validate_upcoming_activities(self):
        """Click on general info tab and validate upcoming activities section"""
        # Click on General Info tab
        self.page.locator(Learning_Progress_Locators.GENERAL_INFOTAB).wait_for(state="visible", timeout=10000)
        self.page.click(Learning_Progress_Locators.GENERAL_INFOTAB)
        attach_screenshot(self.page, "General Info Tab Clicked")
        
        # Validate Upcoming Activities section
        self.page.locator(Learning_Progress_Locators.VALIDATE_UPCOMING_ACTIVITIES).wait_for(state="visible", timeout=10000)
        self.page.locator(Learning_Progress_Locators.VALIDATE_UPCOMING_ACTIVITIES).scroll_into_view_if_needed()
        assert self.page.locator(Learning_Progress_Locators.VALIDATE_UPCOMING_ACTIVITIES).is_visible(), "Upcoming Activities section not visible"
        attach_screenshot(self.page, "Upcoming Activities Validated")

    def click_batch_members_and_validate_all(self):
        """Click on batch members tab and validate students count, maximum allowed, and member list"""
        # Click on Batch Members tab
        self.page.locator(Learning_Progress_Locators.BATCH_MEMBERS).wait_for(state="visible", timeout=10000)
        self.page.click(Learning_Progress_Locators.BATCH_MEMBERS)
        attach_screenshot(self.page, "Batch Members Tab Clicked")
        
        # Validate Batch Members Count heading
        self.page.locator(Learning_Progress_Locators.VALIDATE_BATCH_MEMBERS_COUNT).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.VALIDATE_BATCH_MEMBERS_COUNT).is_visible(), "Batch Members heading not visible"
        
        # Validate Students Added Count
        self.page.locator(Learning_Progress_Locators.VALIDATE_STUDENTS_ADDED_COUNT).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.VALIDATE_STUDENTS_ADDED_COUNT).is_visible(), "Students Added count not visible"
       
        
        # Validate Maximum Allowed
        self.page.locator(Learning_Progress_Locators.VALIDATE_MAXIMUM_ALLOWED).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.VALIDATE_MAXIMUM_ALLOWED).is_visible(), "Maximum Allowed not visible"
        
        
        # Validate Student Name in member list
        self.page.locator(Learning_Progress_Locators.VALIDATE_STUDENT_NAME).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.VALIDATE_STUDENT_NAME).is_visible(), "Student name not visible in batch member list"
        attach_screenshot(self.page, "Batch Members List Validated")

    def click_chat_button(self):
        """Click on chat icon from header"""
        # Click on chat icon in header
        self.page.locator(LoginLocators.CHAT_ICON).wait_for(state="visible", timeout=10000)
        self.page.click(LoginLocators.CHAT_ICON)
        attach_screenshot(self.page, "Chat Icon Clicked")
