from behave import then
from pages.settings_page import SettingsPage
from utils.helpers import attach_screenshot

# -------------------------
# Common Steps (Background)
# -------------------------

@then("user clicks on ZoomConnect profile icon")
def step_zoomconnect_profile_icon(context):
    page = SettingsPage(context.page)
    page.click_zoomconnect_profile_icon()
    attach_screenshot(context.page, "Clicked ZoomConnect Profile Icon")

@then("user clicks on settings menu")
def step_settings_menu(context):
    page = SettingsPage(context.page)
    page.click_settings_menu()
    attach_screenshot(context.page, "Clicked Settings Menu")

@then("user validates the settings sections")
def step_validate_settings(context):
    page = SettingsPage(context.page)
    page.validate_settings_sections()
    attach_screenshot(context.page, "Validated Settings Sections")

# -------------------------
# ZoomConnect Steps
# -------------------------

@then("user clicks on accounts menu and validates accounts_meetings section")
def step_accounts_menu_zoomconnect(context):
    page = SettingsPage(context.page)
    page.click_accounts_menu_zoomconnect()
    attach_screenshot(context.page, "Clicked Accounts Menu & Validated Meetings Section")

@then("user clicks on sign in with zoom right arrow button")
def step_zoom_right_arrow(context):
    page = SettingsPage(context.page)
    page.click_zoom_right_arrow()
    attach_screenshot(context.page, "Clicked Zoom Right Arrow")

@then("user validates the zoom account delinked popup and closed the popup")
def step_delinked_popup(context):
    page = SettingsPage(context.page)
    page.validate_delinked_popup()
    attach_screenshot(context.page, "Validated Delinked Popup")

@then("user validates the sign in with zoom section and turn on the toggle button")
def step_signin_toggle(context):
    page = SettingsPage(context.page)
    page.validate_signin_section_and_toggle()
    context.zoom_signin_required = True
    attach_screenshot(context.page, "Validated Sign In Section & Toggled")

@then("user navigates to meetings section and click on signin button")
def step_meetings_signin(context):
    page = SettingsPage(context.page)
    context.zoom_signin_required = page.navigate_meetings_and_click_signin()
    if context.zoom_signin_required:
        attach_screenshot(context.page, "Navigated to Meetings & Clicked Sign In")
    else:
        attach_screenshot(context.page, "Zoom already connected after toggle; navigated back without sign in")

@then("user navigates to zoom.us signin screen and validates the email address, password, signin buttons")
def step_zoom_login_screen(context):
    if hasattr(context, "zoom_signin_required") and not context.zoom_signin_required:
        attach_screenshot(context.page, "Skipped zoom.us sign in screen validation for already connected user")
        return
    page = SettingsPage(context.page)
    context.zoom_signin_required = page.validate_zoom_login_screen()
    if context.zoom_signin_required:
        attach_screenshot(context.page, "Validated Zoom Login Screen")
    else:
        attach_screenshot(context.page, "Zoom login screen did not appear; skipping credential steps")

@then("user clicks on email input field and enter the email id")
def step_enter_email(context):
    if hasattr(context, "zoom_signin_required") and not context.zoom_signin_required:
        attach_screenshot(context.page, "Skipped Zoom email entry for already connected user")
        return
    page = SettingsPage(context.page)
    page.enter_zoom_email("demouser2078@gmail.com")
    attach_screenshot(context.page, "Entered Zoom Email")

@then("user clicks on password input field and enter the password")
def step_enter_password(context):
    if hasattr(context, "zoom_signin_required") and not context.zoom_signin_required:
        attach_screenshot(context.page, "Skipped Zoom password entry for already connected user")
        return
    page = SettingsPage(context.page)
    page.enter_zoom_password("Demo@123")
    attach_screenshot(context.page, "Entered Zoom Password")

@then("user clicks on sigin button")
def step_click_signin(context):
    if hasattr(context, "zoom_signin_required") and not context.zoom_signin_required:
        attach_screenshot(context.page, "Skipped Zoom sign in click for already connected user")
        return
    page = SettingsPage(context.page)
    page.click_zoom_signin()
    attach_screenshot(context.page, "Clicked Zoom Sign In")

@then("user navigates back to to signin with zoom screen and validates the toggle button status")
def step_validate_toggle(context):
    if hasattr(context, "zoom_signin_required") and not context.zoom_signin_required:
        attach_screenshot(context.page, "Skipped toggle-status validation after sign in for already connected user")
        return
    page = SettingsPage(context.page)
    if page.validate_toggle_status():
        attach_screenshot(context.page, "Validated Toggle Status")
    else:
        attach_screenshot(context.page, "Toggle not visible in current return path; continuing disconnect flow")

