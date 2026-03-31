from pages.base_page import BasePage
from locators.Common_locators.common_activity_insights_locators import CommonActivityInsightsLocators


class CommonActivityInsightsPage(BasePage):
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

	def validate_activity_insights_tab_and_click(self):
		clicked = self._click_first_visible([
			CommonActivityInsightsLocators.ACTIVITY_INSIGHTS_TAB,
			"(//p[normalize-space()='Activity Insights'])[1]",
		], timeout=15000)
		assert clicked, "Activity Insights tab is not visible/clickable"

	def validate_submission_header_module_and_lesson(self):
		header = self._first_visible([CommonActivityInsightsLocators.SUBMISSION_INSIGHTS_HEADER_SECTION])
		module = self._first_visible([CommonActivityInsightsLocators.MODULE_COLUMN_TITLE])
		lesson = self._first_visible([CommonActivityInsightsLocators.LESSON_NAME_COLUMN_TITLE])
		assert header, "Submission insights header section is not visible"
		assert module, "Module column title is not visible"
		assert lesson, "Lesson name column title is not visible"

	def click_students_submitted_icon_and_validate(self):
		clicked = self._click_first_visible([CommonActivityInsightsLocators.STUDENTS_SUBMITTED_I_ICON])
		assert clicked, "Students submitted info icon is not visible/clickable"
		tooltip = self._first_visible([
			"//div[contains(@class,'ant-tooltip-inner')]",
			"//div[@role='tooltip']",
		], timeout=5000)
		assert tooltip, "Tooltip text is not visible for students submitted info"

	def click_students_scored_icon_and_validate(self):
		clicked = self._click_first_visible([CommonActivityInsightsLocators.STUDENTS_SCORED_I_ICON])
		assert clicked, "Students scored info icon is not visible/clickable"
		tooltip = self._first_visible([
			"//div[contains(@class,'ant-tooltip-inner')]",
			"//div[@role='tooltip']",
		], timeout=5000)
		assert tooltip, "Tooltip text is not visible for students scored info"

	def open_lesson_arrow_validate_and_back(self, arrow_locator):
		clicked = self._click_first_visible([arrow_locator], timeout=10000)
		assert clicked, "Lesson row arrow icon is not visible/clickable"

		heading = self._first_visible([CommonActivityInsightsLocators.HEADING_SECTION], timeout=10000)
		table = self._first_visible([CommonActivityInsightsLocators.INSIGHTS_TABLE], timeout=10000)
		assert heading, "Insights detail heading section is not visible"
		assert table, "Insights detail table is not visible"

		back_clicked = self._click_first_visible([CommonActivityInsightsLocators.BACK_ARROW], timeout=10000)
		assert back_clicked, "Insights detail back arrow is not visible/clickable"
