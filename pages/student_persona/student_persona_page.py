"""Base class for the student-persona pages.

Every student feature starts from the same home dashboard, so the "go back to
the dashboard and open card X" sequence lives here once instead of being
repeated as a private `_navigate_to_*` helper in each page object.
"""

import functools

from config.env_config import IS_PROD
from pages.base_page import BasePage, LONG_TIMEOUT
from utils.logger import log

CARD_TIMEOUT = 15000
PROD_PROBE_TIMEOUT = 5000


def dev_only(description):
    """Skip a page action that only exists in the dev environment.

    Several screens (the pitch-trainer flow, some dashboard sections) are not
    rendered for the prod account. The shared scenario still lists those steps,
    so on prod the action logs and returns instead of failing.
    """
    def decorator(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if IS_PROD:
                log.warning("Prod environment - skipping %s (dev-only step)", description)
                return None
            return method(self, *args, **kwargs)
        return wrapper
    return decorator


class StudentPersonaPage(BasePage):
    """Shared dashboard navigation for the student-persona page objects."""

    # Set once the dashboard URL is known; shared across page objects because
    # Behave discards `context` attributes between scenarios.
    shared_dashboard_url = None

    def capture_dashboard_url(self):
        """Remember the current URL as the dashboard URL, if not already set."""
        if not StudentPersonaPage.shared_dashboard_url:
            StudentPersonaPage.shared_dashboard_url = self.page.url

    def open_dashboard(self, ready_locator=None, timeout=LONG_TIMEOUT):
        """Navigate back to the stored dashboard URL.

        Does nothing when no dashboard URL has been captured yet - the caller
        is then already on the dashboard from the shared pre-login.
        """
        if not StudentPersonaPage.shared_dashboard_url:
            return
        self.open_url(StudentPersonaPage.shared_dashboard_url)
        if ready_locator:
            self.wait_for_visible(ready_locator, timeout=timeout)

    def open_card_from_dashboard(self, card_locator, description,
                                 ready_locator=None, timeout=CARD_TIMEOUT):
        """Return to the dashboard and open one of its feature cards."""
        self.open_dashboard()
        self.click(card_locator, description, timeout=timeout)
        if ready_locator:
            self.wait_for_visible(ready_locator, timeout=timeout)
