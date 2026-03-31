from behave import then

from locators.Common_locators.common_activity_insights_locators import CommonActivityInsightsLocators
from pages.Common_pages.common_activityinsights_page import CommonActivityInsightsPage
from utils.helpers import attach_screenshot


@then("common user validates the activity insights tab and clicks on it")
def step_validate_activity_insights_tab(context):
	page = CommonActivityInsightsPage(context.page)
	page.validate_activity_insights_tab_and_click()
	attach_screenshot(context.page, "Validated and clicked Activity Insights tab")


@then("common user validates the submission insights header section and validates the module column title and lesson name column title")
def step_validate_submission_header_columns(context):
	page = CommonActivityInsightsPage(context.page)
	page.validate_submission_header_module_and_lesson()
	attach_screenshot(context.page, "Validated submission insights header, module and lesson columns")


@then("common user clicks on the students submitted i icon and validates the text")
def step_students_submitted_info(context):
	page = CommonActivityInsightsPage(context.page)
	page.click_students_submitted_icon_and_validate()
	attach_screenshot(context.page, "Validated students submitted info icon and tooltip")


@then("common user click on the students scored i icon and validates the text")
def step_students_scored_info(context):
	page = CommonActivityInsightsPage(context.page)
	page.click_students_scored_icon_and_validate()
	attach_screenshot(context.page, "Validated students scored info icon and tooltip")


@then("common user clicks on the pitch trainer pre video arrow icon and validates the heading section and insights table and click on the back arrow")
def step_pitch_trainer_prevideo(context):
	page = CommonActivityInsightsPage(context.page)
	page.open_lesson_arrow_validate_and_back(CommonActivityInsightsLocators.PITCH_TRAINER_PREVIDEO_ARROW_ICON)
	attach_screenshot(context.page, "Validated Pitch Trainer pre-video insights and navigated back")


@then("common user clicks on the active listening arrow icon and validates the heading section and insights table and click on the back arrow")
def step_active_listening(context):
	page = CommonActivityInsightsPage(context.page)
	page.open_lesson_arrow_validate_and_back(CommonActivityInsightsLocators.ACTIVE_LISTENING_ARROW_ICON)
	attach_screenshot(context.page, "Validated Active Listening insights and navigated back")


@then("common user clicks on the LT and TA arrow icon and validates the heading section and insights table and click on the back arrow")
def step_lt_ta(context):
	page = CommonActivityInsightsPage(context.page)
	page.open_lesson_arrow_validate_and_back(CommonActivityInsightsLocators.LA_AND_TA_ARROW_ICON)
	attach_screenshot(context.page, "Validated LT and TA insights and navigated back")


@then("common user clicks on the pitch trainer post video arrow icon and validates the heading section and insights table and click on the back arrow")
def step_pitch_trainer_postvideo(context):
	page = CommonActivityInsightsPage(context.page)
	page.open_lesson_arrow_validate_and_back(CommonActivityInsightsLocators.PITCH_TRAINER_POSTVIDEO_ARROW_ICON)
	attach_screenshot(context.page, "Validated Pitch Trainer post-video insights and navigated back")
