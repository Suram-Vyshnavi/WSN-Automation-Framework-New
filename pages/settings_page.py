from pages.base_page import BasePage
from locators.student_locators.Settings_ZoomConnect_locators import SettingsZoomConnectLocators
from locators.student_locators.Settings_DeleteAccount_locators import SettingsDeleteAccountLocators
from locators.student_locators.Settings_WhatsappNotifications_locators import SettingsWhatsappNotificationsLocators

class SettingsPage(BasePage):

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
        self.page.locator(SettingsZoomConnectLocators.BACK_ARROW).wait_for(state="visible", timeout=10000)
        self.page.click(SettingsZoomConnectLocators.BACK_ARROW)

    # --- ZoomConnect Methods ---
    def click_accounts_menu_zoomconnect(self):
        self.page.locator(SettingsZoomConnectLocators.ACCOUNTS_MENU).wait_for(state="visible", timeout=10000)
        self.page.click(SettingsZoomConnectLocators.ACCOUNTS_MENU)
        self.page.locator(SettingsZoomConnectLocators.MEETING_CARD).wait_for(state="visible", timeout=10000)

    def click_zoom_right_arrow(self):
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
        signin_button = self.page.locator(SettingsZoomConnectLocators.SIGNIN_BUTTON).first

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
        self.page.fill(SettingsZoomConnectLocators.ZOOM_EMAIL_INPUT, email)

    def enter_zoom_password(self, password):
        self.page.fill(SettingsZoomConnectLocators.ZOOM_PASSWORD_INPUT, password)

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
        self.page.locator(SettingsZoomConnectLocators.MEETINGS_DISCONNECT_CONTAINER).wait_for(state="visible", timeout=10000)
        assert self.page.locator(SettingsZoomConnectLocators.MEETINGS_DISCONNECT_CONTAINER).is_visible()

    def click_disconnect_button(self):
        self.page.locator(SettingsZoomConnectLocators.MEETINGS_DISCONNECT_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.click(SettingsZoomConnectLocators.MEETINGS_DISCONNECT_BUTTON)

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
        self.page.locator(SettingsDeleteAccountLocators.DELETE_ACCOUNT_CLOSEICON).wait_for(state="visible", timeout=10000)
        self.page.click(SettingsDeleteAccountLocators.DELETE_ACCOUNT_CLOSEICON)

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
        self.page.locator(SettingsWhatsappNotificationsLocators.WHATSAPP_SECTION_BACKBUTTON).wait_for(state="visible", timeout=10000)
        self.page.click(SettingsWhatsappNotificationsLocators.WHATSAPP_SECTION_BACKBUTTON)
