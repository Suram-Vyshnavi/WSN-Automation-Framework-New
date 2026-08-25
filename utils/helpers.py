"""Reporting and diagnostic helpers shared by page objects and hooks.

UI interactions belong in `pages.base_page.BasePage`; this module only holds
cross-cutting utilities that are not element actions.
"""

import hashlib
import os

import allure
from allure_commons.types import AttachmentType

from utils.logger import log

# Last screenshot hash per Page object, so identical consecutive screenshots
# are not attached to the report twice. Keyed by id(page).
_last_screenshot_hash = {}

_HIGHLIGHT_ON_SCRIPT = """
    (element) => {
        if (element) {
            element.style.border = '5px solid red';
            element.style.backgroundColor = 'rgba(255, 0, 0, 0.2)';
            element.style.outline = '3px solid yellow';
        }
    }
"""

_HIGHLIGHT_OFF_SCRIPT = """
    (element) => {
        if (element) {
            element.style.border = '';
            element.style.backgroundColor = '';
            element.style.outline = '';
        }
    }
"""


def project_root():
    """Absolute path of the repository root (the folder holding behave.ini)."""
    current = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return current


def test_data_file(*parts):
    """Absolute path of a file under the shared `files/` test-data folder."""
    return os.path.join(project_root(), "files", *parts)


def require_test_data_file(*candidates):
    """Return the first existing test-data file, or fail with a clear message.

    Upload steps accept a couple of interchangeable fixtures (e.g. a PNG or a
    JPG), so the caller lists them in preference order.
    """
    paths = [test_data_file(name) for name in candidates]
    for path in paths:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        f"No test-data file found. Looked for: {', '.join(paths)}")


def attach_screenshot(page, name="Screenshot", dedupe: bool = True):
    """Attach a full-page screenshot to the Allure report.

    With `dedupe=True` an identical consecutive screenshot for the same page is
    skipped, which keeps the report readable on long scenarios.
    """
    try:
        image_bytes = page.screenshot(full_page=True)
    except Exception:
        try:
            image_bytes = page.screenshot()
        except Exception as error:
            log.warning("Could not capture screenshot '%s': %s", name, error)
            return None

    if dedupe:
        digest = hashlib.sha256(image_bytes).hexdigest()
        key = id(page)
        if _last_screenshot_hash.get(key) == digest:
            return digest
        _last_screenshot_hash[key] = digest

    allure.attach(image_bytes, name=name, attachment_type=AttachmentType.PNG)
    return True


def highlight_element(page, locator, duration: int = 1500):
    """Outline an element in the browser so report screenshots show the target.

    Purely cosmetic - failures here never fail a test.

    Args:
        page: Playwright page object.
        locator: Selector string or Playwright Locator.
        duration: How long to keep the outline, in milliseconds.
    """
    try:
        element = page.locator(locator) if isinstance(locator, str) else locator

        element.scroll_into_view_if_needed()
        # Nudge the viewport so a heading right under the sticky header is not
        # clipped out of the screenshot.
        page.evaluate("window.scrollBy(0, -150)")

        handle = element.element_handle()
        page.evaluate(_HIGHLIGHT_ON_SCRIPT, handle)
        try:
            element.wait_for(state="visible", timeout=duration)
        except Exception as _ignored:
            log.debug("Optional step in highlight_element() did not apply: %s", _ignored)
        page.evaluate(_HIGHLIGHT_OFF_SCRIPT, handle)
    except Exception as error:
        log.debug("Could not highlight element: %s", error)
