from behave import then
from pages.student_persona.personal_pitch_page import PersonalPitchPage
from utils.helpers import attach_screenshot


@then('user clicks on create pitch button')
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


# These five steps used to live in courses_steps.py and were shared with the
# Courses scenario's pitch-trainer sub-flow. That sub-flow no longer exists in
# the application, so they now belong solely to the Personal Pitch Trainer
# scenario and live with it.
@then('user clicks on video play button')
def click_video_play_button(context):
    PersonalPitchPage(context.page).click_video_play_button()
    attach_screenshot(context.page, "Video play button clicked")


@then('user clicks on video close button')
def click_video_close_button(context):
    PersonalPitchPage(context.page).click_video_close_button()
    attach_screenshot(context.page, "Video close button clicked")


@then('user clicks on share pitch button')
def click_share_pitch_button(context):
    PersonalPitchPage(context.page).click_share_pitch_button()
    attach_screenshot(context.page, "Share Pitch button clicked")


@then('user clicks on copy pitch button')
def click_copy_pitch_button(context):
    PersonalPitchPage(context.page).click_copy_pitch_button()
    attach_screenshot(context.page, "Copy Pitch button clicked")


@then('user clicks on share pitch close button')
def click_share_pitch_close_button(context):
    PersonalPitchPage(context.page).click_share_pitch_close_button()
    attach_screenshot(context.page, "Share Pitch close button clicked")
