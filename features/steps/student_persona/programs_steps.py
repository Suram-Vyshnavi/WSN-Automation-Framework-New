"""Steps for the Programs scenario.

Kept deliberately separate from the Courses steps: the app merged both screens
into one, but the two scenarios stay independent so a change to one cannot
silently move the other.
"""

from behave import then

from pages.student_persona.programs_page import ProgramsPage
from utils.helpers import attach_screenshot


@then('user validates the programs In Progress and Completed tabs')
def validate_programs_tabs(context):
    ProgramsPage(context.page).validate_inprogress_and_completed_tabs()
    attach_screenshot(context.page, "Programs In Progress and Completed tabs validated")


@then('user clicks on the programs In Progress tab')
def click_programs_inprogress_tab(context):
    ProgramsPage(context.page).click_inprogress_tab()
    attach_screenshot(context.page, "Programs In Progress tab clicked")


@then('user clicks on the programs Completed tab')
def click_programs_completed_tab(context):
    ProgramsPage(context.page).click_completed_tab()
    attach_screenshot(context.page, "Programs Completed tab clicked")


@then('user validates program card')
def validate_program_card(context):
    ProgramsPage(context.page).validate_program_card()
    attach_screenshot(context.page, "Program card validated")


@then('user validates recommended by institue header')
def validate_recommended_by_institute_header(context):
    ProgramsPage(context.page).validate_recommended_by_institute_header()
    attach_screenshot(context.page, "Recommended by institute header validated")


@then('user validates recommended program card')
def validate_recommended_program_card(context):
    ProgramsPage(context.page).validate_recommended_program_card()
    attach_screenshot(context.page, "Recommended program card validated")


@then('user validates offered by wadhwani foundation header')
def validate_offered_by_wadhwani_foundation_header(context):
    ProgramsPage(context.page).validate_offered_by_wadhwani_foundation_header()
    attach_screenshot(context.page, "Offered by Wadhwani Foundation header validated")


@then('user validates join a batch section')
def validate_join_a_batch_section(context):
    ProgramsPage(context.page).validate_join_a_batch_section()
    attach_screenshot(context.page, "Join a batch section validated")
