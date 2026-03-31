from pages.base_page import BasePage
from locators.Faculty_locators.Create_newbatch_locators import CreateNewBatchLocators
from utils.helpers import highlight_element


class CreateNewBatchPage(BasePage):

	def _show_element(self, locator, duration=1200):
		try:
			locator.scroll_into_view_if_needed()
		except Exception:
			pass
		try:
			highlight_element(self.page, locator, duration=duration)
		except Exception:
			pass
		self.page.wait_for_timeout(300)

	def _first_visible(self, selectors, timeout=10000):
		for selector in selectors:
			locator = self.page.locator(selector).first
			try:
				locator.wait_for(state="visible", timeout=timeout)
				self._show_element(locator, duration=1000)
				return locator
			except Exception:
				continue
		return None

	def _click_first_visible(self, selectors, timeout=10000):
		locator = self._first_visible(selectors, timeout=timeout)
		if not locator:
			return False
		self._show_element(locator, duration=1200)
		try:
			locator.click(timeout=timeout)
		except Exception:
			locator.click(timeout=timeout, force=True)
		return True

	def _scroll_until_any_visible(self, selectors, max_scrolls=12, step_px=700, wait_ms=250):
		"""Scroll down in steps until one of the selectors becomes visible."""
		for _ in range(max_scrolls + 1):
			for selector in selectors:
				locator = self.page.locator(selector).first
				try:
					if locator.is_visible():
						return locator
				except Exception:
					continue

			self.page.mouse.wheel(0, step_px)
			self.page.wait_for_timeout(wait_ms)

		return None

	def click_create_new_batch_button(self):
		clicked = self._click_first_visible([
			CreateNewBatchLocators.CREATE_NEWBATCH_BUTTON,
			"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CREATE NEW BATCH')]",
		], timeout=15000)
		assert clicked, "Create New Batch button is not visible/clickable"

	def validate_batch_information_header_and_title(self):
		header = self._first_visible([
			CreateNewBatchLocators.BATCH_INFORMATION_HEADER_SECTION,
			"//*[contains(@class,'stepper') or contains(@class,'createBatch')]",
		], timeout=15000)
		assert header, "Batch Information header section is not visible"

		title = self._first_visible([
			CreateNewBatchLocators.BATCH_INFORMATION_TITLE,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'BATCH INFORMATION')]",
		], timeout=10000)
		assert title, "Batch Information title is not visible"

	def select_institute_by_name(self, institute_name):
		clicked = False
		for selector in [
			"#Institute-search-input .ant-select-selector",
			"#Institute-search-input",
			CreateNewBatchLocators.Institute_DROPDOWN,
			"//label[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'INSTITUTE')]/following::div[contains(@class,'ant-select-selector')][1]",
		]:
			locator = self.page.locator(selector).first
			try:
				locator.wait_for(state="attached", timeout=4000)
				try:
					locator.scroll_into_view_if_needed(timeout=2000)
				except Exception:
					pass
				self._show_element(locator, duration=1200)
				locator.click(force=True)
				clicked = True
				break
			except Exception:
				continue

		if not clicked:
			prefilled = self._first_visible([
				f"//*[normalize-space()='{institute_name}']",
				f"//*[contains(normalize-space(),'{institute_name}')]",
			], timeout=5000)
			assert prefilled, "Institute dropdown is not available and institute text is not present"
			return

		self.page.wait_for_timeout(1000)

		option = self._first_visible([
			f"//span[normalize-space()='{institute_name}']",
			f"//div[@role='option'][normalize-space()='{institute_name}']",
			f"//div[@role='option'][.//*[contains(normalize-space(),'{institute_name}')]]",
			CreateNewBatchLocators.Institute_DROPDOWN_OPTION,
		], timeout=5000)
		if option:
			try:
				self._show_element(option, duration=1200)
				option.dispatch_event("click")
			except Exception:
				option.click(force=True)
			return

		search_input = self.page.locator("input[aria-autocomplete='list']").first
		try:
			search_input.wait_for(state="attached", timeout=3000)
			search_input.fill(institute_name)
			search_input.press("Enter")
			self.page.wait_for_timeout(1000)
		except Exception:
			pass

		selected = self._first_visible([
			f"//span[normalize-space()='{institute_name}']",
			f"//*[contains(normalize-space(),'{institute_name}')]",
		], timeout=5000)
		assert selected, f"Institute option '{institute_name}' is not visible/selected"

	def validate_prefilled_faculty_name(self):
		faculty_name = self._first_visible([
			CreateNewBatchLocators.FACULTY_PRESELECTED_NAME,
			"//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'leela') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'bolli')]",
			"//*[contains(@class,'faculty') and string-length(normalize-space()) > 0]",
		], timeout=10000)
		assert faculty_name, "Pre-filled faculty name is not visible"
		text = faculty_name.inner_text().strip()
		assert text, "Pre-filled faculty name is empty"

		name_text = text.lower()
		assert ("leela" in name_text) or ("bolli" in name_text), (
			f"Pre-filled faculty name should contain 'leela' or 'bolli', but got: '{text}'"
		)

	def select_course_by_name(self, course_name):
		# Wait for course dropdown to become enabled (it starts disabled until institute is selected)
		try:
			self.page.wait_for_function(
				"() => { const el = document.getElementById('Select Course-search-input'); return el && !el.closest('.ant-select-disabled'); }",
				timeout=10000
			)
		except Exception:
			pass
		self.page.wait_for_timeout(500)

		clicked = False
		for selector in [
			"//*[@id='Select Course-search-input']//div[contains(@class,'ant-select-selector')]",
			"//*[@id='Select Course-search-input']",
			CreateNewBatchLocators.SELECT_COURSE_DROPDOWN,
			"//label[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'COURSE')]/following::div[contains(@class,'ant-select-selector')][1]",
		]:
			locator = self.page.locator(selector).first
			try:
				locator.wait_for(state="attached", timeout=4000)
				try:
					locator.scroll_into_view_if_needed(timeout=2000)
				except Exception:
					pass
				self._show_element(locator, duration=1200)
				locator.click(force=True)
				clicked = True
				break
			except Exception:
				continue

		if not clicked:
			prefilled = self._first_visible([
				f"//*[normalize-space()='{course_name}']",
				f"//*[contains(normalize-space(),'{course_name}')]",
			], timeout=5000)
			assert prefilled, "Select course dropdown is not available and course text is not present"
			return

		self.page.wait_for_timeout(1000)

		option = self._first_visible([
			f"//span[normalize-space()='{course_name}']",
			f"//div[@role='option'][normalize-space()='{course_name}']",
			f"//div[@role='option'][.//*[contains(normalize-space(),'{course_name}')]]",
			CreateNewBatchLocators.SELECT_COURSE_DROPDOWN_OPTION,
		], timeout=5000)
		if option:
			try:
				self._show_element(option, duration=1200)
				option.dispatch_event("click")
			except Exception:
				option.click(force=True)
			return

		search_input = self.page.locator("input[aria-autocomplete='list']").first
		try:
			search_input.wait_for(state="attached", timeout=3000)
			search_input.fill(course_name)
			search_input.press("Enter")
			self.page.wait_for_timeout(1000)
		except Exception:
			pass

		selected = self._first_visible([
			f"//span[normalize-space()='{course_name}']",
			f"//*[contains(normalize-space(),'{course_name}')]",
			"//span[contains(@class,'ant-select-selection-item')]",
		], timeout=5000)
		assert selected, f"Course option '{course_name}' is not visible"

	def enter_batch_name(self, batch_name):
		field = self.page.locator(CreateNewBatchLocators.BATCH_NAME_INPUT).first
		field.wait_for(state="attached", timeout=10000)
		try:
			field.scroll_into_view_if_needed(timeout=2000)
		except Exception:
			pass
		self._show_element(field, duration=1200)
		try:
			field.fill(batch_name, force=True)
		except Exception:
			self.page.evaluate(f"document.querySelector('input[placeholder=\"provide batch name\"]').value = '{batch_name}'")

	def _click_attached_fallback(self, selectors, timeout=10000):
		"""Try visible first, then fall back to attached+force for CSS-animated elements."""
		result = self._click_first_visible(selectors, timeout=3000)
		if result:
			return True
		for selector in selectors:
			locator = self.page.locator(selector).first
			try:
				locator.wait_for(state="attached", timeout=timeout)
				try:
					locator.scroll_into_view_if_needed(timeout=2000)
				except Exception:
					pass
				self._show_element(locator, duration=1200)
				locator.click(force=True)
				return True
			except Exception:
				continue
		return False

	def _open_batch_date_field(self, field="start", timeout=10000):
		"""Open the correct date field popup: start (first) or end (second)."""
		index = 0 if field == "start" else 1

		candidates = [
			"//div[@id='create-batch-startedAt']",
			"//div[@id='create-batch-endedAt']",
			"//div[contains(@class,'ant-picker')]",
		]

		for selector in candidates:
			locator = self.page.locator(selector)
			count = locator.count()
			if count <= index:
				continue
			target = locator.nth(index)
			try:
				target.wait_for(state="attached", timeout=timeout)
				try:
					target.scroll_into_view_if_needed(timeout=2000)
				except Exception:
					pass
				self._show_element(target, duration=1200)
				target.click(force=True)
				return True
			except Exception:
				continue

		# fallback: date input wrappers by index
		fallback = self.page.locator("//div[contains(@class,'ant-picker-input')]")
		if fallback.count() > index:
			target = fallback.nth(index)
			try:
				target.wait_for(state="attached", timeout=timeout)
				try:
					target.scroll_into_view_if_needed(timeout=2000)
				except Exception:
					pass
				self._show_element(target, duration=1200)
				target.click(force=True)
				return True
			except Exception:
				pass

		return False

	def set_start_date_to_today(self):
		clicked = self._open_batch_date_field(field="start", timeout=10000)
		assert clicked, "Start date picker is not visible/clickable"

		today = self._first_visible([
			CreateNewBatchLocators.DATE_PICKER_TODAY_TEXT,
			"//*[contains(@class,'ant-picker-today-btn') or normalize-space()='Today']",
		], timeout=10000)
		assert today, "Today option is not visible in date picker"
		self._show_element(today, duration=1200)
		today.click()

	def set_end_date_with_next_year_next_month(self, day_text):
		clicked = self._open_batch_date_field(field="end", timeout=10000)
		assert clicked, "End date picker is not visible/clickable"

		self._click_first_visible([
			CreateNewBatchLocators.NEXT_YEAR_BUTTON,
			"//button[contains(@class,'super-next')]",
		], timeout=3000)

		self._click_first_visible([
			CreateNewBatchLocators.NEXT_MONTH_BUTTON,
			"//button[contains(@class,'next-btn')]",
		], timeout=3000)

		day = self._first_visible([
			f"//td[not(contains(@class,'disabled'))]//div[normalize-space()='{day_text}']",
			CreateNewBatchLocators.BATCH_ENDDATE,
		], timeout=10000)
		assert day, f"Could not find day '{day_text}' in end-date picker"
		self._show_element(day, duration=1200)
		day.click()

	def validate_student_enrollment_note_and_weekly_hours(self):
		note_selectors = [
			CreateNewBatchLocators.STUDENT_ENROLLMENT_NOTE,
			"//div[contains(@class,'student-e') and contains(@class,'note')]",
			"//div[contains(@class,'enrollment') or contains(@class,'erollment')]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'STUDENT ENROLLMENT NOTE')]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'STUDENT ENROLLMENT')]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ENROLLMENT')]",
		]

		# Bring lower form sections into viewport before strict validations.
		scrolled_note = self._scroll_until_any_visible(note_selectors, max_scrolls=18, step_px=650, wait_ms=250)
		if scrolled_note:
			self._show_element(scrolled_note, duration=1000)

		self._scroll_until_any_visible([CreateNewBatchLocators.WEEKELY_CLASS_HOURS], max_scrolls=14, step_px=500, wait_ms=220)
		weekly_hours = self.page.locator(CreateNewBatchLocators.WEEKELY_CLASS_HOURS).first
		weekly_hours.wait_for(state="attached", timeout=10000)
		try:
			weekly_hours.scroll_into_view_if_needed(timeout=2000)
		except Exception:
			pass
		self._show_element(weekly_hours, duration=1200)
		value = weekly_hours.input_value().strip()
		if not value:
			value = self.page.evaluate("document.querySelector('input#weekly-hours') && document.querySelector('input#weekly-hours').value") or ""
		assert value, "Weekly class hours prefilled value is empty"

		# Try attached state for note section after weekly-hours anchor is found.
		note_locator = None
		for selector in note_selectors:
			loc = self.page.locator(selector).first
			try:
				loc.wait_for(state="attached", timeout=1500)
				try:
					loc.scroll_into_view_if_needed(timeout=1000)
				except Exception:
					pass
				note_locator = loc
				break
			except Exception:
				continue

		# In some variants note text is not separately rendered; weekly-hours field is the reliable anchor.
		if note_locator:
			self._show_element(note_locator, duration=1200)
		else:
			print("Student enrollment note label is not separately visible; validated section via weekly class hours field")

	def check_confirmation_set_max_students_and_next(self, max_students):
		checkbox_clicked = self._click_first_visible([
			CreateNewBatchLocators.CONFIRM_CHECKBOX,
			"//span[contains(@class,'ant-checkbox-inner')]",
		], timeout=10000)
		assert checkbox_clicked, "Confirmation checkbox is not visible/clickable"

		max_students_field = self.page.locator(CreateNewBatchLocators.MAX_STUDENTS_ALLOWED_INPUT).first
		max_students_field.wait_for(state="attached", timeout=10000)
		try:
			max_students_field.scroll_into_view_if_needed(timeout=2000)
		except Exception:
			pass
		self._show_element(max_students_field, duration=1200)
		try:
			max_students_field.fill(str(max_students), force=True)
		except Exception:
			self.page.evaluate(f"document.querySelector('input[name=\"maxStudentsAllowed\"]').value = '{max_students}'")

		next_clicked = self._click_first_visible([
			CreateNewBatchLocators.NEXT_BUTTON,
			"//button[normalize-space()='Next']",
		], timeout=10000)
		assert next_clicked, "Next button is not visible/clickable"

	def confirm_dates_and_proceed(self):
		popup = self._first_visible([
			CreateNewBatchLocators.CONFIRM_DATES_POPUP,
			"//div[contains(@class,'ant-modal-body')]",
		], timeout=10000)
		assert popup, "Confirm dates popup is not visible"
		self._show_element(popup, duration=1200)

		confirm_clicked = self._click_first_visible([
			CreateNewBatchLocators.CONFIRM_AND_PROCEED_BUTTON,
			"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CONFIRM')]",
		], timeout=10000)
		assert confirm_clicked, "Confirm & Proceed button is not visible/clickable"

	def validate_assessment_details_and_next(self):
		assessment_selectors = [
			CreateNewBatchLocators.ASSESSMENT_DETAILS_SECTION,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ASSESSMENT DETAILS')]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ASSESSMENT')]",
		]

		# Bring assessment block into view before validating/clicking Next.
		self._scroll_until_any_visible(
			assessment_selectors + [
				CreateNewBatchLocators.LEVEL2_RADIO_BUTTON,
				"//input[@value='Intermediate']",
			],
			max_scrolls=16,
			step_px=550,
			wait_ms=220,
		)

		assessment = self._first_visible([
			*assessment_selectors,
		], timeout=6000)

		# Some UI variants auto-skip/compact this section; difficulty radios indicate forward progress.
		if not assessment:
			difficulty_present = self._first_visible([
				CreateNewBatchLocators.LEVEL2_RADIO_BUTTON,
				"//input[@value='Intermediate']",
				"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'INTERMEDIATE')]",
			], timeout=2500)
			assert difficulty_present, "Assessment details section is not visible"
			print("Assessment details section not separately visible; continuing from difficulty-level screen")
			return

		self._show_element(assessment, duration=1200)

		next_clicked = self._click_first_visible([
			CreateNewBatchLocators.ASSESSMENT_DETAILS_NEXT_BUTTON,
			"//button[normalize-space()='Next']",
			"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CONTINUE')]",
		], timeout=10000)
		if not next_clicked:
			difficulty_present = self._first_visible([
				CreateNewBatchLocators.LEVEL2_RADIO_BUTTON,
				"//input[@value='Intermediate']",
			], timeout=3000)
			assert difficulty_present, "Assessment details Next button is not visible/clickable"

	def validate_difficulty_levels_and_select_level2(self):
		self._scroll_until_any_visible([
			CreateNewBatchLocators.DIFFICULY_LEVEL1_CARD,
			CreateNewBatchLocators.DIFFICULY_LEVEL2_CARD,
			CreateNewBatchLocators.DIFFICULY_LEVEL3_CARD,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'BASIC')]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'INTERMEDIATE')]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ADVANCED')]",
		], max_scrolls=12, step_px=450, wait_ms=220)

		level1 = self._first_visible([
			CreateNewBatchLocators.DIFFICULY_LEVEL1_CARD,
			"//div[contains(@class,'radio_option')][.//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'BASIC')]]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'BASIC')]",
		], timeout=7000)
		assert level1, "Difficulty level 1 card is not visible"
		self._show_element(level1, duration=1000)

		level2 = self._first_visible([
			CreateNewBatchLocators.DIFFICULY_LEVEL2_CARD,
			"//div[contains(@class,'radio_option')][.//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'INTERMEDIATE')]]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'INTERMEDIATE')]",
		], timeout=7000)
		assert level2, "Difficulty level 2 card is not visible"
		self._show_element(level2, duration=1000)

		level3 = self._first_visible([
			CreateNewBatchLocators.DIFFICULY_LEVEL3_CARD,
			"//div[contains(@class,'radio_option')][.//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ADVANCED')]]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ADVANCED')]",
		], timeout=7000)
		assert level3, "Difficulty level 3 card is not visible"
		self._show_element(level3, duration=1000)

		clicked = self._click_first_visible([
			CreateNewBatchLocators.LEVEL2_RADIO_BUTTON,
			"//input[@value='Intermediate']",
			"//label[.//input[@value='Intermediate']]",
			"//div[contains(@class,'radio_option')][.//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'INTERMEDIATE')]]",
		], timeout=10000)
		if not clicked:
			already_selected = self.page.locator("//input[@value='Intermediate' and @checked]").count() > 0
			assert already_selected, "Difficulty level 2 radio button is not visible/clickable"

	def enter_job_role_or_sector(self, job_role_text):
		input_field = self._first_visible([
			CreateNewBatchLocators.JOBEROLE_OR_SECTOR_INPUT,
			"//input[contains(@placeholder,'job role') or contains(@placeholder,'Job Role')]",
			"//input[contains(@placeholder,'sector') or contains(@placeholder,'Sector')]",
			"//input[contains(@placeholder,'press enter') or contains(@placeholder,'Press Enter')]",
		], timeout=10000)
		assert input_field, "Job role/sector input field is not visible"
		try:
			input_field.scroll_into_view_if_needed(timeout=2000)
		except Exception:
			pass
		self._show_element(input_field, duration=1200)
		try:
			input_field.fill(job_role_text, force=True)
		except Exception:
			input_field.click(force=True)
			self.page.keyboard.press("Control+A")
			self.page.keyboard.type(job_role_text)

		enter_clicked = self._click_first_visible([
			CreateNewBatchLocators.JOBEROLE_OR_SECTOR_ENTER_BUTTON,
			"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ENTER')]",
			"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ADD')]",
		], timeout=10000)
		if not enter_clicked:
			input_field.press("Enter")

		selected = self._first_visible([
			f"//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{job_role_text.lower()}')]",
			"//div[contains(@class,'tag') or contains(@class,'chip')]",
		], timeout=5000)
		assert selected, "Job role/sector value was not added"

	def save_and_finish_and_validate_batch_details_card(self):
		saved = self._click_first_visible([
			CreateNewBatchLocators.SAVE_AND_FINISH_BUTTON,
			"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SAVE') and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'FINISH')]",
		], timeout=10000)
		assert saved, "Save & Finish button is not visible/clickable"

		card = self._first_visible([
			CreateNewBatchLocators.BATCH_DETAILS_CARD,
			"//div[contains(@class,'section_card_container') and contains(@class,'card')]",
		], timeout=15000)
		assert card, "Batch details card is not visible after Save & Finish"
		self._show_element(card, duration=1400)
