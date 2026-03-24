from behave import then

from utils.helpers import attach_screenshot


@then("current persona login should be successful")
def step_persona_login_success(context):
    current_url = context.page.url.lower()
    assert "login" not in current_url, f"Login appears unsuccessful. Current URL: {context.page.url}"
    attach_screenshot(context.page, "Current persona login successful")


@then("faculty login should be successful")
def step_faculty_login_success(context):
    step_persona_login_success(context)
