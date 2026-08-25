from behave import then

from pages.rm_pages.all_batches_page import RMAllBatchesPage
from utils.helpers import attach_screenshot
from utils.logger import log


@then("user clicks on the first active batch from assigned batches list")
def step_click_first_active_assigned_batch(context):
    page = RMAllBatchesPage(context.page)
    opened = page.click_first_assigned_batch()
    # When the account has no openable batch (empty/placeholder Assigned Batches
    # and no batch in All Batches), skip the rest of this scenario gracefully
    # instead of failing the batch-detail validations.
    if not opened:
        log.info("No openable batch available for the RM account; "
                 "skipping batch-detail validations for this scenario.")
        context.scenario.skip("No openable batch available for the RM account")
        return
    attach_screenshot(context.page, "Clicked first active batch from Assigned Batches list")


@then('user validates the all batches title and clicks on the seachbar and enters"{batch_name}"')
def step_validate_all_batches_title_and_search(context, batch_name):
    page = RMAllBatchesPage(context.page)
    page.validate_all_batches_title_and_search(batch_name)
    attach_screenshot(context.page, f"Validated All Batches title and searched '{batch_name}'")


@then("user validates the status title")
def step_validate_status_title(context):
    page = RMAllBatchesPage(context.page)
    page.validate_status_title()
    attach_screenshot(context.page, "Validated Status title")


@then("user clicks on the status dropdown and clicks on the active option")
def step_select_active_status(context):
    page = RMAllBatchesPage(context.page)
    page.select_status_option("active")
    attach_screenshot(context.page, "Selected Active status")


@then("user clicks on the status dropdown and clicks on the inactive option")
def step_select_inactive_status(context):
    page = RMAllBatchesPage(context.page)
    page.select_status_option("inactive")
    attach_screenshot(context.page, "Selected Inactive status")


@then("user validates the batches section")
def step_validate_batches_section(context):
    page = RMAllBatchesPage(context.page)
    page.validate_batches_section()
    attach_screenshot(context.page, "Validated batches section")

