from pages.base_page import BasePage
from locators.Faculty_locators.Batch_details_collaboratesetup_locators import BatchDetailsCollaboratesetupLocators
from utils.helpers import highlight_element


class BatchDetailsCollaborateSetupPage(BasePage):

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

	def validate_collaboratesetup_tab_and_click(self):
		collab_tab = self._first_visible([
			BatchDetailsCollaboratesetupLocators.COLLABORATESETUP_TAB,
			"//p[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'COLLABORATE SETUP')]",
			"//*[contains(@class,'tab') and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'COLLABORATE')]",
		], timeout=10000)
		assert collab_tab, "Collaborate Setup tab is not visible"

		clicked = self._click_first_visible([
			BatchDetailsCollaboratesetupLocators.COLLABORATESETUP_TAB,
			"//p[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'COLLABORATE SETUP')]",
		], timeout=8000)
		assert clicked, "Collaborate Setup tab is not clickable"

	def click_edit_and_change_level_save(self):
		collab_title = self._first_visible([
			BatchDetailsCollaboratesetupLocators.COLLABORATE_TITLE,
			"//h4[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'COLLABORATE')]",
		], timeout=15000)
		assert collab_title, "Collaborate setup customize title is not visible"

		edit_clicked = self._click_first_visible([
			BatchDetailsCollaboratesetupLocators.COLLABORATE_EDIT_BUTTON,
			"//button[normalize-space()='Edit']",
		], timeout=10000)
		assert edit_clicked, "Edit button is not visible/clickable"

		level1_clicked = self._click_first_visible([
			BatchDetailsCollaboratesetupLocators.LEVEL1_SECTION,
			"(//div[contains(@class,'radio_option')])[1]",
		], timeout=10000)
		assert level1_clicked, "Level 1 option is not visible/clickable"

		save_clicked = self._click_first_visible([
			BatchDetailsCollaboratesetupLocators.COLLABORATE_SAVE_BUTTON,
			"//button[normalize-space()='Save']",
		], timeout=10000)
		assert save_clicked, "Save button is not visible/clickable"

	def navigate_to_collaborate_setup_and_validate_career_plans(self):
		self._full_page_scroll_cycle()
		career_plans = self._first_visible([
			BatchDetailsCollaboratesetupLocators.SELECTED_CAREER_PLANS_SECTION,
			"//div[contains(@class,'career-plans-container')]",
		], timeout=15000)
		assert career_plans, "Selected Career Plans section is not visible"
		self._show_element(career_plans, duration=700)
