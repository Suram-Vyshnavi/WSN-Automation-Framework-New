"""Base class for every page object in the framework.

Every UI operation (click, enter text, select, get text, wait, scroll,
navigate, popup handling, checkbox/radio, assertion) has exactly ONE
implementation and it lives here. Page objects describe *what* to do on a
screen; this class owns *how* it is done, so timeouts, highlighting, retry
behaviour and logging stay identical everywhere.

Rules for page objects:
  * never call ``self.page.locator(...)`` / ``self.page.click(...)`` directly
    for a normal interaction - use the helpers below;
  * pass a human-readable ``description`` so the log line and the assertion
    message are meaningful;
  * keep business flow in step definitions, keep screen actions here.
"""

from utils.logger import log

# Single source of truth for wait durations. Page objects override
# DEFAULT_TIMEOUT when a screen is consistently slower/faster.
DEFAULT_TIMEOUT = 10000
SHORT_TIMEOUT = 5000
LONG_TIMEOUT = 20000
NAVIGATION_TIMEOUT = 60000
HIGHLIGHT_DURATION = 1200


class BasePage:
    """Shared Playwright interactions for all page objects."""

    DEFAULT_TIMEOUT = DEFAULT_TIMEOUT

    def __init__(self, page):
        self.page = page

    # ------------------------------------------------------------------
    # Element resolution
    # ------------------------------------------------------------------
    def _timeout(self, timeout=None):
        return self.DEFAULT_TIMEOUT if timeout is None else timeout

    def element(self, locator):
        """Return the first match for `locator` without waiting."""
        return self.page.locator(locator).first

    def wait_for_visible(self, locator, timeout=None, state="visible"):
        """Wait until `locator` reaches `state` and return the element."""
        element = self.element(locator)
        element.wait_for(state=state, timeout=self._timeout(timeout))
        return element

    def first_visible(self, selectors, timeout=None):
        """Return the first selector in `selectors` that becomes visible.

        Returns ``None`` when none of them show up - callers decide whether
        that is a failure or a graceful skip.
        """
        wait = self._timeout(timeout)
        for selector in selectors:
            element = self.element(selector)
            try:
                element.wait_for(state="visible", timeout=wait)
                return element
            except Exception:
                continue
        return None

    def first_visible_in_any_frame(self, selectors, timeout_per_try=2500):
        """Like `first_visible`, but also searches inside every iframe.

        Chat/LTI screens render their controls inside nested frames, so a
        main-frame-only lookup silently misses them.
        """
        frames = [self.page.main_frame] + [f for f in self.page.frames if f != self.page.main_frame]
        for frame in frames:
            for selector in selectors:
                element = frame.locator(selector).first
                try:
                    element.wait_for(state="visible", timeout=timeout_per_try)
                    return element
                except Exception:
                    continue
        return None

    def is_visible(self, locator, timeout=SHORT_TIMEOUT):
        """True when `locator` becomes visible within `timeout`."""
        try:
            self.wait_for_visible(locator, timeout=timeout)
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Highlighting (used by the Allure screenshots to show what was acted on)
    # ------------------------------------------------------------------
    def highlight(self, target, duration=HIGHLIGHT_DURATION):
        """Outline an element in the browser; never fails the test."""
        from utils.helpers import highlight_element

        try:
            highlight_element(self.page, target, duration=duration)
        except Exception as error:
            log.debug("Could not highlight %s: %s", target, error)

    def show_element(self, element, duration=HIGHLIGHT_DURATION):
        """Scroll an element into view and highlight it."""
        self.scroll_into_view(element)
        self.highlight(element, duration=duration)
        self.pause(300)

    # ------------------------------------------------------------------
    # Click
    # ------------------------------------------------------------------
    def click(self, locator, description=None, timeout=None, state="visible", force=False):
        """Wait for `locator`, highlight it and click it."""
        wait = self._timeout(timeout)
        element = self.wait_for_visible(locator, timeout=wait, state=state)
        self.highlight(locator)
        self._click_element(element, wait, force=force)
        log.info("Clicked %s", description or locator)
        return element

    def click_first_visible(self, selectors, description=None, timeout=None):
        """Click the first visible selector. Returns False when none matched."""
        wait = self._timeout(timeout)
        element = self.first_visible(selectors, timeout=wait)
        if element is None:
            return False
        self.scroll_into_view(element)
        self.highlight(element)
        self._click_element(element, wait)
        log.info("Clicked %s", description or selectors[0])
        return True

    def click_required(self, selectors, description, timeout=None):
        """Click the first visible selector or fail with a readable message."""
        assert self.click_first_visible(selectors, description, timeout=timeout), \
            f"{description} is not visible/clickable"

    def _click_element(self, element, timeout, force=False):
        """Click with a forced-click fallback for overlay-covered elements."""
        if force:
            element.click(timeout=timeout, force=True)
            return
        try:
            element.click(timeout=timeout)
        except Exception:
            element.click(timeout=timeout, force=True)

    # ------------------------------------------------------------------
    # Text entry
    # ------------------------------------------------------------------
    def enter_text(self, locator, text, description=None, timeout=None, sensitive=False):
        """Fill an input, replacing any existing value."""
        element = self.wait_for_visible(locator, timeout=timeout)
        self.highlight(locator)
        element.fill(text)
        log.info("Entered %s in %s", "***" if sensitive else f"'{text}'", description or locator)
        return element

    def type_text(self, locator, text, description=None, timeout=None, delay=80, sensitive=False):
        """Type character by character - for inputs that need key events."""
        element = self.wait_for_visible(locator, timeout=timeout)
        self.highlight(locator)
        element.click()
        element.type(text, delay=delay)
        log.info("Typed %s in %s", "***" if sensitive else f"'{text}'", description or locator)
        return element

    def clear_text(self, locator, description=None, timeout=None):
        """Empty an input field."""
        element = self.wait_for_visible(locator, timeout=timeout)
        element.fill("")
        log.info("Cleared %s", description or locator)
        return element

    # ------------------------------------------------------------------
    # Dropdowns / checkboxes / radios
    # ------------------------------------------------------------------
    def select_dropdown_option(self, locator, value, description=None, timeout=None):
        """Select a value in a native <select> element."""
        element = self.wait_for_visible(locator, timeout=timeout)
        self.show_element(element)
        element.select_option(value)
        log.info("Selected '%s' in %s", value, description or locator)
        return element

    def dropdown_options(self, locator, timeout=None):
        """Return the option labels of a native <select> element."""
        element = self.wait_for_visible(locator, timeout=timeout)
        return element.locator("option").all_inner_texts()

    def open_dropdown_and_select(self, dropdown_locator, option_selectors, description, timeout=None):
        """Open a custom (non-native) dropdown and pick the first matching option."""
        self.click(dropdown_locator, f"{description} dropdown", timeout=timeout)
        self.click_required(option_selectors, f"{description} option", timeout=timeout)

    def set_checkbox(self, locator, checked=True, description=None, timeout=None):
        """Tick/untick a checkbox or radio only when it is not already there."""
        element = self.wait_for_visible(locator, timeout=timeout)
        self.highlight(locator)
        if element.is_checked() == checked:
            log.info("%s already %s", description or locator, "checked" if checked else "unchecked")
            return element
        element.check() if checked else element.uncheck()
        log.info("%s %s", description or locator, "checked" if checked else "unchecked")
        return element

    # ------------------------------------------------------------------
    # Reading state
    # ------------------------------------------------------------------
    def get_text(self, locator, timeout=None):
        """Return the trimmed inner text of an element."""
        return self.wait_for_visible(locator, timeout=timeout).inner_text().strip()

    def get_value(self, locator, timeout=None):
        """Return the trimmed value of an input element."""
        return (self.wait_for_visible(locator, timeout=timeout).input_value() or "").strip()

    def count(self, locator):
        """Number of elements matching `locator`."""
        return self.page.locator(locator).count()

    # ------------------------------------------------------------------
    # Waiting / synchronisation
    # ------------------------------------------------------------------
    def pause(self, milliseconds):
        """Deliberate fixed pause.

        Used only where the app has no observable end-state to wait for (CSS
        animations, debounce timers). Prefer an explicit wait wherever an
        element or load state can be waited on instead.
        """
        try:
            self.page.wait_for_timeout(milliseconds)
        except Exception as error:
            log.debug("Pause interrupted: %s", error)

    def wait_for_load(self, state="domcontentloaded", timeout=LONG_TIMEOUT):
        """Wait for a page load state; never raises."""
        try:
            self.page.wait_for_load_state(state, timeout=timeout)
        except Exception as error:
            log.debug("Load state '%s' not reached: %s", state, error)

    # ------------------------------------------------------------------
    # Scrolling
    # ------------------------------------------------------------------
    def scroll_into_view(self, target):
        """Scroll an element (locator string or Locator) into the viewport.

        Uses the browser's native scrollIntoView, which walks the real
        scrollable-ancestor chain; Playwright's own helper can report success
        while leaving the element at the edge of a nested scroll container and
        a later click then fails with "element is outside of the viewport".
        """
        element = self.element(target) if isinstance(target, str) else target
        try:
            element.evaluate("el => el.scrollIntoView({block: 'center', behavior: 'instant'})")
        except Exception:
            try:
                element.scroll_into_view_if_needed()
            except Exception as error:
                log.debug("Could not scroll element into view: %s", error)

    def scroll_to_bottom(self, max_attempts=25, pause_ms=350):
        """Scroll down until the page stops moving (lazy-rendered sections)."""
        last_scroll_top = -1
        for _ in range(max_attempts):
            current_scroll_top = self.page.evaluate(
                "() => document.scrollingElement ? document.scrollingElement.scrollTop : window.scrollY"
            )
            if current_scroll_top == last_scroll_top:
                break
            last_scroll_top = current_scroll_top
            self.page.evaluate(
                "() => {"
                "const el = document.scrollingElement || document.documentElement;"
                "el.scrollBy(0, Math.max(window.innerHeight * 0.8, 500));"
                "}"
            )
            self.pause(pause_ms)

    def click_arrow_until_end(self, selectors, max_clicks=15, pause_ms=300):
        """Click a carousel/pagination next-arrow until it stops being available."""
        clicked_any = False
        for _ in range(max_clicks):
            arrow = self.first_visible(selectors, timeout=2000)
            if arrow is None:
                break
            try:
                if not arrow.is_enabled():
                    break
            except Exception as _ignored:
                log.debug("Optional step in click_arrow_until_end() did not apply: %s", _ignored)
            self.show_element(arrow, duration=900)
            try:
                self._click_element(arrow, 2000)
            except Exception:
                break
            clicked_any = True
            self.pause(pause_ms)
        return clicked_any

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------
    def open_url(self, url, wait_until="domcontentloaded", timeout=NAVIGATION_TIMEOUT):
        """Navigate the current tab to `url`."""
        self.page.goto(url, wait_until=wait_until, timeout=timeout)
        log.info("Opened %s", url)

    def reload(self, wait_until="domcontentloaded", timeout=LONG_TIMEOUT):
        """Reload the current page; never raises."""
        try:
            self.page.reload(wait_until=wait_until, timeout=timeout)
        except Exception as error:
            log.debug("Reload did not settle: %s", error)

    def go_back(self):
        """Browser back; never raises."""
        try:
            self.page.go_back()
        except Exception as error:
            log.debug("Browser back failed: %s", error)

    def current_url(self):
        """Current URL, or an empty string if the page is gone."""
        try:
            return self.page.url
        except Exception:
            return ""

    # ------------------------------------------------------------------
    # Popups / new tabs / overlays
    # ------------------------------------------------------------------
    def open_in_new_tab_and_close(self, locator, description=None, timeout=None):
        """Click something that opens a new tab, then close it and come back."""
        element = self.wait_for_visible(locator, timeout=timeout)
        self.show_element(element)
        with self.page.context.expect_page() as new_page_info:
            element.click()
        new_tab = new_page_info.value
        new_tab.wait_for_load_state("domcontentloaded")
        new_tab.close()
        self.page.bring_to_front()
        log.info("Opened and closed the new tab from %s", description or locator)

    def press_escape(self):
        """Dismiss an open modal/drawer with the Escape key; never raises."""
        try:
            self.page.keyboard.press("Escape")
        except Exception as error:
            log.debug("Escape key press failed: %s", error)

    def dismiss_if_present(self, selectors, description="popup", timeout=SHORT_TIMEOUT):
        """Close an optional overlay. Returns True when something was closed."""
        if self.click_first_visible(selectors, description, timeout=timeout):
            return True
        log.info("%s not present - nothing to dismiss", description)
        return False

    def close_extra_tabs(self):
        """Close every tab except the one this page object drives."""
        try:
            for tab in list(self.page.context.pages):
                if tab is not self.page and not tab.is_closed():
                    tab.close()
        except Exception as error:
            log.debug("Could not close extra tabs: %s", error)

    # ------------------------------------------------------------------
    # Assertions
    # ------------------------------------------------------------------
    def validate_visible(self, locator, description, timeout=None):
        """Assert an element is visible, highlighting it for the report."""
        element = self.wait_for_visible(locator, timeout=timeout)
        self.highlight(locator)
        assert element.is_visible(), f"{description} is not visible"
        log.info("Validated %s", description)
        return element

    def validate_any_visible(self, selectors, description, timeout=None):
        """Assert at least one of `selectors` is visible and return it."""
        element = self.first_visible(selectors, timeout=timeout)
        assert element is not None, f"{description} is not visible"
        self.show_element(element)
        log.info("Validated %s", description)
        return element

    def validate_text(self, locator, expected_text, timeout=None):
        """Assert an element's inner text contains `expected_text`."""
        actual_text = self.get_text(locator, timeout=timeout).lower()
        assert expected_text.lower() in actual_text, \
            f"Expected '{expected_text}' to be in '{actual_text}'"
        log.info("Validated text '%s' in %s", expected_text, locator)
        return actual_text
