from behave import given, when, then
from pages.login_page import LoginPage
from utils.helpers import attach_screenshot, validate_header
from utils.helpers import validate_navigation
from utils.config import Config

@given("user is on login page")
def open_login_url(context):
    login_page = LoginPage(context.page)
    
    login_page.open(Config.BASE_URL)
    login_page.dismiss_popup_if_present()
    attach_screenshot(context.page, "Popup Handled")
    
    attach_screenshot(context.page, "Login Page Loaded")
    login_page.click_get_started()
    login_page.click_continue_with_email()



@when("user enters valid login details")
def step_login(context):
    # Username
    login_page = LoginPage(context.page)
    login_page.login(Config.USERNAME_INPUT, Config.PASSWORD_INPUT)
    attach_screenshot(context.page, "Login Details Entered")

@then("user logged into home page")
def login_user(context):
    login_page = LoginPage(context.page)
    login_page.wait_for_home_page()
    attach_screenshot(context.page, "Logged into home page")
@then("user navigates through dashboard")
def navigate_dashboard(context):
    login_page = LoginPage(context.page)
    login_page.navigate_to_dashboard()
    # Validate header on dashboard
    header = validate_header(context.page)
    attach_screenshot(context.page, f"Dashboard header: {header}")
@then("user clicks on Career Advisor")
def click_career_advisor(context):
    page = context.page
    login_page = LoginPage(page)
    
    prev = page.url
    login_page.click_career_advisor()
    
    # validate navigation
    new = validate_navigation(prev, page)
    header = validate_header(page)
    attach_screenshot(page, f"Career Advisor header: {header} | url: {new}")
@then("user clicks on Placement Prep")
def click_placement_prep(context):
    page = context.page
    login_page = LoginPage(page)
    
    prev = page.url
    login_page.click_placement_prep()
    new = validate_navigation(prev, page)
    header = validate_header(page)
    attach_screenshot(page, f"Placement Prep header: {header} | url: {new}")
@then("user clicks on Jobs Connect")
def click_jobs_connect(context):
    page = context.page
    login_page = LoginPage(page)
    
    prev = page.url
    login_page.click_jobs_connect()
    new = validate_navigation(prev, page)
    header = validate_header(page)
    attach_screenshot(page, f"Jobs Connect header: {header} | url: {new}")
@then("user clicks on Calender")
def click_calender(context):
    page = context.page
    login_page = LoginPage(page)
    
    prev = page.url
    login_page.click_calendar()
    new = validate_navigation(prev, page)
    header = validate_header(page)
    attach_screenshot(page, f"Calendar header: {header} | url: {new}")
@then("user navigates with support")
def navigate_support(context):
    page = context.page
    login_page = LoginPage(page)
    
    login_page.navigate_support()
    # Validate header after returning from support
    header = validate_header(page)
    attach_screenshot(page, f"After support header: {header}")

@then("user checks notifications and chat")
def check_notifications_chat(context):
    login_page = LoginPage(context.page)
    login_page.check_notifications_and_chat()
    


@then("user clicks on profile icon")
def click_profile_icon(context):
    login_page = LoginPage(context.page)
    login_page.click_profile_icon()


@then("profile fields should be visible")
def profile_fields_visible(context):
    page = context.page
    login_page = LoginPage(page)
    
    login_page.verify_profile_fields_visible()
    attach_screenshot(page, "Profile Fields Visible")

@then("user edits profile details")
def edit_profile_details(context):
    login_page = LoginPage(context.page)
    login_page.edit_profile_details("Vyshnavi", "Suram", "India", "Bangalore, Bangalore, Karnataka, India", "9182269382")


@then("user clicks on logout")
def click_logout(context):
    login_page = LoginPage(context.page)
    login_page.click_logout()
    attach_screenshot(context.page, "After Login")

@then("user logs out")
def step_logs_out(context):
    login_page = LoginPage(context.page)
    login_page.logout()
    attach_screenshot(context.page, "Logged Out")

@then("dashboard should be displayed")
def verify_dashboard(context):
    attach_screenshot(context.page, "Dashboard Loaded")
    assert "Dashboard" in context.page.title()
    card = context.page.locator("//div[contains(@class,'program_card__container')]")
    card.wait_for(state="visible", timeout=15000)
    card.click()
    attach_screenshot(context.page, "Dashboard Verified")

@then("user validates recommended activities section")
def validate_recommended_activities(context):
    login_page = LoginPage(context.page)
    login_page.validate_recommended_activities_section()

@then("user validates ongoing course section")
def validate_ongoing_course(context):
    login_page = LoginPage(context.page)
    login_page.validate_ongoing_course_section()

@then("user validates institute specific courses")
def validate_institute_courses(context):
    login_page = LoginPage(context.page)
    login_page.validate_institute_specific_courses()

@then("user validates wadhwani courses and programs")
def validate_wadhwani_courses(context):
    login_page = LoginPage(context.page)
    login_page.validate_wadhwani_courses_and_programs()

@then("user validates enrol batch card")
def validate_enrol_batch(context):
    login_page = LoginPage(context.page)
    login_page.validate_enrol_batch_card()

@then("user validates footer section")
def validate_footer(context):
    login_page = LoginPage(context.page)
    login_page.validate_footer_section()



