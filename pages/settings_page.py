from pages.base_page import BasePage
from locators.student_locators.Settings_ZoomConnect_locators import SettingsZoomConnectLocators
from locators.student_locators.Settings_DeleteAccount_locators import SettingsDeleteAccountLocators
from locators.student_locators.Settings_WhatsappNotifications_locators import SettingsWhatsappNotificationsLocators

class SettingsPage(BasePage):

    def _click_first_visible(self, selectors, timeout=10000):
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

    # --- Common Methods ---
    def click_zoomconnect_profile_icon(self):
        self.page.locator(SettingsZoomConnectLocators.PROFILE_ICON).wait_for(state="visible", timeout=10000)
        self.page.click(SettingsZoomConnectLocators.PROFILE_ICON)

    def click_settings_menu(self):
        self.page.locator(SettingsZoomConnectLocators.SETTINGS_ICON).wait_for(state="visible", timeout=10000)
        self.page.click(SettingsZoomConnectLocators.SETTINGS_ICON)

    def validate_settings_sections(self):
        self.page.locator(SettingsZoomConnectLocators.ACCOUNTS_MENU).wait_for(state="visible", timeout=10000)
        assert self.page.locator(SettingsZoomConnectLocators.ACCOUNTS_MENU).is_visible()

    def click_back_arrow(self):
        clicked = self._click_first_visible([
            SettingsZoomConnectLocators.BACK_ARROW,
            "//img[contains(@alt,'arrow') and (contains(@alt,'left') or contains(@class,'left_icon'))]",
            "//img[contains(@class,'left_icon')]",
        ])
        if not clicked:
            raise AssertionError("Back arrow not visible in settings flow")

    # --- ZoomConnect Methods ---
    def click_accounts_menu_zoomconnect(self):
        self.page.locator(SettingsZoomConnectLocators.ACCOUNTS_MENU).wait_for(state="visible", timeout=10000)
        self.page.click(SettingsZoomConnectLocators.ACCOUNTS_MENU)
        self.page.locator(SettingsZoomConnectLocators.MEETING_CARD).wait_for(state="visible", timeout=10000)

    def click_zoom_right_arrow(self):
        # Only treat as already-open when inside Zoom detail screen (not accounts list).
        signed_in_section = self.page.locator(SettingsZoomConnectLocators.SIGNIN_WITH_ZOOM_SECTION).first
        try:
            signed_in_section.wait_for(state="visible", timeout=1500)
            return  # Already on Zoom detail screen
        except Exception:
            pass
        self.page.locator(SettingsZoomConnectLocators.ZOOM_SETTINGS_ARROW).wait_for(state="visible", timeout=10000)
        self.page.click(SettingsZoomConnectLocators.ZOOM_SETTINGS_ARROW)

    def validate_delinked_popup(self):
        popup = self.page.locator(SettingsZoomConnectLocators.DELINKED_POPUP).first
        try:
            popup.wait_for(state="visible", timeout=3000)
            self.page.click(SettingsZoomConnectLocators.DELINKED_CLOSEICON)
        except Exception:
            pass

    def validate_signin_section_and_toggle(self):
        self.page.locator(SettingsZoomConnectLocators.SIGNIN_WITH_ZOOM_SECTION).wait_for(state="visible", timeout=10000)
        self.page.click(SettingsZoomConnectLocators.ZOOMCONNECTION_TOGGLER)

    def navigate_meetings_and_click_signin(self):
        self.page.locator(SettingsZoomConnectLocators.MEETINGS_CARD).wait_for(state="visible", timeout=10000)
        disconnect_button = self.page.locator("//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'DISCONNECT')]").first
        try:
            disconnect_button.wait_for(state="visible", timeout=3000)
            disconnect_button.click()
            for selector in [
                "//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CONFIRM')]",
                "//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'YES')]",
                "//button[contains(@class,'ant-btn-primary')]",
            ]:
                confirm = self.page.locator(selector).first
                try:
                    confirm.wait_for(state="visible", timeout=1200)
                    confirm.click()
                    break
                except Exception:
                    continue
            self.page.wait_for_timeout(1200)
        except Exception:
            pass

        signin_button = self.page.locator(
            "//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SIGN IN') or contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CONNECT')]"
        ).first

        if signin_button.count() > 0 and signin_button.is_visible():
            signin_button.click()
            return True

        self.click_back_arrow()
        return False

    def validate_zoom_login_screen(self):
        try:
            self.page.locator(SettingsZoomConnectLocators.ZOOM_EMAIL_INPUT).wait_for(state="visible", timeout=10000)
            self.page.locator(SettingsZoomConnectLocators.ZOOM_PASSWORD_INPUT).wait_for(state="visible", timeout=10000)
            self.page.locator(SettingsZoomConnectLocators.ZOOM_SIGNIN_BUTTON).wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False

    def enter_zoom_email(self, email):
        field = self.page.locator(SettingsZoomConnectLocators.ZOOM_EMAIL_INPUT).first
        field.wait_for(state="visible", timeout=10000)
        field.click()
        field.press("Control+A")
        field.press("Backspace")
        field.type(email, delay=80)

    def enter_zoom_password(self, password):
        field = self.page.locator(SettingsZoomConnectLocators.ZOOM_PASSWORD_INPUT).first
        field.wait_for(state="visible", timeout=10000)
        field.click()
        field.press("Control+A")
        field.press("Backspace")
        field.type(password, delay=80)

    def click_zoom_signin(self):
        self.page.click(SettingsZoomConnectLocators.ZOOM_SIGNIN_BUTTON)

    def validate_toggle_status(self):
        toggle = self.page.locator(SettingsZoomConnectLocators.ZOOMCONNECTION_TOGGLER).first
        try:
            toggle.wait_for(state="visible", timeout=5000)
            return toggle.is_visible()
        except Exception:
            return False

    def validate_disconnect_section(self):
        candidates = [
            SettingsZoomConnectLocators.MEETINGS_DISCONNECT_CONTAINER,
            "//div[contains(@class,'zoom-container') and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'MEETINGS')]",
            "//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'DISCONNECT')]",
        ]
        visible = False
        for selector in candidates:
            loc = self.page.locator(selector).first
            try:
                loc.wait_for(state="visible", timeout=5000)
                visible = True
                break
            except Exception:
                continue
        assert visible, "Disconnect section not visible"

    def click_disconnect_button(self):
        clicked = self._click_first_visible([
            SettingsZoomConnectLocators.MEETINGS_DISCONNECT_BUTTON,
            "//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'DISCONNECT')]",
            "//button[contains(@class,'zoom-button')]",
        ])
        if not clicked:
            raise AssertionError("Disconnect button not visible")

    # --- Delete Account Methods ---
    def click_delete_account_profile_icon(self):
        self.page.locator(SettingsDeleteAccountLocators.DELETE_ACCOUNT).wait_for(state="visible", timeout=10000)
        self.page.click(SettingsDeleteAccountLocators.DELETE_ACCOUNT)

    def click_delete_account_arrow(self):
        arrow = self.page.locator(SettingsDeleteAccountLocators.DELETE_ACCOUNT_ARROW).first
        arrow.wait_for(state="visible", timeout=10000)
        arrow.scroll_into_view_if_needed()
        try:
            arrow.click(timeout=10000)
        except Exception:
            arrow.click(timeout=10000, force=True)

    def validate_delete_account_popup_and_getotp(self):
        popup = self.page.locator(SettingsDeleteAccountLocators.DELETE_ACCOUNT_POPUP).first
        popup.wait_for(state="visible", timeout=10000)

        candidate_locators = [
            self.page.locator(SettingsDeleteAccountLocators.DELETE_ACCOUNT_GETOTP),
            popup.locator("//button[contains(@class,'unified-next-button') or contains(@class,'ant-btn-primary')]")
        ]

        clicked = False
        for candidate in candidate_locators:
            button = candidate.first
            try:
                button.wait_for(state="visible", timeout=3000)
                button.scroll_into_view_if_needed()
                try:
                    button.click(timeout=10000)
                except Exception:
                    button.click(timeout=10000, force=True)
                clicked = True
                break
            except Exception:
                continue

        if not clicked:
            raise AssertionError("OTP button not found or not clickable in Delete Account popup")

        self.page.locator(SettingsDeleteAccountLocators.DELETE_ACCOUNT_OTP_INPUT).first.wait_for(state="visible", timeout=20000)

    def click_delete_account_backarrow(self):
        self.page.locator(SettingsDeleteAccountLocators.DELETE_ACCOUNT_BACKARROW).wait_for(state="visible", timeout=10000)
        self.page.click(SettingsDeleteAccountLocators.DELETE_ACCOUNT_BACKARROW)

    def click_delete_account_closeicon(self):
        clicked = self._click_first_visible([
            SettingsDeleteAccountLocators.DELETE_ACCOUNT_CLOSEICON,
            "//span[@aria-label='close']",
            "//button[@aria-label='Close']",
            "//img[contains(@alt,'close') or contains(@class,'close')]",
        ])
        if not clicked:
            raise AssertionError("Delete-account close icon not visible")

    # --- WhatsApp Notifications Methods ---
    def click_whatsapp_profile_icon(self):
        self.page.locator(SettingsWhatsappNotificationsLocators.NOTIFICATIONS_MENU).wait_for(state="visible", timeout=10000)
        self.page.click(SettingsWhatsappNotificationsLocators.NOTIFICATIONS_MENU)

    def validate_whatsapp_container_section(self):
        container = self.page.locator(SettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER).first
        container.wait_for(state="visible", timeout=10000)
        assert container.is_visible()
        container.scroll_into_view_if_needed()
        try:
            container.click(timeout=10000)
        except Exception:
            container.click(timeout=10000, force=True)

    def click_whatsapp_right_arrow(self):
        self.page.locator(SettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER_RIGHTARROW).wait_for(state="visible", timeout=10000)
        self.page.click(SettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER_RIGHTARROW)

    def validate_whatsapp_section_and_toggle(self):
        self.page.locator(SettingsWhatsappNotificationsLocators.WHATSAPP_SECTION).wait_for(state="visible", timeout=10000)
        self.page.click(SettingsWhatsappNotificationsLocators.WHATSAPP_TOGGLEBUTTON)

    def click_whatsapp_backbutton(self):
        clicked = self._click_first_visible([
            SettingsWhatsappNotificationsLocators.WHATSAPP_SECTION_BACKBUTTON,
            "//img[contains(@alt,'arrow') and (contains(@alt,'left') or contains(@class,'left_icon'))]",
            "//img[contains(@class,'left_icon')]",
        ])
        if not clicked:
            raise AssertionError("WhatsApp section back button not visible")
