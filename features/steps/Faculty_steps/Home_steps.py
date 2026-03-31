from behave import then

from pages.Faculty_pages.Home_page import FacultyHomePage
from utils.helpers import attach_screenshot


@then("user clicks on Home menu")
def step_click_home_menu(context):
	page = FacultyHomePage(context.page)
	page.click_home_menu()
	attach_screenshot(context.page, "Clicked Home menu")


@then("user clicks on Batches menu")
def step_click_batches_menu(context):
	page = FacultyHomePage(context.page)
	page.click_batches_menu()
	attach_screenshot(context.page, "Clicked Batches menu")


@then("user clicks on Performance menu")
def step_click_performance_menu(context):
	page = FacultyHomePage(context.page)
	page.click_performance_menu()
	attach_screenshot(context.page, "Clicked Performance menu")


@then("user navigates with Help/support")
def step_navigate_help_support(context):
	page = FacultyHomePage(context.page)
	page.navigate_help_support()
	attach_screenshot(context.page, "Validated Help/Support navigation")


@then("user validates batches section and create new batch button")
def step_validate_batches(context):
	page = FacultyHomePage(context.page)
	page.validate_batches_section()
	attach_screenshot(context.page, "Validated batches section and Create New Batch button")


@then("user validates Active and Inactive tabs under batches section")
def step_validate_active_inactive_tabs(context):
	page = FacultyHomePage(context.page)
	page.validate_active_inactive_tabs_under_batches()
	attach_screenshot(context.page, "Validated Active and Inactive tabs")


@then("user clicks on the batches next arrow button")
def step_click_batches_next_arrow(context):
	page = FacultyHomePage(context.page)
	page.click_batches_next_arrow_button()
	attach_screenshot(context.page, "Clicked batches next arrow")


@then("user validates certified courses section and clicks on carousal arrow")
def step_validate_certified_courses(context):
	page = FacultyHomePage(context.page)
	page.validate_certified_courses_and_click_carousal_arrow()
	attach_screenshot(context.page, "Validated certified courses and clicked carousel arrow")


@then("user validates My Forums section")
def step_validate_my_forums(context):
	page = FacultyHomePage(context.page)
	page.validate_my_forums_section()
	attach_screenshot(context.page, "Validated My Forums section")


@then("user edits profile details for first name and clicks on the save button")
def step_edit_profile_details_and_save(context):
	page = FacultyHomePage(context.page)
	page.edit_profile_details()
	attach_screenshot(context.page, "Edited first name and clicked save")


@then("user validates My Forums section and validates the recommended forums section")
def step_validate_my_and_recommended_forums(context):
	page = FacultyHomePage(context.page)
	page.validate_my_forums_section()
	attach_screenshot(context.page, "Validated My Forums and Recommended Forums sections")
