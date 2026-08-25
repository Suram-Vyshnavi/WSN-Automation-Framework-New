from locators.common_locators.common_notifications_locators import CommonNotificationLocators
from locators.faculty_locators.home_locators import HomeLocators
from pages.base_page import BasePage

# The header renders the bell differently per persona, so both entry points are
# tried in order.
NOTIFICATION_ICON_SELECTORS = [
    CommonNotificationLocators.NOTIFICATIONS_ICON,
    HomeLocators.NOTIFICATIONS_MENU,
]


class CommonNotificationsPage(BasePage):
    """The notifications panel shared by the faculty/RM-style personas."""

    def click_notification_icon(self):
        self.click_required(NOTIFICATION_ICON_SELECTORS, "Notification icon")

    def validate_notifications(self):
        self.validate_visible(CommonNotificationLocators.VALIDATE_NOTIFICATION_CONTAINER,
                              "Notifications container")

    def click_first_notification(self):
        self.click(CommonNotificationLocators.FIRST_NOTIFICATION, "first notification")
