from pages.base_page import BasePage
from locators.mentor_locators.mentor_locators import MentorLocators


class MentorPage(BasePage):
    def click_customize_weekly_schedule(self):
        """Click the Customise Weekly Schedule button. Returns True if found, False if not available."""
        locators = [
            MentorLocators.CUSTOMISE_WEEKLY_SCHEDULE,
            "//button[contains(text(), 'Customis') or contains(text(), 'Customiz')]",
            "//button[contains(translate(normalize-space(.), 'CUSTOMISEZ', 'customisez'), 'customis') or contains(translate(normalize-space(.), 'CUSTOMISEZ', 'customisez'), 'customiz')]",
        ]
        for loc in locators:
            try:
                self.page.locator(loc).first.wait_for(state="visible", timeout=5000)
                self.page.locator(loc).first.click()
                print("Clicked on Customise Weekly Schedule")
                self.page.wait_for_timeout(1500)
                return True
            except Exception:
                continue
        print("[INFO] 'Customise/Customize Weekly Schedule' button not found — feature may not be available on this environment")
        return False

    def add_slot_select_start_and_end_time(self):
        self.page.locator(MentorLocators.ADD_SLOT_BUTTON).wait_for(state="visible", timeout=15000)
        self.page.click(MentorLocators.ADD_SLOT_BUTTON)
        print("Clicked Add Slot button")
        self.page.wait_for_timeout(1000)

        self.page.locator(MentorLocators.START_TIME_SLOT).wait_for(state="visible", timeout=10000)
        self.page.click(MentorLocators.START_TIME_SLOT)
        self.page.locator(MentorLocators.START_TIME_OPTION).last.wait_for(state="visible", timeout=10000)
        self.page.locator(MentorLocators.START_TIME_OPTION).last.click()
        print("Selected start time: 12:00 AM")

        self.page.locator(MentorLocators.END_TIME_SLOT).wait_for(state="visible", timeout=10000)
        self.page.click(MentorLocators.END_TIME_SLOT)
        self.page.locator(MentorLocators.END_TIME_SLOT_OPTION).last.wait_for(state="visible", timeout=10000)
        self.page.locator(MentorLocators.END_TIME_SLOT_OPTION).last.click()
        print("Selected end time: 12:30 AM")
        self.page.wait_for_timeout(1000)

    def click_copy_slot_and_select_day(self):
        self.page.locator(MentorLocators.COPY_SLOT_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.locator(MentorLocators.COPY_SLOT_BUTTON).click()
        print("Clicked Copy Slot button")
        self.page.wait_for_timeout(1000)

        # Wait for the copy panel to open
        self.page.wait_for_selector("//*[contains(text(),'Copy Times to')]", state="visible", timeout=10000)
        print("Copy panel opened")
        self.page.wait_for_timeout(500)

        # Use JS to click Tuesday in the copy panel (bypasses visibility check)
        clicked = self.page.evaluate("""
            () => {
                const all = Array.from(document.querySelectorAll('*'));
                const tuesdays = all.filter(el =>
                    Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim() === 'Tuesday')
                );
                if (tuesdays.length === 0) return 'NOT FOUND';
                const target = tuesdays[tuesdays.length - 1];
                const clickable = target.closest('label') || target.closest('.ant-checkbox-wrapper') || target;
                clickable.click();
                return 'Clicked: ' + clickable.tagName + ' class=' + clickable.className;
            }
        """)
        print(f"JS click result: {clicked}")
        self.page.wait_for_timeout(500)

    def click_apply_and_close_slot(self):
        self.page.locator(MentorLocators.SLOT_COPY_APPLY_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.click(MentorLocators.SLOT_COPY_APPLY_BUTTON)
        print("Clicked Apply button")
        self.page.wait_for_timeout(1000)
        # Close 2 slots (Monday + Tuesday created by copy)
        for i in range(2):
            try:
                self.page.locator(MentorLocators.CLOSE_SLOT_BUTTON).wait_for(state="visible", timeout=8000)
                self.page.locator(MentorLocators.CLOSE_SLOT_BUTTON).click()
                print(f"Closed slot {i+1}")
                self.page.wait_for_timeout(1000)
            except Exception as e:
                print(f"Close slot {i+1} not found (may be normal): {e}")
                break

    def click_add_override_select_start_and_end_time(self):
        self.page.locator(MentorLocators.ADD_OVERRIDE_BUTTON).wait_for(state="visible", timeout=15000)
        self.page.click(MentorLocators.ADD_OVERRIDE_BUTTON)
        print("Clicked Add an Override button")
        self.page.wait_for_timeout(1000)

        self.page.locator(MentorLocators.FIRST_DATE_OVERRIDE).wait_for(state="visible", timeout=10000)
        self.page.click(MentorLocators.FIRST_DATE_OVERRIDE)
        print("Selected first available date for override")
        self.page.wait_for_timeout(500)

        self.page.locator(MentorLocators.SAVE_DATE_OVERRIDE_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.click(MentorLocators.SAVE_DATE_OVERRIDE_BUTTON)
        print("Saved override date selection")
        self.page.wait_for_timeout(1000)


    def click_save_button(self):
        self.page.locator(MentorLocators.SAVE_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.click(MentorLocators.SAVE_BUTTON)
        print("Clicked Save button")
        self.page.wait_for_timeout(1500)

    def delete_override_slot_and_save(self):
        self.page.locator(MentorLocators.DELETE_ICON).wait_for(state="visible", timeout=10000)
        self.page.click(MentorLocators.DELETE_ICON)
        print("Clicked Delete icon on override slot")
        self.page.wait_for_timeout(1000)

        self.page.locator(MentorLocators.SAVE_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.click(MentorLocators.SAVE_BUTTON)
        print("Clicked Save button after deleting override slot")
        self.page.wait_for_timeout(1500)
