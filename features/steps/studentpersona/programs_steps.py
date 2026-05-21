from behave import then
from pages.studentpersona.programs_page import ProgramsPage
from utils.helpers import attach_screenshot


@then('user validates recommended by institue header')
def validate_recommended_by_institute_header(context):
    programs_page = ProgramsPage(context.page)
    programs_page.validate_recommended_by_institute_header()
    attach_screenshot(context.page, "Recommended by Institute Header Validated")


@then('user clicks on recommended by institute tab')
def click_recommended_by_institute_tab(context):
    programs_page = ProgramsPage(context.page)
    programs_page.click_recommended_by_institute_tab()
    attach_screenshot(context.page, "Recommended by Institute Tab Clicked")


@then('user clicks on enroll button')
def click_enroll_button(context):
    programs_page = ProgramsPage(context.page)
    programs_page.click_enroll_button()
    attach_screenshot(context.page, "Enroll Button Clicked")


@then('user validate confirm button and cancel button')
def validate_confirm_and_cancel_buttons(context):
    programs_page = ProgramsPage(context.page)
    programs_page.validate_confirm_and_cancel_buttons()
    attach_screenshot(context.page, "Confirm and Cancel Buttons Validated")


@then('user clicks on close modal button')
def click_close_modal_button(context):
    programs_page = ProgramsPage(context.page)
    programs_page.click_close_modal_button()
    attach_screenshot(context.page, "Close Modal Button Clicked")


@then('user validates offered by wadhwani foundation header')
def validate_offered_by_wadhwani_foundation_header(context):
    programs_page = ProgramsPage(context.page)
    programs_page.validate_offered_by_wadhwani_foundation_header()
    attach_screenshot(context.page, "Offered by Wadhwani Foundation Header Validated")


@then('user clicks on offered by wadhwani foundation tab')
def click_offered_by_wadhwani_foundation_tab(context):
    programs_page = ProgramsPage(context.page)
    programs_page.click_offered_by_wadhwani_foundation_tab()
    attach_screenshot(context.page, "Offered by Wadhwani Foundation Tab Clicked")
