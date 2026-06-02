from pages.base_page import BasePage
from locators.student_persona_locators.courses_locators import coursesLocators
from utils.helpers import attach_screenshot, highlight_element


class CoursesPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def _navigate_to_courses(self):
        """Navigate from dashboard to the Courses page."""
        from pages.studentpersona.home_dashboard_page import HomeDashboardPage
        if HomeDashboardPage._shared_dashboard_url:
            self.page.goto(HomeDashboardPage._shared_dashboard_url, wait_until="domcontentloaded", timeout=60000)
        self.page.locator(coursesLocators.COURSES_CARD).wait_for(state="visible", timeout=15000)
        self.page.locator(coursesLocators.COURSES_CARD).click()
        self.page.locator(coursesLocators.VALIDATE_INPROGRESS_TAB).wait_for(state="visible", timeout=15000)

    def validate_inprogress_and_completed_tabs(self):
        self._navigate_to_courses()
        highlight_element(self.page, coursesLocators.VALIDATE_INPROGRESS_TAB)
        assert self.page.locator(coursesLocators.VALIDATE_INPROGRESS_TAB).count() > 0, "In Progress tab not found"
        highlight_element(self.page, coursesLocators.VALIDATE_COMPLETED_TAB)
        assert self.page.locator(coursesLocators.VALIDATE_COMPLETED_TAB).count() > 0, "Completed tab not found"
        print("In Progress and Completed tabs validated")

    def click_inprogress_tab(self):
        self.page.locator(coursesLocators.VALIDATE_INPROGRESS_TAB).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.VALIDATE_INPROGRESS_TAB)
        self.page.locator(coursesLocators.VALIDATE_INPROGRESS_TAB).click()
        print("Clicked In Progress tab")

    def click_completed_tab(self):
        self.page.locator(coursesLocators.VALIDATE_COMPLETED_TAB).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.VALIDATE_COMPLETED_TAB)
        self.page.locator(coursesLocators.VALIDATE_COMPLETED_TAB).click()
        self.page.locator(coursesLocators.VALIDATE_INPROGRESS_TAB).click()  # Click back to In Progress to ensure Completed tab content loads
        print("Clicked Completed tab")

    def validate_enrolled_course_card(self):
        self.page.locator(coursesLocators.ENROLLED_COURSE_CARD).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.ENROLLED_COURSE_CARD)
        assert self.page.locator(coursesLocators.ENROLLED_COURSE_CARD).count() > 0, "Enrolled course card not found"
        print("Enrolled course card validated")

    def click_view_details_button(self):
        self.page.locator(coursesLocators.VIEW_DETAILS_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.VIEW_DETAILS_BUTTON)
        self.page.locator(coursesLocators.VIEW_DETAILS_BUTTON).click()
        print("Clicked View Details button")

    def validate_overview_course_content_performance_tabs(self):
        self.page.locator(coursesLocators.OVERVIEW).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.OVERVIEW)
        assert self.page.locator(coursesLocators.OVERVIEW).count() > 0, "Overview tab not found"
        highlight_element(self.page, coursesLocators.COURSE_CONTENT)
        assert self.page.locator(coursesLocators.COURSE_CONTENT).count() > 0, "Course Content tab not found"
        highlight_element(self.page, coursesLocators.PERFORMANCE)
        assert self.page.locator(coursesLocators.PERFORMANCE).count() > 0, "Performance tab not found"
        print("Overview, Course Content, and Performance tabs validated")

    def click_performance_tab(self):
        self.page.locator(coursesLocators.PERFORMANCE).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.PERFORMANCE)
        self.page.locator(coursesLocators.PERFORMANCE).click()
        print("Clicked Performance tab")

    def validate_final_score_certificate_performance(self):
        self.page.locator(coursesLocators.VALIDATE_FINAL_SCORE).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.VALIDATE_FINAL_SCORE)
        assert self.page.locator(coursesLocators.VALIDATE_FINAL_SCORE).count() > 0, "Final score section not found"
        highlight_element(self.page, coursesLocators.VALIDATE_CERTIFICATE)
        assert self.page.locator(coursesLocators.VALIDATE_CERTIFICATE).count() > 0, "Certificate section not found"
        highlight_element(self.page, coursesLocators.VALIDATE_PERFORMANCE)
        assert self.page.locator(coursesLocators.VALIDATE_PERFORMANCE).count() > 0, "Performance section not found"
        print("Final score, Certificate, and Performance sections validated")

    def click_view_analysis_button(self):
        self.page.locator(coursesLocators.VIEW_ANALYSIS_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.VIEW_ANALYSIS_BUTTON)
        self.page.locator(coursesLocators.VIEW_ANALYSIS_BUTTON).click()
        print("Clicked View Analysis button")

    def click_view_pitch_button(self):
        self.page.locator(coursesLocators.VIEW_PITCH_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.VIEW_PITCH_BUTTON)
        self.page.locator(coursesLocators.VIEW_PITCH_BUTTON).click()
        print("Clicked View Pitch button")

    def click_video_play_button(self):
        self.page.locator(coursesLocators.VIDEO_PLAY_BUTTON).wait_for(state="attached", timeout=15000)
        self.page.locator(coursesLocators.VIDEO_PLAY_BUTTON).click(force=True)
        print("Clicked video play button")

    def click_video_close_button(self):
        self.page.locator(coursesLocators.VIDEO_CLOSE_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.VIDEO_CLOSE_BUTTON)
        self.page.locator(coursesLocators.VIDEO_CLOSE_BUTTON).click()
        print("Clicked video close button")

    def click_share_pitch_button(self):
        self.page.locator(coursesLocators.SHARE_PITCH_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.SHARE_PITCH_BUTTON)
        self.page.locator(coursesLocators.SHARE_PITCH_BUTTON).click()
        print("Clicked Share Pitch button")

    def click_copy_pitch_button(self):
        self.page.locator(coursesLocators.COPY_SHARE_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.COPY_SHARE_BUTTON)
        self.page.locator(coursesLocators.COPY_SHARE_BUTTON).click()
        print("Clicked Copy Pitch button")

    def click_share_pitch_close_button(self):
        self.page.locator(coursesLocators.SHARE_PITCH_CLOSE_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.SHARE_PITCH_CLOSE_BUTTON)
        self.page.locator(coursesLocators.SHARE_PITCH_CLOSE_BUTTON).click()
        print("Clicked Share Pitch Close button")

    def click_back_arrow_button(self):
        self.page.locator(coursesLocators.BACK_ARROW_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.BACK_ARROW_BUTTON)
        self.page.locator(coursesLocators.BACK_ARROW_BUTTON).click()
        self.page.locator(coursesLocators.PERFORMANCE).click()
        print("Clicked Back Arrow button")

    def click_create_post_video_button(self):
        self.page.locator(coursesLocators.CREATE_POST_VIDEO_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.CREATE_POST_VIDEO_BUTTON)
        self.page.locator(coursesLocators.CREATE_POST_VIDEO_BUTTON).click()
        print("Clicked Create Post-Video button")

    def click_pitch_trainer_back_arrow_button(self):
        self.page.locator(coursesLocators.PITCH_TRAINER_BACK_ARROW_BUTTON).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.PITCH_TRAINER_BACK_ARROW_BUTTON)
        self.page.locator(coursesLocators.PITCH_TRAINER_BACK_ARROW_BUTTON).click()
        self.page.locator(coursesLocators.HOME).click()
        self.page.locator(coursesLocators.COURSES_CARD).click()
        print("Clicked Pitch Trainer Back Arrow button")

    def validate_courses_recommended_by_institute(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(1000)
        self.page.locator(coursesLocators.COURSES_RECOMMENDED_BY_INSTITUTE).wait_for(state="visible", timeout=20000)
        highlight_element(self.page, coursesLocators.COURSES_RECOMMENDED_BY_INSTITUTE)
        assert self.page.locator(coursesLocators.COURSES_RECOMMENDED_BY_INSTITUTE).count() > 0, "Courses recommended by institute section not found"
        print("Courses recommended by institute validated")

    def validate_recommended_course_card(self):
        self.page.locator(coursesLocators.VALIDATE_RECOMMENDED_COURSE_CARD).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.VALIDATE_RECOMMENDED_COURSE_CARD)
        assert self.page.locator(coursesLocators.VALIDATE_RECOMMENDED_COURSE_CARD).count() > 0, "Recommended course card not found"
        print("Recommended course card validated")

    def validate_courses_offered_by_wadhwani_foundation(self):
        self.page.locator(coursesLocators.COURSES_OFFERED_BY_WADHWANI_FOUNDATION).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.COURSES_OFFERED_BY_WADHWANI_FOUNDATION)
        assert self.page.locator(coursesLocators.COURSES_OFFERED_BY_WADHWANI_FOUNDATION).count() > 0, "Courses offered by Wadhwani Foundation section not found"
        print("Courses offered by Wadhwani Foundation validated")

    def validate_offered_course_card(self):
        self.page.locator(coursesLocators.VALIDATE_OFFERED_COURSE_CARD).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, coursesLocators.VALIDATE_OFFERED_COURSE_CARD)
        assert self.page.locator(coursesLocators.VALIDATE_OFFERED_COURSE_CARD).count() > 0, "Offered course card not found"
        print("Offered course card validated")
