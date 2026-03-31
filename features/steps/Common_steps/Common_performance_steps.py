from behave import then

from pages.Common_pages.common_performance_page import CommonPerformancePage
from utils.helpers import attach_screenshot


@then("common user clicks on the performance menu")
def step_click_performance_menu(context):
	page = CommonPerformancePage(context.page)
	page.click_performance_menu()
	attach_screenshot(context.page, "Clicked performance menu")


@then("common user validates the reports title")
def step_validate_reports_title(context):
	page = CommonPerformancePage(context.page)
	page.validate_reports_title()
	attach_screenshot(context.page, "Validated reports title")


@then("common user validate the course name container and clicks on the select course name input field and clicks on the first course from dropdown")
def step_select_course_name(context):
	page = CommonPerformancePage(context.page)
	page.select_first_course()
	attach_screenshot(context.page, "Selected first course from dropdown")


@then("common user validates the status container and clicks on the select satus input field and clicks on the first status from the dropdown")
def step_select_status(context):
	page = CommonPerformancePage(context.page)
	page.select_first_status()
	attach_screenshot(context.page, "Selected first status from dropdown")


@then('common user validates the batch name container and clicks on the select batch input field and clicks on the "{batch_name}" from dropdown')
def step_select_batch_name(context, batch_name):
	page = CommonPerformancePage(context.page)
	page.select_batch_name(batch_name)
	attach_screenshot(context.page, f"Selected batch {batch_name} from dropdown")


@then("common user validates the batch assessment title and batch assessment graph")
def step_validate_batch_assessment(context):
	page = CommonPerformancePage(context.page)
	page.validate_batch_assessment_title_and_graph()
	attach_screenshot(context.page, "Validated batch assessment title and graph")


@then("common user validates the assessment status title and validates the show score toggle button")
def step_validate_assessment_status_and_toggle(context):
	page = CommonPerformancePage(context.page)
	page.validate_assessment_status_and_toggle()
	attach_screenshot(context.page, "Validated assessment status and show score toggle")


@then("common user clicks on the score toggle button and clicks on the assessment status next arrow button")
def step_click_toggle_and_next_arrow(context):
	page = CommonPerformancePage(context.page)
	page.click_score_toggle_and_next_arrow()
	attach_screenshot(context.page, "Clicked score toggle and next arrow")


@then("common user clicks on the student name link from second screen")
def step_click_student_name_link(context):
	page = CommonPerformancePage(context.page)
	page.click_student_name_link()
	attach_screenshot(context.page, "Clicked student name link")


@then("common user validates the course name dropdown and validates the student name card")
def step_validate_course_dropdown_and_student_card(context):
	page = CommonPerformancePage(context.page)
	page.validate_student_performance_cards()
	attach_screenshot(context.page, "Validated course dropdown and student card")


@then("common user validates the course name card , institute name card , completion status card  and assessment score details card")
def step_validate_performance_detail_cards(context):
	page = CommonPerformancePage(context.page)
	page.validate_student_performance_cards()
	attach_screenshot(context.page, "Validated performance detail cards")
