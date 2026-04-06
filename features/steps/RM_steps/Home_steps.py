from behave import then

from pages.RM_pages.Home_page import RMHomePage
from utils.helpers import attach_screenshot


@then("user clicks on All Batches menu")
def step_click_all_batches_menu(context):
	page = RMHomePage(context.page)
	page.click_all_batches_menu()
	attach_screenshot(context.page, "Clicked All Batches menu")


@then("user validates Assigned batches section")
def step_validate_assigned_batches_section(context):
	page = RMHomePage(context.page)
	page.validate_assigned_batches_section()
	attach_screenshot(context.page, "Validated Assigned Batches section")


@then("user validates the batch name title , institute name title,course name title,start date title ,end date title,no.of student title , actions title")
def step_validate_assigned_batches_titles(context):
	page = RMHomePage(context.page)
	page.validate_assigned_batches_table_headers()
	attach_screenshot(context.page, "Validated Assigned Batches table headers")

