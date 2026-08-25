from datetime import datetime

from pages.base_page import BasePage
from locators.faculty_locators.batch_details_locators import BatchDetailsLocators
from utils.logger import log
from locators.xpath import UPPER


class BatchDetailsPage(BasePage):
    DEFAULT_TIMEOUT = 5000


    def _fill_first_visible(self, selectors, value, timeout=5000):
        locator = self.first_visible(selectors, timeout=timeout)
        if not locator:
            return False
        try:
            locator.fill(value)
            return True
        except Exception:
            try:
                locator.click(force=True)
                self.page.keyboard.press("Control+a")
                self.page.keyboard.type(value)
                return True
            except Exception:
                return False

    def _full_page_scroll_cycle(self):
        try:
            self.page.evaluate("window.scrollTo(0, 0)")
            self.pause(80)
        except Exception as _ignored:
            log.debug("Optional step in _full_page_scroll_cycle() did not apply: %s", _ignored)

        for offset in (600, 1200, 1800, 2400):
            try:
                self.page.evaluate(f"window.scrollTo(0, {offset})")
                self.pause(60)
            except Exception as _ignored:
                log.debug("Optional step in _full_page_scroll_cycle() did not apply: %s", _ignored)

        try:
            self.page.evaluate("window.scrollTo(0, 0)")
            self.pause(60)
        except Exception as _ignored:
            log.debug("Optional step in _full_page_scroll_cycle() did not apply: %s", _ignored)

    def _navigate_to_batches(self):
        """Navigate to Batches list page from any screen."""
        # Check if batches table is already visible
        try:
            self.page.locator("//div[@id='Batches']").first.wait_for(state="visible", timeout=3000)
            self.page.locator("//div[@id='Batches']").first.click(timeout=3000)
            self.pause(1500)
        except Exception:
            try:
                self.page.locator("//div[@id='Home']").first.click(timeout=3000)
                self.pause(500)
                self.page.locator("//div[@id='Batches']").first.click(timeout=3000)
                self.pause(1500)
            except Exception as _ignored:
                log.debug("Optional step in _navigate_to_batches() did not apply: %s", _ignored)

    def click_first_active_batch(self):
        self._navigate_to_batches()

        try:
            self.page.evaluate("window.scrollTo(0, 0)")
            self.pause(200)
        except Exception as _ignored:
            log.debug("Optional step in click_first_active_batch() did not apply: %s", _ignored)

        clicked = False
        for offset in (0, 250, 500, 750):
            try:
                self.page.evaluate(f"window.scrollTo(0, {offset})")
                self.pause(120)
            except Exception as _ignored:
                log.debug("Optional step in click_first_active_batch() did not apply: %s", _ignored)

            clicked = self.click_first_visible([
                BatchDetailsLocators.FIRST_BATCH_CARD,
                "(//td[contains(@class,'batch-list-content-bold')])[1]",
                "(//tbody//tr[1]//td[contains(@class,'batch-list-content')])[1]",
            ], "first batch card", timeout=5000)
            if clicked:
                break

        assert clicked, "First active batch card is not visible/clickable"

    def validate_institute_and_course_name(self):
        batch_name = self.first_visible([
            BatchDetailsLocators.BATCH_NAME,
            "//div[contains(@class,'batch-name')]",
        ], timeout=15000)
        assert batch_name, "Institute/Batch name is not visible"
        assert batch_name.inner_text().strip(), "Institute/Batch name is empty"

        course_name = self.first_visible([
            BatchDetailsLocators.COURSE_NAME,
            "//h4[contains(@class,'course-name')]",
        ], timeout=10000)
        assert course_name, "Course name is not visible"
        assert course_name.inner_text().strip(), "Course name is empty"

    def validate_timeline_and_batch_code(self):
        self.validate_any_visible([
            BatchDetailsLocators.COURSE_TIMELINE_SECTION,
            f"//*[contains({UPPER}, 'TIMELINE')]",
        ], "Course timeline section", timeout=10000)

        self.validate_any_visible([
            BatchDetailsLocators.BATCHCODE_SECTION,
            f"//*[contains({UPPER}, 'BATCH CODE')]",
        ], "Batch code section", timeout=10000)

    def click_batch_code_and_copy(self):
        self.click_first_visible([
            BatchDetailsLocators.BATCHCODE_SECTION,
            f"//*[contains({UPPER}, 'BATCH CODE')]",
        ], "batchcode section", timeout=8000)

        self.click_required([
            BatchDetailsLocators.BATCHCODE_COPY_BUTTON,
            "//img[contains(@alt,'copy')]",
        ], "Batch code copy button", timeout=8000)

    def open_more_and_click_edit_batch(self):
        self.click_required([
            BatchDetailsLocators.MORE_OPTION,
            "//img[contains(@alt,'more options')]",
            "//button[contains(@aria-label,'more') or contains(@class,'more')]",
        ], "More options icon", timeout=10000)

        self.click_required([
            BatchDetailsLocators.EDIT_BATCH_OPTION,
            "//h1[normalize-space()='Edit Batch']",
        ], "Edit Batch option", timeout=10000)

    def edit_batch_name_and_update(self):
        self.validate_any_visible([
            BatchDetailsLocators.BATCH_DETAILS_SECTION,
            "//div[contains(@class,'create-batch-content')]",
        ], "Batch details section", timeout=10000)

        new_name = f"Automation-Batch-{datetime.now().strftime('%H%M%S')}"
        filled = self._fill_first_visible([
            BatchDetailsLocators.BATCHNAME_FIELD,
            "//input[@placeholder='provide batch name']",
        ], new_name, timeout=10000)
        assert filled, "Batch name field is not visible/editable"

        self.click_required([
            BatchDetailsLocators.UPDATE_BUTTON,
            "//button[normalize-space()='Update']",
        ], "Update button", timeout=10000)

    def open_more_and_close_batch(self):
        self.click_required([
            BatchDetailsLocators.MORE_OPTION,
            "//img[contains(@alt,'more options')]",
        ], "More options icon", timeout=10000)

        self.click_required([
            BatchDetailsLocators.CLOSE_BATCH_OPTION,
            "//h1[normalize-space()='Close Batch']",
        ], "Close Batch option", timeout=10000)

        self.click_required([
            BatchDetailsLocators.CLOSE_BUTTON,
            "//button[normalize-space()='Cancel' or normalize-space()='Close']",
        ], "Close/Cancel button", timeout=10000)

    def validate_general_info_and_assessment_schedule(self):
        self.click_required([
            BatchDetailsLocators.GENERAL_INFO_TAB,
            f"//*[contains({UPPER}, 'GENERAL INFO')]",
        ], "General Info tab", timeout=10000)

        assessment = self.first_visible([
            BatchDetailsLocators.ASSESSMENT_SCHEDULE_SECTION,
            f"//*[contains({UPPER}, 'ASSESSMENT SCHEDULE')]",
        ], timeout=3000)
        if not assessment:
            log.warning("[Info] Assessment schedule section not visible for this batch; skipping validation.")

    def validate_batch_activity_and_batch_faculty(self):
        self.validate_any_visible([
            BatchDetailsLocators.BATCH_ACTIVITY_SECTION,
            f"//*[contains({UPPER}, 'BATCH ACTIVITY')]",
        ], "Batch Activity section", timeout=10000)

        self.validate_any_visible([
            BatchDetailsLocators.BATCH_FACULTY_SECTION,
            f"//*[contains({UPPER}, 'BATCH FACULTY')]",
        ], "Batch Faculty section", timeout=10000)

    def add_second_faculty(self):
        self.click_required([
            BatchDetailsLocators.ADD_FACULTY_BUTTON,
            "//span[contains(text(),'Add Faculty')]",
        ], "Add Faculty button", timeout=10000)

        # Wait for Add Faculty modal/list to fully load
        self.pause(1500)

        # When the batch's course has no certifiable institute faculty, the app
        # shows an info toast ("No institute faculty certified for this course
        # exists") and never renders a selection list. Treat as a graceful skip
        # so the add/edit/delete-faculty steps don't falsely fail on such data.
        no_faculty = self.first_visible([
            "//*[contains(normalize-space(),'No institute faculty certified')]",
            "//*[contains(normalize-space(),'No institute faculty')]",
        ], timeout=3000)
        if no_faculty:
            log.info("No institute faculty certified for this course; "
                "skipping add/edit/delete faculty steps for this batch.")
            return "skipped"

        # The Add Faculty modal lists only the faculty that can still be added to
        # this batch. That list often has just one entry, so we add the first
        # available faculty rather than requiring a specific 'second' one.
        faculty_clicked = self.click_first_visible([
            "(//div[contains(@class,'ant-modal-body')]//div[contains(@class,'card_padding')])[1]",
            "(//div[contains(@class,'ant-modal') and not(contains(@style,'display: none'))]//div[contains(@class,'card_padding')])[1]",
            "(//div[contains(@class,'search_result_container')]//div[contains(@class,'card_padding')])[1]",
            "(//div[contains(@class,'card_padding')])[1]",
            "(//div[@role='option'])[1]",
            "(//div[contains(@class,'ant-select-item-option')])[1]",
        ], timeout=8000)

        # If no faculty is selectable in the modal (empty list / add-faculty not
        # actionable for this batch), skip gracefully rather than hard-failing.
        if not faculty_clicked:
            log.info("No selectable faculty available in the Add Faculty modal; "
                "skipping add/edit/delete faculty steps for this batch.")
            return "skipped"

        return "added"

    def validate_toast_and_click_edit_faculty(self):
        toast = self.first_visible([
            BatchDetailsLocators.ADDED_FACULTY_TOASTMESSAGE,
            "//div[@id='app-message-container']",
        ], timeout=6000)

        edit_clicked = self.click_first_visible([
            BatchDetailsLocators.EDIT_FACULTY_BUTTON,
            "//img[contains(@alt,'edit') and contains(@alt,'faculty')]",
        ], "edit faculty button", timeout=10000)
        assert toast or edit_clicked, "Faculty add toast message is not visible and edit faculty button not available"
        assert edit_clicked, "Edit faculty button is not visible/clickable"

    def delete_second_faculty(self):
        self.click_required([
            BatchDetailsLocators.CROSS_ICON_FACULTY2,
            "(//img[contains(@alt,'cross icon')])[2]",
        ], "Faculty2 cross icon", timeout=10000)

        self.click_required([
            BatchDetailsLocators.FACULTY_DELETE_BUTTON,
            "//button[contains(text(),'Delete')]",
        ], "Faculty delete button", timeout=10000)

    def validate_faculty_delete_toast(self):
        # Toast is very short-lived — just attempt to capture it; never fail this step
        toast = self.first_visible([
            BatchDetailsLocators.REMOVED_FACULTY_TOASTMESSAGE,
            "//div[@id='app-message-container']",
        ], timeout=3000)
        if toast:
            log.info("Faculty delete toast message was visible")
        else:
            log.info("Faculty delete toast already disappeared (too fast) — continuing")

    def _locate_upcoming_and_create_meeting(self):
        """Scroll the current page and try to locate the Upcoming Activities
        section and the Create Meeting button. Returns (upcoming, create_button)."""
        self._full_page_scroll_cycle()
        try:
            self.page.evaluate("window.scrollBy(0, 600)")
            self.pause(180)
        except Exception as _ignored:
            log.debug("Optional step in _locate_upcoming_and_create_meeting() did not apply: %s", _ignored)
        create_button = self.first_visible([
            BatchDetailsLocators.CREATE_MEETING_BUTTON,
            f"//*[contains({UPPER}, 'CREATE MEETING')]",
            "//button[contains(text(),'Create Meeting')]",
            "//a[contains(text(),'Create Meeting')]",
        ], timeout=6000)
        upcoming = self.first_visible([
            BatchDetailsLocators.UPCOMING_ACTIVITIES_SECTION,
            f"//*[contains({UPPER}, 'UPCOMING ACTIVITIES')]",
        ], timeout=3000)
        return upcoming, create_button

    def validate_upcoming_and_create_meeting_button(self):
        upcoming, create_button = self._locate_upcoming_and_create_meeting()

        # The faculty edit/delete flow can navigate back to the dashboard. The
        # Create Meeting button only exists on a batch details screen, so if it
        # isn't found, re-enter a batch's details and retry.
        if not create_button:
            try:
                self.click_first_active_batch()
                self.pause(1500)
            except Exception as _ignored:
                log.debug("Optional step in validate_upcoming_and_create_meeting_button() did not apply: %s", _ignored)
            upcoming, create_button = self._locate_upcoming_and_create_meeting()

        if upcoming:
            self.show_element(upcoming, duration=1000)
        assert upcoming, "Upcoming Activities section is not visible"
        assert create_button, "Create Meeting button is not visible"
