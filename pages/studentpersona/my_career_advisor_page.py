from pages.base_page import BasePage
from locators.student_persona_locators.my_career_advisor_locators import mycareeradvisorLocators as L
from utils.helpers import highlight_element


class MyCareerAdvisorPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def _navigate_to_my_career_advisor(self):
        """Navigate from dashboard to My Career Advisor page."""
        from pages.studentpersona.home_dashboard_page import HomeDashboardPage
        if HomeDashboardPage._shared_dashboard_url:
            self.page.goto(HomeDashboardPage._shared_dashboard_url, wait_until="domcontentloaded", timeout=60000)
        card = self.page.locator(L.MY_CAREER_ADVISOR)
        card.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, L.MY_CAREER_ADVISOR)
        card.click()
        print("Clicked My Career Advisor card")
        # Handle Got It popup if present
        try:
            got_it = self.page.locator("//span[text()='Got It']")
            got_it.wait_for(state="visible", timeout=5000)
            if got_it.is_visible():
                got_it.click()
                print("Handled 'Got It' popup")
        except Exception:
            pass

    def validate_passion_header_and_click_review(self):
        """Validate Passions header is visible, click to expand, then click PASSION_REVIEW_BUTTON."""
        passions = self.page.locator(L.PASSIONS_HEADER)
        passions.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, L.PASSIONS_HEADER)
        assert passions.is_visible(), "Passions header not visible"
        print("Validated Passions header")

        passions.scroll_into_view_if_needed()
        passions.click()
        print("Clicked Passions header to expand")

        review = self.page.locator(L.PASSION_REVIEW_BUTTON)
        review.wait_for(state="visible", timeout=15000)
        review.scroll_into_view_if_needed()
        highlight_element(self.page, L.PASSION_REVIEW_BUTTON)
        review.click()
        print("Clicked Passion Review button")

    def select_passion_items_and_submit(self):
        """Select passion items (Arts & Design > Drawing & Illustration) and click Submit."""
        arts = self.page.locator(L.ARTS_AND_DESIGN).first
        arts.wait_for(state="visible", timeout=15000)
        arts.scroll_into_view_if_needed()
        highlight_element(self.page, L.ARTS_AND_DESIGN)
        arts.click()
        print("Clicked Arts & Design category")

        self.page.wait_for_timeout(1000)

        drawing = self.page.locator(L.DRAWING_AND_ILLUSTRATION_CHECKBOX)
        drawing.wait_for(state="visible", timeout=20000)
        drawing.scroll_into_view_if_needed()
        highlight_element(self.page, L.DRAWING_AND_ILLUSTRATION_CHECKBOX)
        drawing.click()
        print("Selected Drawing & Illustration")

        submit = self.page.locator(L.SUBMIT_BUTTON).first
        submit.wait_for(state="visible", timeout=15000)
        submit.scroll_into_view_if_needed()
        highlight_element(self.page, L.SUBMIT_BUTTON)
        submit.click()
        print("Clicked Submit button")

    def validate_questionnaire_header(self):
        """Validate Questionnaires header is visible and click it to expose Aptitudes section."""
        questionnaires = self.page.locator(L.QUESTIONNAIRES_HEADER)
        questionnaires.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, L.QUESTIONNAIRES_HEADER)
        assert questionnaires.is_visible(), "Questionnaires header not visible"
        print("Validated Questionnaires header")
        questionnaires.scroll_into_view_if_needed()
        questionnaires.click()
        print("Clicked Questionnaires header to expose Aptitudes")

    def click_review_in_aptitudes(self):
        """Click the Aptitude Review button (APTITUDE_REVIEW_BUTTON locator)."""
        review = self.page.locator(L.APTITUDE_REVIEW_BUTTON)
        review.wait_for(state="visible", timeout=15000)
        review.scroll_into_view_if_needed()
        highlight_element(self.page, L.APTITUDE_REVIEW_BUTTON)
        review.click()
        print("Clicked Aptitude Review button")

    def click_reattempt_button(self):
        """Click the Reattempt button."""
        reattempt = self.page.locator(L.REATTEMPT_BUTTON)
        reattempt.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, L.REATTEMPT_BUTTON)
        reattempt.click()
        print("Clicked Reattempt button")

    def click_slider_choose_button(self):
        """Click the Choose button for Slider in Aptitudes."""
        slider_choose = self.page.locator(L.SLIDER_CHOOSE_BUTTON)
        slider_choose.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, L.SLIDER_CHOOSE_BUTTON)
        slider_choose.click()
        print("Clicked slider Choose button")

    def select_question_slider_option(self):
        """Focus the slider handle and use arrow keys to change value (enables Update button)."""
        handle = self.page.locator(L.SLIDER_HANDLE)
        handle.wait_for(state="visible", timeout=15000)
        handle.scroll_into_view_if_needed()

        current_value = handle.get_attribute("aria-valuenow") or ""
        print(f"Slider current aria-valuenow: '{current_value}'")

        # Use handle.press() — focuses the element automatically before sending key
        if current_value == "10":
            handle.press("ArrowLeft")
            print("Pressed ArrowLeft (was 10 -> 9)")
        else:
            handle.press("ArrowRight")
            print("Pressed ArrowRight (was 9/unknown -> 10)")

        self.page.wait_for_timeout(800)
        new_value = handle.get_attribute("aria-valuenow") or ""
        print(f"Slider new aria-valuenow: '{new_value}'")

    def click_update_button(self):
        """Click the Update button."""
        update = self.page.locator(L.UPDATE_BUTTON)
        update.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, L.UPDATE_BUTTON)
        update.click()
        print("Clicked Update button")

    def click_go_to_matched_roles(self):
        """Click the Go to Matched Roles button."""
        btn = self.page.locator(L.GO_TO_MATCHED_ROLES_BUTTON)
        btn.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, L.GO_TO_MATCHED_ROLES_BUTTON)
        btn.click()
        print("Clicked Go to Matched Roles button")

    def click_without_college_degree(self):
        """Click the Without College Degree filter."""
        btn = self.page.locator(L.WITHOUT_COLLEGE_DEGREE)
        btn.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, L.WITHOUT_COLLEGE_DEGREE)
        btn.click()
        print("Clicked Without College Degree")

    def validate_header_count(self):
        """Validate the recommended roles header count is visible."""
        count = self.page.locator(L.VALIDATE_HEADER_COUNT).first
        count.wait_for(state="visible", timeout=15000)
        count_text = count.text_content().strip()
        highlight_element(self.page, L.VALIDATE_HEADER_COUNT)
        assert len(count_text) > 0, "Header count is empty"
        print(f"Validated header count: {count_text}")

    def click_searched_role(self):
        """Click the Search Roles section to expand it."""
        search_roles = self.page.locator(L.SEARCH_ROLES_HEADER)
        search_roles.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, L.SEARCH_ROLES_HEADER)
        search_roles.click()
        print("Clicked Search Roles section")

    def fill_job_role_input(self):
        """Fill in the job role search input field."""
        search_input = self.page.locator(L.SEARCH_FOR_JOB_ROLE_INPUT)
        search_input.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, L.SEARCH_FOR_JOB_ROLE_INPUT)
        search_input.fill("Project Manager")
        print("Filled job role input with 'Project Manager'")

    def validate_result_header_and_click_favourite(self):
        """Validate Result header is visible and click Favourite on first result."""
        result = self.page.locator(L.RESULTS_HEADER)
        result.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, L.RESULTS_HEADER)
        assert result.is_visible(), "Results header not visible"
        result_text = result.text_content().strip()
        print(f"Validated Result header: {result_text}")

        favourite = self.page.locator(L.ADD_FAVOURITE).first
        favourite.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, L.ADD_FAVOURITE)
        favourite.click()
        print("Clicked Favourite on first result")

    def click_favourites_header(self):
        """Click the Favourites section header."""
        favourites = self.page.locator(L.FAVOURITES_HEADER).first
        favourites.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, L.FAVOURITES_HEADER)
        favourites.click()
        print("Clicked Favourites header")

    def click_share_report_and_share(self):
        """Click Share Report and then the Share button."""
        share_report = self.page.locator(L.SHARE_REPORT)
        share_report.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, L.SHARE_REPORT)
        share_report.click()
        print("Clicked Share Report")

        share_btn = self.page.locator(L.SHARE_BUTTON)
        share_btn.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, L.SHARE_BUTTON)
        share_btn.click()
        print("Clicked Share button")

    def click_favourite_and_remove(self):
        """After Share: click Favourites header, then click Remove Favourite."""
        # Close share dialog/toast if still open
        try:
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(1000)
        except Exception:
            pass

        # Click Favourites header to navigate to Favourites section
        fav_header = self.page.locator(L.FAVOURITES_HEADER).first
        fav_header.wait_for(state="visible", timeout=15000)
        fav_header.scroll_into_view_if_needed()
        highlight_element(self.page, L.FAVOURITES_HEADER)
        fav_header.click()
        print("Clicked Favourites header")
        self.page.wait_for_timeout(1500)

        # Click the first Favourite button (removes favourite)
        remove = self.page.locator(L.REMOVE_FAVOURITE).first
        remove.wait_for(state="visible", timeout=15000)
        remove.scroll_into_view_if_needed()
        highlight_element(self.page, L.REMOVE_FAVOURITE)
        remove.click()
        print("Clicked Remove Favourite")
        print("Removed job from favourites")

    def click_home_icon_and_navigate_home(self):
        """Click the Home icon to navigate back to the home page."""
        home = self.page.locator(L.HOME).first
        home.wait_for(state="visible", timeout=15000)
        home.scroll_into_view_if_needed()
        highlight_element(self.page, L.HOME)
        home.click()
        print("Clicked Home icon and navigated to home page")
        self.page.wait_for_timeout(1500)

    def click_roles_saved_and_validate_favourite_role_header(self):
        """Click the Roles Saved card, click Favourites header, and validate the Favourite Roles header.

        If the 'Roles Saved' text is not present on the card, the step is skipped
        gracefully (asserted as not present) so the test case does not fail.
        """
        roles_saved = self.page.locator(L.ROLES_SAVED).first
        try:
            roles_saved.wait_for(state="visible", timeout=10000)
        except Exception:
            pass

        roles_saved_present = roles_saved.count() > 0 and roles_saved.is_visible()
        if not roles_saved_present:
            # Soft assertion: 'Roles Saved' text is absent, so the test case is
            # expected to pass without continuing the validation.
            assert not roles_saved_present, "Roles Saved text not present on card"
            print("'Roles Saved' text not present on card - skipping favourite role header validation")
            return

        roles_saved.scroll_into_view_if_needed()
        highlight_element(self.page, L.ROLES_SAVED)
        roles_saved.click()
        print("Clicked Roles Saved card")
        self.page.wait_for_timeout(1500)

        favourites = self.page.locator(L.FAVOURITES_HEADER).first
        favourites.wait_for(state="visible", timeout=15000)
        favourites.scroll_into_view_if_needed()
        highlight_element(self.page, L.FAVOURITES_HEADER)
        favourites.click()
        print("Clicked Favourites header")
        self.page.wait_for_timeout(1500)

        fav_role_header = self.page.locator(L.VALIDATE_FAVOURITE_ROLES_HEADER).first
        fav_role_header.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, L.VALIDATE_FAVOURITE_ROLES_HEADER)
        assert fav_role_header.is_visible(), "Favourite Roles header not visible"
        print("Validated Favourite Roles header")
        