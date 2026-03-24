from behave import then

from pages.Faculty_pages.Batch_details_page import BatchDetailsPage
from utils.helpers import attach_screenshot


@then("user clicks on first batch from Active batches list")
def step_click_first_batch(context):
	page = BatchDetailsPage(context.page)
	page.click_first_active_batch()
	attach_screenshot(context.page, "Clicked first batch from Active list")


@then("user validates the institute name and course name")
def step_validate_institute_and_course(context):
	page = BatchDetailsPage(context.page)
	page.validate_institute_and_course_name()
	attach_screenshot(context.page, "Validated institute name and course name")


@then("user validates the course timeline section and batch code section")
def step_validate_timeline_and_batch_code(context):
	page = BatchDetailsPage(context.page)
	page.validate_timeline_and_batch_code()
	attach_screenshot(context.page, "Validated timeline and batch code sections")


@then("user clicks on the batch code and copy it")
def step_copy_batch_code(context):
	page = BatchDetailsPage(context.page)
	page.click_batch_code_and_copy()
	attach_screenshot(context.page, "Clicked batch code copy")


@then("user clicks on the more option and clicks on the edit batch option")
def step_open_more_and_edit(context):
	page = BatchDetailsPage(context.page)
	page.open_more_and_click_edit_batch()
	attach_screenshot(context.page, "Opened more option and clicked Edit Batch")


@then("user validates the batch details section and edits the batch name and update the details")
def step_edit_batch_details(context):
	page = BatchDetailsPage(context.page)
	page.edit_batch_name_and_update()
	attach_screenshot(context.page, "Updated batch details")


@then("user clicks on the more option and clicks on the close batch option and clicks on close button")
def step_open_more_and_close(context):
	page = BatchDetailsPage(context.page)
	page.open_more_and_close_batch()
	attach_screenshot(context.page, "Opened close batch option and clicked close")


@then("user validates the general info tab and validates the assessment schedule section")
def step_validate_general_info_and_assessment(context):
	page = BatchDetailsPage(context.page)
	page.validate_general_info_and_assessment_schedule()
	attach_screenshot(context.page, "Validated General Info and Assessment Schedule")


@then("user validates the batch activity section and validates the batch faculty section")
def step_validate_batch_activity_and_faculty(context):
	page = BatchDetailsPage(context.page)
	page.validate_batch_activity_and_batch_faculty()
	attach_screenshot(context.page, "Validated Batch Activity and Batch Faculty")


@then("user clicks on the add faculty button and clicks on the second faculty")
def step_add_second_faculty(context):
	page = BatchDetailsPage(context.page)
	page.add_second_faculty()
	attach_screenshot(context.page, "Added second faculty")


@then("user validates the toast message and user clicks on the edit faculty button")
def step_validate_toast_and_edit_faculty(context):
	page = BatchDetailsPage(context.page)
	page.validate_toast_and_click_edit_faculty()
	attach_screenshot(context.page, "Validated toast and clicked edit faculty")


@then("user clicks on the faculty2 cross icon and clicks on the faculty delete button")
def step_delete_second_faculty(context):
	page = BatchDetailsPage(context.page)
	page.delete_second_faculty()
	attach_screenshot(context.page, "Deleted second faculty")


@then("validates the faculty delete toast message")
def step_validate_faculty_delete_toast(context):
	page = BatchDetailsPage(context.page)
	page.validate_faculty_delete_toast()
	attach_screenshot(context.page, "Validated faculty delete toast")


@then("user validates the upcoming activities section and validates the create meeting button")
def step_validate_upcoming_and_create_meeting_button(context):
	page = BatchDetailsPage(context.page)
	page.validate_upcoming_and_create_meeting_button()
	attach_screenshot(context.page, "Validated upcoming activities and create meeting button")