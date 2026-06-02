from pages.base_page import BasePage
from locators.mentor_locators.myprofile_locators import myprofileLocators


class MentorProfilePage(BasePage):

    def click_profile_icon(self):
        self.page.locator(myprofileLocators.PROFILE_ICON).wait_for(state="visible", timeout=15000)
        self.page.click(myprofileLocators.PROFILE_ICON)
        print("Clicked on Profile Icon")
        # Wait for any resulting navigation to fully settle
        try:
            self.page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            self.page.wait_for_timeout(2000)

    def validate_profile_page(self):
        self.page.locator(myprofileLocators.VALIDATE_PROFILE_INFORMATION_HEADER).wait_for(state="visible", timeout=15000)
        header_text = self.page.locator(myprofileLocators.VALIDATE_PROFILE_INFORMATION_HEADER).inner_text().strip()
        assert len(header_text) > 0, f"Profile page header not found or empty"
        print(f"Profile page validated — header: '{header_text}'")
        # Wait for the page to fully settle (avoids TargetClosedError on next step)
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            self.page.wait_for_timeout(1500)

    def _select_city(self, search_text, option_locator):
        """Open the city ant-select dropdown, type to search, and click the matching option."""
        city_div = self.page.locator(myprofileLocators.SELECT_CITY_INPUT)
        city_div.scroll_into_view_if_needed()
        city_div.wait_for(state="visible", timeout=10000)
        city_div.click()
        self.page.wait_for_timeout(500)
        # Use JS to fill the now-active ant-select search input and fire React events
        self.page.evaluate(f"""() => {{
            const input = document.querySelector('.ant-select-selection-search input');
            if (input) {{
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                nativeInputValueSetter.call(input, '{search_text}');
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }}""")
        self.page.wait_for_timeout(2000)
        # Try exact locator first, fall back to contains-text
        option = self.page.locator(option_locator)
        try:
            option.wait_for(state="visible", timeout=6000)
        except Exception:
            option = self.page.locator(
                f"//div[contains(@class,'ant-select-item-option-content')][contains(.,'{search_text}')]"
            )
            option.first.wait_for(state="visible", timeout=8000)
        option.first.click()
        self.page.wait_for_timeout(500)

    def _ensure_edit_mode(self):
        """Click the Edit button if input fields are not yet editable."""
        try:
            self.page.locator(myprofileLocators.FIRSTNAME).wait_for(state="visible", timeout=5000)
        except Exception:
            # Try clicking an Edit button to unlock the form
            try:
                edit_btn = self.page.locator("//button[text()='Edit']")
                edit_btn.wait_for(state="visible", timeout=8000)
                edit_btn.click()
                print("Clicked Edit button to enter edit mode")
                self.page.wait_for_timeout(1000)
            except Exception:
                pass

    def change_firstname_lastname_city_and_save(self):
        # Ensure the form fields are editable
        self._ensure_edit_mode()

        # Clear and update First Name
        firstname_input = self.page.locator(myprofileLocators.FIRSTNAME)
        firstname_input.scroll_into_view_if_needed()
        firstname_input.wait_for(state="visible", timeout=10000)
        current_firstname = firstname_input.input_value()
        # Store originals on page object for revert step
        self.page._original_firstname = current_firstname
        firstname_input.click(click_count=3)
        firstname_input.fill("TestFirst")
        print(f"Changed firstname from '{current_firstname}' to 'TestFirst'")

        # Clear and update Last Name
        lastname_input = self.page.locator(myprofileLocators.LASTNAME)
        lastname_input.wait_for(state="visible", timeout=10000)
        current_lastname = lastname_input.input_value()
        self.page._original_lastname = current_lastname
        lastname_input.click(click_count=3)
        lastname_input.fill("TestLast")
        print(f"Changed lastname from '{current_lastname}' to 'TestLast'")

        # Update City — search and pick Bengaluru
        self._select_city("Bengaluru", myprofileLocators.BENGALURU_OPTION)
        print("Selected city: Bengaluru")

        # Save
        self.page.locator(myprofileLocators.SAVE_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.click(myprofileLocators.SAVE_BUTTON)
        print("Saved profile with updated firstname, lastname, and city")
        self.page.wait_for_timeout(2000)

    def revert_firstname_lastname_city_and_save(self):
        original_firstname = getattr(self.page, "_original_firstname", "TestFirst")
        original_lastname = getattr(self.page, "_original_lastname", "TestLast")

        # Ensure the form fields are editable
        self._ensure_edit_mode()

        # Revert First Name
        firstname_input = self.page.locator(myprofileLocators.FIRSTNAME)
        firstname_input.scroll_into_view_if_needed()
        firstname_input.wait_for(state="visible", timeout=10000)
        firstname_input.click(click_count=3)
        firstname_input.fill(original_firstname)
        print(f"Reverted firstname to '{original_firstname}'")

        # Revert Last Name
        lastname_input = self.page.locator(myprofileLocators.LASTNAME)
        lastname_input.wait_for(state="visible", timeout=10000)
        lastname_input.click(click_count=3)
        lastname_input.fill(original_lastname)
        print(f"Reverted lastname to '{original_lastname}'")

        # Revert City back to Hyderabad
        self._select_city("Hyderabad", myprofileLocators.HYDERABAD_OPTION)
        print("Reverted city to: Hyderabad")

        # Save
        self.page.locator(myprofileLocators.SAVE_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.click(myprofileLocators.SAVE_BUTTON)
        print("Saved profile with reverted firstname, lastname, and city")
        self.page.wait_for_timeout(2000)

    def _select_language(self, dropdown_locator, search_text, option_locator):
        """Open a language ant-select dropdown and pick the matching option."""
        dropdown = self.page.locator(dropdown_locator)
        dropdown.scroll_into_view_if_needed()
        dropdown.wait_for(state="visible", timeout=10000)
        dropdown.click()
        self.page.wait_for_timeout(500)
        # Fill the active search input via JS to trigger React's onChange
        self.page.evaluate(f"""() => {{
            const input = document.querySelector('.ant-select-selection-search input');
            if (input) {{
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                nativeInputValueSetter.call(input, '{search_text}');
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }}""")
        self.page.wait_for_timeout(1500)
        option = self.page.locator(option_locator)
        try:
            option.wait_for(state="visible", timeout=6000)
        except Exception:
            option = self.page.locator(
                f"//div[contains(@class,'ant-select-item-option-content')][contains(.,'{search_text}')]"
            )
            option.first.wait_for(state="visible", timeout=8000)
        option.first.click()
        self.page.wait_for_timeout(500)

    def change_language_to_spanish_and_save(self):
        self._select_language(
            myprofileLocators.LANGUAGE_DROPDOWN_ENGLISH,
            "Spanish",
            myprofileLocators.SPANISH_LANGUAGE
        )
        print("Selected language: Spanish")

        # Save
        self.page.locator(myprofileLocators.SAVE_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.click(myprofileLocators.SAVE_BUTTON)
        print("Saved profile with Spanish language")
        self.page.wait_for_timeout(2000)

    def revert_language_to_english_and_save(self):
        # After switching to Spanish the UI changes — use Spanish-label dropdown locator
        dropdown = self.page.locator(myprofileLocators.LANGUAGE_DROPDOWN_SPANISH)
        dropdown.scroll_into_view_if_needed()
        dropdown.wait_for(state="visible", timeout=10000)
        dropdown.click()
        self.page.wait_for_timeout(1000)

        # First try: options may appear without typing (single-select opens full list)
        option = self.page.locator("//span[text()='English' or text()='Inglés']")
        try:
            option.first.wait_for(state="visible", timeout=4000)
            option.first.click()
            print("Selected language: English (direct click)")
        except Exception:
            # Second try: type via keyboard to filter
            self.page.keyboard.type("Eng", delay=50)
            self.page.wait_for_timeout(1500)
            option2 = self.page.locator(
                "//span[text()='English' or text()='Inglés']"
                " | //div[contains(@class,'ant-select-item-option-content')][contains(.,'nglish') or contains(.,'nglés')]"
            )
            option2.first.wait_for(state="visible", timeout=6000)
            option2.first.click()
            print("Selected language: English (keyboard filter)")
        self.page.wait_for_timeout(500)

        # Save (button label is 'Guardar' when UI is in Spanish)
        self.page.locator(myprofileLocators.Guardar_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.click(myprofileLocators.Guardar_BUTTON)
        print("Saved profile with reverted language to English")
        self.page.wait_for_timeout(3000)
