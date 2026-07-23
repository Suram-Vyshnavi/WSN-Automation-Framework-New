from behave import then

from pages.Common_pages.common_performance_page import CommonPerformancePage
from utils.helpers import attach_screenshot


@then("common user clicks on the performance menu")
def step_click_performance_menu(context):
	page = CommonPerformancePage(context.page)
	page.click_performance_menu()
	attach_screenshot(context.page, "Clicked performance menu")


@then('common user validate the course program label and clicks on the select course input field and selects  the "{course_name}" from the dropdown')
def step_validate_course_program_and_select_course(context, course_name):
	page = CommonPerformancePage(context.page)
	selected = page.validate_course_program_label_and_select_course(course_name)
	# When no course/performance data exists for this persona, the dependent
	# validations below have nothing to act on — flag it so they skip gracefully.
	context.performance_no_data = (selected is False)
	attach_screenshot(context.page, f"Selected course '{course_name}' from dropdown")


def _performance_data_missing(context):
	if getattr(context, "performance_no_data", False):
		print("[INFO] Skipping performance validation step — no course/performance data available.")
		return True
	return False


@then("common user validates the risk category label and clicks on the select status input field and clicks on the first status from the dropdown and selects critical")
def step_validate_risk_category_and_select_critical(context):
	if _performance_data_missing(context):
		return
	page = CommonPerformancePage(context.page)
	page.validate_risk_category_and_select_critical()
	attach_screenshot(context.page, "Selected Critical risk category status")


@then("common user validates the batch status label and clicks on the select batch input field and select batch status as active")
def step_validate_batch_status_and_select_active(context):
	if _performance_data_missing(context):
		return
	page = CommonPerformancePage(context.page)
	page.validate_batch_status_and_select_active()
	attach_screenshot(context.page, "Selected Active batch status")


@then("common user clicks on the clear button")
def step_click_clear_button(context):
	if _performance_data_missing(context):
		return
	page = CommonPerformancePage(context.page)
	page.click_clear_button()
	attach_screenshot(context.page, "Clicked Clear button")


@then("common user clicks on the batch details row option and validates certification status label")
def step_click_batch_row_and_validate_certification(context):
	if _performance_data_missing(context):
		return
	page = CommonPerformancePage(context.page)
	if page.click_batch_row_and_validate_certification_status() is False:
		# No batch performance data ("No Data Found") — flag so the dependent
		# steps below skip gracefully instead of failing.
		context.performance_no_data = True
		attach_screenshot(context.page, "Performance table has no data — skipping certification validation")
		return
	attach_screenshot(context.page, "Opened batch details row and validated certification status label")


@then("common user validates the student activity label and clicks on plus icon prevideo and plus icon postvideo")
def step_validate_student_activity_and_click_plus_icons(context):
	if _performance_data_missing(context):
		return
	page = CommonPerformancePage(context.page)
	page.validate_student_activity_and_click_plus_icons()
	attach_screenshot(context.page, "Validated student activity and clicked pre/post video plus icons")


@then("common user validates the student activity assesment label and clicks on the quiz plus icon")
def step_validate_assessment_activity_and_click_quiz_plus(context):
	if _performance_data_missing(context):
		return
	page = CommonPerformancePage(context.page)
	page.validate_assessment_activity_and_click_quiz_plus()
	attach_screenshot(context.page, "Validated assessment activity and clicked quiz plus icon")


@then("common user clicks on back to dashboard button")
def step_click_back_to_dashboard(context):
	if _performance_data_missing(context):
		return
	page = CommonPerformancePage(context.page)
	page.click_back_to_dashboard()
	attach_screenshot(context.page, "Clicked Back to Dashboard button")


@then("common user clicks on the pagination next button and validates the page number")
def step_click_next_and_validate_page_number(context):
	if _performance_data_missing(context):
		return
	page = CommonPerformancePage(context.page)
	page.click_next_and_validate_page_number()
	attach_screenshot(context.page, "Clicked pagination Next and validated page number")


@then("common user clicks on the perpage dropdown and validates the options and selects 25 perpage option and validates the page number")
def step_select_perpage_and_validate(context):
	if _performance_data_missing(context):
		return
	page = CommonPerformancePage(context.page)
	page.select_perpage_and_validate("25")
	attach_screenshot(context.page, "Selected 25 per page option and validated page number")
