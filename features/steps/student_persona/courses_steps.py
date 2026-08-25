"""Steps for the Courses scenario.

These used to share step wording with the Programs scenario and branch on a
`context.current_section` flag, which coupled the two scenarios together. The
app has since merged both screens into one, so the wording is now explicit
("courses ...") and each scenario drives its own page object.
"""

from behave import then

from pages.student_persona.courses_page import CoursesPage
from utils.helpers import attach_screenshot


@then('user validates the courses In Progress and Completed tabs')
def validate_courses_tabs(context):
    CoursesPage(context.page).validate_inprogress_and_completed_tabs()
    attach_screenshot(context.page, "Courses In Progress and Completed tabs validated")


@then('user clicks on the courses In Progress tab')
def click_courses_inprogress_tab(context):
    CoursesPage(context.page).click_inprogress_tab()
    attach_screenshot(context.page, "Courses In Progress tab clicked")


@then('user clicks on the courses Completed tab')
def click_courses_completed_tab(context):
    CoursesPage(context.page).click_completed_tab()
    attach_screenshot(context.page, "Courses Completed tab clicked")


@then('user validates enrolled course card')
def validate_enrolled_course_card(context):
    CoursesPage(context.page).validate_enrolled_course_card()
    attach_screenshot(context.page, "Enrolled course card validated")


@then('user opens the first course')
def open_first_course(context):
    CoursesPage(context.page).open_first_course()
    attach_screenshot(context.page, "First course opened")


@then('user validates the course detail sections')
def validate_course_detail_sections(context):
    CoursesPage(context.page).validate_course_detail_sections()
    attach_screenshot(context.page, "Course detail sections validated")


@then('user expands the first lesson section')
def expand_first_lesson_section(context):
    CoursesPage(context.page).expand_first_lesson_section()
    attach_screenshot(context.page, "First lesson section expanded")


@then('user validates the assessment score')
def validate_assessment_score(context):
    CoursesPage(context.page).validate_assessment_score()
    attach_screenshot(context.page, "Assessment score validated")


@then('user navigates back to the courses list')
def go_back_to_course_list(context):
    CoursesPage(context.page).go_back_to_course_list()
    attach_screenshot(context.page, "Back on the Programs & Courses list")


@then('user validates courses recommended by institute')
def validate_courses_recommended_by_institute(context):
    CoursesPage(context.page).validate_courses_recommended_by_institute()
    attach_screenshot(context.page, "Courses recommended by institute validated")


@then('user validates recommended course card')
def validate_recommended_course_card(context):
    CoursesPage(context.page).validate_recommended_course_card()
    attach_screenshot(context.page, "Recommended course card validated")


@then('user validates courses offered by wadhwani foundation')
def validate_courses_offered_by_wadhwani_foundation(context):
    CoursesPage(context.page).validate_courses_offered_by_wadhwani_foundation()
    attach_screenshot(context.page, "Courses offered by Wadhwani Foundation validated")
