from playwright.sync_api import Page
from locators.student_locators import NotificationLocators
from utils.helpers import attach_screenshot


class NotificationPage:
    def __init__(self, page: Page):
        self.page = page

    def click_notification_icon(self):
        """Click on notification icon"""
        # The primary locator is positional ((...//img)[3]); prefer the stable
        # class-based selector and fall back to the positional one so a change in
        # the header's icon order doesn't break this step.
        for selector in [
            "//img[contains(@class,'notification_icon')]",
            NotificationLocators.NOTIFICATIONS_ICON,
        ]:
            try:
                locator = self.page.locator(selector).first
                locator.wait_for(state="visible", timeout=10000)
                locator.click(timeout=5000)
                attach_screenshot(self.page, "Notification Icon Clicked")
                return
            except Exception:
                continue
        raise AssertionError("Notification icon is not visible/clickable")

    def validate_notifications(self):
        """Validate notifications container is visible"""
        self.page.locator(NotificationLocators.VALIDATE_NOTIFICATION_CONTAINER).wait_for(state="visible", timeout=10000)
        assert self.page.locator(NotificationLocators.VALIDATE_NOTIFICATION_CONTAINER).is_visible(), "Notifications container not visible"
        attach_screenshot(self.page, "Notifications Validated")

    def click_first_notification(self):
        """Click on first notification"""
        self.page.locator(NotificationLocators.FIRST_NOTIFICATION).wait_for(state="visible", timeout=10000)
        self.page.locator(NotificationLocators.FIRST_NOTIFICATION).scroll_into_view_if_needed()
        self.page.click(NotificationLocators.FIRST_NOTIFICATION)
        attach_screenshot(self.page, "First Notification Clicked")
