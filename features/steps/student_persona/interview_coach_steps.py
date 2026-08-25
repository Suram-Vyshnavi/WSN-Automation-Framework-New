from behave import then
from pages.student_persona.interview_coach_page import InterviewCoachPage
from utils.helpers import attach_screenshot


@then('user navigates to interview coach card')
def navigate_to_interview_coach_card(context):
    coach_page = InterviewCoachPage(context.page)
    coach_page._navigate_to_interview_coach()
    attach_screenshot(context.page, "Interview Coach Card Clicked")


@then('user clicks on audio button image')
def click_audio_button_image(context):
    coach_page = InterviewCoachPage(context.page)
    coach_page.click_audio_button_image()
    attach_screenshot(context.page, "Audio Button Image Clicked")


@then('user fills the textbox and clicks on send icon')
def fill_textbox_and_click_send(context):
    coach_page = InterviewCoachPage(context.page)
    coach_page.fill_textbox_and_click_send()
    attach_screenshot(context.page, "Textbox Filled and Send Clicked")


@then('user validates start button')
def validate_start_button(context):
    coach_page = InterviewCoachPage(context.page)
    coach_page.validate_start_button()
    attach_screenshot(context.page, "Start Button Validated")


@then('user clicks on pitch trainer back icon')
def click_pitch_trainer_back_icon(context):
    coach_page = InterviewCoachPage(context.page)
    coach_page.click_pitch_trainer_back_icon()
    attach_screenshot(context.page, "Pitch Trainer Back Icon Clicked")


@then('user validates your recent roles header')
def validate_your_recent_roles_header(context):
    coach_page = InterviewCoachPage(context.page)
    coach_page.validate_your_recent_roles_header()
    attach_screenshot(context.page, "Your Recent Roles Header Validated")


@then('user validates ongoing header and completed header')
def validate_ongoing_and_completed_headers(context):
    coach_page = InterviewCoachPage(context.page)
    coach_page.validate_ongoing_and_completed_headers()
    attach_screenshot(context.page, "Ongoing and Completed Headers Validated")


@then('user clicks on threedots icon')
def click_threedots_icon(context):
    coach_page = InterviewCoachPage(context.page)
    coach_page.click_threedots_icon()
    attach_screenshot(context.page, "Three Dots Icon Clicked")


@then('user clicks on delete this role icon and confirms delete action')
def click_delete_role_and_confirm(context):
    coach_page = InterviewCoachPage(context.page)
    coach_page.click_delete_role_and_confirm()
    attach_screenshot(context.page, "Delete Role Confirmed")


@then('user validates textbox and mic button in Interview Coach page')
def validate_textbox_and_mic_button(context):
    coach_page = InterviewCoachPage(context.page)
    coach_page.validate_textbox_and_mic_button()
    attach_screenshot(context.page, "Textbox and Mic Button Validated")


@then('user clicks on Practise Interviewing for the role')
def click_practise_interviewing_for_role(context):
    coach_page = InterviewCoachPage(context.page)
    coach_page.click_practise_interviewing_for_role()
    attach_screenshot(context.page, "Practise Interviewing Clicked")
