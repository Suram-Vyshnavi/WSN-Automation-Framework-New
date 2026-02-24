class BasePage:
    def __init__(self, page):
        self.page = page
    def validate_using_inner_text(self, locator, expected_text, timeout=10000):
        """Validate that the element located by `locator` contains `expected_text` in its inner text."""
        element = self.page.locator(locator)
        element.wait_for(state="visible", timeout=timeout)
        actual_text = element.inner_text().strip().lower()
        assert expected_text.lower() in actual_text, f"Expected '{expected_text}' to be in '{actual_text}'"
        print(f"Validated text '{expected_text}' is present in element located by '{locator}'")