import re

from pages.base_page import BasePage
from locators.Faculty_locators.Home_locators import HomeLocators
from utils.helpers import highlight_element


class FacultyHomePage(BasePage):

	def navigate_to_dashboard(self):
		self.page.locator(HomeLocators.HOME_MENU).first.wait_for(state="visible", timeout=20000)
		self.click_home_menu()
		dashboard = self._first_visible([
			HomeLocators.FACULTY_DASHBOARD_CONTAINER,
			HomeLocators.RECOMMENDED_ACTIVITIES_SECTION,
			HomeLocators.BATCHES_TITLE,
		], timeout=20000)
		assert dashboard, "Faculty dashboard did not load after login"

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
		locator = self._first_visible(selectors, timeout=timeout)
		if not locator:
			return False
		self._show_element(locator, duration=1200)
		try:
			locator.scroll_into_view_if_needed()
		except Exception:
			pass
		try:
			locator.click(timeout=timeout)
		except Exception:
			locator.click(timeout=timeout, force=True)
		return True

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

	def click_home_menu(self):
		clicked = self._click_first_visible([
			HomeLocators.HOME_MENU,
			"//div[@role='menuitem' and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'HOME')]",
		])
		assert clicked, "Home menu is not visible/clickable"

	def click_batches_menu(self):
		clicked = self._click_first_visible([
			HomeLocators.BATCHES_MENU,
			"//div[@role='menuitem' and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'BATCH')]",
		])
		assert clicked, "Batches menu is not visible/clickable"

	def click_performance_menu(self):
		clicked = self._click_first_visible([
			HomeLocators.PERFORMANCE_MENU,
			"//div[@role='menuitem' and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'PERFORMANCE')]",
		])
		assert clicked, "Performance menu is not visible/clickable"

	def click_calendar_menu(self):
		clicked = self._click_first_visible([
			HomeLocators.CALENDER_MENU,
			"//div[@id='Calendar']",
			"(//img[contains(@alt,'calendar') or contains(@class,'calendar')])[1]",
		])
		assert clicked, "Calendar menu is not visible/clickable"

	def navigate_to_home(self):
		self.click_home_menu()
		section = self._first_visible([
			HomeLocators.FACULTY_DASHBOARD_CONTAINER,
			HomeLocators.RECOMMENDED_ACTIVITIES_SECTION,
		], timeout=15000)
		assert section, "Faculty home page did not become visible"

	def navigate_help_support(self):
		support_menu = self.page.locator(HomeLocators.SUPPORT_MENU).first
		support_menu.wait_for(state="visible", timeout=10000)
		self._show_element(support_menu, duration=1200)
		with self.page.context.expect_page() as page_info:
			support_menu.click()
		support_page = page_info.value
		support_page.wait_for_load_state("domcontentloaded")
		support_page.close()
		self.page.bring_to_front()

	def check_notifications_and_chat(self):
		chat_menu = self.page.locator(HomeLocators.CHAT_MENU).first
		chat_menu.wait_for(state="visible", timeout=10000)
		self._show_element(chat_menu, duration=1200)
		chat_menu.click()

		notifications_menu = self.page.locator(HomeLocators.NOTIFICATIONS_MENU).first
		notifications_menu.wait_for(state="visible", timeout=10000)
		self._show_element(notifications_menu, duration=1200)
		notifications_menu.click()

		close_icon = self.page.locator(HomeLocators.CLOSE_NOTIFICATION).first
		try:
			close_icon.wait_for(state="visible", timeout=5000)
			self._show_element(close_icon, duration=800)
			close_icon.click()
		except Exception:
			pass

	def click_profile_icon(self):
		profile_menu = self.page.locator(HomeLocators.PROFILE_MENU).first
		profile_menu.wait_for(state="visible", timeout=10000)
		self._show_element(profile_menu, duration=1200)
		profile_menu.click()

	def edit_profile_details(self):
		profile = self._first_visible([HomeLocators.MY_PROFILE, "//span[contains(.,'My Profile')]"], timeout=8000)
		assert profile, "My Profile option is not visible"
		self._show_element(profile, duration=1200)
		profile.click()

		first_name = self.page.locator(HomeLocators.FIRST_NAME).first
		is_edit_mode_open = False
		try:
			first_name.wait_for(state="visible", timeout=5000)
			assert first_name.is_visible(), "First name field is not visible in profile edit"
			is_edit_mode_open = True
		except Exception:
			pass

		if not is_edit_mode_open:
			edit = self._first_visible([
				HomeLocators.EDIT_PROFILE,
				HomeLocators.EDIT_BUTTON,
				"//button[normalize-space()='Edit' or .//span[normalize-space()='Edit']]",
				"//*[self::button or self::span][contains(@class,'edit') and not(contains(@class,'credit'))]",
			], timeout=8000)
			assert edit, "Edit profile action is not visible"
			self._show_element(edit, duration=1200)
			edit.click()

			first_name.wait_for(state="visible", timeout=10000)
			assert first_name.is_visible(), "First name field is not visible in profile edit"

		current_first_name = (first_name.input_value() or "").strip()
		match = re.match(r"^(.*?)(\d+)$", current_first_name)
		if match:
			name_prefix = match.group(1) or "FacultyAuto"
			next_number = int(match.group(2)) + 1
			next_first_name = f"{name_prefix}{next_number}"
		else:
			name_prefix = current_first_name or "FacultyAuto"
			next_first_name = f"{name_prefix}1"

		first_name.fill(next_first_name)
		self._show_element(first_name, duration=1200)
		self.page.wait_for_timeout(300)
		print(f"Updated first name: {next_first_name}")

	def validate_recommended_activities_section(self):
		section = self._first_visible([
			HomeLocators.RECOMMENDED_ACTIVITIES_SECTION,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'RECOMMENDED ACTIVITIES')]",
		], timeout=10000)
		assert section, "Recommended Activities section is not visible"
		self._show_element(section, duration=1400)

		card = self.page.locator(HomeLocators.RECOMMENDED_ACTIVITY_CARD).first
		card.wait_for(state="visible", timeout=10000)
		assert card.is_visible(), "Recommended activity card is not visible"
		self._show_element(card, duration=1000)

	def validate_batches_section(self):
		title = self._first_visible([
			HomeLocators.BATCHES_TITLE,
			"//*[self::h2 or self::h3][contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'BATCH')]",
		], timeout=10000)
		assert title, "Batches title is not visible"
		self._show_element(title, duration=1200)

		section = self.page.locator(HomeLocators.BATCHES_SECTION).first
		section.wait_for(state="visible", timeout=10000)
		assert section.is_visible(), "Batches section is not visible"
		self._show_element(section, duration=1200)

		create_batch_button = self._first_visible([
			HomeLocators.CREATE_NEWBATCH_BUTTON,
			"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CREATE NEW BATCH')]",
		], timeout=10000)
		assert create_batch_button, "Create New Batch button is not visible"
		self._show_element(create_batch_button, duration=1200)

	def validate_active_inactive_tabs_under_batches(self):
		active = self._first_visible([
			HomeLocators.ACTIVE_BATCHES,
			"//button[@role='tab'][contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ACTIVE')]",
		], timeout=10000)
		assert active, "Active tab is not visible"
		self._show_element(active, duration=1000)
		active.click()

		inactive = self._first_visible([
			HomeLocators.INACTIVE_BATCHES,
			"//button[@role='tab'][contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'INACTIVE')]",
		], timeout=10000)
		assert inactive, "Inactive tab is not visible"
		self._show_element(inactive, duration=1000)
		inactive.click()

		active = self._first_visible([
			HomeLocators.ACTIVE_BATCHES,
			"//button[@role='tab'][contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ACTIVE')]",
		], timeout=10000)
		assert active, "Active tab is not visible after switching"
		self._show_element(active, duration=1000)
		active.click()

	def click_batches_next_arrow_button(self):
		clicked = self._click_first_visible([
			HomeLocators.BATCHES_PAGES_ARROW,
			"(//button[contains(@aria-label,'next') or contains(@class,'next')])[1]",
		], timeout=10000)
		assert clicked, "Batches next arrow is not visible/clickable"

	def validate_certified_courses_and_click_carousal_arrow(self):
		courses = self._first_visible([
			HomeLocators.CERTIFIED_COURSES,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CERTIFIED COURSES')]",
		], timeout=10000)
		assert courses, "Certified Courses section is not visible"
		self._show_element(courses, duration=1600)

		carousel = self.page.locator(HomeLocators.CERTIFIED_COURSES_CARUSOL).first
		carousel.wait_for(state="visible", timeout=10000)
		assert carousel.is_visible(), "Certified courses carousel is not visible"
		self._show_element(carousel, duration=1200)

		clicked = self._click_first_visible([
			HomeLocators.CERTIFIED_COURSES_CARUSOL_ARROW,
			"(//button[contains(@aria-label,'Go to next slide')])[1]",
		], timeout=10000)
		assert clicked, "Certified courses carousel next arrow is not visible/clickable"

	def validate_my_forums_section(self):
		section = self._first_visible([
			HomeLocators.FORUMS_SECTION,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'FORUM')]",
		], timeout=10000)
		assert section, "Forums section is not visible"
		self._show_element(section, duration=1600)

		title = self.page.locator(HomeLocators.MY_FORUMS_TITLE).first
		title.wait_for(state="visible", timeout=10000)
		assert title.is_visible(), "My Forums title is not visible"
		self._show_element(title, duration=1400)

		card = self.page.locator(HomeLocators.FORUM_CARD).first
		card.wait_for(state="visible", timeout=10000)
		assert card.is_visible(), "Forum card is not visible"
		self._show_element(card, duration=1400)
