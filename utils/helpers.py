import allure
from allure_commons.types import AttachmentType
from utils.locators import LoginLocators
import hashlib

# cache last screenshot hash per page (use id(page) as key)
_last_screenshot_hash = {}


def attach_screenshot(page, name="Screenshot", dedupe: bool = True):
    """Attach a full-page screenshot to Allure unless it's identical
    to the previous screenshot taken for the same Page object.

    - `dedupe=True` will skip attaching if the screenshot hash matches the
      last one recorded for that page during this process run.
    """
    try:
        img_bytes = page.screenshot(full_page=True)
    except Exception:
        # fallback: try a smaller screenshot
        try:
            img_bytes = page.screenshot()
        except Exception:
            return None

    if dedupe:
        h = hashlib.sha256(img_bytes).hexdigest()
        key = id(page)
        if _last_screenshot_hash.get(key) == h:
            return h
        _last_screenshot_hash[key] = h

    allure.attach(img_bytes, name=name, attachment_type=AttachmentType.PNG)
    return True


def login(page, username, password, locators=LoginLocators):
    """Fill credentials and submit the login form.

    Defaults to using `LoginLocators` but a different locator set
    can be passed for tests if needed.
    """
    page.fill(locators.USERNAME_INPUT, username)
    page.click(locators.NEXT_BUTTON)
    page.fill(locators.PASSWORD_INPUT, password)
    # Submit using the explicit submit button
    page.click(locators.SUBMIT_BUTTON)


def validate_header(page, timeout: int = 10000):
    """Validate that a page header (h1 or h2) is present and non-empty.

    Returns the header text on success, raises on timeout or empty text.
    """
    # Try several common header selectors in order, each with a fraction of the total timeout.
    selectors = ["h1, h2", "[role=heading]", "header h1, header h2", "header", "[data-header]"]
    per_try = max(1000, timeout // len(selectors))

    for sel in selectors:
        try:
            header = page.locator(sel).first
            header.wait_for(state="visible", timeout=per_try)
            text = header.inner_text().strip()
            if text:
                return text
        except Exception:
            # try next selector
            continue

    # Fallback: try page title
    try:
        title = page.title().strip()
        if title:
            return title
    except Exception:
        pass

    raise AssertionError("No page header (h1/h2/role=heading/header) or non-empty title found")


from typing import Optional


def validate_navigation(previous_url: str, page, expected_fragment: Optional[str] = None, timeout: int = 10000):
    """Validate that navigation happened after a click.

    - If `expected_fragment` is provided, assert it is present in the new URL.
    - Otherwise assert the URL changed from `previous_url`.

    Returns the new URL.
    """
    # wait a short time for navigation to settle
    # Use page.wait_for_load_state to ensure navigation finished (if any)
    try:
        page.wait_for_load_state("load", timeout=timeout)
    except Exception:
        # ignore load timeout, we'll still read the URL
        pass

    new_url = page.url
    if expected_fragment:
        assert expected_fragment in new_url, f"Expected '{expected_fragment}' in URL '{new_url}'"
    else:
        assert new_url != previous_url, f"URL did not change after click (still '{new_url}')"

    return new_url


def collect_validation_messages(page, timeout: int = 3000):
    """Collect visible validation/error messages on the page.

    Tries common selectors used by UI frameworks and common text patterns.
    Returns a list of unique non-empty message strings.
    """
    selectors = [
        "//div[contains(@class,'ant-form-item-explain')]",
        "//div[contains(@class,'error') or contains(@class,'invalid')]//span",
        "//span[contains(@class,'error') or contains(@class,'validation')]",
        '//*[contains(text(),"required") or contains(text(),"Please") or contains(text(),"cannot be") or contains(text(),"can\'t")]',
    ]

    messages = []
    # give page a short moment to render validation messages
    try:
        pass
    except Exception:
        pass

    for sel in selectors:
        try:
            elems = page.locator(sel)
            count = elems.count()
            for i in range(count):
                try:
                    text = elems.nth(i).inner_text().strip()
                    if text:
                        messages.append(text)
                except Exception:
                    continue
        except Exception:
            continue

    # dedupe and return
    unique = []
    for m in messages:
        if m not in unique:
            unique.append(m)
    return unique


def highlight_element(page, locator, duration: int = 1500):
    """Highlight an element by adding a red border temporarily.
    
    Args:
        page: Playwright page object
        locator: Element locator (can be string or locator object)
        duration: How long to highlight in milliseconds (default 1500ms)
    """
    try:
        # Convert string locator to locator object if needed
        if isinstance(locator, str):
            element = page.locator(locator)
        else:
            element = locator
        
        # Scroll element into view first
        element.scroll_into_view_if_needed()
        
        # Scroll up a bit to ensure title/heading is fully visible (not cut off at top)
        page.evaluate("window.scrollBy(0, -150)")
        
        # Add red border with JavaScript
        page.evaluate("""
            (element) => {
                if (element) {
                    element.style.border = '5px solid red';
                    element.style.backgroundColor = 'rgba(255, 0, 0, 0.2)';
                    element.style.outline = '3px solid yellow';
                }
            }
        """, element.element_handle())
        
        # Wait briefly for visualization (using locator wait instead of sleep)
        try:
            element.wait_for(state="visible", timeout=duration)
        except:
            pass
        
        # Remove the highlight
        page.evaluate("""
            (element) => {
                if (element) {
                    element.style.border = '';
                    element.style.backgroundColor = '';
                    element.style.outline = '';
                }
            }
        """, element.element_handle())
    except Exception as e:
        print(f"Could not highlight element: {e}")
