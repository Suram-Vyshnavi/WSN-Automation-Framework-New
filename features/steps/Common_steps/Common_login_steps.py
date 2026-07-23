from behave import then

from utils.helpers import attach_screenshot


@then("current persona login should be successful")
def step_persona_login_success(context):
    try:
        context.page.wait_for_function(
            "() => !window.location.href.toLowerCase().includes('login')",
            timeout=15000,
        )
    except Exception:
        pass

    current_url = context.page.url.lower()
    if "login" in current_url:
        error_message = ""
        for selector in [
            "//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'INVALID') or contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'INCORRECT') or contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'EXPIRED') or contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'LOCKED')]",
            "//div[contains(@class,'error') or contains(@class,'alert')]",
        ]:
            try:
                loc = context.page.locator(selector).first
                loc.wait_for(state="visible", timeout=1500)
                text = (loc.inner_text() or "").strip()
                if text:
                    error_message = text
                    break
            except Exception:
                continue

        extra = f" Login page error: {error_message}" if error_message else ""
        raise AssertionError(
            f"Login appears unsuccessful. Current URL: {context.page.url}.{extra}"
        )

    attach_screenshot(context.page, "Current persona login successful")


@then("faculty login should be successful")
def step_faculty_login_success(context):
    step_persona_login_success(context)
