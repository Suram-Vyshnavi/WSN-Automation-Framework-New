from behave import then

from pages.Faculty_pages.Create_newbatch_page import CreateNewBatchPage
from utils.helpers import attach_screenshot


@then("user clicks on craete new batch button")
def step_click_create_new_batch_button(context):
	page = CreateNewBatchPage(context.page)
	page.click_create_new_batch_button()
	attach_screenshot(context.page, "Clicked Create New Batch button")


@then("user validates the batch information header section and validates the batch information title")
def step_validate_batch_info_header_and_title(context):
	page = CreateNewBatchPage(context.page)
	page.validate_batch_information_header_and_title()
	attach_screenshot(context.page, "Validated batch information header and title")


@then('user clicks in Institute selection dropdown and select the "{institute_name}" name from list')
def step_select_institute(context, institute_name):
	page = CreateNewBatchPage(context.page)
	page.select_institute_by_name(institute_name)
	attach_screenshot(context.page, f"Selected institute: {institute_name}")


@then("user validates the faculty pre filled name")
def step_validate_prefilled_faculty_name(context):
	page = CreateNewBatchPage(context.page)
	page.validate_prefilled_faculty_name()
	attach_screenshot(context.page, "Validated faculty pre-filled name")


@then('user clicks on select course selection dropdown and select the "{course_name}" course from list')
def step_select_course(context, course_name):
	page = CreateNewBatchPage(context.page)
	page.select_course_by_name(course_name)
	attach_screenshot(context.page, f"Selected course: {course_name}")


@then('user clicks on Batch name input filed and enters the "{batch_name}" name')
def step_enter_batch_name(context, batch_name):
	page = CreateNewBatchPage(context.page)
	page.enter_batch_name(batch_name)
	attach_screenshot(context.page, f"Entered batch name: {batch_name}")


@then("user validates the start date input field and click on the calendar icon and clicks on the today text")
def step_set_start_date_today(context):
	page = CreateNewBatchPage(context.page)
	page.set_start_date_to_today()
	attach_screenshot(context.page, "Set start date to today")


@then('user validates the end date input field and clicks on the calendar icon and clicks on the next year/next month arrow and select "{day_text}" from month')
def step_set_end_date(context, day_text):
	page = CreateNewBatchPage(context.page)
	page.set_end_date_with_next_year_next_month(day_text)
	attach_screenshot(context.page, f"Selected end-date day: {day_text}")


@then("user validates the student enrollment note section and validates the prefilled weekly class hours value")
def step_validate_student_enrollment_note(context):
	page = CreateNewBatchPage(context.page)
	page.validate_student_enrollment_note_and_weekly_hours()
	attach_screenshot(context.page, "Validated student enrollment note and weekly class hours")


@then("user check the confirmation checkbox and clicks on the maximum students allowed input field and enter 200 value and clicks on Next button")
def step_set_max_students_and_next(context):
	page = CreateNewBatchPage(context.page)
	page.check_confirmation_set_max_students_and_next(200)
	attach_screenshot(context.page, "Checked confirmation, set max students to 200, clicked Next")


@then("user validates the confirm dates popup and clicks on the confirm and proceed button")
def step_confirm_dates_and_proceed(context):
	page = CreateNewBatchPage(context.page)
	page.confirm_dates_and_proceed()
	attach_screenshot(context.page, "Confirmed dates and proceeded")


@then("user validates the assessment details section and click on the next button")
def step_validate_assessment_and_next(context):
	page = CreateNewBatchPage(context.page)
	page.validate_assessment_details_and_next()
	attach_screenshot(context.page, "Validated assessment details and clicked Next")


@then("user validates the difficulty level 1 , difficulty level 2 , difficulty level 3 and clicks on the difficulty level 2 radio button")
def step_validate_difficulty_and_select_level2(context):
	page = CreateNewBatchPage(context.page)
	page.validate_difficulty_levels_and_select_level2()
	attach_screenshot(context.page, "Validated difficulty levels and selected level 2")


@then('user clicks on the "job role or sector" input field and enters the "{job_role_text}" text and clicks on the enter button')
def step_enter_job_role_or_sector(context, job_role_text):
	page = CreateNewBatchPage(context.page)
	page.enter_job_role_or_sector(job_role_text)
	attach_screenshot(context.page, f"Entered job role/sector: {job_role_text}")


@then("user clicks on the save and finish button and validate the batch details card")
def step_save_finish_and_validate_batch_card(context):
	page = CreateNewBatchPage(context.page)
	page.save_and_finish_and_validate_batch_details_card()
	attach_screenshot(context.page, "Clicked Save & Finish and validated batch details card")
