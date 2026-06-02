from behave import then
from pages.studentpersona.personal_pitch_page import PersonalPitchPage
from utils.helpers import attach_screenshot


@then('user clicks on create your pitch button')
def click_create_your_pitch_button(context):
    pitch_page = PersonalPitchPage(context.page)
    pitch_page.click_create_your_pitch_button()
    attach_screenshot(context.page, "Create Your Pitch Button Clicked")


@then('user clicks on create your pitch back button')
def click_create_your_pitch_back_button(context):
    pitch_page = PersonalPitchPage(context.page)
    pitch_page.click_create_your_pitch_back_button()
    attach_screenshot(context.page, "Create Your Pitch Back Button Clicked")


@then('user clicks on pitch summary view button')
def click_pitch_summary_view_button(context):
    pitch_page = PersonalPitchPage(context.page)
    pitch_page.click_pitch_summary_view_button()
    attach_screenshot(context.page, "Pitch Summary View Button Clicked")


@then('user clicks on view pitch button')
def click_view_pitch_button(context):
    pitch_page = PersonalPitchPage(context.page)
    pitch_page.click_view_pitch_button()
    attach_screenshot(context.page, "View Pitch Button Clicked")


@then('user clicks on home icon and navigates to home page')
def click_home_icon_and_navigate_home(context):
    pitch_page = PersonalPitchPage(context.page)
    pitch_page.click_home_icon_and_navigate_home()
    attach_screenshot(context.page, "Home Icon Clicked and Navigated to Home")


@then('user clicks on passed text on personal pitch trainer card')
def click_passed_text_on_pitch_card(context):
    pitch_page = PersonalPitchPage(context.page)
    context.passed_text_present = pitch_page.click_passed_text_on_pitch_card()
    attach_screenshot(context.page, "Passed Text Clicked on Personal Pitch Trainer Card")


@then('user validates check button')
def validate_check_button(context):
    pitch_page = PersonalPitchPage(context.page)
    pitch_page.validate_check_button()
    attach_screenshot(context.page, "Check Button Validated")
