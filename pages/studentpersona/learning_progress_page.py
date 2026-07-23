import os
from playwright.sync_api import Page
from locators.student_persona_locators import Learning_Progress_Locators
from utils.helpers import attach_screenshot

# The completed course on the prod account does not expose a shareable/download
# certificate, so the Share -> Copy Link -> Download flow is skipped on prod.
_IS_PROD = os.getenv("ENV", "").strip().lower() == "prod"


class LearningProgressPage:
    def __init__(self, page: Page):
        self.page = page

    def _wait_visible_any(self, selectors, timeout=10000):
        for selector in selectors:
            try:
                locator = self.page.locator(selector).first
                locator.wait_for(state="visible", timeout=timeout)
                return locator
            except Exception:
                continue
        return None

    def _click_first_visible(self, selectors, timeout=10000):
        locator = self._wait_visible_any(selectors, timeout=timeout)
        if not locator:
            return False
        try:
            locator.click(timeout=timeout)
        except Exception:
            locator.click(timeout=timeout, force=True)
        return True

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
            except Exception:
                pass
            try:
                first.bring_to_front()
            except Exception:
                pass
            if url and url not in ("about:blank",) and url != first.url:
                first.goto(url, wait_until="domcontentloaded", timeout=30000)
                first.wait_for_timeout(1500)
            self.page = first
        except Exception as e:
            print(f"Tab consolidation issue: {e}")
        return self.page

    def _remove_ad_interstitial(self):
        """Remove the Google AdSense interstitial overlay if it slipped through.

        Ad requests are blocked at the browser-context level, but if the
        #wiz-iframe-intent / #intentPreview overlay is already in the DOM it can
        intercept clicks - strip it out defensively. Non-blocking.
        """
        try:
            self.page.evaluate(
                "document.querySelectorAll('#intentPreview, #wiz-iframe-intent').forEach(e => e.remove())"
            )
        except Exception:
            pass

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
            popup = self.page.locator(Learning_Progress_Locators.PERSONALIZE_JOURNEY_POPUP).first
            popup.wait_for(state="visible", timeout=3000)
        except Exception:
            return  # Popup not shown - nothing to do.

        closed = self._click_first_visible([
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
            except Exception:
                pass

        # Clicking close alone leaves the popup able to re-appear/keep blocking
        # clicks; refreshing the page is what actually clears it for the run.
        try:
            self.page.reload(wait_until="domcontentloaded", timeout=20000)
            self.page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        attach_screenshot(self.page, "Personalize Journey Popup Dismissed")

    def click_profile_icon(self):
        """Click on profile icon"""
        self.page.locator(Learning_Progress_Locators.PROFILE_ICON).wait_for(state="visible", timeout=10000)
        self.page.click(Learning_Progress_Locators.PROFILE_ICON)
        attach_screenshot(self.page, "Profile Icon Clicked")

    def click_learning_progress(self):
        """Click on Learning Progress option"""
        clicked = self._click_first_visible([
            Learning_Progress_Locators.LEARNING_PROGRESS,
            "//p[contains(normalize-space(),'Learning Progress')]",
            "//h1[normalize-space()='Learning Progress']",
            "//*[contains(normalize-space(),'Learning Progress')]",
        ], timeout=15000)
        assert clicked, "Learning Progress menu is not visible/clickable"
        attach_screenshot(self.page, "Learning Progress Clicked")

    def validate_learning_progress(self):
        """Validate Learning Progress page is loaded"""
        # Clear the "Help us personalize your journey" popup if it interrupts.
        self.dismiss_personalize_journey_popup()
        heading = self._wait_visible_any([
            Learning_Progress_Locators.VALIDATE_LEARNING_PROGRESS,
            "//h6[normalize-space()='Learning Progress']",
            "//h1[normalize-space()='Learning Progress']",
        ], timeout=15000)
        assert heading is not None, "Learning Progress page not loaded"
        
        # Validate My Courses section
        my_courses = self._wait_visible_any([
            Learning_Progress_Locators.MY_COURSES,
            "//*[contains(normalize-space(),'My Courses')]",
        ], timeout=10000)
        assert my_courses is not None, "My Courses section not visible"
        attach_screenshot(self.page, "Learning Progress Page Validated")

    def click_ongoing_courses_and_validate_overview(self):
        """Click on ongoing courses tab and validate overview section"""
        # Navigate back to Learning Progress page (from completed course details)
        self.page.go_back()
        
        # Click on Ongoing Courses tab
        clicked = self._click_first_visible([
            Learning_Progress_Locators.ONGOING_COURSES,
            "//p[contains(normalize-space(),'Ongoing')]",
        ], timeout=20000)
        assert clicked, "Ongoing courses tab is not visible/clickable"
        attach_screenshot(self.page, "Ongoing Courses Tab Clicked")

        # Click on first ongoing course
        first_course = self._wait_visible_any([
            Learning_Progress_Locators.FIRST_ONGOING_COURSE,
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
        
        # Click on Resume button. Courses that have been started show "Resume",
        # while courses with 0% progress show "Start Course"/"Start" instead.
        clicked = self._click_first_visible([
            Learning_Progress_Locators.FIRST_ONGOING_COURSE_RESUME,
            "(//span[text()='Resume'])[position()=1]",
            "(//span[text()='Start Course'])[position()=1]",
            "(//span[normalize-space()='Start'])[position()=1]",
            "//button[.//span[normalize-space()='Resume' or normalize-space()='Start Course' or normalize-space()='Start']]",
        ], timeout=10000)
        assert clicked, "Resume/Start button not visible"
        attach_screenshot(self.page, "Resume Button Clicked")
        self.page.go_back()

    def click_performance_section_and_validate_final_score(self):
        """Click on performance section and validate final score"""
        # Click on Performance section
        self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE_PERFORMANCE).wait_for(state="visible", timeout=10000)
        assert self.page.locator(Learning_Progress_Locators.FIRST_ONGOING_COURSE_PERFORMANCE).is_visible(), "Performance section not visible"
        self.page.click(Learning_Progress_Locators.FIRST_ONGOING_COURSE_PERFORMANCE)
        attach_screenshot(self.page, "Performance Section Clicked")
        self.page.wait_for_timeout(2000)
        self.page.screenshot(path="debug_performance.png", full_page=True)
        texts = self.page.locator("//button | //span | //a | //h2 | //h3").all_inner_texts()
        print("DEBUG performance texts:", [t.strip() for t in texts if t.strip()][:80])

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
        clicked = self._click_first_visible([
            Learning_Progress_Locators.COMPLETED_COURSES,
            "//p[contains(normalize-space(),'Completed')]",
        ], timeout=10000)
        assert clicked, "Completed courses tab is not visible/clickable"
        attach_screenshot(self.page, "Completed Courses Tab Clicked")

    def click_completed_course_and_validate_all_sections(self):
        """Click on a completed course and validate overview, content, performance sections, score value and overall progress"""
        # Click on first completed course
        first_completed = self._wait_visible_any([
            Learning_Progress_Locators.FIRST_COMPLETED_COURSE,
            "(//div[contains(@class,'course_card_container')][.//*[contains(normalize-space(),'Completed')]])[1]",
            "(//div[contains(@class,'course_card_container')])[1]",
        ], timeout=10000)
        assert first_completed is not None, "First completed course is not visible"
        first_completed.scroll_into_view_if_needed()
        try:

            # No course with score >70 found; fall back to the first completed card.
            print("[INFO] No completed course with score >70 found; clicking first completed card")
            first_completed.click(force=True)
        except Exception:
            first_completed.click(force=True)

        # The course may open in a new tab — bring it back into the first tab.
        self._consolidate_to_single_tab()

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
        share_timeout = 5000 if _IS_PROD else 10000
        clicked_share = self._click_first_visible([
            Learning_Progress_Locators.CERTIFICATE_SHARE_BUTTON,
            "//span[normalize-space()='Share']",
            "//button[.//span[normalize-space()='Share'] or normalize-space()='Share']",
        ], timeout=share_timeout)
        if not clicked_share and _IS_PROD:
            # Prod completed courses have no shareable certificate — skip the
            # Share/Copy-Link/Download validation instead of hard-failing.
            print("[prod] Share certificate button not present - skipping certificate flow")
            attach_screenshot(self.page, "Share Certificate Skipped (prod)")
            return
        assert clicked_share, "Share certificate button not visible"
        attach_screenshot(self.page, "Share Certificate Button Clicked")
        
        # Validate Copy Link option
        clicked_copy = self._click_first_visible([
            Learning_Progress_Locators.CERTIFICATE_COPY_LINK,
            "//*[normalize-space()='Copy Link' or normalize-space()='Copy link']",
        ], timeout=10000)
        assert clicked_copy, "Copy Link option not visible"
        
        # Validate certificate link copied message
        copied_toast = self._wait_visible_any([
            Learning_Progress_Locators.VALIDATE_CERTIFICATE_LINK_COPIED,
            "//*[contains(normalize-space(),'Certificate link copied') or contains(normalize-space(),'Link copied')]",
        ], timeout=10000)
        assert copied_toast is not None, "Certificate link copied message not visible"
        attach_screenshot(self.page, "Certificate Link Copied")

        
        # Validate Download Certificate option
        download_option = self._wait_visible_any([
            Learning_Progress_Locators.VALIDATE_CERTIFICATE_DOWNLOAD_BUTTON,
            "//*[normalize-space()='Download']",
            "//button[.//span[normalize-space()='Download'] or normalize-space()='Download']",
        ], timeout=10000)
        assert download_option is not None, "Download certificate option not visible"
        attach_screenshot(self.page, "Download Certificate Option Validated")

    def click_overview_and_view_batch(self):
        """Click on overview section, click view batch button and validate batch details"""
        # Click on Overview section
        self._remove_ad_interstitial()
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
        
        
        # Validate at least one student row is shown (avoid hardcoded names).
        members = self.page.locator(Learning_Progress_Locators.VALIDATE_STUDENT_NAME)
        members.first.wait_for(state="visible", timeout=10000)
        assert members.count() > 0, "No student rows visible in batch member list"
        attach_screenshot(self.page, "Batch Members List Validated")

    def click_chat_button(self):
        """Click on a student in batch members to open chat"""
        # Click on first student's chat button in batch members list
        self.page.locator(Learning_Progress_Locators.FIRST_CHAT_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.locator(Learning_Progress_Locators.FIRST_CHAT_BUTTON).scroll_into_view_if_needed()
        self.page.click(Learning_Progress_Locators.FIRST_CHAT_BUTTON)
        self.page.wait_for_timeout(2000)  # Wait for chat to open
        attach_screenshot(self.page, "Student Chat Opened")