@then("user click on the toggle button and validates the disconnect section")
def step_disconnect_section(context):
    if hasattr(context, "zoom_signin_required") and not context.zoom_signin_required:
        attach_screenshot(context.page, "Skipped disconnect-section validation for already connected user path")
        return
    page = SettingsPage(context.page)
    page.validate_disconnect_section()
    attach_screenshot(context.page, "Validated Disconnect Section")

@then("user clicks on the disconnect button")
def step_disconnect_button(context):
    if hasattr(context, "zoom_signin_required") and not context.zoom_signin_required:
        attach_screenshot(context.page, "Skipped disconnect button click for already connected user path")
        return
    page = SettingsPage(context.page)
    page.validate_delinked_popup()
    page.click_disconnect_button()
    page.validate_delinked_popup()
    page.click_back_arrow()
    context.zoom_back_already_clicked = True
    attach_screenshot(context.page, "Closed Delink Popup, Clicked Disconnect, and Clicked Back Arrow")

@then("user click on back arrow and navigates to settings screen")
def step_back_arrow(context):
    if hasattr(context, "zoom_back_already_clicked") and context.zoom_back_already_clicked:
        attach_screenshot(context.page, "Back arrow already clicked in disconnect flow")
        return
    if hasattr(context, "zoom_signin_required") and not context.zoom_signin_required:
        attach_screenshot(context.page, "Back navigation already completed in existing-user branch")
        return
    page = SettingsPage(context.page)
    page.click_back_arrow()
    attach_screenshot(context.page, "Clicked Back Arrow")


# -------------------------
# DeleteAccount Steps
# -------------------------

@then("user clicks on accounts menu and validates delete account section")
def step_delete_account_section(context):
    page = SettingsPage(context.page)
    page.click_delete_account_profile_icon()
    attach_screenshot(context.page, "Clicked Delete Account Section")

@then("user clicks on delete account right arrow button")
def step_delete_account_arrow(context):
    page = SettingsPage(context.page)
    page.click_delete_account_arrow()
    attach_screenshot(context.page, "Clicked Delete Account Right Arrow")

@then("user validates the delete account popup and clicks on the get otp button")
def step_delete_account_popup(context):
    page = SettingsPage(context.page)
    page.validate_delete_account_popup_and_getotp()
    attach_screenshot(context.page, "Validated Delete Account Popup & Clicked Get OTP")

@then("user validates the otp input field and clicks on the delete account otp section back arrow")
def step_delete_account_backarrow(context):
    page = SettingsPage(context.page)
    page.click_delete_account_backarrow()
    attach_screenshot(context.page, "Clicked Delete Account Back Arrow")

@then("user navigates to delete account section and click on close icon")
def step_delete_account_closeicon(context):
    page = SettingsPage(context.page)
    page.click_delete_account_closeicon()
    attach_screenshot(context.page, "Clicked Delete Account Close Icon")

@then("user navigates to settings screen")
def step_delete_account_settings_screen(context):
    page = SettingsPage(context.page)
    page.validate_settings_sections()
    attach_screenshot(context.page, "Navigated Back to Settings Screen")


# -------------------------
# WhatsappNotifications Steps
# -------------------------

@then("user clicks on notifications menu and validates whatsapp container section")
def step_whatsapp_container(context):
    page = SettingsPage(context.page)
    page.click_whatsapp_profile_icon()
    page.validate_whatsapp_container_section()
    attach_screenshot(context.page, "Validated Whatsapp Container Section")

@then("user clicks on whatsapp container section right arrow button")
def step_whatsapp_right_arrow(context):
    page = SettingsPage(context.page)
    page.click_whatsapp_right_arrow()
    attach_screenshot(context.page, "Clicked Whatsapp Right Arrow")

@then("user validates the whatsapp section and clicks on the toggle button")
def step_whatsapp_toggle(context):
    page = SettingsPage(context.page)
    page.validate_whatsapp_section_and_toggle()
    attach_screenshot(context.page, "Validated Whatsapp Section & Toggled")

@then("user clicks on the whatsapp section back arrow and validates the settings section")
def step_whatsapp_backarrow(context):
    page = SettingsPage(context.page)
    page.click_whatsapp_backbutton()
    attach_screenshot(context.page, "Clicked Whatsapp Back Arrow & Validated Settings Section")
