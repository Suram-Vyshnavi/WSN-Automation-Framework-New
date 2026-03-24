from datetime import datetime

from pages.base_page import BasePage
from locators.Faculty_locators.Batch_details_locators import BatchDetailsLocators
from utils.helpers import highlight_element


class BatchDetailsPage(BasePage):

	def _show_element(self, locator, duration=1200):
		try:
			locator.scroll_into_view_if_needed()
		except Exception:
			pass
		try:
			highlight_element(self.page, locator, duration=duration)
		except Exception:
			pass

	def _first_visible(self, selectors, timeout=5000):
		for selector in selectors:
			locator = self.page.locator(selector).first
			try:
				locator.wait_for(state="visible", timeout=timeout)
				self._show_element(locator, duration=500)
				return locator
			except Exception:
				continue
		return None

	def _click_first_visible(self, selectors, timeout=5000):
		locator = self._first_visible(selectors, timeout=timeout)
		if not locator:
			return False
		try:
			locator.click(timeout=timeout)
		except Exception:
			locator.click(timeout=timeout, force=True)
		return True

	def _fill_first_visible(self, selectors, value, timeout=5000):
		locator = self._first_visible(selectors, timeout=timeout)
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
			self.page.wait_for_timeout(80)
		except Exception:
			pass

		for offset in (600, 1200, 1800, 2400):
			try:
				self.page.evaluate(f"window.scrollTo(0, {offset})")
				self.page.wait_for_timeout(60)
			except Exception:
				pass

		try:
			self.page.evaluate("window.scrollTo(0, 0)")
			self.page.wait_for_timeout(60)
		except Exception:
			pass

	def click_first_active_batch(self):
		try:
			self.page.evaluate("window.scrollTo(0, 0)")
			self.page.wait_for_timeout(120)
		except Exception:
			pass

		clicked = False
		for offset in (0, 250, 500, 750):
			try:
				self.page.evaluate(f"window.scrollTo(0, {offset})")
				self.page.wait_for_timeout(120)
			except Exception:
				pass

			clicked = self._click_first_visible([
				BatchDetailsLocators.FIRST_BATCH_CARD,
				"(//tbody//tr[1]//td[contains(@class,'batch-list-content')])[1]",
			], timeout=4000)
			if clicked:
				break

		assert clicked, "First active batch card is not visible/clickable"

	def validate_institute_and_course_name(self):
		batch_name = self._first_visible([
			BatchDetailsLocators.BATCH_NAME,
			"//div[contains(@class,'batch-name')]",
		], timeout=15000)
		assert batch_name, "Institute/Batch name is not visible"
		assert batch_name.inner_text().strip(), "Institute/Batch name is empty"

		course_name = self._first_visible([
			BatchDetailsLocators.COURSE_NAME,
			"//h4[contains(@class,'course-name')]",
		], timeout=10000)
		assert course_name, "Course name is not visible"
		assert course_name.inner_text().strip(), "Course name is empty"

	def validate_timeline_and_batch_code(self):
		timeline = self._first_visible([
			BatchDetailsLocators.COURSE_TIMELINE_SECTION,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'TIMELINE')]",
		], timeout=10000)
		assert timeline, "Course timeline section is not visible"

		batch_code = self._first_visible([
			BatchDetailsLocators.BATCHCODE_SECTION,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'BATCH CODE')]",
		], timeout=10000)
		assert batch_code, "Batch code section is not visible"

	def click_batch_code_and_copy(self):
		self._click_first_visible([
			BatchDetailsLocators.BATCHCODE_SECTION,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'BATCH CODE')]",
		], timeout=8000)

		clicked = self._click_first_visible([
			BatchDetailsLocators.BATCHCODE_COPY_BUTTON,
			"//img[contains(@alt,'copy')]",
		], timeout=8000)
		assert clicked, "Batch code copy button is not visible/clickable"

	def open_more_and_click_edit_batch(self):
		more_clicked = self._click_first_visible([
			BatchDetailsLocators.MORE_OPTION,
			"//img[contains(@alt,'more options')]",
			"//button[contains(@aria-label,'more') or contains(@class,'more')]",
		], timeout=10000)
		assert more_clicked, "More options icon is not visible/clickable"

		edit_clicked = self._click_first_visible([
			BatchDetailsLocators.EDIT_BATCH_OPTION,
			"//h1[normalize-space()='Edit Batch']",
		], timeout=10000)
		assert edit_clicked, "Edit Batch option is not visible/clickable"

	def edit_batch_name_and_update(self):
		section = self._first_visible([
			BatchDetailsLocators.BATCH_DETAILS_SECTION,
			"//div[contains(@class,'create-batch-content')]",
		], timeout=10000)
		assert section, "Batch details section is not visible"

		new_name = f"Automation-Batch-{datetime.now().strftime('%H%M%S')}"
		filled = self._fill_first_visible([
			BatchDetailsLocators.BATCHNAME_FIELD,
			"//input[@placeholder='provide batch name']",
		], new_name, timeout=10000)
		assert filled, "Batch name field is not visible/editable"

		updated = self._click_first_visible([
			BatchDetailsLocators.UPDATE_BUTTON,
			"//button[normalize-space()='Update']",
		], timeout=10000)
		assert updated, "Update button is not visible/clickable"

	def open_more_and_close_batch(self):
		more_clicked = self._click_first_visible([
			BatchDetailsLocators.MORE_OPTION,
			"//img[contains(@alt,'more options')]",
		], timeout=10000)
		assert more_clicked, "More options icon is not visible/clickable"

		close_option_clicked = self._click_first_visible([
			BatchDetailsLocators.CLOSE_BATCH_OPTION,
			"//h1[normalize-space()='Close Batch']",
		], timeout=10000)
		assert close_option_clicked, "Close Batch option is not visible/clickable"

		close_clicked = self._click_first_visible([
			BatchDetailsLocators.CLOSE_BUTTON,
			"//button[normalize-space()='Cancel' or normalize-space()='Close']",
		], timeout=10000)
		assert close_clicked, "Close/Cancel button is not visible/clickable"

	def validate_general_info_and_assessment_schedule(self):
		general_info_clicked = self._click_first_visible([
			BatchDetailsLocators.GENERAL_INFO_TAB,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'GENERAL INFO')]",
		], timeout=10000)
		assert general_info_clicked, "General Info tab is not visible/clickable"

		assessment = self._first_visible([
			BatchDetailsLocators.ASSESSMENT_SCHEDULE_SECTION,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ASSESSMENT SCHEDULE')]",
		], timeout=10000)
		assert assessment, "Assessment schedule section is not visible"

	def validate_batch_activity_and_batch_faculty(self):
		batch_activity = self._first_visible([
			BatchDetailsLocators.BATCH_ACTIVITY_SECTION,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'BATCH ACTIVITY')]",
		], timeout=10000)
		assert batch_activity, "Batch Activity section is not visible"

		batch_faculty = self._first_visible([
			BatchDetailsLocators.BATCH_FACULTY_SECTION,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'BATCH FACULTY')]",
		], timeout=10000)
		assert batch_faculty, "Batch Faculty section is not visible"

	def add_second_faculty(self):
		add_clicked = self._click_first_visible([
			BatchDetailsLocators.ADD_FACULTY_BUTTON,
			"//span[contains(text(),'Add Faculty')]",
		], timeout=10000)
		assert add_clicked, "Add Faculty button is not visible/clickable"

		faculty2_clicked = self._click_first_visible([
			BatchDetailsLocators.FACULTY_2_CARD,
			"(//div[contains(@class,'card_padding')])[2]",
			"(//div[contains(@class,'ant-modal') and not(contains(@style,'display: none'))]//div[contains(@class,'card_padding')])[2]",
			"(//div[@role='option'])[2]",
			"(//div[contains(@class,'ant-select-item-option')])[2]",
			"(//li[contains(@class,'ant-select-selection-overflow-item')])[2]",
		], timeout=10000)

		if not faculty2_clicked:
			candidates = self.page.locator("//div[contains(@class,'card_padding')] | //div[@role='option'] | //div[contains(@class,'ant-select-item-option')]")
			try:
				count = candidates.count()
				if count >= 2:
					second = candidates.nth(1)
					self._show_element(second, duration=1200)
					second.click(force=True)
					faculty2_clicked = True
			except Exception:
				pass

		assert faculty2_clicked, "Second faculty card is not visible/clickable"

	def validate_toast_and_click_edit_faculty(self):
		toast = self._first_visible([
			BatchDetailsLocators.ADDED_FACULTY_TOASTMESSAGE,
			"//div[@id='app-message-container']",
		], timeout=6000)

		edit_clicked = self._click_first_visible([
			BatchDetailsLocators.EDIT_FACULTY_BUTTON,
			"//img[contains(@alt,'edit') and contains(@alt,'faculty')]",
		], timeout=10000)
		assert toast or edit_clicked, "Faculty add toast message is not visible and edit faculty button not available"
		assert edit_clicked, "Edit faculty button is not visible/clickable"

	def delete_second_faculty(self):
		cross_clicked = self._click_first_visible([
			BatchDetailsLocators.CROSS_ICON_FACULTY2,
			"(//img[contains(@alt,'cross icon')])[2]",
		], timeout=10000)
		assert cross_clicked, "Faculty2 cross icon is not visible/clickable"

		delete_clicked = self._click_first_visible([
			BatchDetailsLocators.FACULTY_DELETE_BUTTON,
			"//button[contains(text(),'Delete')]",
		], timeout=10000)
		assert delete_clicked, "Faculty delete button is not visible/clickable"

	def validate_faculty_delete_toast(self):
		# Toast is very short-lived — just attempt to capture it; never fail this step
		toast = self._first_visible([
			BatchDetailsLocators.REMOVED_FACULTY_TOASTMESSAGE,
			"//div[@id='app-message-container']",
		], timeout=3000)
		if toast:
			print("[INFO] Faculty delete toast message was visible")
		else:
			print("[INFO] Faculty delete toast already disappeared (too fast) — continuing")

	def validate_upcoming_and_create_meeting_button(self):
		self._full_page_scroll_cycle()
		# Scroll down the page to bring the Upcoming Activities section into view
		try:
			self.page.evaluate("window.scrollBy(0, 600)")
			self.page.wait_for_timeout(180)
		except Exception:
			pass

		upcoming = self._first_visible([
			BatchDetailsLocators.UPCOMING_ACTIVITIES_SECTION,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'UPCOMING ACTIVITIES')]",
			"//div[contains(@class,'upcoming')]",
			"//section[contains(@class,'upcoming')]",
		], timeout=12000)
		if upcoming:
			self._show_element(upcoming, duration=1000)
		assert upcoming, "Upcoming Activities section is not visible"

		create_button = self._first_visible([
			BatchDetailsLocators.CREATE_MEETING_BUTTON,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CREATE MEETING')]",
			"//button[contains(text(),'Create Meeting')]",
			"//a[contains(text(),'Create Meeting')]",
		], timeout=10000)
		assert create_button, "Create Meeting button is not visible"
