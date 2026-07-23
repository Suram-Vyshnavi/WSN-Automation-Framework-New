from behave import given, then
from pages.login_page import LoginPage
from pages.studentpersona.home_dashboard_page import HomeDashboardPage
from utils.helpers import attach_screenshot


@given("user is on the home page")
def user_is_on_home_page(context):
    # Login is handled by before_all in environment.py; just verify home page is ready
    login_page = LoginPage(context.page)
    login_page.wait_for_home_page()
    attach_screenshot(context.page, "Home Page Loaded")


@then("user validates the home icon")
def validate_home_icon(context):
    dashboard = HomeDashboardPage(context.page)
    dashboard.validate_home_icon()
    attach_screenshot(context.page, "Home Icon Validated")


@then("user validates the welcome header and wadhwani skilling header")
def validate_welcome_and_wadhwani_header(context):
    dashboard = HomeDashboardPage(context.page)
    dashboard.validate_welcome_and_wadhwani_header()
    attach_screenshot(context.page, "Welcome and Wadhwani Headers Validated")

@then("user validates genie")
def validate_genie_ai(context):
    dashboard = HomeDashboardPage(context.page)
    dashboard.validate_genie_ai()
    attach_screenshot(context.page, "Genie AI Validated")


@then("user clicks on courses card")
def click_courses_card(context):
    context.current_section = 'courses'
    dashboard = HomeDashboardPage(context.page)
    dashboard.click_courses_card()
    attach_screenshot(context.page, "Courses Card Clicked")


@then("user clicks on programs card")
def click_programs_card(context):
    context.current_section = 'programs'
    dashboard = HomeDashboardPage(context.page)
    dashboard.click_programs_card()
    attach_screenshot(context.page, "Programs Card Clicked")


@then("user clicks on personal pitch trainer card")
def click_personal_pitch_trainer_card(context):
    context.current_section = 'personal_pitch'
    dashboard = HomeDashboardPage(context.page)
    dashboard.click_personal_pitch_trainer_card()
    attach_screenshot(context.page, "Personal Pitch Trainer Card Clicked")


@then("user clicks on Interview coach card")
def click_interview_coach_card(context):
    dashboard = HomeDashboardPage(context.page)
    dashboard.click_interview_coach_card()
    attach_screenshot(context.page, "Interview Coach Card Clicked")


@then("user clicks on forums card")
def click_forums_card(context):
    # If the scenario continues into the Forums page (validates the My Forums
    # header), stay on the page via ForumsPage. Otherwise (e.g. home dashboard
    # validation) use HomeDashboardPage, which returns to the dashboard.
    stays_on_forums = any(
        "my forums header" in step.name.lower()
        for step in context.scenario.steps
    )
    if context.feature.name.lower() == "forums" or stays_on_forums:
        from pages.studentpersona.forums_page import ForumsPage
        forums = ForumsPage(context.page)
        forums.click_forums_card()
    else:
        dashboard = HomeDashboardPage(context.page)
        dashboard.click_forums_card()
    attach_screenshot(context.page, "Forums Card Clicked")


@then("user clicks on My carrer advisory card")
def click_my_career_advisor_card(context):
    dashboard = HomeDashboardPage(context.page)
    dashboard.click_my_career_advisor_card()
    attach_screenshot(context.page, "My Career Advisor Card Clicked")


@then("user clicks on Carrer Buddy card")
def click_career_buddy_card(context):
    dashboard = HomeDashboardPage(context.page)
    dashboard.click_career_buddy_card()
    attach_screenshot(context.page, "Career Buddy Card Clicked")


@then("user clicks on Jobs Connect card")
def click_jobs_connect_card(context):
    dashboard = HomeDashboardPage(context.page)
    dashboard.click_jobs_connect_card()
    attach_screenshot(context.page, "Jobs Connect Card Clicked")


@then("user clicks on menu help icon")
def click_menu_help_icon(context):
    dashboard = HomeDashboardPage(context.page)
    dashboard.click_menu_help_icon()
    attach_screenshot(context.page, "Menu Help Icon Clicked")


@then("user clicks on header profile menu icon")
def click_header_profile_menu_icon(context):
    dashboard = HomeDashboardPage(context.page)
    dashboard.click_header_profile_menu_icon()
    attach_screenshot(context.page, "Header Profile Menu Icon Clicked")


@then("user clicks on messages and discussions")
def click_messages_and_discussions(context):
    dashboard = HomeDashboardPage(context.page)
    dashboard.click_messages_and_discussions()
    attach_screenshot(context.page, "Messages and Discussions Clicked")


@then("user clicks on settings")
def click_settings(context):
    dashboard = HomeDashboardPage(context.page)
    dashboard.click_settings()
    attach_screenshot(context.page, "Settings Clicked")


@then("user clicks on log out")
def click_log_out(context):
    dashboard = HomeDashboardPage(context.page)
    dashboard.click_log_out()
    attach_screenshot(context.page, "Logged Out")
