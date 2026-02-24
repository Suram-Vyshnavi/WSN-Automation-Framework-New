from behave import given, when, then
from pages.notification_page import NotificationPage


@then('user clicks on notification icon')
def click_notification_icon(context):
    notification_page = NotificationPage(context.page)
    notification_page.click_notification_icon()


@then('user validates the notifications')
def validate_notifications(context):
    notification_page = NotificationPage(context.page)
    notification_page.validate_notifications()


@then('user clicks on first notification')
def click_first_notification(context):
    notification_page = NotificationPage(context.page)
    notification_page.click_first_notification()
