from pages.base_page import BasePage
from locators.Common_locators.common_performance_locators import CommonPerformanceLocators
from locators.Faculty_locators.Home_locators import HomeLocators


class CommonPerformancePage(BasePage):
	def _first_visible(self, selectors, timeout=10000):
		for selector in selectors:
			locator = self.page.locator(selector).first
			try:
				locator.wait_for(state="visible", timeout=timeout)
				return locator
			except Exception:
				continue
		return None

	def _click_first_visible(self, selectors, timeout=10000):
		target = self._first_visible(selectors, timeout=timeout)
		if not target:
			return False
		try:
			target.scroll_into_view_if_needed()
		except Exception:
			pass
		try:
			target.click(timeout=timeout)
		except Exception:
			target.click(timeout=timeout, force=True)
		return True

	def _navigate_to_home(self):
		"""Navigate to home page from any screen."""
		try:
			self.page.locator(HomeLocators.HOME_MENU).first.wait_for(state="visible", timeout=3000)
			self.page.locator(HomeLocators.HOME_MENU).first.click(timeout=3000)
			self.page.wait_for_timeout(800)
		except Exception:
			pass

	def click_performance_menu(self):
		# Navigate to home first to ensure sidebar is in correct state
		self._navigate_to_home()

		clicked = self._click_first_visible([
			CommonPerformanceLocators.PERFORMANCE_MENU,
			HomeLocators.PERFORMANCE_MENU,
		], timeout=12000)
		assert clicked, "Performance menu is not visible/clickable"

	def validate_course_program_label_and_select_course(self, course_name):
		assert self._first_visible([CommonPerformanceLocators.VALIDATE_COURSE_PROGRAM_LABEL], timeout=12000), \
			"Course / Program label is not visible"
		assert self._click_first_visible([CommonPerformanceLocators.SELECT_COURSE_INPUT_FIELD]), \
			"Select course input field is not visible/clickable"
		clicked = self._click_first_visible([
			f"(//div[@class='ant-select-item-option-content' and normalize-space()='{course_name}'])[1]",
			f"(//div[contains(@class,'ant-select-item-option-content') and normalize-space()='{course_name}'])[1]",
			f"(//span[normalize-space()='{course_name}'])[1]",
			CommonPerformanceLocators.FIRST_COURSE_IN_DROPDOWN,
		], timeout=10000)
		assert clicked, f"Course '{course_name}' is not visible/clickable in dropdown"

	def validate_risk_category_and_select_critical(self):
		assert self._first_visible([CommonPerformanceLocators.VALIDATE_RISK_CATEGORY_LABEL], timeout=12000), \
			"Risk Category label is not visible"
		assert self._click_first_visible([CommonPerformanceLocators.SELECT_STATUS_INPUT_FIELD]), \
			"Select status input field is not visible/clickable"
		assert self._click_first_visible([CommonPerformanceLocators.FIRST_STATUS_IN_DROPDOWN]), \
			"Critical status option is not visible/clickable"

	def validate_batch_status_and_select_active(self):
		# Batch Status is a pill toggle (All / Active / Inactive) - just click the Active pill.
		assert self._first_visible([CommonPerformanceLocators.VALIDATE_BATCH_STATUS_LABEL], timeout=12000), \
			"Batch Status label is not visible"
		assert self._click_first_visible([CommonPerformanceLocators.BATCH_STATUS]), \
			"Active batch status pill is not visible/clickable"

	def click_clear_button(self):
		assert self._click_first_visible([CommonPerformanceLocators.CLEAR_BUTTON], timeout=12000), \
			"Clear button is not visible/clickable"

	def click_batch_row_and_validate_certification_status(self):
		assert self._click_first_visible([CommonPerformanceLocators.BATCH_DETAILS_ROW_OPTION], timeout=12000), \
			"Batch details row is not visible/clickable"
		assert self._first_visible([CommonPerformanceLocators.VALIDATE_CERTIFICATION_STATUS_LABEL], timeout=12000), \
			"Certification Status label is not visible"

	def validate_student_activity_and_click_plus_icons(self):
		assert self._first_visible([CommonPerformanceLocators.VALIDATE_STUDENT_ACTIVITY_LABEL], timeout=12000), \
			"Student Activity label is not visible"
		assert self._click_first_visible([CommonPerformanceLocators.PLUS_ICON_PREVIDEO]), \
			"Pre-video plus icon is not visible/clickable"
		assert self._click_first_visible([CommonPerformanceLocators.PLUS_ICON_POSTVIDEO]), \
			"Post-video plus icon is not visible/clickable"

	def validate_assessment_activity_and_click_quiz_plus(self):
		assert self._first_visible([CommonPerformanceLocators.VALIDATE_STUDENT_ACTIVITY_ASSESSMENTS_LABEL], timeout=12000), \
			"Student Activity - Assessments label is not visible"
		assert self._click_first_visible([CommonPerformanceLocators.QUIZ_PLUS_ICON]), \
			"Quiz plus icon is not visible/clickable"

	def click_back_to_dashboard(self):
		assert self._click_first_visible([CommonPerformanceLocators.BACK_TO_DASHBOARD_BUTTON], timeout=12000), \
			"Back to Dashboard button is not visible/clickable"

	def _scroll_into_view(self, locator):
		try:
			locator.scroll_into_view_if_needed(timeout=5000)
		except Exception:
			pass

	def click_next_and_validate_page_number(self):
		# Pagination sits at the bottom of the list - bring it into view first.
		active = self._first_visible([CommonPerformanceLocators.ACTIVE_PAGE_BUTTON], timeout=12000)
		assert active, "Pagination active page indicator is not visible"
		self._scroll_into_view(active)
		# Page numbers 1/2/3 are always rendered, so assert the *active* page actually moves.
		page_before = active.inner_text().strip()

		assert self._click_first_visible([CommonPerformanceLocators.NEXT_BUTTON], timeout=12000), \
			"Pagination Next button is not visible/clickable"
		self.page.wait_for_timeout(1000)

		new_active = self._first_visible([CommonPerformanceLocators.ACTIVE_PAGE_BUTTON], timeout=12000)
		assert new_active, "Pagination active page indicator is not visible after clicking Next"
		page_after = new_active.inner_text().strip()
		assert page_after != page_before, \
			f"Page number did not advance after clicking Next (still on page '{page_after}')"
		print(f"Pagination advanced from page {page_before} to page {page_after}")

	def select_perpage_and_validate(self, per_page="25"):
		dropdown = self._first_visible([CommonPerformanceLocators.PER_PAGE_DROPDOWN], timeout=12000)
		assert dropdown, "Per page dropdown is not visible"
		# Per-page control sits at the bottom of the list - bring it into view first.
		self._scroll_into_view(dropdown)

		options = dropdown.locator("option").all_inner_texts()
		assert options, "Per page dropdown has no options"
		assert any(per_page in option for option in options), \
			f"Per page option '{per_page}' is not available in {options}"

		dropdown.select_option(per_page)
		self.page.wait_for_timeout(1000)

		# Changing per-page resets the list to page 1 - validate the active page reflects that.
		active = self._first_visible([CommonPerformanceLocators.ACTIVE_PAGE_BUTTON], timeout=12000)
		assert active, "Pagination active page indicator is not visible after changing per page"
		page_after = active.inner_text().strip()
		assert page_after == "1", \
			f"Expected to reset to page 1 after selecting {per_page} per page, but on page '{page_after}'"
		print(f"Per page set to {per_page}; active page is {page_after}")
