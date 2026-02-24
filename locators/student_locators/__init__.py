"""
Student Locators Module
This module contains all locator classes for student-facing features.
"""

from .login_locators import LoginLocators
from .home_page_locators import HomePageLocators
from .dashboard_locators import DashboardLocators
from .career_advisor_locators import CareerAdvisorLocators
from .placement_prep_locators import PlacementPrepLocators
from .interview_prep_locators import InterviewPrepLocators
from .placement_locators import PlacementLocators
from .career_buddy_locators import CareerBuddyLocators
from .jobs_connect_locators import JobsConnectLocators
from .messages_locators import Messages_and_discussionsLocators
from .learning_progress_locators import Learning_Progress_Locators
from .notification_locators import NotificationLocators

__all__ = [
    'LoginLocators',
    'HomePageLocators',
    'DashboardLocators',
    'CareerAdvisorLocators',
    'PlacementPrepLocators',
    'InterviewPrepLocators',
    'PlacementLocators',
    'CareerBuddyLocators',
    'JobsConnectLocators',
    'Messages_and_discussionsLocators',
    'Learning_Progress_Locators',
    'NotificationLocators',
]
