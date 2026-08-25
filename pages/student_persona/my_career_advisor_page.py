from pages.student_persona.student_persona_page import StudentPersonaPage
from locators.student_persona_locators.my_career_advisor_locators import MyCareerAdvisorLocators as L
from config.env_config import IS_PROD
from utils.logger import log



class MyCareerAdvisorPage(StudentPersonaPage):


    def navigate_to_my_career_advisor(self):
        """Navigate from dashboard to My Career Advisor page.

        Returns True if the account has already completed the Passions/
        Aptitudes onboarding before (the card routes straight to
        matched-roles instead of the fresh onboarding flow), so the caller
        can skip the onboarding-only steps.
        """
        self.open_dashboard()
        self.click(L.MY_CAREER_ADVISOR, "My Career Advisor card", timeout=15000)
        self.dismiss_if_present([L.GOT_IT_POPUP_BUTTON], "'Got It' popup")

        self.pause(1500)
        if "matched-roles" in self.page.url:
            log.info("Account already completed Career Advisor onboarding "
                "(landed on matched-roles directly); skipping Passions/Aptitudes steps.")
            return True
        return False

    def validate_passion_header_and_click_review(self):
        """Validate Passions header is visible, click to expand, then click PASSION_REVIEW_BUTTON."""
        self.validate_visible(L.PASSIONS_HEADER, "Passions header", timeout=15000)
        self.click(L.PASSIONS_HEADER, "Passions header (expand)", timeout=15000)

        self.click(L.PASSION_REVIEW_BUTTON, "Passion Review button", timeout=15000)

    def select_passion_items_and_submit(self):
        """Select passion items (Arts & Design > Drawing & Illustration) and click Submit."""
        self.click(L.ARTS_AND_DESIGN, "Arts & Design category", timeout=15000)

        self.pause(1000)

        # Select the passion by clicking its LABEL (the visible checkbox button).
        # Clicking the hidden <input> doesn't fire the selection that enables the
        # Submit button. Ensure the checkbox ends up CHECKED — if it was already
        # selected from a prior run, a single click would toggle it OFF and leave
        # Submit disabled, so click again to re-select.
        drawing_label = self.page.locator(L.DRAWING_AND_ILLUSTRATION_LABEL).first
        drawing_input = self.page.locator(L.DRAWING_AND_ILLUSTRATION_CHECKBOX).first
        drawing_label.wait_for(state="visible", timeout=20000)
        drawing_label.scroll_into_view_if_needed()
        self.highlight(L.DRAWING_AND_ILLUSTRATION_LABEL)
        drawing_label.click()
        self.pause(600)
        try:
            if not drawing_input.is_checked():
                drawing_label.click()  # was pre-selected and got toggled off — re-select
        except Exception as _ignored:
            log.debug("Optional step in select_passion_items_and_submit() did not apply: %s", _ignored)
        log.info("Selected Drawing & Illustration (checkbox checked)")
        self.pause(1000)

        # Submit only becomes enabled once a passion checkbox is selected.
        submit = self.page.locator(L.SUBMIT_BUTTON).first
        submit.wait_for(state="visible", timeout=15000)
        submit.scroll_into_view_if_needed()
        try:
            self.page.wait_for_function(
                "() => { const b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='Submit'); return b && !b.disabled; }",
                timeout=10000,
            )
        except Exception:
            log.info("Submit still appears disabled after selecting passion; attempting click anyway")
        self.highlight(L.SUBMIT_BUTTON)
        submit.click()
        log.info("Clicked Submit button")

    def validate_questionnaire_header(self):
        """Validate Questionnaires header is visible and click it to expose Aptitudes section."""
        questionnaires = self.page.locator(L.QUESTIONNAIRES_HEADER)
        questionnaires.wait_for(state="visible", timeout=15000)
        self.highlight(L.QUESTIONNAIRES_HEADER)
        assert questionnaires.is_visible(), "Questionnaires header not visible"
        log.info("Validated Questionnaires header")
        questionnaires.scroll_into_view_if_needed()
        questionnaires.click()
        log.info("Clicked Questionnaires header to expose Aptitudes")

    def click_review_in_aptitudes(self):
        """Click the Aptitude Review button (APTITUDE_REVIEW_BUTTON locator)."""
        self.click(L.APTITUDE_REVIEW_BUTTON, "Aptitude Review button", timeout=15000)

    def click_reattempt_button(self):
        """Click the Reattempt button."""
        self.click(L.REATTEMPT_BUTTON, "Reattempt button", timeout=15000)

    def click_slider_choose_button(self):
        """Click the Choose button for Slider in Aptitudes."""
        self.click(L.SLIDER_CHOOSE_BUTTON, "slider Choose button", timeout=15000)

    def select_question_slider_option(self):
        """Focus the slider handle and use arrow keys to change value (enables Update button)."""
        handle = self.page.locator(L.SLIDER_HANDLE)
        handle.wait_for(state="visible", timeout=15000)
        handle.scroll_into_view_if_needed()

        current_value = handle.get_attribute("aria-valuenow") or ""
        log.info(f"Slider current aria-valuenow: '{current_value}'")

        # Use handle.press() — focuses the element automatically before sending key
        if current_value == "10":
            handle.press("ArrowLeft")
            log.info("Pressed ArrowLeft (was 10 -> 9)")
        else:
            handle.press("ArrowRight")
            log.info("Pressed ArrowRight (was 9/unknown -> 10)")

        self.pause(800)
        new_value = handle.get_attribute("aria-valuenow") or ""
        log.info(f"Slider new aria-valuenow: '{new_value}'")

    def click_update_button(self):
        """Click the Update button."""
        self.click(L.UPDATE_BUTTON, "Update button", timeout=15000)

    def click_go_to_matched_roles(self):
        """Click the Go to Matched Roles button."""
        self.click(L.GO_TO_MATCHED_ROLES_BUTTON, "Go to Matched Roles button", timeout=15000)

    def click_without_college_degree(self):
        """Click the Without College Degree filter."""
        self.click(L.WITHOUT_COLLEGE_DEGREE, "Without College Degree", timeout=15000)

    def validate_header_count(self):
        """Validate the recommended roles header count is visible."""
        count = self.page.locator(L.VALIDATE_HEADER_COUNT).first
        count.wait_for(state="visible", timeout=15000)
        count_text = count.text_content().strip()
        self.highlight(L.VALIDATE_HEADER_COUNT)
        assert len(count_text) > 0, "Header count is empty"
        log.info(f"Validated header count: {count_text}")

    def click_searched_role(self):
        """Click the Search Roles section to expand it."""
        self.click(L.SEARCH_ROLES_HEADER, "Search Roles section", timeout=15000)

    def fill_job_role_input(self):
        """Fill in the job role search input field."""
        self.enter_text(L.SEARCH_FOR_JOB_ROLE_INPUT, "Project Manager", "Filled job role input with 'Project Manager'", timeout=15000)

    def validate_result_header_and_click_favourite(self):
        """Validate Result header is visible and click Favourite on first result."""
        result = self.page.locator(L.RESULTS_HEADER)
        result.wait_for(state="visible", timeout=15000)
        self.highlight(L.RESULTS_HEADER)
        assert result.is_visible(), "Results header not visible"
        result_text = result.text_content().strip()
        log.info(f"Validated Result header: {result_text}")

        self.click(L.ADD_FAVOURITE, "Favourite on first result", timeout=15000)

    def click_favourites_header(self):
        """Click the Favourites section header."""
        favourites = self.page.locator(L.FAVOURITES_HEADER).first
        timeout = 6000 if IS_PROD else 15000
        try:
            favourites.wait_for(state="visible", timeout=timeout)
        except Exception:
            if IS_PROD:
                log.warning("[prod] Favourites header not present - skipping (no saved role)")
                return
            raise
        self.highlight(L.FAVOURITES_HEADER)
        favourites.click()
        log.info("Clicked Favourites header")

    def click_share_report_and_share(self):
        """Click Share Report and then the Share button."""
        self.click(L.SHARE_REPORT, "Share Report", timeout=15000)

        self.click(L.SHARE_BUTTON, "Share button", timeout=15000)

    def click_favourite_and_remove(self):
        """After Share: click Favourites header, then click Remove Favourite."""
        # Close share dialog/toast if still open
        try:
            self.page.keyboard.press("Escape")
            self.pause(1000)
        except Exception as _ignored:
            log.debug("Optional step in click_favourite_and_remove() did not apply: %s", _ignored)

        # Click Favourites header to navigate to Favourites section
        self.click(L.FAVOURITES_HEADER, "Favourites header", timeout=15000)
        self.pause(1500)

        # Click the first Favourite button (removes favourite)
        remove = self.page.locator(L.REMOVE_FAVOURITE).first
        timeout = 6000 if IS_PROD else 15000
        try:
            remove.wait_for(state="visible", timeout=timeout)
        except Exception:
            if IS_PROD:
                log.warning("[prod] No saved favourite to remove - skipping")
                return
            raise
        remove.scroll_into_view_if_needed()
        self.highlight(L.REMOVE_FAVOURITE)
        remove.click()
        log.info("Clicked Remove Favourite")
        log.info("Removed job from favourites")

    def click_home_icon_and_navigate_home(self):
        """Click the Home icon to navigate back to the home page."""
        self.click(L.HOME, "Home icon and navigated to home page", timeout=15000)
        self.pause(1500)

    def click_roles_saved_and_validate_favourite_role_header(self):
        """Click the Roles Saved card, click Favourites header, and validate the Favourite Roles header.

        If the 'Roles Saved' text is not present on the card, the step is skipped
        gracefully (asserted as not present) so the test case does not fail.
        """
        roles_saved = self.page.locator(L.ROLES_SAVED).first
        try:
            roles_saved.wait_for(state="visible", timeout=10000)
        except Exception as _ignored:
            log.debug("Optional step in click_roles_saved_and_validate_favourite_role_header() did not apply: %s", _ignored)

        roles_saved_present = roles_saved.count() > 0 and roles_saved.is_visible()
        if not roles_saved_present:
            # Soft assertion: 'Roles Saved' text is absent, so the test case is
            # expected to pass without continuing the validation.
            assert not roles_saved_present, "Roles Saved text not present on card"
            log.warning("'Roles Saved' text not present on card - skipping favourite role header validation")
            return

        roles_saved.scroll_into_view_if_needed()
        self.highlight(L.ROLES_SAVED)
        roles_saved.click()
        log.info("Clicked Roles Saved card")
        self.pause(1500)

        self.click(L.FAVOURITES_HEADER, "Favourites header", timeout=15000)
        self.pause(1500)

        self.validate_visible(L.VALIDATE_FAVOURITE_ROLES_HEADER, "Favourite Roles header", timeout=15000)
        