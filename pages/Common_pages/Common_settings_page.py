from pages.base_page import BasePage
from locators.Common_locators.common_settings_zoomconnect_locators import CommonSettingsZoomConnectLocators
from locators.Common_locators.common_WhatsappNotifications_locators import CommonSettingsWhatsappNotificationsLocators
from locators.Faculty_locators.Home_locators import HomeLocators


class CommonSettingsPage(BasePage):

	def _settings_panel_visible(self, timeout=1500):
		panel = self._first_visible([
			"//div[contains(@class,'userSettings_menuItem')]",
			"//div[contains(@class,'userSettings')]//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ACCOUNTS')]",
			"//div[contains(@class,'userSettings')]//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTIFICATIONS')]",
		], timeout=timeout)
		return bool(panel)

	def _first_visible(self, selectors, timeout=1500):
		for selector in selectors:
			locator = self.page.locator(selector).first
			try:
				locator.wait_for(state="visible", timeout=timeout)
				return locator
			except Exception:
				continue
		return None

	def _click_first_visible(self, selectors, timeout=1500):
		for selector in selectors:
			target = self.page.locator(selector).first
			try:
				target.wait_for(state="visible", timeout=timeout)
				try:
					target.scroll_into_view_if_needed()
				except Exception:
					pass
				try:
					target.click(timeout=timeout)
				except Exception:
					target.click(timeout=timeout, force=True)
				return True
			except Exception:
				continue
		return False

	def _click_first_attached(self, selectors, timeout=1500):
		for selector in selectors:
			locator = self.page.locator(selector).first
			try:
				locator.wait_for(state="attached", timeout=timeout)
				try:
					locator.scroll_into_view_if_needed(timeout=2000)
				except Exception:
					pass
				locator.click(force=True)
				return True
			except Exception:
				continue
		return False

	def click_zoomconnect_profile_icon(self):
		# Quick readiness check so profile click is attempted only after dashboard shell appears.
		self._first_visible([
			HomeLocators.FACULTY_DASHBOARD_CONTAINER,
			HomeLocators.HOME_MENU,
		], timeout=4000)

		# If already inside settings screen, skip profile click.
		if self._settings_panel_visible(timeout=2500):
			return

		clicked = self._click_first_visible([
			HomeLocators.PROFILE_MENU,
			CommonSettingsZoomConnectLocators.PROFILE_ICON,
		], timeout=1500)

		if not clicked:
			clicked = self._click_first_attached([
				HomeLocators.PROFILE_MENU,
				CommonSettingsZoomConnectLocators.PROFILE_ICON,
			], timeout=1500)

		if not clicked:
			# Try up to 3 back navigations in case previous scenario left us deep in nested screens.
			for _ in range(3):
				try:
					self.click_back_arrow()
				except Exception:
					pass
				clicked = self._click_first_visible([
					HomeLocators.PROFILE_MENU,
					CommonSettingsZoomConnectLocators.PROFILE_ICON,
				], timeout=1500)
				if clicked:
					break
				if self._settings_panel_visible(timeout=1500):
					return

		if not clicked:
			# Last resort: navigate to home via sidebar then retry.
			try:
				self.page.locator(HomeLocators.HOME_MENU).first.click(timeout=3000)
				self.page.wait_for_timeout(800)
			except Exception:
				pass
			clicked = self._click_first_visible([
				HomeLocators.PROFILE_MENU,
				CommonSettingsZoomConnectLocators.PROFILE_ICON,
			], timeout=3000)

		if not clicked:
			assert self._settings_panel_visible(timeout=2500), "Profile icon is not visible/clickable"

	def click_settings_menu(self):
		if self._settings_panel_visible(timeout=2500):
			return

		selectors = [
			CommonSettingsZoomConnectLocators.SETTINGS_ICON,
			"//div[@id='Settings']",
			"//*[normalize-space()='Settings']",
			"//div[contains(@class,'menu_item') and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SETTINGS')]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SETTINGS')]",
			"(//div[contains(@class,'app__layout_menu_item')])[2]",
			"(//div[contains(@class,'app__layout_menu_item')])[3]",
		]
		clicked = self._click_first_visible(selectors, timeout=1500)
		if not clicked:
			clicked = self._click_first_attached(selectors, timeout=1500)
		assert clicked, "Settings menu is not visible/clickable"
		assert self._settings_panel_visible(timeout=8000), "Settings panel did not open after clicking settings menu"

	def validate_settings_sections(self):
		assert self._settings_panel_visible(timeout=6000), "Settings sections are not visible"

	def click_back_arrow(self):
		clicked = self._click_first_visible([
			CommonSettingsZoomConnectLocators.BACK_ARROW,
			"//img[contains(@alt,'arrow') and (contains(@alt,'left') or contains(@class,'left_icon'))]",
			"//img[contains(@class,'left_icon')]",
		])
		if clicked:
			return

		if self._settings_panel_visible(timeout=2500):
			return

		try:
			self.page.go_back(wait_until="domcontentloaded")
		except Exception:
			pass

		if self._settings_panel_visible(timeout=3000):
			return

		raise AssertionError("Back arrow not visible in settings flow")

	def click_accounts_menu_zoomconnect(self):
		clicked = self._click_first_visible([
			CommonSettingsZoomConnectLocators.ACCOUNTS_MENU,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ACCOUNTS')]",
		], timeout=5000)
		assert clicked, "Accounts menu is not visible/clickable"

		meeting = self._first_visible([
			CommonSettingsZoomConnectLocators.MEETING_CARD,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'MEETING')]",
			CommonSettingsZoomConnectLocators.ZOOM_SETTINGS_ARROW,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ZOOM')]",
		], timeout=5000)
		assert meeting, "Meetings/Zoom section is not visible under Accounts"

	def click_zoom_right_arrow(self):
		# Only treat as already-open when we are inside the Zoom detail screen.
		# Text like 'SIGN IN WITH ZOOM' can appear on the accounts LIST card too,
		# so use only detail-screen specific containers/controls.
		already_open = self._first_visible([
			CommonSettingsZoomConnectLocators.SIGNIN_WITH_ZOOM_SECTION,
			CommonSettingsZoomConnectLocators.ZOOMCONNECTION_TOGGLER,
			CommonSettingsZoomConnectLocators.MEETINGS_CARD,
		], timeout=1500)
		if already_open:
			print("[ZoomDebug] Zoom detail is already open; skipping right-arrow click")
			return

		selectors = [
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SIGN IN WITH ZOOM')]/ancestor::div[contains(@class,'section-container') or contains(@class,'zoom-container')][1]//img[contains(@alt,'right_arrow') or contains(@alt,'arrow')][1]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ZOOM')]/ancestor::div[contains(@class,'section-container') or contains(@class,'zoom-container')][1]//img[contains(@alt,'right_arrow') or contains(@alt,'arrow')][1]",
			CommonSettingsZoomConnectLocators.ZOOM_SETTINGS_ARROW,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ZOOM')]/ancestor::*[1]//img[contains(@alt,'right_arrow') or contains(@alt,'arrow')][1]",
			"(//img[contains(@alt,'right_arrow') or contains(@alt,'arrow-right')])[1]",
		]
		clicked = self._click_first_visible(selectors, timeout=4000)
		if not clicked:
			clicked = self._click_first_attached(selectors, timeout=4000)
		if clicked:
			print("[ZoomDebug] Clicked Zoom right-arrow/open control")

		if not clicked:
			# Fallback: open first settings card directly when arrow is not a separate clickable control.
			clicked = self._click_first_visible([
				"(//div[contains(@class,'section-container')])[1]",
				"(//div[contains(@class,'zoom-container')])[1]",
			], timeout=3000)

		if not clicked:
			already_open = self._first_visible([
				CommonSettingsZoomConnectLocators.SIGNIN_WITH_ZOOM_SECTION,
				CommonSettingsZoomConnectLocators.MEETINGS_CARD,
				CommonSettingsZoomConnectLocators.ZOOMCONNECTION_TOGGLER,
				CommonSettingsZoomConnectLocators.SIGNIN_BUTTON,
			], timeout=2500)
			if already_open:
				print("[ZoomDebug] Zoom detail became visible through fallback path")
			assert already_open, "Zoom right arrow is not visible/clickable"

	def validate_delinked_popup(self):
		popup = self.page.locator(CommonSettingsZoomConnectLocators.DELINKED_POPUP).first
		try:
			popup.wait_for(state="visible", timeout=3000)
			self.page.click(CommonSettingsZoomConnectLocators.DELINKED_CLOSEICON)
		except Exception:
			pass

	def validate_signin_section_and_toggle(self):
		section = self._first_visible([
			CommonSettingsZoomConnectLocators.SIGNIN_WITH_ZOOM_SECTION,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SIGN IN WITH ZOOM')]",
		], timeout=5000)
		assert section, "Sign in with Zoom section is not visible"

		clicked = self._click_first_visible([
			CommonSettingsZoomConnectLocators.ZOOMCONNECTION_TOGGLER,
			"//button[@role='switch']",
			"//button[contains(@class,'switch') or contains(@class,'toggle')]",
			"//button[contains(@class,'ant-switch')]",
			"//span[contains(@class,'ant-switch')]",
		], timeout=5000)
		if clicked:
			return

		# Some accounts render Sign In/Meetings/Disconnect directly without a visible toggle.
		already_ready = self._first_visible([
			CommonSettingsZoomConnectLocators.SIGNIN_BUTTON,
			CommonSettingsZoomConnectLocators.MEETINGS_CARD,
			"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'DISCONNECT')]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SIGN IN')]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'MEETINGS')]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CONNECTED')]",
		], timeout=4000)
		assert already_ready, "Zoom toggle button is not visible/clickable"

	def navigate_meetings_and_click_signin(self):
		meeting = self._first_visible([
			CommonSettingsZoomConnectLocators.MEETINGS_CARD,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'MEETINGS')]",
		], timeout=12000)
		assert meeting, "Meetings card is not visible"

		# If account is already connected, disconnect first so Sign In flow becomes available.
		disconnect_button = self._first_visible([
			"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'DISCONNECT')]",
		], timeout=3000)
		if disconnect_button:
			disconnect_button.click()
			# Handle optional confirmation dialogs.
			self._click_first_visible([
				"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CONFIRM')]",
				"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'YES')]",
				"//button[contains(@class,'ant-btn-primary')]",
			], timeout=2500)
			self.page.wait_for_timeout(1200)

		signin_button = self._first_visible([
			CommonSettingsZoomConnectLocators.SIGNIN_BUTTON,
			"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SIGN IN')]",
			"//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CONNECT')]",
		], timeout=5000)

		if signin_button:
			signin_button.click()
			return True

		try:
			self.click_back_arrow()
		except Exception:
			pass
		return False

	def validate_zoom_login_screen(self):
		pages = [self.page] + [p for p in self.page.context.pages if p != self.page]
		for candidate in pages:
			try:
				candidate.locator(CommonSettingsZoomConnectLocators.ZOOM_EMAIL_INPUT).first.wait_for(state="visible", timeout=5000)
				candidate.locator(CommonSettingsZoomConnectLocators.ZOOM_PASSWORD_INPUT).first.wait_for(state="visible", timeout=5000)
				candidate.locator(CommonSettingsZoomConnectLocators.ZOOM_SIGNIN_BUTTON).first.wait_for(state="visible", timeout=5000)
				self.page = candidate
				self.active_page = candidate
				return True
			except Exception:
				continue
		return False

	def enter_zoom_email(self, email):
		field = self.page.locator(CommonSettingsZoomConnectLocators.ZOOM_EMAIL_INPUT).first
		field.wait_for(state="visible", timeout=10000)
		field.click()
		field.press("Control+A")
		field.press("Backspace")
		field.type(email, delay=80)

	def enter_zoom_password(self, password):
		field = self.page.locator(CommonSettingsZoomConnectLocators.ZOOM_PASSWORD_INPUT).first
		field.wait_for(state="visible", timeout=10000)
		field.click()
		field.press("Control+A")
		field.press("Backspace")
		field.type(password, delay=80)

	def click_zoom_signin(self):
		self.page.click(CommonSettingsZoomConnectLocators.ZOOM_SIGNIN_BUTTON)

	def validate_toggle_status(self):
		toggle = self._first_visible([
			CommonSettingsZoomConnectLocators.ZOOMCONNECTION_TOGGLER,
			"//button[contains(@class,'ant-switch')]",
		], timeout=5000)
		try:
			return bool(toggle and toggle.is_visible())
		except Exception:
			return False

	def click_whatsapp_profile_icon(self):
		assert self._settings_panel_visible(timeout=6000), "Settings panel is not open before clicking Notifications"

		# If whatsapp settings content already visible, skip menu click.
		already_open = self._first_visible([
			CommonSettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER,
			CommonSettingsWhatsappNotificationsLocators.WHATSAPP_SECTION,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'WHATSAPP')]",
		], timeout=2500)
		if already_open:
			return

		selectors = [
			CommonSettingsWhatsappNotificationsLocators.NOTIFICATIONS_MENU,
			"//div[contains(@class,'userSettings_menuItem')][.//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTIFICATIONS')]]",
			"//h1[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTIFICATIONS')]/ancestor::div[contains(@class,'userSettings_menuItem')][1]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTIFICATIONS')]",
			"(//div[contains(@class,'userSettings_menuItem')])[2]",
		]
		clicked = self._click_first_visible(selectors, timeout=4000)
		if not clicked:
			clicked = self._click_first_attached(selectors, timeout=4000)

		if not clicked:
			menu_items = self.page.locator("//div[contains(@class,'userSettings_menuItem')]")
			try:
				if menu_items.count() >= 2:
					candidate = menu_items.nth(1)
					candidate.scroll_into_view_if_needed()
					candidate.click(force=True)
					clicked = True
			except Exception:
				pass

		if not clicked:
			# Fallback: directly open a WhatsApp-looking section card.
			clicked = self._click_first_visible([
				"//div[contains(@class,'section-container') and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'WHATSAPP')]",
				"(//div[contains(@class,'section-container')])[1]",
			], timeout=3000)

		if not clicked:
			already_open = self._first_visible([
				CommonSettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER,
				CommonSettingsWhatsappNotificationsLocators.WHATSAPP_SECTION,
				"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'WHATSAPP')]",
			], timeout=2500)
			assert already_open, "Notifications menu is not visible/clickable"

		# Ensure notifications content area is actually open before proceeding.
		content_ready = self._first_visible([
			CommonSettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'WHATSAPP')]",
			"//div[contains(@class,'section-container')]",
		], timeout=5000)
		assert content_ready, "Notifications content did not open"

	def validate_whatsapp_container_section(self):
		container = self._first_visible([
			CommonSettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER,
			"//div[contains(@class,'section-container') and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'WHATS APP')]",
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'WHATSAPP')]",
			"(//div[contains(@class,'section-container')])[1]",
		], timeout=8000)

		if not container:
			# Retry by reopening notifications once.
			self.click_whatsapp_profile_icon()
			container = self._first_visible([
				CommonSettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER,
				"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'WHATSAPP')]",
				"(//div[contains(@class,'section-container')])[1]",
			], timeout=6000)

		assert container and container.is_visible(), "WhatsApp container is not visible"
		container.scroll_into_view_if_needed()
		try:
			container.click(timeout=10000)
		except Exception:
			container.click(timeout=10000, force=True)

	def click_whatsapp_right_arrow(self):
		clicked = self._click_first_visible([
			CommonSettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER_RIGHTARROW,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'WHATSAPP')]/ancestor::*[1]//img[contains(@alt,'right_arrow') or contains(@alt,'arrow')][1]",
		], timeout=4000)
		assert clicked, "WhatsApp right arrow is not visible/clickable"

	def validate_whatsapp_section_and_toggle(self):
		section = self._first_visible([
			CommonSettingsWhatsappNotificationsLocators.WHATSAPP_SECTION,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'WHATSAPP')]",
		], timeout=5000)
		assert section, "WhatsApp section is not visible"

		clicked = self._click_first_visible([
			CommonSettingsWhatsappNotificationsLocators.WHATSAPP_TOGGLEBUTTON,
			"//button[contains(@class,'ant-switch')]",
			"//span[contains(@class,'ant-switch-handle')]",
		], timeout=5000)
		assert clicked, "WhatsApp toggle button is not visible/clickable"

	def click_whatsapp_backbutton(self):
		clicked = self._click_first_visible([
			CommonSettingsWhatsappNotificationsLocators.WHATSAPP_SECTION_BACKBUTTON,
			"//img[contains(@alt,'arrow') and (contains(@alt,'left') or contains(@class,'left_icon'))]",
			"//img[contains(@class,'left_icon')]",
		])
		if not clicked:
			raise AssertionError("WhatsApp section back button not visible")
