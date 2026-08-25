from pages.base_page import SHORT_TIMEOUT
from pages.student_persona.student_persona_page import StudentPersonaPage
from locators.student_persona_locators import LearningProgressLocators
from utils.helpers import attach_screenshot
from config.env_config import IS_PROD
from utils.logger import log

# The completed course on the prod account does not expose a shareable/download
# certificate, so the Share -> Copy Link -> Download flow is skipped on prod.


class LearningProgressPage(StudentPersonaPage):
    def _consolidate_to_single_tab(self):
        """Keep everything in ONE tab.

        Clicking a course can open it in a new (second) tab, which leaves the
        subsequent clicks/validations running against the wrong (first) tab. So
        if a new tab opened, take its URL, close it, bring the first tab to the
        front and load that URL there — then continue on the first tab.
        """
        try:
            pages = self.page.context.pages
            if len(pages) <= 1:
                return self.page
            new_tab = pages[-1]
            try:
                new_tab.wait_for_load_state("domcontentloaded", timeout=20000)
                url = new_tab.url
            except Exception:
                url = None
            first = pages[0]
            try:
                new_tab.close()
            except Exception as _ignored:
                log.debug("Optional step in _consolidate_to_single_tab() did not apply: %s", _ignored)
            try:
                first.bring_to_front()
            except Exception as _ignored:
                log.debug("Optional step in _consolidate_to_single_tab() did not apply: %s", _ignored)
            if url and url not in ("about:blank",) and url != first.url:
                first.goto(url, wait_until="domcontentloaded", timeout=30000)
                first.wait_for_timeout(1500)
            self.page = first
        except Exception as e:
            log.warning(f"Tab consolidation issue: {e}")
        return self.page

    def dismiss_personalize_journey_popup(self):
        """Best-effort close of the 'Help us personalize your journey' popup.

        The popup appears intermittently and blocks clicks underneath. Simply
        clicking the close (x) control is not enough - the popup only stays
        dismissed after the page is refreshed, so we click the x and then
        reload. This is non-blocking - if the popup isn't present the flow
        continues unchanged.
        """
        popup = None
        try:
            popup = self.page.locator(LearningProgressLocators.PERSONALIZE_JOURNEY_POPUP).first
            popup.wait_for(state="visible", timeout=3000)
        except Exception:
            return  # Popup not shown - nothing to do.

        closed = self.click_first_visible([
            "//div[contains(@class,'ant-modal')]//button[contains(@class,'ant-modal-close') or contains(@aria-label,'close') or contains(@aria-label,'Close')]",
            "//div[contains(@class,'ant-modal')]//span[contains(@class,'close')]",
            "//div[contains(@class,'ant-modal')]//button[normalize-space()='x' or normalize-space()='X' or normalize-space()='×']",
            "//button[normalize-space()='Skip' or normalize-space()='Maybe Later' or normalize-space()='Close' or normalize-space()='No, Thanks']",
            "//*[normalize-space()='Skip' or normalize-space()='Maybe Later' or normalize-space()='Close']",
        ], timeout=3000)
        if not closed:
            # Fall back to dismissing via Escape if no close control matched.
            try:
                self.page.keyboard.press("Escape")
            except Exception as _ignored:
                log.debug("Optional step in dismiss_personalize_journey_popup() did not apply: %s", _ignored)

        # Clicking close alone leaves the popup able to re-appear/keep blocking
        # clicks; refreshing the page is what actually clears it for the run.
        try:
            self.page.reload(wait_until="domcontentloaded", timeout=20000)
            self.page.wait_for_load_state("networkidle", timeout=15000)
        except Exception as _ignored:
            log.debug("Optional step in dismiss_personalize_journey_popup() did not apply: %s", _ignored)
        attach_screenshot(self.page, "Personalize Journey Popup Dismissed")

    def click_profile_icon(self):
        """Click on profile icon"""
        self.wait_for_visible(LearningProgressLocators.PROFILE_ICON, timeout=10000)
        self.click(LearningProgressLocators.PROFILE_ICON, "profile icon")
        attach_screenshot(self.page, "Profile Icon Clicked")

    def click_learning_progress(self):
        """Click on Learning Progress option"""
        self.click_required([
            LearningProgressLocators.LEARNING_PROGRESS,
            "//p[contains(normalize-space(),'Learning Progress')]",
            "//h1[normalize-space()='Learning Progress']",
            "//*[contains(normalize-space(),'Learning Progress')]",
        ], "Learning Progress menu", timeout=15000)
        attach_screenshot(self.page, "Learning Progress Clicked")

    def validate_learning_progress(self):
        """Validate Learning Progress page is loaded"""
        # Clear the "Help us personalize your journey" popup if it interrupts.
        self.dismiss_personalize_journey_popup()
        heading = self.first_visible([
            LearningProgressLocators.VALIDATE_LEARNING_PROGRESS,
            "//h6[normalize-space()='Learning Progress']",
            "//h1[normalize-space()='Learning Progress']",
        ], timeout=15000)
        assert heading is not None, "Learning Progress page not loaded"
        
        # Validate My Courses section
        my_courses = self.first_visible([
            LearningProgressLocators.MY_COURSES,
            "//*[contains(normalize-space(),'My Courses')]",
        ], timeout=10000)
        assert my_courses is not None, "My Courses section not visible"
        attach_screenshot(self.page, "Learning Progress Page Validated")

    def click_ongoing_courses_and_validate_overview(self):
        """Click on ongoing courses tab and validate overview section"""
        # Navigate back to Learning Progress page (from completed course details)
        self.page.go_back()
        
        # Click on Ongoing Courses tab
        self.click_required([
            LearningProgressLocators.ONGOING_COURSES,
            "//p[contains(normalize-space(),'Ongoing')]",
        ], "Ongoing courses tab", timeout=20000)
        attach_screenshot(self.page, "Ongoing Courses Tab Clicked")

        # Click on first ongoing course
        first_course = self.first_visible([
            LearningProgressLocators.FIRST_ONGOING_COURSE,
            "(//div[contains(@class,'course_card_container')])[1]",
        ], timeout=10000)
        assert first_course is not None, "First ongoing course is not visible"
        first_course.scroll_into_view_if_needed()
        try:
            first_course.click()
        except Exception:
            first_course.click(force=True)

        # The course may open in a new tab — bring it back into the first tab.
        self._consolidate_to_single_tab()

        # Validate course page heading
        self.wait_for_visible(LearningProgressLocators.VALIDATE_LEARNING_PROGRESSFIRST_ONGOING_COURSE_HEADING, timeout=10000)
        assert self.page.locator(LearningProgressLocators.VALIDATE_LEARNING_PROGRESSFIRST_ONGOING_COURSE_HEADING).is_visible(), "Ongoing course heading not visible"
        attach_screenshot(self.page, "First Ongoing Course Opened")
        
        # The course detail page no longer has Overview / Course Content /
        # Performance tabs - it now shows a certificate-progress panel, the
        # lesson accordions and the assessment score.
        self.validate_visible(LearningProgressLocators.CERTIFICATE_PROGRESS,
                              "Certificate Progress panel", timeout=15000)
        self.validate_visible(LearningProgressLocators.EARNED_MICRO_CERTIFICATES,
                              "Earned Micro Certificates panel")
        self.validate_visible(LearningProgressLocators.LESSON_ACCORDION, "lesson accordion")
        attach_screenshot(self.page, "Completed course detail sections validated")

        self.validate_visible(LearningProgressLocators.ASSESSMENT_SCORE_LABEL,
                              "Assessment Score label")
        score = self.get_text(LearningProgressLocators.ASSESSMENT_SCORE_VALUE)
        assert "%" in score, f"Assessment score '{score}' is not shown as a percentage"
        log.info("Completed course assessment score is %s", score)
        attach_screenshot(self.page, "Completed course score validated")

    def click_share_certificate_and_validate_download(self):
        """Click on share certificate button and validate download certificate option"""
        # Click on Share Certificate button
        share_timeout = 5000 if IS_PROD else 10000
        clicked_share = self.click_first_visible([
            LearningProgressLocators.CERTIFICATE_SHARE_BUTTON,
            "//span[normalize-space()='Share']",
            "//button[.//span[normalize-space()='Share'] or normalize-space()='Share']",
        ], "certificate share button", timeout=share_timeout)
        if not clicked_share and IS_PROD:
            # Prod completed courses have no shareable certificate — skip the
            # Share/Copy-Link/Download validation instead of hard-failing.
            log.warning("[prod] Share certificate button not present - skipping certificate flow")
            attach_screenshot(self.page, "Share Certificate Skipped (prod)")
            return
        assert clicked_share, "Share certificate button not visible"
        attach_screenshot(self.page, "Share Certificate Button Clicked")
        
        # Validate Copy Link option
        self.click_required([
            LearningProgressLocators.CERTIFICATE_COPY_LINK,
            "//*[normalize-space()='Copy Link' or normalize-space()='Copy link']",
        ], "Copy Link option not visible", timeout=10000)
        
        # Validate certificate link copied message
        copied_toast = self.first_visible([
            LearningProgressLocators.VALIDATE_CERTIFICATE_LINK_COPIED,
            "//*[contains(normalize-space(),'Certificate link copied') or contains(normalize-space(),'Link copied')]",
        ], timeout=10000)
        assert copied_toast is not None, "Certificate link copied message not visible"
        attach_screenshot(self.page, "Certificate Link Copied")

        
        # Validate Download Certificate option
        download_option = self.first_visible([
            LearningProgressLocators.VALIDATE_CERTIFICATE_DOWNLOAD_BUTTON,
            "//*[normalize-space()='Download']",
            "//button[.//span[normalize-space()='Download'] or normalize-space()='Download']",
        ], timeout=10000)
        assert download_option is not None, "Download certificate option not visible"
        attach_screenshot(self.page, "Download Certificate Option Validated")

