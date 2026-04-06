from pages.base_page import BasePage
from locators.RM_locators.All_batches_locators import AllBatchesLocators
from utils.helpers import highlight_element


class RMAllBatchesPage(BasePage):

	def _show_element(self, locator, duration=1000):
		try:
			locator.scroll_into_view_if_needed()
		except Exception:
			pass
		try:
			highlight_element(self.page, locator, duration=duration)
		except Exception:
			pass

	def _first_visible(self, selectors, timeout=8000):
		for selector in selectors:
			locator = self.page.locator(selector).first
			try:
				locator.wait_for(state="visible", timeout=timeout)
				self._show_element(locator, duration=850)
				return locator
			except Exception:
				continue
		return None

	def _click_first_visible(self, selectors, timeout=8000):
		locator = self._first_visible(selectors, timeout=timeout)
		if not locator:
			return False
		try:
			locator.click(timeout=timeout)
		except Exception:
			locator.click(timeout=timeout, force=True)
		return True

	def _go_to_home_menu(self):
		self._click_first_visible([
			"//div[@id='Home']",
			"//div[@role='menuitem' and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'HOME')]",
		], timeout=7000)
		self.page.wait_for_timeout(700)

	def click_batch_by_name(self, batch_name):
		"""Navigate to Home → Assigned Batches and click the row matching batch_name."""
		self._go_to_home_menu()

		assigned_title = self._first_visible([
			"(//h2[normalize-space()='Assigned Batches'])[1]",
			"//*[self::h2 or self::h3][contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ASSIGNED BATCH')]",
		], timeout=12000)
		assert assigned_title, "Assigned Batches section is not visible on RM home screen"

		batch_row = self._click_first_visible([
			f"(//tbody//tr//td[normalize-space()='{batch_name}'])[1]",
			f"(//table//td[normalize-space()='{batch_name}'])[1]",
			f"(//*[contains(@class,'batch-list-content') and normalize-space()='{batch_name}'])[1]",
		], timeout=12000)

		if batch_row:
			return

		# Fallback: use All Batches screen and search by name
		self._click_first_visible([
			"//div[@id='All']",
			"//div[@role='menuitem' and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ALL BATCH')]",
		], timeout=10000)
		self.page.wait_for_timeout(700)
		clicked_fallback = self._click_first_visible([
			f"(//tbody//tr//td[normalize-space()='{batch_name}'])[1]",
			f"(//table//td[normalize-space()='{batch_name}'])[1]",
			f"(//*[contains(@class,'batch-list-content') and normalize-space()='{batch_name}'])[1]",
		], timeout=12000)
		assert clicked_fallback, f"Batch '{batch_name}' is not visible/clickable in Assigned Batches or All Batches list"

	def click_first_assigned_batch(self):
		# RM dashboard uses Assigned Batches on Home screen (not Active Batches tab).
		self._go_to_home_menu()

		assigned_title = self._first_visible([
			"(//h2[normalize-space()='Assigned Batches'])[1]",
			"//*[self::h2 or self::h3][contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ASSIGNED BATCH')]",
		], timeout=12000)
		assert assigned_title, "Assigned Batches section is not visible on RM home screen"

		clicked_assigned = self._click_first_visible([
			"(//tbody//tr[1]//td[contains(@class,'batch-list-content-bold')])[1]",
			"(//tbody//tr[1]//td[contains(@class,'batch-list-content')])[1]",
			"(//tbody//tr[1]//td)[1]",
			"(//div[contains(@class,'ant-table-tbody')]//tr[1]//td[1])[1]",
		], timeout=10000)

		if clicked_assigned:
			return

		# Fallback: if Assigned Batches row is not interactable, use All Batches list.
		opened = self._click_first_visible([
			"//div[@id='All']",
			"//div[@role='menuitem' and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ALL BATCH')]",
		], timeout=10000)
		assert opened, "Unable to open All Batches menu from RM flow"

		all_batches_title = self._first_visible([
			AllBatchesLocators.ALL_BATCHES_TITLE,
			"//*[self::h2 or self::h3][contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ALL BATCH')]",
		], timeout=15000)
		assert all_batches_title, "All Batches page did not load"

		clicked_fallback = self._click_first_visible([
			"(//tbody//tr[1]//td[contains(@class,'batch-list-content-bold')])[1]",
			"(//tbody//tr[1]//td[contains(@class,'batch-list-content')])[1]",
			"(//tbody//tr[1]//td)[1]",
		], timeout=10000)
		assert clicked_fallback, "First batch row is not visible/clickable in RM flow"

	def click_first_active_batch(self):
		# Backward-compatible alias for existing step text.
		self.click_first_assigned_batch()

	def click_all_batches_menu(self):
		clicked = self._click_first_visible([
			"(//div[@id='All'])[1]",
			"//div[@id='All']",
			"//div[@role='menuitem' and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ALL BATCH')]",
		], timeout=12000)
		assert clicked, "All Batches menu is not visible/clickable"

	def validate_all_batches_title_and_search(self, batch_name):
		title = self._first_visible([
			AllBatchesLocators.ALL_BATCHES_TITLE,
			"//*[self::h2 or self::h3][contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ALL BATCH')]",
		], timeout=15000)
		assert title, "All Batches title is not visible"

		search = self._first_visible([
			AllBatchesLocators.SEARCHBAR,
			"(//input[contains(@placeholder,'Search')])[1]",
		], timeout=10000)
		assert search, "All Batches search bar is not visible"
		search.click(timeout=3000)
		search.fill(batch_name, timeout=4000)
		try:
			search.press("Enter")
		except Exception:
			pass
		self.page.wait_for_timeout(800)

	def validate_status_title(self):
		status_title = self._first_visible([
			AllBatchesLocators.STATUS_TITLE,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'STATUS')]",
		], timeout=10000)
		assert status_title, "Status title is not visible on All Batches screen"

	def select_status_option(self, option_text):
		dropdown = self._first_visible([
			AllBatchesLocators.STATUS_DROPDOWN,
			"(//button[contains(@class,'dropdown-btn')])[1]",
			"(//button[contains(@class,'ant-btn') and .//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'STATUS')]])[1]",
		], timeout=10000)
		assert dropdown, "Status dropdown is not visible/clickable"
		try:
			dropdown.click(timeout=4000)
		except Exception:
			dropdown.click(timeout=4000, force=True)

		if option_text.strip().lower() == "active":
			option_locators = [
				AllBatchesLocators.ACTIVE_OPTION_IN_DROPDOWN,
				"//div[contains(@class,'ant-dropdown')]//span[normalize-space(text())='Active']",
			]
		else:
			option_locators = [
				AllBatchesLocators.INACTIVE_OPTION_IN_DROPDOWN,
				"//div[contains(@class,'ant-dropdown')]//span[normalize-space(text())='Inactive']",
			]

		selected = self._click_first_visible(option_locators, timeout=8000)
		assert selected, f"Unable to select '{option_text}' option from Status dropdown"
		self.page.wait_for_timeout(900)

	def validate_batches_section(self):
		container = self._first_visible([
			AllBatchesLocators.ALL_BATCHES_CONTAINER,
			"(//div[contains(@class,'site-content')])[1]",
			"(//table[contains(@class,'ant-table')])[1]",
		], timeout=12000)
		assert container, "All Batches section/container is not visible"

