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


@then('user clicks on ongoing courses and validates overview section')
def click_ongoing_courses_and_validate_overview(context):
    learning_progress_page = LearningProgressPage(context.page)
    learning_progress_page.click_ongoing_courses_and_validate_overview()


@then('user clicks on content section and clicks on resume')
def click_content_section_and_resume(context):
    learning_progress_page = LearningProgressPage(context.page)
    learning_progress_page.click_content_section_and_resume()


@then('user clicks on performance section and validates final score')
def click_performance_section_and_validate_score(context):
    learning_progress_page = LearningProgressPage(context.page)
    learning_progress_page.click_performance_section_and_validate_final_score()


@then('user navigates to learning progress page and clicks on completed courses')
def navigate_to_learning_progress_and_click_completed(context):
    learning_progress_page = LearningProgressPage(context.page)
    learning_progress_page.navigate_to_learning_progress_and_click_completed_courses()


@then('user clicks on a completed course and validates overview, content, performance sections, score value and overall progress')
def click_completed_course_and_validate_all(context):
    learning_progress_page = LearningProgressPage(context.page)
    learning_progress_page.click_completed_course_and_validate_all_sections()


@then('user clicks on share certificate button and validates download certificate option')
def click_share_certificate_and_validate_download(context):
    learning_progress_page = LearningProgressPage(context.page)
    learning_progress_page.click_share_certificate_and_validate_download()


@then('user clicks on overview section and clicks on view batch and validates')
def click_overview_and_view_batch(context):
    learning_progress_page = LearningProgressPage(context.page)
    learning_progress_page.click_overview_and_view_batch()


@then('user clicks on general info and validates upcoming activities')
def click_general_info_and_validate_activities(context):
    learning_progress_page = LearningProgressPage(context.page)
    learning_progress_page.click_general_info_and_validate_upcoming_activities()


@then('user clicks on batch members and validates students added count and maximum allowed and batch member list')
def click_batch_members_and_validate(context):
    learning_progress_page = LearningProgressPage(context.page)
    learning_progress_page.click_batch_members_and_validate_all()


@then('user clicks on chat button')
def click_chat_button(context):
    learning_progress_page = LearningProgressPage(context.page)
    learning_progress_page.click_chat_button()
