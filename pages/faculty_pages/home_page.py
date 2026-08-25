import re

from pages.base_page import BasePage
from locators.faculty_locators.home_locators import HomeLocators
from utils.logger import log
from locators.xpath import UPPER


class FacultyHomePage(BasePage):

    def navigate_to_dashboard(self):
        self.page.locator(HomeLocators.HOME_MENU).first.wait_for(state="visible", timeout=20000)
        self.click_home_menu()
        self.validate_any_visible([
            HomeLocators.FACULTY_DASHBOARD_CONTAINER,
            HomeLocators.RECOMMENDED_ACTIVITIES_SECTION,
            HomeLocators.BATCHES_TITLE,
        ], "Faculty dashboard did not load after login", timeout=20000)

    def click_home_menu(self):
        self.click_required([
            HomeLocators.HOME_MENU,
            f"//div[@role='menuitem' and contains({UPPER}, 'HOME')]",
        ], "Home menu")

    def click_batches_menu(self):
        self.click_required([
            HomeLocators.BATCHES_MENU,
            f"//div[@role='menuitem' and contains({UPPER}, 'BATCH')]",
        ], "Batches menu")

    def click_performance_menu(self):
        self.click_required([
            HomeLocators.PERFORMANCE_MENU,
            f"//div[@role='menuitem' and contains({UPPER}, 'PERFORMANCE')]",
        ], "Performance menu")

    def click_calendar_menu(self):
        self.click_required([
            HomeLocators.CALENDER_MENU,
            "//div[@id='Calendar']",
            "(//img[contains(@alt,'calendar') or contains(@class,'calendar')])[1]",
        ], "Calendar menu")

    def navigate_to_home(self):
        self.click_home_menu()
        self.validate_any_visible([
            HomeLocators.FACULTY_DASHBOARD_CONTAINER,
            HomeLocators.RECOMMENDED_ACTIVITIES_SECTION,
        ], "Faculty home page did not become visible", timeout=15000)

    def navigate_help_support(self):
        support_menu = self.page.locator(HomeLocators.SUPPORT_MENU).first
        support_menu.wait_for(state="visible", timeout=10000)
        self.show_element(support_menu, duration=1200)
        with self.page.context.expect_page() as page_info:
            support_menu.click()
        support_page = page_info.value
        support_page.wait_for_load_state("domcontentloaded")
        support_page.close()
        self.page.bring_to_front()

    def check_notifications_and_chat(self):
        # Faculty header has no chat icon; only the notifications panel is available here.
        notifications_menu = self.page.locator(HomeLocators.NOTIFICATIONS_MENU).first
        notifications_menu.wait_for(state="visible", timeout=10000)
        self.show_element(notifications_menu, duration=1200)
        notifications_menu.click()

        close_icon = self.page.locator(HomeLocators.CLOSE_NOTIFICATION).first
        try:
            close_icon.wait_for(state="visible", timeout=5000)
            self.show_element(close_icon, duration=800)
            close_icon.click()
        except Exception as _ignored:
            log.debug("Optional step in check_notifications_and_chat() did not apply: %s", _ignored)

    def click_profile_icon(self):
        profile_menu = self.page.locator(HomeLocators.PROFILE_MENU).first
        profile_menu.wait_for(state="visible", timeout=10000)
        self.show_element(profile_menu, duration=1200)
        profile_menu.click()

    def edit_profile_details(self):
        # Clicking the profile avatar already navigates to the profile page.
        # If a separate "My Profile" entry is present, open it; otherwise continue.
        profile = self.first_visible([HomeLocators.MY_PROFILE, "//span[contains(.,'My Profile')]"], timeout=3000)
        if profile:
            self.show_element(profile, duration=1200)
            profile.click()

        first_name = self.page.locator(HomeLocators.FIRST_NAME).first
        is_edit_mode_open = False
        try:
            first_name.wait_for(state="visible", timeout=5000)
            assert first_name.is_visible(), "First name field is not visible in profile edit"
            is_edit_mode_open = True
        except Exception as _ignored:
            log.debug("Optional step in edit_profile_details() did not apply: %s", _ignored)

        if not is_edit_mode_open:
            edit = self.first_visible([
                HomeLocators.EDIT_PROFILE,
                HomeLocators.EDIT_BUTTON,
                "//button[normalize-space()='Edit' or .//span[normalize-space()='Edit']]",
                "//*[self::button or self::span][contains(@class,'edit') and not(contains(@class,'credit'))]",
            ], timeout=8000)
            assert edit, "Edit profile action is not visible"
            self.show_element(edit, duration=1200)
            edit.click()

            first_name.wait_for(state="visible", timeout=10000)
            assert first_name.is_visible(), "First name field is not visible in profile edit"

        current_first_name = (first_name.input_value() or "").strip()
        match = re.match(r"^(.*?)(\d+)$", current_first_name)
        if match:
            name_prefix = match.group(1) or "FacultyAuto"
            next_number = int(match.group(2)) + 1
            next_first_name = f"{name_prefix}{next_number}"
        else:
            name_prefix = current_first_name or "FacultyAuto"
            next_first_name = f"{name_prefix}1"

        first_name.fill(next_first_name)
        self.show_element(first_name, duration=1200)
        self.pause(300)

        # Persist profile changes; otherwise the value only changes in the input field.
        self.click_required([
            HomeLocators.SAVE_BUTTON,
            "(//button[normalize-space()='Update'])[1]",
            "(//button[normalize-space()='Save'])[1]",
            f"//button[contains({UPPER}, 'UPDATE')]",
            f"//button[contains({UPPER}, 'SAVE')]",
        ], "Update/Save button", timeout=10000)
        self.pause(1200)
        log.info(f"Updated first name: {next_first_name}")
    def validate_batches_section(self):
        title = self.first_visible([
            HomeLocators.BATCHES_TITLE,
            f"//*[self::h2 or self::h3][contains({UPPER}, 'BATCH')]",
        ], timeout=10000)
        assert title, "Batches title is not visible"
        self.show_element(title, duration=1200)

        section = self.page.locator(HomeLocators.BATCHES_SECTION).first
        section.wait_for(state="visible", timeout=10000)
        assert section.is_visible(), "Batches section is not visible"
        self.show_element(section, duration=1200)

        create_batch_button = self.first_visible([
            HomeLocators.CREATE_NEWBATCH_BUTTON,
            f"//button[contains({UPPER}, 'CREATE NEW BATCH')]",
        ], timeout=10000)
        assert create_batch_button, "Create New Batch button is not visible"
        self.show_element(create_batch_button, duration=1200)

    def validate_active_inactive_tabs_under_batches(self):
        active = self.first_visible([
            HomeLocators.ACTIVE_BATCHES,
            f"//button[@role='tab'][contains({UPPER}, 'ACTIVE')]",
        ], timeout=10000)
        assert active, "Active tab is not visible"
        self.show_element(active, duration=1000)
        active.click()

        inactive = self.first_visible([
            HomeLocators.INACTIVE_BATCHES,
            f"//button[@role='tab'][contains({UPPER}, 'INACTIVE')]",
        ], timeout=10000)
        assert inactive, "Inactive tab is not visible"
        self.show_element(inactive, duration=1000)
        inactive.click()

        active = self.first_visible([
            HomeLocators.ACTIVE_BATCHES,
            f"//button[@role='tab'][contains({UPPER}, 'ACTIVE')]",
        ], timeout=10000)
        assert active, "Active tab is not visible after switching"
        self.show_element(active, duration=1000)
        active.click()

    def click_batches_next_arrow_button(self):
        clicked = self.click_arrow_until_end([
            HomeLocators.BATCHES_PAGES_ARROW,
            "(//button[contains(@aria-label,'next') or contains(@class,'next')])[1]",
        ], max_clicks=20, pause_ms=250)
        assert clicked, "Batches next arrow is not visible/clickable"

    def validate_certified_courses_and_click_carousal_arrow(self):
        courses = self.first_visible([
            HomeLocators.CERTIFIED_COURSES,
            f"//*[contains({UPPER}, 'CERTIFIED COURSES')]",
        ], timeout=10000)
        assert courses, "Certified Courses section is not visible"
        self.show_element(courses, duration=1600)

        carousel = self.page.locator(HomeLocators.CERTIFIED_COURSES_CARUSOL).first
        carousel.wait_for(state="visible", timeout=10000)
        assert carousel.is_visible(), "Certified courses carousel is not visible"
        self.show_element(carousel, duration=1200)

        clicked = self.click_arrow_until_end([
            HomeLocators.CERTIFIED_COURSES_CARUSOL_ARROW,
            "(//button[contains(@aria-label,'Go to next slide')])[1]",
        ], max_clicks=12, pause_ms=300)
        if not clicked:
            log.info("Certified courses carousel next arrow not visible; continuing with scroll to end")
        # Move through the remaining dashboard cards until the bottom is reached.
        self.scroll_to_bottom(max_attempts=30, pause_ms=300)

    def validate_my_forums_section(self):
        # Reach lower dashboard sections that are lazy-rendered as user scrolls.
        self.scroll_to_bottom(max_attempts=30, pause_ms=350)

        section = self.first_visible([
            HomeLocators.FORUMS_SECTION,
            HomeLocators.RECOMMENDED_FORUMS_TITLE,
            HomeLocators.MY_FORUMS_TITLE,
            f"//*[self::h2 or self::h3 or self::h4 or self::p][contains({UPPER}, 'RECOMMENDED FORUMS')]",
            f"//*[self::h2 or self::h3 or self::h4 or self::p][contains({UPPER}, 'MY FORUMS')]",
            f"//*[contains({UPPER}, 'FORUM')]",
        ], timeout=15000)
        assert section, "Forums section is not visible"
        self.show_element(section, duration=1600)

        recommended_title = self.first_visible([
            HomeLocators.RECOMMENDED_FORUMS_TITLE,
            f"//*[self::h2 or self::h3 or self::h4 or self::p][contains({UPPER}, 'RECOMMENDED FORUMS')]",
        ], timeout=3500)
        recommended_present = bool(recommended_title)
        if recommended_title:
            self.show_element(recommended_title, duration=1400)

        my_forums_title = self.first_visible([
            HomeLocators.MY_FORUMS_TITLE,
            f"//*[self::h2 or self::h3 or self::h4 or self::p][contains({UPPER}, 'MY FORUMS')]",
        ], timeout=3500)
        my_forums_present = bool(my_forums_title)
        if my_forums_title:
            self.show_element(my_forums_title, duration=1400)

        assert recommended_present or my_forums_present, "Neither Recommended Forums nor My Forums section is visible"

        # Validate cards only for sections that are present.
        if recommended_present:
            recommended_card = self.first_visible([
                HomeLocators.RECOMMENDED_FORUM_CARD,
                "(//span[@id='recommended_forum_container'])[1]//ancestor::*[contains(@class,'forum') or contains(@class,'card')][1]",
            ], timeout=3000)
            if recommended_card:
                self.show_element(recommended_card, duration=1200)
            else:
                log.info("Recommended Forums is visible; no recommended forum card found to highlight")
        if my_forums_present:
            my_forums_card = self.first_visible([
                HomeLocators.FORUM_CARD,
                f"//*[contains(@class,'forum') and .//*[contains({UPPER}, 'MY FORUMS')]]//*[contains(@class,'card')]",
            ], timeout=3000)
            if my_forums_card:
                self.show_element(my_forums_card, duration=1200)
            else:
                log.info("My Forums is visible; no my-forums card found to highlight")