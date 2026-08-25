"""Locator classes for the student-facing screens."""

from ..student_persona_locators.learning_progress_locators import LearningProgressLocators
from ..student_persona_locators.messages_locators import MessagesAndDiscussionsLocators
from ..student_persona_locators.notification_locators import NotificationLocators
from .settings_delete_account_locators import SettingsDeleteAccountLocators
from .settings_whatsapp_notifications_locators import SettingsWhatsappNotificationsLocators
from .settings_zoom_connect_locators import SettingsZoomConnectLocators
from .login_locators import LoginLocators

__all__ = [
    "LearningProgressLocators",
    "LoginLocators",
    "MessagesAndDiscussionsLocators",
    "NotificationLocators",
    "SettingsDeleteAccountLocators",
    "SettingsWhatsappNotificationsLocators",
    "SettingsZoomConnectLocators",
]
