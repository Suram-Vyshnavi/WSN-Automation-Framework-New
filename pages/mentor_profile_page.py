from pages.base_page import BasePage
from locators.mentor_locators.my_profile_locators import MyProfileLocators
from utils.logger import log


class MentorProfilePage(BasePage):

    def _dismiss_marketing_overlay(self):
        """Dismiss transient marketing overlays (e.g. CleverTap) that can
        intercept clicks on the profile avatar."""
        # First try explicit close controls.
        for selector in [
            "#wzrk-cancel",
            "#wzrk-close",
            "//*[@id='wzrkImageOnlyDiv']//button[contains(@aria-label,'close') or contains(@class,'close')]",
            "//*[@id='wzrkImageOnlyDiv']//*[contains(@class,'close')]",
        ]:
            try:
                btn = self.page.locator(selector).first
                btn.wait_for(state="visible", timeout=1000)
                btn.click(timeout=2000, force=True)
                self.pause(300)
            except Exception:
                continue

        # If still present, remove the overlay node as last resort.
        try:
            self.page.evaluate(
                """() => {
                    const ids = ['wzrkImageOnlyDiv', 'wzrk_wrapper', 'wzrk_popup'];
                    ids.forEach(id => {
                        const el = document.getElementById(id);
                        if (el) el.remove();
                    });
                    const floating = document.querySelectorAll('ct-web-popup-imageonly, [id*="wzrk"], [class*="wzrk"]');
                    floating.forEach(el => {
                        try { el.remove(); } catch (_) {}
                    });
                }"""
            )
        except Exception as _ignored:
            log.debug("Optional step in _dismiss_marketing_overlay() did not apply: %s", _ignored)

    def click_profile_icon(self):
        self._dismiss_marketing_overlay()
        self.page.locator(MyProfileLocators.PROFILE_ICON).wait_for(state="visible", timeout=15000)
        try:
            self.click(MyProfileLocators.PROFILE_ICON, "profile icon")
        except Exception:
            self._dismiss_marketing_overlay()
            self.page.locator(MyProfileLocators.PROFILE_ICON).first.click(force=True)
        log.info("Clicked on Profile Icon")
        # Wait for any resulting navigation to fully settle
        try:
            self.page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            self.pause(2000)

    def validate_profile_page(self):
        self.page.locator(MyProfileLocators.VALIDATE_PROFILE_INFORMATION_HEADER).wait_for(state="visible", timeout=15000)
        header_text = self.page.locator(MyProfileLocators.VALIDATE_PROFILE_INFORMATION_HEADER).inner_text().strip()
        assert len(header_text) > 0, f"Profile page header not found or empty"
        log.info(f"Profile page validated — header: '{header_text}'")
        # Wait for the page to fully settle (avoids TargetClosedError on next step)
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            self.pause(1500)

    def _select_city(self, search_text, option_locator):
        """Open the city ant-select dropdown, type to search, and click the matching option."""
        city_div = self.page.locator(MyProfileLocators.SELECT_CITY_INPUT)
        city_div.scroll_into_view_if_needed()
        city_div.wait_for(state="visible", timeout=10000)
        city_div.click()
        self.pause(500)
        # Clicking the select focuses ITS search input, so type via the keyboard.
        # (A global querySelector for '.ant-select-selection-search input' can hit
        # the wrong select on a page with multiple ant-selects, e.g. the language
        # dropdown, leaving the city list unfiltered.)
        self.page.keyboard.press("Control+A")  # clear any pre-filled text
        self.page.keyboard.type(search_text, delay=50)
        self.pause(2000)
        # Try exact locator first, fall back to contains-text
        option = self.page.locator(option_locator)
        try:
            option.wait_for(state="visible", timeout=6000)
        except Exception:
            option = self.page.locator(
                f"//div[contains(@class,'ant-select-item-option-content')][contains(.,'{search_text}')]"
            )
            option.first.wait_for(state="visible", timeout=8000)
        # The dropdown option may be geometrically outside the viewport — scroll it into
        # view first, then fall back to force=True if a normal click still fails.
        try:
            option.first.scroll_into_view_if_needed(timeout=3000)
        except Exception as _ignored:
            log.debug("Optional step in _select_city() did not apply: %s", _ignored)
        try:
            option.first.click(timeout=5000)
        except Exception:
            option.first.click(force=True)
        self.pause(500)

    def _ensure_edit_mode(self):
        """Click the Edit button if input fields are not yet editable."""
        try:
            self.page.locator(MyProfileLocators.FIRSTNAME).wait_for(state="visible", timeout=5000)
        except Exception:
            # Try clicking an Edit button to unlock the form
            try:
                edit_btn = self.page.locator("//button[text()='Edit']")
                edit_btn.wait_for(state="visible", timeout=8000)
                edit_btn.click()
                log.info("Clicked Edit button to enter edit mode")
                self.pause(1000)
            except Exception as _ignored:
                log.debug("Optional step in _ensure_edit_mode() did not apply: %s", _ignored)

    def change_firstname_lastname_city_and_save(self):
        # Ensure the form fields are editable
        self._ensure_edit_mode()

        # Clear and update First Name
        firstname_input = self.page.locator(MyProfileLocators.FIRSTNAME)
        firstname_input.scroll_into_view_if_needed()
        firstname_input.wait_for(state="visible", timeout=10000)
        current_firstname = firstname_input.input_value()
        # Store originals on page object for revert step
        self.page._original_firstname = current_firstname
        firstname_input.click(click_count=3)
        firstname_input.fill("TestFirst")
        log.info(f"Changed firstname from '{current_firstname}' to 'TestFirst'")

        # Clear and update Last Name
        lastname_input = self.page.locator(MyProfileLocators.LASTNAME)
        lastname_input.wait_for(state="visible", timeout=10000)
        current_lastname = lastname_input.input_value()
        self.page._original_lastname = current_lastname
        lastname_input.click(click_count=3)
        lastname_input.fill("TestLast")
        log.info(f"Changed lastname from '{current_lastname}' to 'TestLast'")

        # Update City — search and pick Bengaluru
        self._select_city("Bengaluru", MyProfileLocators.BENGALURU_OPTION)
        log.info("Selected city: Bengaluru")

        # Save
        self.click(MyProfileLocators.SAVE_BUTTON, "save button", timeout=10000)
        log.info("Saved profile with updated firstname, lastname, and city")
        self.pause(2000)

    def revert_firstname_lastname_city_and_save(self):
        original_firstname = getattr(self.page, "_original_firstname", "TestFirst")
        original_lastname = getattr(self.page, "_original_lastname", "TestLast")

        # Ensure the form fields are editable
        self._ensure_edit_mode()

        # Revert First Name
        firstname_input = self.page.locator(MyProfileLocators.FIRSTNAME)
        firstname_input.scroll_into_view_if_needed()
        firstname_input.wait_for(state="visible", timeout=10000)
        firstname_input.click(click_count=3)
        firstname_input.fill(original_firstname)
        log.info(f"Reverted firstname to '{original_firstname}'")

        # Revert Last Name
        lastname_input = self.page.locator(MyProfileLocators.LASTNAME)
        lastname_input.wait_for(state="visible", timeout=10000)
        lastname_input.click(click_count=3)
        lastname_input.fill(original_lastname)
        log.info(f"Reverted lastname to '{original_lastname}'")

        # Revert City back to Hyderabad
        self._select_city("Hyderabad", MyProfileLocators.HYDERABAD_OPTION)
        log.info("Reverted city to: Hyderabad")

        # Save
        self.click(MyProfileLocators.SAVE_BUTTON, "save button", timeout=10000)
        log.info("Saved profile with reverted firstname, lastname, and city")
        self.pause(2000)

    def _select_language(self, dropdown_locator, search_text, option_locator):
        """Open a language ant-select dropdown and pick the matching option."""
        dropdown = self.page.locator(dropdown_locator)
        dropdown.scroll_into_view_if_needed()
        dropdown.wait_for(state="visible", timeout=10000)
        dropdown.click()
        self.pause(500)
        # Type into the focused search input of THIS dropdown (see _select_city
        # for why a global querySelector is unreliable with multiple ant-selects).
        self.page.keyboard.type(search_text, delay=50)
        self.pause(1500)
        option = self.page.locator(option_locator)
        try:
            option.wait_for(state="visible", timeout=6000)
        except Exception:
            option = self.page.locator(
                f"//div[contains(@class,'ant-select-item-option-content')][contains(.,'{search_text}')]"
            )
            option.first.wait_for(state="visible", timeout=8000)
        option.first.click()
        self.pause(500)

    def change_language_to_spanish_and_save(self):
        self._select_language(
            MyProfileLocators.LANGUAGE_DROPDOWN_ENGLISH,
            "Spanish",
            MyProfileLocators.SPANISH_LANGUAGE
        )
        log.info("Selected language: Spanish")

        # Save
        self.click(MyProfileLocators.SAVE_BUTTON, "save button", timeout=10000)
        log.info("Saved profile with Spanish language")
        self.pause(2000)

    def revert_language_to_english_and_save(self):
        # After switching to Spanish the UI changes — use Spanish-label dropdown locator
        dropdown = self.page.locator(MyProfileLocators.LANGUAGE_DROPDOWN_SPANISH)
        dropdown.scroll_into_view_if_needed()
        dropdown.wait_for(state="visible", timeout=10000)
        dropdown.click()
        self.pause(1000)

        # First try: options may appear without typing (single-select opens full list)
        option = self.page.locator("//span[text()='English' or text()='Inglés']")
        try:
            option.first.wait_for(state="visible", timeout=4000)
            option.first.click()
            log.info("Selected language: English (direct click)")
        except Exception:
            # Second try: type via keyboard to filter
            self.page.keyboard.type("Eng", delay=50)
            self.pause(1500)
            option2 = self.page.locator(
                "//span[text()='English' or text()='Inglés']"
                " | //div[contains(@class,'ant-select-item-option-content')][contains(.,'nglish') or contains(.,'nglés')]"
            )
            option2.first.wait_for(state="visible", timeout=6000)
            option2.first.click()
            log.info("Selected language: English (keyboard filter)")
        self.pause(500)

        # Save (button label is 'Guardar' when UI is in Spanish)
        self.click(MyProfileLocators.GUARDAR_BUTTON, "guardar button", timeout=10000)
        log.info("Saved profile with reverted language to English")
        self.pause(3000)
