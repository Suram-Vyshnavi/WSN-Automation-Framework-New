from pages.base_page import BasePage
from locators.common_locators.common_settings_zoom_connect_locators import CommonSettingsZoomConnectLocators
from locators.common_locators.common_whatsapp_notifications_locators import CommonSettingsWhatsappNotificationsLocators
from locators.faculty_locators.home_locators import HomeLocators
from utils.logger import log
from locators.xpath import UPPER


class CommonSettingsPage(BasePage):
    DEFAULT_TIMEOUT = 1500


    def _settings_panel_visible(self, timeout=1500):
        panel = self.first_visible([
            "//div[contains(@class,'userSettings-container')]",
            "//div[contains(@class,'userSettings_menuItem')]",
            f"//div[contains(@class,'userSettings')]//*[contains({UPPER}, 'ACCOUNTS')]",
            f"//div[contains(@class,'userSettings')]//*[contains({UPPER}, 'NOTIFICATIONS')]",
        ], timeout=timeout)
        return bool(panel)

    def _click_first_attached(self, selectors, timeout=1500):
        for selector in selectors:
            locator = self.page.locator(selector).first
            try:
                locator.wait_for(state="attached", timeout=timeout)
                try:
                    locator.scroll_into_view_if_needed(timeout=2000)
                except Exception as _ignored:
                    log.debug("Optional step in _click_first_attached() did not apply: %s", _ignored)
                locator.click(force=True)
                return True
            except Exception:
                continue
        return False

    def _open_accounts_menu(self, timeout=8000):
        """Open the Accounts (hamburger) dropdown that holds Settings / Messages / Logout."""
        # If the dropdown is already open (Settings item visible), nothing to do.
        if self.first_visible([HomeLocators.DROPDOWN_SETTINGS_ITEM], timeout=1000):
            return True
        return self.click_first_visible([HomeLocators.ACCOUNTS_MENU_TRIGGER], "accounts menu trigger", timeout=timeout)

    def click_zoomconnect_profile_icon(self):
        # Quick readiness check so the click is attempted only after dashboard shell appears.
        self.first_visible([
            HomeLocators.FACULTY_DASHBOARD_CONTAINER,
            HomeLocators.HOME_MENU,
        ], timeout=4000)

        # If already inside settings screen, skip menu open.
        if self._settings_panel_visible(timeout=2500):
            return

        opened = self._open_accounts_menu(timeout=8000)

        if not opened:
            # Previous scenario may have left us deep in a nested screen. Navigate
            # home then retry opening the Accounts menu.
            try:
                self.page.locator(HomeLocators.HOME_MENU).first.click(timeout=3000)
                self.pause(800)
            except Exception as _ignored:
                log.debug("Optional step in click_zoomconnect_profile_icon() did not apply: %s", _ignored)
            opened = self._open_accounts_menu(timeout=5000)

        assert opened or self._settings_panel_visible(timeout=2500), \
            "Accounts menu / profile icon is not visible/clickable"

    def click_settings_menu(self):
        if self._settings_panel_visible(timeout=2500):
            return

        # Ensure the Accounts dropdown is open before clicking the Settings item.
        if not self.first_visible([HomeLocators.DROPDOWN_SETTINGS_ITEM], timeout=1500):
            self._open_accounts_menu(timeout=5000)

        selectors = [
            HomeLocators.DROPDOWN_SETTINGS_ITEM,
            CommonSettingsZoomConnectLocators.SETTINGS_ICON,
            "//*[normalize-space()='Settings']",
        ]
        clicked = self.click_first_visible(selectors, "selectors", timeout=4000)
        if not clicked:
            clicked = self._click_first_attached(selectors, timeout=2000)
        assert clicked, "Settings menu is not visible/clickable"
        assert self._settings_panel_visible(timeout=8000), "Settings panel did not open after clicking settings menu"

    def validate_settings_sections(self):
        assert self._settings_panel_visible(timeout=6000), "Settings sections are not visible"

    def click_back_arrow(self):
        clicked = self.click_first_visible([
            CommonSettingsZoomConnectLocators.BACK_ARROW,
            "//img[contains(@alt,'arrow') and (contains(@alt,'left') or contains(@class,'left_icon'))]",
            "//img[contains(@class,'left_icon')]",
            "//img[contains(@alt,'Go back') or contains(@alt,'go back') or contains(@alt,'back')]",
            "(//img[contains(@class,'wf_image')])[1]",
            "//button[contains(@class,'back') or contains(@aria-label,'back')]",
        ], "back arrow", timeout=5000)
        if clicked:
            self.pause(500)
            return

        if self._settings_panel_visible(timeout=2500):
            return

        try:
            self.page.go_back(wait_until="domcontentloaded", timeout=5000)
            self.pause(800)
        except Exception as _ignored:
            log.debug("Optional step in click_back_arrow() did not apply: %s", _ignored)

        if self._settings_panel_visible(timeout=3000):
            return

        # Try to navigate back to home and then to settings as last resort
        try:
            self.page.locator("//div[@id='Home']").first.click(timeout=3000)
            self.pause(500)
        except Exception as _ignored:
            log.debug("Optional step in click_back_arrow() did not apply: %s", _ignored)

        if self._settings_panel_visible(timeout=1500):
            return

    def click_accounts_menu_zoomconnect(self):
        self.click_required([
            CommonSettingsZoomConnectLocators.ACCOUNTS_MENU,
            f"//*[contains({UPPER}, 'ACCOUNTS')]",
        ], "Accounts menu", timeout=5000)

        self.validate_any_visible([
            CommonSettingsZoomConnectLocators.MEETING_CARD,
            f"//*[contains({UPPER}, 'MEETING')]",
            CommonSettingsZoomConnectLocators.ZOOM_SETTINGS_ARROW,
            f"//*[contains({UPPER}, 'ZOOM')]",
        ], "Meetings/Zoom section", timeout=5000)

    def click_zoom_right_arrow(self):
        # Only treat as already-open when we are inside the Zoom detail screen.
        # Text like 'SIGN IN WITH ZOOM' can appear on the accounts LIST card too,
        # so use only detail-screen specific containers/controls.
        already_open = self.first_visible([
            CommonSettingsZoomConnectLocators.SIGNIN_WITH_ZOOM_SECTION,
            CommonSettingsZoomConnectLocators.ZOOMCONNECTION_TOGGLER,
            CommonSettingsZoomConnectLocators.MEETINGS_CARD,
        ], timeout=1500)
        if already_open:
            log.warning("[ZoomDebug] Zoom detail is already open; skipping right-arrow click")
            return

        selectors = [
            f"//*[contains({UPPER}, 'SIGN IN WITH ZOOM')]/ancestor::div[contains(@class,'section-container') or contains(@class,'zoom-container')][1]//img[contains(@alt,'right_arrow') or contains(@alt,'arrow')][1]",
            f"//*[contains({UPPER}, 'ZOOM')]/ancestor::div[contains(@class,'section-container') or contains(@class,'zoom-container')][1]//img[contains(@alt,'right_arrow') or contains(@alt,'arrow')][1]",
            CommonSettingsZoomConnectLocators.ZOOM_SETTINGS_ARROW,
            f"//*[contains({UPPER}, 'ZOOM')]/ancestor::*[1]//img[contains(@alt,'right_arrow') or contains(@alt,'arrow')][1]",
            "(//img[contains(@alt,'right_arrow') or contains(@alt,'arrow-right')])[1]",
        ]
        clicked = self.click_first_visible(selectors, "selectors", timeout=4000)
        if not clicked:
            clicked = self._click_first_attached(selectors, timeout=4000)
        if clicked:
            log.info("[ZoomDebug] Clicked Zoom right-arrow/open control")

        if not clicked:
            # Fallback: open first settings card directly when arrow is not a separate clickable control.
            clicked = self.click_first_visible([
                "(//div[contains(@class,'section-container')])[1]",
                "(//div[contains(@class,'zoom-container')])[1]",
            ], timeout=3000)

        if not clicked:
            already_open = self.first_visible([
                CommonSettingsZoomConnectLocators.SIGNIN_WITH_ZOOM_SECTION,
                CommonSettingsZoomConnectLocators.MEETINGS_CARD,
                CommonSettingsZoomConnectLocators.ZOOMCONNECTION_TOGGLER,
                CommonSettingsZoomConnectLocators.SIGNIN_BUTTON,
            ], timeout=2500)
            if already_open:
                log.info("[ZoomDebug] Zoom detail became visible through fallback path")
            assert already_open, "Zoom right arrow is not visible/clickable"

    def validate_delinked_popup(self):
        popup = self.page.locator(CommonSettingsZoomConnectLocators.DELINKED_POPUP).first
        try:
            popup.wait_for(state="visible", timeout=3000)
            self.click(CommonSettingsZoomConnectLocators.DELINKED_CLOSEICON, "delinked closeicon")
        except Exception as _ignored:
            log.debug("Optional step in validate_delinked_popup() did not apply: %s", _ignored)

    def validate_signin_section_and_toggle(self):
        self.validate_any_visible([
            CommonSettingsZoomConnectLocators.SIGNIN_WITH_ZOOM_SECTION,
            f"//*[contains({UPPER}, 'SIGN IN WITH ZOOM')]",
        ], "Sign in with Zoom section", timeout=5000)

        clicked = self.click_first_visible([
            CommonSettingsZoomConnectLocators.ZOOMCONNECTION_TOGGLER,
            "//button[@role='switch']",
            "//button[contains(@class,'switch') or contains(@class,'toggle')]",
            "//button[contains(@class,'ant-switch')]",
            "//span[contains(@class,'ant-switch')]",
        ], "zoomconnection toggler", timeout=5000)
        if clicked:
            return

        # Some accounts render Sign In/Meetings/Disconnect directly without a visible toggle.
        self.validate_any_visible([
            CommonSettingsZoomConnectLocators.SIGNIN_BUTTON,
            CommonSettingsZoomConnectLocators.MEETINGS_CARD,
            f"//button[contains({UPPER}, 'DISCONNECT')]",
            f"//*[contains({UPPER}, 'SIGN IN')]",
            f"//*[contains({UPPER}, 'MEETINGS')]",
            f"//*[contains({UPPER}, 'CONNECTED')]",
        ], "Zoom toggle button", timeout=4000)

    def navigate_meetings_and_click_signin(self):
        self.validate_any_visible([
            CommonSettingsZoomConnectLocators.MEETINGS_CARD,
            f"//*[contains({UPPER}, 'MEETINGS')]",
        ], "Meetings card", timeout=12000)

        # If account is already connected, disconnect first so Sign In flow becomes available.
        disconnect_button = self.first_visible([
            f"//button[contains({UPPER}, 'DISCONNECT')]",
        ], timeout=3000)
        if disconnect_button:
            disconnect_button.click()
            # Handle optional confirmation dialogs.
            self.click_first_visible([
                f"//button[contains({UPPER}, 'CONFIRM')]",
                f"//button[contains({UPPER}, 'YES')]",
                "//button[contains(@class,'ant-btn-primary')]",
            ], timeout=2500)
            self.pause(1200)

        signin_button = self.first_visible([
            CommonSettingsZoomConnectLocators.SIGNIN_BUTTON,
            f"//button[contains({UPPER}, 'SIGN IN')]",
            f"//button[contains({UPPER}, 'CONNECT')]",
        ], timeout=5000)

        if signin_button:
            signin_button.click()
            return True

        try:
            self.click_back_arrow()
        except Exception as _ignored:
            log.debug("Optional step in navigate_meetings_and_click_signin() did not apply: %s", _ignored)
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
        self.click(CommonSettingsZoomConnectLocators.ZOOM_SIGNIN_BUTTON, "zoom signin button")

    def validate_toggle_status(self):
        toggle = self.first_visible([
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
        already_open = self.first_visible([
            CommonSettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER,
            CommonSettingsWhatsappNotificationsLocators.WHATSAPP_SECTION,
            f"//*[contains({UPPER}, 'WHATSAPP')]",
        ], timeout=2500)
        if already_open:
            return

        selectors = [
            CommonSettingsWhatsappNotificationsLocators.NOTIFICATIONS_MENU,
            f"//div[contains(@class,'userSettings_menuItem')][.//*[contains({UPPER}, 'NOTIFICATIONS')]]",
            f"//h1[contains({UPPER}, 'NOTIFICATIONS')]/ancestor::div[contains(@class,'userSettings_menuItem')][1]",
            f"//*[contains({UPPER}, 'NOTIFICATIONS')]",
            "(//div[contains(@class,'userSettings_menuItem')])[2]",
        ]
        clicked = self.click_first_visible(selectors, "selectors", timeout=4000)
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
            except Exception as _ignored:
                log.debug("Optional step in click_whatsapp_profile_icon() did not apply: %s", _ignored)

        if not clicked:
            # Fallback: directly open a WhatsApp-looking section card.
            clicked = self.click_first_visible([
                f"//div[contains(@class,'section-container') and contains({UPPER}, 'WHATSAPP')]",
                "(//div[contains(@class,'section-container')])[1]",
            ], timeout=3000)

        if not clicked:
            self.validate_any_visible([
                CommonSettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER,
                CommonSettingsWhatsappNotificationsLocators.WHATSAPP_SECTION,
                f"//*[contains({UPPER}, 'WHATSAPP')]",
            ], "Notifications menu", timeout=2500)

        # Ensure notifications content area is actually open before proceeding.
        self.validate_any_visible([
            CommonSettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER,
            f"//*[contains({UPPER}, 'WHATSAPP')]",
            "//div[contains(@class,'section-container')]",
        ], "Notifications content did not open", timeout=5000)

    def validate_whatsapp_container_section(self):
        container = self.first_visible([
            CommonSettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER,
            f"//div[contains(@class,'section-container') and contains({UPPER}, 'WHATS APP')]",
            f"//*[contains({UPPER}, 'WHATSAPP')]",
            "(//div[contains(@class,'section-container')])[1]",
        ], timeout=8000)

        if not container:
            # Retry by reopening notifications once.
            self.click_whatsapp_profile_icon()
            container = self.first_visible([
                CommonSettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER,
                f"//*[contains({UPPER}, 'WHATSAPP')]",
                "(//div[contains(@class,'section-container')])[1]",
            ], timeout=6000)

        assert container and container.is_visible(), "WhatsApp container is not visible"
        container.scroll_into_view_if_needed()
        try:
            container.click(timeout=10000)
        except Exception:
            container.click(timeout=10000, force=True)

    def click_whatsapp_right_arrow(self):
        self.click_required([
            CommonSettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER_RIGHTARROW,
            f"//*[contains({UPPER}, 'WHATSAPP')]/ancestor::*[1]//img[contains(@alt,'right_arrow') or contains(@alt,'arrow')][1]",
        ], "WhatsApp right arrow", timeout=4000)

    def validate_whatsapp_section_and_toggle(self):
        self.validate_any_visible([
            CommonSettingsWhatsappNotificationsLocators.WHATSAPP_SECTION,
            f"//*[contains({UPPER}, 'WHATSAPP')]",
        ], "WhatsApp section", timeout=5000)

        self.click_required([
            CommonSettingsWhatsappNotificationsLocators.WHATSAPP_TOGGLEBUTTON,
            "//button[contains(@class,'ant-switch')]",
            "//span[contains(@class,'ant-switch-handle')]",
        ], "WhatsApp toggle button", timeout=5000)

    def click_whatsapp_backbutton(self):
        clicked = self.click_first_visible([
            CommonSettingsWhatsappNotificationsLocators.WHATSAPP_SECTION_BACKBUTTON,
            "//img[contains(@alt,'arrow') and (contains(@alt,'left') or contains(@class,'left_icon'))]",
            "//img[contains(@class,'left_icon')]",
        ], "whatsapp section backbutton")
        if not clicked:
            raise AssertionError("WhatsApp section back button not visible")
