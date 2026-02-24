from playwright.sync_api import Page
from locators.student_locators import Learning_Progress_Locators
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
        
        # Validate Final Score
        self.page.locator(Learning_Progress_Locators.VALIDATE_FINAL_SCORE).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.VALIDATE_FINAL_SCORE).is_visible(), "Final Score not visible"
        attach_screenshot(self.page, "Final Score Validated")

    def navigate_to_learning_progress_and_click_completed_courses(self):
        """Navigate back to Learning Progress page and click on Completed Courses tab"""
        # Navigate back to Learning Progress
        self.page.go_back()
        
        # Click on Completed Courses tab
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
