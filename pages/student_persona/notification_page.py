from locators.student_locators import NotificationLocators
from pages.student_persona.student_persona_page import StudentPersonaPage
from utils.helpers import attach_screenshot

# The locator class ships a positional selector ((...//img)[3]); the stable
# class-based selector is tried first so a change in header icon order does not
# break the step.
NOTIFICATION_ICON_SELECTORS = [
    "//img[contains(@class,'notification_icon')]",
    NotificationLocators.NOTIFICATIONS_ICON,
]


class NotificationPage(StudentPersonaPage):
    """The student notifications panel."""

    def click_notification_icon(self):
        self.click_required(NOTIFICATION_ICON_SELECTORS, "Notification icon")
        attach_screenshot(self.page, "Notification Icon Clicked")

    def validate_notifications(self):
        self.validate_visible(NotificationLocators.VALIDATE_NOTIFICATION_CONTAINER,
                              "Notifications container")
        attach_screenshot(self.page, "Notifications Validated")

    def click_first_notification(self):
        self.click(NotificationLocators.FIRST_NOTIFICATION, "first notification")
        attach_screenshot(self.page, "First Notification Clicked")
