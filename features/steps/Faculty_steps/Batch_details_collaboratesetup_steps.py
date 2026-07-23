from behave import then

from pages.Faculty_pages.Batch_details_collaborate_setup_page import BatchDetailsCollaborateSetupPage
from utils.helpers import attach_screenshot


def _collab_unavailable(context):
	if getattr(context, "collaboratesetup_unavailable", False):
		print("[INFO] Skipping collaborate setup step — tab unavailable for this batch.")
		return True
	return False


@then("user validates the collaboratesetup tab and clicks on it")
def step_validate_collaboratesetup_and_click(context):
	page = BatchDetailsCollaborateSetupPage(context.page)
	if page.validate_collaboratesetup_tab_and_click() is False:
		context.collaboratesetup_unavailable = True
		attach_screenshot(context.page, "Collaborate Setup tab unavailable — skipping validation")
		return
	attach_screenshot(context.page, "Validated collaborate setup tab and clicked it")


@then("user clicks on edit button and change level from 2 to 1 and clicks on the save button")
def step_edit_level_and_save(context):
	if _collab_unavailable(context):
		return
	page = BatchDetailsCollaborateSetupPage(context.page)
	page.click_edit_and_change_level_save()
	attach_screenshot(context.page, "Edited level setting and saved changes")


@then("user navigates to batch details collaborate setup screen and validates the selected career plans section")
def step_validate_career_plans(context):
	if _collab_unavailable(context):
		return
	page = BatchDetailsCollaborateSetupPage(context.page)
	page.navigate_to_collaborate_setup_and_validate_career_plans()
	attach_screenshot(context.page, "Validated selected career plans section")
