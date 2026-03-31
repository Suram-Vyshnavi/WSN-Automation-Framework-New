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

	def validate_reports_title(self):
		title = self._first_visible([CommonPerformanceLocators.REPORTS_TITLE], timeout=12000)
		assert title, "Reports title is not visible"

	def select_first_course(self):
		container = self._first_visible([CommonPerformanceLocators.COURSE_NAME_CONTAINER])
		assert container, "Course name container is not visible"
		assert self._click_first_visible([CommonPerformanceLocators.SELECT_COURSE_INPUT_FIELD]), "Select course input field is not visible/clickable"
		assert self._click_first_visible([CommonPerformanceLocators.FIRST_COURSE_IN_DROPDOWN]), "First course option is not visible/clickable"

	def select_first_status(self):
		container = self._first_visible([CommonPerformanceLocators.STATUS_CONTAINER])
		assert container, "Status container is not visible"
		assert self._click_first_visible([CommonPerformanceLocators.SELECT_STATUS_INPUT_FIELD]), "Select status input field is not visible/clickable"
		assert self._click_first_visible([CommonPerformanceLocators.FIRST_STATUS_IN_DROPDOWN]), "First status option is not visible/clickable"

	def select_batch_name(self, batch_name):
		container = self._first_visible([CommonPerformanceLocators.BATCH_NAME_CONTAINER])
		assert container, "Batch name container is not visible"
		assert self._click_first_visible([CommonPerformanceLocators.SELECT_BATCH_INPUT_FIELD]), "Select batch input field is not visible/clickable"

		clicked = self._click_first_visible([
			f"(//div[@class='ant-select-item-option-content' and normalize-space()='{batch_name}'])[1]",
			f"(//span[normalize-space()='{batch_name}'])[1]",
			CommonPerformanceLocators.BATCH_NAME_IN_DROPDOWN,
		], timeout=10000)
		assert clicked, f"Batch '{batch_name}' is not visible/clickable in dropdown"

	def validate_batch_assessment_title_and_graph(self):
		title = self._first_visible([CommonPerformanceLocators.BATCH_ASSESEMENT_TITLE], timeout=12000)
		graph = self._first_visible([CommonPerformanceLocators.BATCH_ASSESSMENT_GRAPH], timeout=12000)
		assert title, "Batch assessment title is not visible"
		assert graph, "Batch assessment graph is not visible"

	def validate_assessment_status_and_toggle(self):
		status = self._first_visible([CommonPerformanceLocators.ASSESSMENT_STATUS_TITLE], timeout=12000)
		toggle = self._first_visible([CommonPerformanceLocators.SHOW_SCORE_TOGGLE_BUTTON], timeout=12000)
		assert status, "Assessment status title is not visible"
		assert toggle, "Show score toggle button is not visible"

	def click_score_toggle_and_next_arrow(self):
		toggled = self._click_first_visible([CommonPerformanceLocators.SHOW_SCORE_TOGGLE_BUTTON])
		assert toggled, "Score toggle button is not visible/clickable"

		next_clicked = self._click_first_visible([CommonPerformanceLocators.ASSESSMENT_STATUS_NEXTSCREEN_ARROW], timeout=12000)
		assert next_clicked, "Assessment status next arrow button is not visible/clickable"

	def click_student_name_link(self):
		clicked = self._click_first_visible([CommonPerformanceLocators.STUDENT_NAME_LINK], timeout=12000)
		assert clicked, "Student name link is not visible/clickable"

	def validate_student_performance_cards(self):
		assert self._first_visible([CommonPerformanceLocators.COURSE_NAME_DROPDOWN], timeout=12000), "Course name dropdown is not visible"
		assert self._first_visible([CommonPerformanceLocators.STUDENT_NAME_CARD], timeout=12000), "Student name card is not visible"
		assert self._first_visible([CommonPerformanceLocators.COURSE_NAME_CARD], timeout=12000), "Course name card is not visible"
		assert self._first_visible([CommonPerformanceLocators.INSTITUTE_NAME_CARD], timeout=12000), "Institute name card is not visible"
		assert self._first_visible([CommonPerformanceLocators.COMPLETION_STATUS_CARD], timeout=12000), "Completion status card is not visible"
		assert self._first_visible([CommonPerformanceLocators.ASSESSMENT_SCORE_DETAILS_CARD], timeout=12000), "Assessment score details card is not visible"
