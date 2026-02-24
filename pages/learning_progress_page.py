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

    def click_ongoing_courses_and_validate_sections(self):
        """Click on ongoing courses tab and validate overview, content and performance sections"""
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
        attach_screenshot(self.page, "Overview Section Validated")
        
        # Validate Content section
        self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE_CONTENT).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE_CONTENT).is_visible(), "Content section not visible"
        self.page.click(Learning_Progress_Locators.FIRST_ONGOING_COURSE_CONTENT)
        attach_screenshot(self.page, "Content Section Validated")
        
        # Validate Performance section
        self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE_PERFORMANCE).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE_PERFORMANCE).is_visible(), "Performance section not visible"
        self.page.click(Learning_Progress_Locators.FIRST_ONGOING_COURSE_PERFORMANCE)
        attach_screenshot(self.page, "Performance Section Validated")

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
