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

	def _scroll_page_to_end(self, max_attempts=25, pause_ms=350):
		"""Scroll down until no further vertical movement is possible."""
		last_scroll_top = -1
		for _ in range(max_attempts):
			current_scroll_top = self.page.evaluate(
				"() => document.scrollingElement ? document.scrollingElement.scrollTop : window.scrollY"
			)
			if current_scroll_top == last_scroll_top:
				break
			last_scroll_top = current_scroll_top
			self.page.evaluate(
				"() => {"
				"const el = document.scrollingElement || document.documentElement;"
				"el.scrollBy(0, Math.max(window.innerHeight * 0.8, 500));"
				"}"
			)
			self.page.wait_for_timeout(pause_ms)

	def _click_arrow_until_end(self, selectors, max_clicks=15, pause_ms=300):
		"""Click a next-arrow until it is no longer available."""
		clicked_any = False
		for _ in range(max_clicks):
			arrow = self._first_visible(selectors, timeout=2000)
			if not arrow:
				break
			try:
				if not arrow.is_enabled():
					break
			except Exception:
				pass

			self._show_element(arrow, duration=900)
			try:
				arrow.click(timeout=2000)
			except Exception:
				try:
					arrow.click(timeout=2000, force=True)
				except Exception:
					break

			clicked_any = True
			self.page.wait_for_timeout(pause_ms)

		return clicked_any

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

		# Persist profile changes; otherwise the value only changes in the input field.
		updated = self._click_first_visible([
			HomeLocators.SAVE_BUTTON,
			"(//button[normalize-space()='Update'])[1]",
			"(//button[normalize-space()='Save'])[1]",
			"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'UPDATE')]",
			"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SAVE')]",
		], timeout=10000)
		assert updated, "Update/Save button is not visible/clickable in profile edit"
		self.page.wait_for_timeout(1200)
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
		clicked = self._click_arrow_until_end([
			HomeLocators.BATCHES_PAGES_ARROW,
			"(//button[contains(@aria-label,'next') or contains(@class,'next')])[1]",
		], max_clicks=20, pause_ms=250)
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

		clicked = self._click_arrow_until_end([
			HomeLocators.CERTIFIED_COURSES_CARUSOL_ARROW,
			"(//button[contains(@aria-label,'Go to next slide')])[1]",
		], max_clicks=12, pause_ms=300)
		if not clicked:
			print("Certified courses carousel next arrow not visible; continuing with scroll to end")

		# Move through the remaining dashboard cards until the bottom is reached.
		self._scroll_page_to_end(max_attempts=30, pause_ms=300)

	def validate_my_forums_section(self):
		# Reach lower dashboard sections that are lazy-rendered as user scrolls.
		self._scroll_page_to_end(max_attempts=30, pause_ms=350)

		section = self._first_visible([
			HomeLocators.FORUMS_SECTION,
			HomeLocators.RECOMMENDED_FORUMS_TITLE,
			HomeLocators.MY_FORUMS_TITLE,
			"//*[self::h2 or self::h3 or self::h4 or self::p][contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'RECOMMENDED FORUMS')]",
			"//*[self::h2 or self::h3 or self::h4 or self::p][contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'MY FORUMS')]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'FORUM')]",
		], timeout=15000)
		assert section, "Forums section is not visible"
		self._show_element(section, duration=1600)

		recommended_title = self._first_visible([
			HomeLocators.RECOMMENDED_FORUMS_TITLE,
			"//*[self::h2 or self::h3 or self::h4 or self::p][contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'RECOMMENDED FORUMS')]",
		], timeout=3500)
		recommended_present = bool(recommended_title)
		if recommended_title:
			self._show_element(recommended_title, duration=1400)

		my_forums_title = self._first_visible([
			HomeLocators.MY_FORUMS_TITLE,
			"//*[self::h2 or self::h3 or self::h4 or self::p][contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'MY FORUMS')]",
		], timeout=3500)
		my_forums_present = bool(my_forums_title)
		if my_forums_title:
			self._show_element(my_forums_title, duration=1400)

		assert recommended_present or my_forums_present, "Neither Recommended Forums nor My Forums section is visible"

		# Validate cards only for sections that are present.
		if recommended_present:
			recommended_card = self._first_visible([
				HomeLocators.RECOMMENDED_FORUM_CARD,
				"(//span[@id='recommended_forum_container'])[1]//ancestor::*[contains(@class,'forum') or contains(@class,'card')][1]",
			], timeout=3000)
			if recommended_card:
				self._show_element(recommended_card, duration=1200)
			else:
				print("Recommended Forums is visible; no recommended forum card found to highlight")

		if my_forums_present:
			my_forums_card = self._first_visible([
				HomeLocators.FORUM_CARD,
				"//*[contains(@class,'forum') and .//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'MY FORUMS')]]//*[contains(@class,'card')]",
			], timeout=3000)
			if my_forums_card:
				self._show_element(my_forums_card, duration=1200)
			else:
				print("My Forums is visible; no my-forums card found to highlight")
