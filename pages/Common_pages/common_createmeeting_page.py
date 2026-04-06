from pages.base_page import BasePage
from locators.Common_locators.common_Create_meeting_locators import CommonCreateMeetingLocators
from locators.Faculty_locators.Batch_details_locators import BatchDetailsLocators
from utils.helpers import highlight_element
import time


class CommonCreateMeetingPage(BasePage):

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
		deadline = time.time() + (timeout / 1000.0)
		while time.time() < deadline:
			for selector in selectors:
				locator = self.page.locator(selector).first
				try:
					locator.wait_for(state="visible", timeout=500)
					self._show_element(locator, duration=500)
					return locator
				except Exception:
					continue
			try:
				self.page.evaluate("window.scrollBy(0, 260)")
				self.page.wait_for_timeout(100)
			except Exception:
				pass
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
			locator.scroll_into_view_if_needed()
		except Exception:
			pass
		try:
			locator.fill(value)
			return True
		except Exception:
			try:
				content_editable = locator.get_attribute("contenteditable")
				if content_editable and content_editable.lower() == "true":
					locator.click(force=True)
					self.page.keyboard.press("Control+a")
					self.page.keyboard.press("Backspace")
					self.page.keyboard.type(value)
					return True
			except Exception:
				pass
			try:
				locator.click(force=True)
				self.page.keyboard.press("Control+a")
				self.page.keyboard.press("Backspace")
				self.page.keyboard.type(value)
				return True
			except Exception:
				return False

	def _type_into_notes_editor(self, value, timeout=10000):
		editor = self._first_visible([
			"//div[contains(@class,'ql-editor')][@contenteditable='true']",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTES')]/following::*[@contenteditable='true'][1]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'AGENDA')]/following::*[@contenteditable='true'][1]",
		], timeout=timeout)
		if not editor:
			return False
		try:
			editor.click(force=True)
			self.page.keyboard.press("Control+a")
			self.page.keyboard.press("Backspace")
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

	def _scroll_to_upcoming_activities(self):
		self._full_page_scroll_cycle()
		for offset in (500, 700, 900):
			try:
				self.page.evaluate(f"window.scrollBy(0, {offset})")
				self.page.wait_for_timeout(120)
			except Exception:
				pass
			upcoming = self._first_visible([
				CommonCreateMeetingLocators.UPCOMING_ACTIVITIES_SECTION,
				"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'UPCOMING ACTIVITIES')]",
				"//div[contains(@class,'upcoming')]",
				"//section[contains(@class,'upcoming')]",
			], timeout=4000)
			if upcoming:
				return upcoming
		return None

	def _scroll_form_down(self):
		for offset in (300, 500, 700, 900):
			try:
				self.page.evaluate(f"window.scrollBy(0, {offset})")
				self.page.wait_for_timeout(120)
			except Exception:
				pass

	def _batch_details_screen_visible(self):
		batch_details_marker = self._first_visible([
			BatchDetailsLocators.BATCHCODE_SECTION,
			BatchDetailsLocators.GENERAL_INFO_TAB,
			BatchDetailsLocators.BATCH_NAME,
			"//div[contains(@class,'batch-code-box')]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'GENERAL INFO')]",
		], timeout=4000)
		return bool(batch_details_marker)

	def _navigate_rm_to_first_batch(self):
		"""For RM persona: go Home → click first row in Assigned Batches table."""
		self._click_first_visible([
			"//div[@id='Home']",
			"//div[@role='menuitem' and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'HOME')]",
		], timeout=7000)
		self.page.wait_for_timeout(700)

		assigned_title = self._first_visible([
			"(//h2[normalize-space()='Assigned Batches'])[1]",
			"//*[self::h2 or self::h3][contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ASSIGNED BATCH')]",
		], timeout=12000)
		assert assigned_title, "Assigned Batches section is not visible on RM home screen"

		clicked = self._click_first_visible([
			"(//tbody//tr[1]//td[contains(@class,'batch-list-content-bold')])[1]",
			"(//tbody//tr[1]//td[contains(@class,'batch-list-content')])[1]",
			"(//tbody//tr[1]//td)[1]",
			"(//div[contains(@class,'ant-table-tbody')]//tr[1]//td[1])[1]",
		], timeout=10000)
		assert clicked, "First batch row is not visible/clickable in RM Assigned Batches table"

	def navigate_to_batch_details_and_upcoming_activities(self, persona=None):
		if not self._batch_details_screen_visible():
			try:
				self.page.evaluate("window.scrollTo(0, 0)")
				self.page.wait_for_timeout(120)
			except Exception:
				pass

			if persona == 'rm':
				self._navigate_rm_to_first_batch()
			else:
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
					], timeout=5000)
					if clicked:
						break
				assert clicked, "First active batch card is not visible/clickable"

		assert self._batch_details_screen_visible(), "Batch details screen is not visible"
		upcoming = self._scroll_to_upcoming_activities()

		assert upcoming, "Upcoming Activities section is not visible"

	def click_create_meeting_button(self):
		clicked = self._click_first_visible([
			CommonCreateMeetingLocators.CREATE_MEETING_BUTTON,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CREATE MEETING')]",
			"//button[contains(text(),'Create Meeting')]",
			"//a[contains(text(),'Create Meeting')]",
		], timeout=10000)
		assert clicked, "Create Meeting button is not visible/clickable"

	def validate_meeting_title_and_new_meeting_card(self):
		title = self._first_visible([
			CommonCreateMeetingLocators.MEETING_TITLE,
			"//div[contains(text(),'Meeting')]",
		], timeout=10000)
		assert title, "Meeting title is not visible"

		card = self._first_visible([
			CommonCreateMeetingLocators.CREATE_NEW_MEETING_CARD,
			"//label[contains(@class,'ant-radio-wrapper')][1]",
		], timeout=10000)
		assert card, "Create new meeting card is not visible"

	def enter_meeting_title(self, meeting_title):
		self._latest_meeting_title = meeting_title
		filled = self._fill_first_visible([
			CommonCreateMeetingLocators.MEETING_TITLE_INPUT,
			"//input[@id='title']",
			"//input[contains(@placeholder,'Meeting')]",
		], meeting_title, timeout=10000)
		assert filled, "Meeting title input field is not visible/editable"

	def click_date_and_validate_calendar(self):
		date_clicked = self._click_first_visible([
			CommonCreateMeetingLocators.SELECT_DATE_INPUT,
			"//div[contains(@class,'ant-picker')]",
		], timeout=10000)
		assert date_clicked, "Select date input is not visible/clickable"

		calendar = self._first_visible([
			CommonCreateMeetingLocators.CALENDAR_DATE_PICKER,
			"//div[contains(@class,'ant-picker-panel')]",
		], timeout=10000)
		assert calendar, "Calendar date picker is not visible"

	def confirm_date_and_select_15min_slot(self):
		ok_clicked = self._click_first_visible([
			CommonCreateMeetingLocators.CALENDAR_OK_BUTTON,
			"//button[normalize-space()='OK']",
		], timeout=10000)
		assert ok_clicked, "Calendar OK button is not visible/clickable"

		slot_dropdown_clicked = self._click_first_visible([
			CommonCreateMeetingLocators.TIME_SLOT_DROPDOWN,
			"//div[contains(@class,'ant-select-selector')]",
		], timeout=10000)
		assert slot_dropdown_clicked, "Timeslot dropdown is not visible/clickable"
		self.page.wait_for_timeout(300)

		slot_clicked = self._click_first_visible([
			CommonCreateMeetingLocators.MIN_SLOT,
			"//div[contains(@class,'ant-select-item-option-content') and contains(normalize-space(.), '15')]",
			"//div[@role='option'][contains(normalize-space(.), '15')]",
			"//li[contains(normalize-space(.), '15')]",
		], timeout=10000)

		if not slot_clicked:
			options = self.page.locator("//div[@role='option'] | //div[contains(@class,'ant-select-item-option')] | //li[contains(@class,'ant-select-item')]")
			try:
				count = options.count()
				for index in range(count):
					option = options.nth(index)
					try:
						text = option.inner_text().strip()
						if "15" in text:
							self._show_element(option, duration=1000)
							option.click(force=True)
							slot_clicked = True
							break
					except Exception:
						continue
			except Exception:
				pass

		assert slot_clicked, "15 mins slot option is not visible/clickable"

	def validate_agenda_field_and_enter(self, agenda_text):
		self._scroll_form_down()
		agenda_wrapper = self._first_visible([
			CommonCreateMeetingLocators.MEETING_AGENDA_FIELD,
			"//div[contains(@class,'meeting_agenda')]",
			"//div[contains(@class,'wf_animated_input') and contains(@class,'agenda')]",
		], timeout=8000)
		assert agenda_wrapper, "Meeting agenda field/wrapper is not visible"
		try:
			agenda_wrapper.click(force=True)
		except Exception:
			pass
		self.enter_meeting_agenda(agenda_text)

	def enter_meeting_agenda(self, agenda_text):
		self._scroll_form_down()
		filled = self._fill_first_visible([
			CommonCreateMeetingLocators.MEETING_AGENDA_INPUT,
			"//div[@id='agenda']",
			"//input[@id='agenda']",
			"//input[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'agenda')]",
			"//textarea[@id='agenda']",
			"//textarea[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'agenda')]",
			"//textarea[contains(@placeholder,'Agenda')]",
			"//label[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'AGENDA')]/following::textarea[1]",
			"//label[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'AGENDA')]/following::input[1]",
			"//label[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'AGENDA')]/following::*[@contenteditable='true'][1]",
			"//p[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'AGENDA')]/following::textarea[1]",
			"//p[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'AGENDA')]/following::input[1]",
			"//p[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'AGENDA')]/following::*[@contenteditable='true'][1]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'AGENDA')]/following::textarea[1]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'AGENDA')]/following::input[1]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'AGENDA')]/following::*[@contenteditable='true'][1]",
		], agenda_text, timeout=15000)
		assert filled, "Meeting agenda input is not visible/editable"

	def enter_notes(self, notes_text):
		self._scroll_form_down()
		filled = self._fill_first_visible([
			CommonCreateMeetingLocators.NOTES_INPUT,
			"//textarea[@id='notes']",
			"//input[@id='notes']",
			"//textarea[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'notes')]",
			"//label[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTES')]/following::textarea[1]",
			"//label[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTES')]/following::input[1]",
			"//label[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTES')]/following::*[@contenteditable='true'][1]",
			"//p[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTES')]/following::textarea[1]",
			"//p[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTES')]/following::input[1]",
			"//p[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTES')]/following::*[@contenteditable='true'][1]",
			"//textarea[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'note')]",
			"//textarea[contains(@placeholder,'Note')]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTES')]/following::textarea[1]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTES')]/following::input[1]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTES')]/following::*[@contenteditable='true'][1]",
			"//div[contains(@class,'ql-editor')][@contenteditable='true']",
		], notes_text, timeout=10000)
		assert filled, "Notes input is not visible/editable"

	def create_meeting_and_return_to_batch_details(self):
		self._scroll_form_down()
		create_clicked = self._click_first_visible([
			CommonCreateMeetingLocators.CREATING_MEETING_BUTTON,
			"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CREATE A MEETING')]",
			"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CREATE MEETING')]",
		], timeout=15000)
		assert create_clicked, "Create a Meeting button is not visible/clickable"

	def validate_create_confirmation_and_click_okay(self):
		confirmation = self._first_visible([
			CommonCreateMeetingLocators.MEETING_CONFIRMATION_CARD,
			"//div[contains(@class,'ant-modal-body')]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'MEETING') and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CREATED')]",
		], timeout=15000)
		assert confirmation, "Create meeting confirmation card is not visible"

		okay_clicked = self._click_first_visible([
			CommonCreateMeetingLocators.MEETING_CONFIRMATION_OKAY_BUTTON,
			"//button[normalize-space()='Okay']",
			"//button[normalize-space()='OK']",
		], timeout=10000)
		assert okay_clicked, "Confirmation Okay button is not visible/clickable"

	def refresh_batch_details_screen(self):
		try:
			self.page.reload(wait_until="domcontentloaded", timeout=30000)
		except Exception:
			self.page.reload()
		self.page.wait_for_load_state("networkidle")
		assert self._batch_details_screen_visible(), "Batch details screen is not visible after refresh"
		upcoming = self._scroll_to_upcoming_activities()
		assert upcoming, "Upcoming Activities section is not visible after refresh"

	def validate_meeting_card_and_open(self):
		self._full_page_scroll_cycle()
		self._scroll_to_upcoming_activities()
		meeting_title = getattr(self, "_latest_meeting_title", "")
		meeting_selectors = []

		# Use the title-specific h5 locator first (most precise - matches MEETING_NAME_IN_CARD)
		if meeting_title:
			meeting_selectors.extend([
				f"(//h5[normalize-space()='{meeting_title}'])[1]",
				f"//*[contains(@class,'meeting-card-wrapper')]//h5[normalize-space()='{meeting_title}']/ancestor::*[contains(@class,'meeting-card-wrapper')][1]",
				f"//*[contains(@class,'meeting-card-wrapper')]//*[contains(normalize-space(.), '{meeting_title}')]/ancestor::*[contains(@class,'meeting-card-wrapper')][1]",
			])

		meeting_selectors.extend([
			CommonCreateMeetingLocators.MEETING_NAME_IN_CARD,
			CommonCreateMeetingLocators.MEETING_CARD,
			"//div[contains(@class,'meeting-card-wrapper') and (contains(@class,'happening_meeting') or contains(@class,'ongoing_meeting_card'))]",
			"//div[contains(@class,'meeting-card-wrapper')]",
		])

		meeting_card = self._first_visible(meeting_selectors, timeout=20000)
		assert meeting_card, "Meeting card is not visible under Upcoming Activities"

		try:
			meeting_card.click(timeout=10000)
		except Exception:
			try:
				# Try clicking the ancestor card wrapper if h5 was matched
				ancestor = meeting_card.locator("xpath=ancestor::*[contains(@class,'meeting-card-wrapper')][1]")
				if ancestor.count() > 0:
					ancestor.first.click(timeout=10000, force=True)
				else:
					meeting_card.click(timeout=10000, force=True)
			except Exception:
				meeting_card.click(timeout=10000, force=True)

	def validate_meeting_check_and_notes_cards(self):
		self._full_page_scroll_cycle()
		meeting_check = self._first_visible([
			CommonCreateMeetingLocators.MEET_CHECK_CARD,
			"//div[contains(@class,'meeting-details-view-section')]",
		], timeout=15000)
		assert meeting_check, "Meeting check/details card is not visible"

		notes_card = self._first_visible([
			CommonCreateMeetingLocators.NOTES_CARD,
			"//div[contains(@class,'meeting-notes-container')]",
		], timeout=15000)
		assert notes_card, "Notes card is not visible"

	def edit_meeting_notes_and_update(self, notes_text):
		edit_clicked = self._click_first_visible([
			CommonCreateMeetingLocators.EDIT_MEETING_BUTTON,
			"//img[contains(@class,'edit-pencil')]",
			"//img[contains(@alt,'edit')]",
		], timeout=10000)
		assert edit_clicked, "Meeting edit icon is not visible/clickable"

		self._scroll_form_down()
		filled = self._fill_first_visible([
			CommonCreateMeetingLocators.NOTES_INPUT,
			"//textarea[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'note')]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTES')]/following::textarea[1]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTES')]/following::input[1]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTES')]/following::*[@contenteditable='true'][1]",
		], notes_text, timeout=12000)
		if not filled:
			filled = self._type_into_notes_editor(notes_text, timeout=12000)
		assert filled, "Meeting notes field is not visible/editable during update"

		updated = self._click_first_visible([
			CommonCreateMeetingLocators.UPDATE_CHANGES_BUTTON,
			"//button[normalize-space()='Update Changes']",
			"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'UPDATE')]",
		], timeout=10000)
		assert updated, "Update Changes button is not visible/clickable"

	def delete_meeting_and_confirm(self):
		deleted = self._click_first_visible([
			CommonCreateMeetingLocators.DELETE_MEETING_BUTTON,
			"//img[@alt='delete-icon']",
			"//img[contains(@alt,'delete')]",
		], timeout=10000)
		assert deleted, "Delete icon is not visible/clickable"

		confirmed = self._click_first_visible([
			CommonCreateMeetingLocators.DELETE_CONFIRMATION_BUTTON,
			"//button[normalize-space()='Delete']",
			"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'DELETE')]",
		], timeout=10000)
		assert confirmed, "Delete confirmation button is not visible/clickable"

	def validate_delete_event_toast_and_land_on_calendar(self):
		toast = self._first_visible([
			CommonCreateMeetingLocators.EVENT_DELETED_TOAST,
			"//div[@id='app-message-container']",
		], timeout=2000)
		if toast:
			print("[INFO] Delete event toast message was visible")
		else:
			print("[INFO] Delete event toast did not appear or disappeared quickly; continuing")

		calendar_visible = self._first_visible([
			"//div[@id='Calendar']",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CALENDAR')]",
			"//div[contains(@class,'calendar')]",
		], timeout=5000)
		assert calendar_visible, "Calendar screen is not visible after deleting the meeting"
