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
