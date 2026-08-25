from locators.student_locators.settings_delete_account_locators import SettingsDeleteAccountLocators
from locators.student_locators.settings_whatsapp_notifications_locators import SettingsWhatsappNotificationsLocators
from locators.student_locators.settings_zoom_connect_locators import SettingsZoomConnectLocators
from pages.base_page import BasePage, LONG_TIMEOUT, SHORT_TIMEOUT

ACCOUNTS_MENU_FALLBACK = "//button[@aria-label='Accounts menu']"
SETTINGS_MENU_FALLBACK = "//p[contains(normalize-space(),'Settings')]"
ACCOUNTS_TAB_FALLBACK = "//div[contains(@class,'userSettings_menuItem')][.//h1[normalize-space()='Accounts']]"


class SettingsPage(BasePage):
    """Student Settings: Zoom Connect, Delete Account and WhatsApp notifications."""

    def _ensure_back_on_app(self):
        """Come back from an external zoom.us page into the app's settings view."""
        for _ in range(3):
            if "zoom.us" not in self.current_url().lower():
                return
            self.go_back()
            self.pause(1000)

    # ------------------------------------------------------------------
    # Shared settings navigation
    # ------------------------------------------------------------------
    def click_zoomconnect_profile_icon(self):
        self.click(SettingsZoomConnectLocators.PROFILE_ICON, "profile icon")

    def click_account_menu_from_home(self):
        self.click_required([
            SettingsZoomConnectLocators.ACCOUNTS_MENU_ICON,
            ACCOUNTS_MENU_FALLBACK,
        ], "Account menu", timeout=15000)

    def click_settings_menu(self):
        self.click_required([
            SettingsZoomConnectLocators.SETTINGS_ICON,
            SETTINGS_MENU_FALLBACK,
        ], "Settings menu", timeout=15000)

    def validate_settings_sections(self):
        self.validate_any_visible([
            SettingsZoomConnectLocators.ACCOUNTS_SECTION_TITLE,
            SettingsZoomConnectLocators.ACCOUNTS_MENU,
            "//h1[normalize-space()='Accounts']",
            SettingsZoomConnectLocators.MEETING_CARD,
            SettingsZoomConnectLocators.ZOOM_SETTINGS_ARROW,
            SettingsDeleteAccountLocators.DELETE_ACCOUNT,
        ], "Settings sections", timeout=15000)

    def click_back_arrow(self):
        self.click(SettingsZoomConnectLocators.BACK_ARROW, "back arrow")

    # ------------------------------------------------------------------
    # Zoom Connect
    # ------------------------------------------------------------------
    def click_accounts_menu_zoomconnect(self):
        # Some builds keep Accounts selected by default, so the click is optional.
        self.click_first_visible([
            ACCOUNTS_TAB_FALLBACK,
            SettingsZoomConnectLocators.ACCOUNTS_MENU,
        ], "Accounts tab", timeout=6000)
        self.validate_visible(SettingsZoomConnectLocators.MEETING_CARD, "Accounts meetings card")

    def click_zoom_right_arrow(self):
        self.click(SettingsZoomConnectLocators.ZOOM_SETTINGS_ARROW, "Zoom settings arrow")

    def validate_delinked_popup(self):
        """Close the 'Zoom account delinked' popup when it is shown."""
        self.dismiss_if_present([SettingsZoomConnectLocators.DELINKED_CLOSEICON],
                                "Zoom delinked popup", timeout=3000)

    def validate_signin_section_and_toggle(self):
        self.validate_visible(SettingsZoomConnectLocators.SIGNIN_WITH_ZOOM_SECTION,
                              "Sign in with Zoom section")
        self.click(SettingsZoomConnectLocators.ZOOMCONNECTION_TOGGLER, "Zoom connection toggle")

    def navigate_meetings_and_click_signin(self):
        """Open the Meetings card. False when the account is already connected."""
        self.validate_visible(SettingsZoomConnectLocators.MEETINGS_CARD, "Meetings card")
        if self.click_first_visible([SettingsZoomConnectLocators.SIGNIN_BUTTON],
                                    "Zoom Sign In button", timeout=SHORT_TIMEOUT):
            return True
        self.click_back_arrow()
        return False

    def validate_zoom_login_screen(self):
        """True when the zoom.us login form rendered."""
        return all(self.is_visible(locator) for locator in (
            SettingsZoomConnectLocators.ZOOM_EMAIL_INPUT,
            SettingsZoomConnectLocators.ZOOM_PASSWORD_INPUT,
            SettingsZoomConnectLocators.ZOOM_SIGNIN_BUTTON,
        ))

    def enter_zoom_email(self, email):
        self.enter_text(SettingsZoomConnectLocators.ZOOM_EMAIL_INPUT, email, "Zoom email")

    def enter_zoom_password(self, password):
        self.enter_text(SettingsZoomConnectLocators.ZOOM_PASSWORD_INPUT, password,
                        "Zoom password", sensitive=True)

    def click_zoom_signin(self):
        self.click(SettingsZoomConnectLocators.ZOOM_SIGNIN_BUTTON, "Zoom Sign In button")

    def validate_toggle_status(self):
        """True when the Zoom connection toggle is back on screen."""
        self._ensure_back_on_app()
        return self.is_visible(SettingsZoomConnectLocators.ZOOMCONNECTION_TOGGLER)

    def validate_disconnect_section(self):
        self._ensure_back_on_app()
        self.validate_visible(SettingsZoomConnectLocators.MEETINGS_CARD, "Meetings card")
        # In some builds the Disconnect button only appears after toggling.
        if self.count(SettingsZoomConnectLocators.MEETINGS_DISCONNECT_BUTTON) == 0:
            self.click_first_visible([SettingsZoomConnectLocators.ZOOMCONNECTION_TOGGLER],
                                     "Zoom connection toggle", timeout=SHORT_TIMEOUT)
        self.validate_visible(SettingsZoomConnectLocators.MEETINGS_DISCONNECT_BUTTON,
                              "Zoom Disconnect button")

    def click_disconnect_button(self):
        self._ensure_back_on_app()
        self.click(SettingsZoomConnectLocators.MEETINGS_DISCONNECT_BUTTON, "Zoom Disconnect button")

    # ------------------------------------------------------------------
    # Delete Account
    # ------------------------------------------------------------------
    def click_delete_account_profile_icon(self):
        self.click(SettingsDeleteAccountLocators.DELETE_ACCOUNT, "Delete Account section")

    def click_delete_account_arrow(self):
        self.click(SettingsDeleteAccountLocators.DELETE_ACCOUNT_ARROW, "Delete Account right arrow")

    def validate_delete_account_popup_and_getotp(self):
        """Open the Delete Account popup and request the OTP."""
        self.validate_visible(SettingsDeleteAccountLocators.DELETE_ACCOUNT_POPUP,
                              "Delete Account popup")
        self.click_required([
            SettingsDeleteAccountLocators.DELETE_ACCOUNT_GETOTP,
            "//div[contains(@class,'ant-modal')]//button[contains(@class,'unified-next-button') "
            "or contains(@class,'ant-btn-primary')]",
        ], "Get OTP button", timeout=SHORT_TIMEOUT)
        self.validate_visible(SettingsDeleteAccountLocators.DELETE_ACCOUNT_OTP_INPUT,
                              "Delete Account OTP input", timeout=LONG_TIMEOUT)

    def click_delete_account_backarrow(self):
        self.click(SettingsDeleteAccountLocators.DELETE_ACCOUNT_BACKARROW,
                   "Delete Account back arrow")

    def click_delete_account_closeicon(self):
        self.click(SettingsDeleteAccountLocators.DELETE_ACCOUNT_CLOSEICON,
                   "Delete Account close icon")

    # ------------------------------------------------------------------
    # WhatsApp notifications
    # ------------------------------------------------------------------
    def click_whatsapp_profile_icon(self):
        self.click(SettingsWhatsappNotificationsLocators.NOTIFICATIONS_MENU, "Notifications menu")

    def validate_whatsapp_container_section(self):
        self.validate_visible(SettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER,
                              "WhatsApp container section")
        self.click(SettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER,
                   "WhatsApp container section")

    def click_whatsapp_right_arrow(self):
        self.click(SettingsWhatsappNotificationsLocators.WHATSAPP_CONTAINER_RIGHTARROW,
                   "WhatsApp right arrow")

    def validate_whatsapp_section_and_toggle(self):
        self.validate_visible(SettingsWhatsappNotificationsLocators.WHATSAPP_SECTION,
                              "WhatsApp section")
        self.click(SettingsWhatsappNotificationsLocators.WHATSAPP_TOGGLEBUTTON,
                   "WhatsApp toggle button")

    def click_whatsapp_backbutton(self):
        self.click(SettingsWhatsappNotificationsLocators.WHATSAPP_SECTION_BACKBUTTON,
                   "WhatsApp section back arrow")
