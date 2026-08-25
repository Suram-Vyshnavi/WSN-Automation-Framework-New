"""Home/dashboard steps that every persona shares.

The same Gherkin sentence drives a different page object per persona, so the
persona lookup lives here in one place instead of being repeated per step.
"""

from behave import then

from pages.faculty_pages.home_page import FacultyHomePage
from pages.student_persona.home_dashboard_page import HomeDashboardPage
from utils.helpers import attach_screenshot

FACULTY_LIKE_PERSONAS = ("faculty", "rm")


def _persona(context):
    return getattr(context, "persona", "student")


def _is_faculty_like(context):
    return _persona(context) in FACULTY_LIKE_PERSONAS


@then("user navigates through dashboard")
def step_navigate_through_dashboard(context):
    FacultyHomePage(context.page).navigate_to_dashboard()
    attach_screenshot(context.page, "Navigated through dashboard")


@then("user clicks on Calender")
def step_click_calendar(context):
    if _is_faculty_like(context):
        FacultyHomePage(context.page).click_calendar_menu()
    else:
        HomeDashboardPage(context.page).click_calendar()
    attach_screenshot(context.page, "Clicked Calendar")


@then("user checks notifications and chat")
def step_check_notifications_and_chat(context):
    FacultyHomePage(context.page).check_notifications_and_chat()
    attach_screenshot(context.page, "Checked notifications and chat")


@then("user clicks on profile icon")
def step_click_profile_icon(context):
    if _is_faculty_like(context):
        FacultyHomePage(context.page).click_profile_icon()
    else:
        HomeDashboardPage(context.page).click_profile_icon()
    attach_screenshot(context.page, "Clicked profile icon")

