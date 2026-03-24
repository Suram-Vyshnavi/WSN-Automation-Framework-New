from behave import then

from pages.Faculty_pages.Batch_details_scorecard_page import BatchDetailsScorecardPage
from utils.helpers import attach_screenshot


@then("user validates the scorecard tab and clicks on it")
def step_validate_scorecard_and_click(context):
	page = BatchDetailsScorecardPage(context.page)
	page.validate_scorecard_tab_and_click()
	attach_screenshot(context.page, "Validated scorecard tab and clicked it")


@then("user validates the Assessment schedule title and validates the Assessment schedule container")
def step_validate_assessment_schedule(context):
	page = BatchDetailsScorecardPage(context.page)
	page.validate_assessment_schedule_title_and_container()
	attach_screenshot(context.page, "Validated assessment schedule title and container")
