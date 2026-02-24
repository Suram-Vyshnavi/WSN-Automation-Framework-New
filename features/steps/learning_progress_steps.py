from behave import given, when, then
from pages.learning_progress_page import LearningProgressPage
from pages.login_page import LoginPage


@then('user clicks on learning progress')
def click_learning_progress(context):
    learning_progress_page = LearningProgressPage(context.page)
    learning_progress_page.click_learning_progress()


@then('user validates the learning progress')
def validate_learning_progress(context):
    learning_progress_page = LearningProgressPage(context.page)
    learning_progress_page.validate_learning_progress()


@then('user clicks on ongoing courses and validates overview, content amd performance sections')
def click_ongoing_courses_and_validate(context):
    learning_progress_page = LearningProgressPage(context.page)
    learning_progress_page.click_ongoing_courses_and_validate_sections()


@then('user navigates to learning progress page and clicks on completed courses')
def navigate_to_learning_progress_and_click_completed(context):
    learning_progress_page = LearningProgressPage(context.page)
    learning_progress_page.navigate_to_learning_progress_and_click_completed_courses()


@then('user user clicks on a completed course and validates overview, content, performance sections , score value and overall progress')
def click_completed_course_and_validate_all(context):
    learning_progress_page = LearningProgressPage(context.page)
    learning_progress_page.click_completed_course_and_validate_all_sections()
