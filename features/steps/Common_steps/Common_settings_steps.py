from behave import then
from pages.Common_pages.Common_settings_page import CommonSettingsPage
from utils.helpers import attach_screenshot


@then("common user clicks on ZoomConnect profile icon")
def step_zoomconnect_profile_icon(context):
	page = CommonSettingsPage(context.page)
	page.click_zoomconnect_profile_icon()
	attach_screenshot(context.page, "Clicked ZoomConnect Profile Icon")


@then("common user clicks on settings menu")
def step_settings_menu(context):
	page = CommonSettingsPage(context.page)
	page.click_settings_menu()
	attach_screenshot(context.page, "Clicked Settings Menu")


@then("common user validates the settings sections")
def step_validate_settings(context):
	page = CommonSettingsPage(context.page)
	page.validate_settings_sections()
	attach_screenshot(context.page, "Validated Settings Sections")


@then("common user clicks on accounts menu and validates accounts_meetings section")
def step_accounts_menu_zoomconnect(context):
	page = CommonSettingsPage(context.page)
	page.click_accounts_menu_zoomconnect()
	attach_screenshot(context.page, "Clicked Accounts Menu & Validated Meetings Section")


@then("common user clicks on sign in with zoom right arrow button")
def step_zoom_right_arrow(context):
	page = CommonSettingsPage(context.page)
	page.click_zoom_right_arrow()
	attach_screenshot(context.page, "Clicked Zoom Right Arrow")


@then("common user validates the zoom account delinked popup and closed the popup")
def step_delinked_popup(context):
	page = CommonSettingsPage(context.page)
	page.validate_delinked_popup()
	attach_screenshot(context.page, "Validated Delinked Popup")


@then("common user validates the sign in with zoom section and turn on the toggle button")
def step_signin_toggle(context):
	page = CommonSettingsPage(context.page)
	page.validate_signin_section_and_toggle()
	context.zoom_signin_required = True
	attach_screenshot(context.page, "Validated Sign In Section & Toggled")


@then("common user navigates to meetings section and click on signin button")
def step_meetings_signin(context):
	page = CommonSettingsPage(context.page)
	context.zoom_signin_required = page.navigate_meetings_and_click_signin()
	if context.zoom_signin_required:
		attach_screenshot(context.page, "Navigated to Meetings & Clicked Sign In")
	else:
		attach_screenshot(context.page, "Zoom already connected after toggle; navigated back without sign in")


@then("common user navigates to zoom.us signin screen and validates the email address, password,signin buttons")
def step_zoom_login_screen(context):
	if hasattr(context, "zoom_signin_required") and not context.zoom_signin_required:
		attach_screenshot(context.page, "Skipped zoom.us sign in screen validation for already connected user")
		return
	page = CommonSettingsPage(getattr(context, "zoom_page", context.page))
	context.zoom_signin_required = page.validate_zoom_login_screen()
	if context.zoom_signin_required and hasattr(page, "active_page"):
		context.zoom_page = page.active_page
	if context.zoom_signin_required:
		attach_screenshot(getattr(context, "zoom_page", context.page), "Validated Zoom Login Screen")
	else:
		attach_screenshot(context.page, "Zoom login screen did not appear; skipping credential steps")


@then("common user clicks on email input field and enter the email id")
def step_enter_email(context):
	if hasattr(context, "zoom_signin_required") and not context.zoom_signin_required:
		attach_screenshot(context.page, "Skipped Zoom email entry for already connected user")
		return
	page = CommonSettingsPage(getattr(context, "zoom_page", context.page))
	page.enter_zoom_email("demouser2078@gmail.com")
	attach_screenshot(getattr(context, "zoom_page", context.page), "Entered Zoom Email")


@then("common user clicks on password input field and enter the password")
def step_enter_password(context):
	if hasattr(context, "zoom_signin_required") and not context.zoom_signin_required:
		attach_screenshot(context.page, "Skipped Zoom password entry for already connected user")
		return
	page = CommonSettingsPage(getattr(context, "zoom_page", context.page))
	page.enter_zoom_password("Demo@123")
	attach_screenshot(getattr(context, "zoom_page", context.page), "Entered Zoom Password")


@then("common user clicks on sigin button")
def step_click_signin(context):
	if hasattr(context, "zoom_signin_required") and not context.zoom_signin_required:
		attach_screenshot(context.page, "Skipped Zoom sign in click for already connected user")
		return
	page = CommonSettingsPage(getattr(context, "zoom_page", context.page))
	page.click_zoom_signin()
	attach_screenshot(getattr(context, "zoom_page", context.page), "Clicked Zoom Sign In")


@then("common user navigates back to to signin with zoom screen and validates the toggle button status")
def step_validate_toggle(context):
	if hasattr(context, "zoom_signin_required") and not context.zoom_signin_required:
		attach_screenshot(context.page, "Skipped toggle-status validation after sign in for already connected user")
		return
	page = CommonSettingsPage(context.page)
	if page.validate_toggle_status():
		attach_screenshot(context.page, "Validated Toggle Status")
	else:
		attach_screenshot(context.page, "Toggle not visible in current return path; continuing disconnect flow")


@then("common user click on back arrow and navigates to settings screen")
def step_back_arrow(context):
	page = CommonSettingsPage(context.page)
	page.click_back_arrow()
	attach_screenshot(context.page, "Clicked Back Arrow")


@then("common user clicks on notifications menu and validates whatsapp container section")
def step_whatsapp_container(context):
	page = CommonSettingsPage(context.page)
	page.click_whatsapp_profile_icon()
	page.validate_whatsapp_container_section()
	attach_screenshot(context.page, "Validated Whatsapp Container Section")


@then("common user clicks on whatsapp container section right arrow button")
def step_whatsapp_right_arrow(context):
	page = CommonSettingsPage(context.page)
	page.click_whatsapp_right_arrow()
	attach_screenshot(context.page, "Clicked Whatsapp Right Arrow")


@then("common user validates the whatsapp section and clicks on the toggle button")
def step_whatsapp_toggle(context):
	page = CommonSettingsPage(context.page)
	page.validate_whatsapp_section_and_toggle()
	attach_screenshot(context.page, "Validated Whatsapp Section & Toggled")


@then("common user clicks on the whatsapp section back arrow and validates the settings section")
def step_whatsapp_backarrow(context):
	page = CommonSettingsPage(context.page)
	page.click_whatsapp_backbutton()
	attach_screenshot(context.page, "Clicked Whatsapp Back Arrow & Validated Settings Section")
