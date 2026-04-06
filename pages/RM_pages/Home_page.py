from pages.base_page import BasePage
from locators.RM_locators.Home_locators import HomeLocators
from utils.helpers import highlight_element


class RMHomePage(BasePage):

	def _show_element(self, locator, duration=1000):
		try:
			locator.scroll_into_view_if_needed()
		except Exception:
			pass
		try:
			highlight_element(self.page, locator, duration=duration)
		except Exception:
			pass

	def _first_visible(self, selectors, timeout=10000):
		for selector in selectors:
			locator = self.page.locator(selector).first
			try:
				locator.wait_for(state="visible", timeout=timeout)
				self._show_element(locator, duration=900)
				return locator
			except Exception:
				continue
		return None

	def _click_first_visible(self, selectors, timeout=10000):
		locator = self._first_visible(selectors, timeout=timeout)
		if not locator:
			return False
		try:
			locator.click(timeout=timeout)
		except Exception:
			locator.click(timeout=timeout, force=True)
		return True

	def click_all_batches_menu(self):
		clicked = self._click_first_visible([
			HomeLocators.ALL_BATCHES_MENU,
			"//div[@id='All']",
			"//div[@role='menuitem' and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ALL BATCH')]",
		])
		assert clicked, "All Batches menu is not visible/clickable"

	def validate_assigned_batches_section(self):
		title = self._first_visible([
			HomeLocators.ASSIGNED_BATCHES_TITLE,
			"//*[self::h2 or self::h3][contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ASSIGNED BATCH')]",
		], timeout=15000)
		assert title, "Assigned Batches section is not visible"

	def validate_assigned_batches_table_headers(self):
		expected_headers = [
			("Batch Name", HomeLocators.BATCH_NAME_TITLE),
			("Institute Name", HomeLocators.INSTITUTE_NAME_TITLE),
			("Course Name", HomeLocators.COURSE_NAME_TITLE),
			("Start Date", HomeLocators.START_DATE_TITLE),
			("End Date", HomeLocators.END_DATE_TITLE),
			("No. of Students", HomeLocators.NO_OF_STUDENTS_TITLE),
			("Action", HomeLocators.ACTION_TITLE),
		]

		for header_name, locator in expected_headers:
			header = self._first_visible([
				locator,
				f"//*[contains(@class,'ant-table') and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), '{header_name.upper()}')]",
			], timeout=10000)
			assert header, f"'{header_name}' column title is not visible in Assigned Batches section"

	def click_assigned_batches_next_arrow_button(self):
		next_arrow = self._first_visible([
			HomeLocators.ASSIGNED_BATCHES_NEXT_BUTTON,
			"//li[contains(@class,'ant-pagination-next')]/button[not(@disabled)]",
		], timeout=5000)
		assert next_arrow, "Assigned Batches next arrow is not visible/clickable"
		try:
			next_arrow.click(timeout=4000)
		except Exception:
			next_arrow.click(timeout=4000, force=True)

