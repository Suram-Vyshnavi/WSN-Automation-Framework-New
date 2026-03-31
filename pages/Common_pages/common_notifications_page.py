from pages.base_page import BasePage
from locators.Common_locators.common_notifications_locators import CommonNotificationLocators
from locators.Faculty_locators.Home_locators import HomeLocators


class CommonNotificationsPage(BasePage):
	def click_notification_icon(self):
		icon = self.page.locator(CommonNotificationLocators.NOTIFICATIONS_ICON).first
		try:
			icon.wait_for(state="visible", timeout=10000)
			icon.click()
			return
		except Exception:
			pass

		fallback = self.page.locator(HomeLocators.NOTIFICATIONS_MENU).first
		fallback.wait_for(state="visible", timeout=10000)
		fallback.click()

	def validate_notifications(self):
		container = self.page.locator(CommonNotificationLocators.VALIDATE_NOTIFICATION_CONTAINER).first
		container.wait_for(state="visible", timeout=10000)
		assert container.is_visible(), "Notifications container is not visible"

	def click_first_notification(self):
		notification = self.page.locator(CommonNotificationLocators.FIRST_NOTIFICATION).first
		notification.wait_for(state="visible", timeout=10000)
		try:
			notification.scroll_into_view_if_needed()
		except Exception:
			pass
		notification.click()
