from behave import then

from pages.Common_pages.common_notifications_page import CommonNotificationsPage
from utils.helpers import attach_screenshot


@then("common user clicks on notification icon")
def step_click_notification_icon(context):
	page = CommonNotificationsPage(context.page)
	page.click_notification_icon()
	attach_screenshot(context.page, "Clicked notification icon")


@then("common user validates the notifications")
def step_validate_notifications(context):
	page = CommonNotificationsPage(context.page)
	page.validate_notifications()
	attach_screenshot(context.page, "Validated notifications")


@then("common user clicks on first notification")
def step_click_first_notification(context):
	page = CommonNotificationsPage(context.page)
	page.click_first_notification()
	attach_screenshot(context.page, "Clicked first notification")
