from behave import then

from pages.common_pages.common_login_page import CommonLoginPage
from utils.helpers import attach_screenshot


@then("current persona login should be successful")
def step_persona_login_success(context):
    CommonLoginPage(context.page).validate_login_successful()
    attach_screenshot(context.page, "Current persona login successful")
