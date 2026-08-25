from pages.base_page import BasePage
from locators.mentor_locators.mentor_locators import MentorLocators
from utils.logger import log


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
                log.info("Clicked on Customise Weekly Schedule")
                self.pause(1500)
                return True
            except Exception:
                continue
        log.info("'Customise/Customize Weekly Schedule' button not found — feature may not be available on this environment")
        return False

    def add_slot_select_start_and_end_time(self):
        self.click(MentorLocators.ADD_SLOT_BUTTON, "add slot button", timeout=15000)
        log.info("Clicked Add Slot button")
        self.pause(1000)

        self.click(MentorLocators.START_TIME_SLOT, "start time slot", timeout=10000)
        self.page.locator(MentorLocators.START_TIME_OPTION).last.wait_for(state="visible", timeout=10000)
        self.page.locator(MentorLocators.START_TIME_OPTION).last.click()
        log.info("Selected start time: 12:00 AM")

        self.click(MentorLocators.END_TIME_SLOT, "end time slot", timeout=10000)
        self.page.locator(MentorLocators.END_TIME_SLOT_OPTION).last.wait_for(state="visible", timeout=10000)
        self.page.locator(MentorLocators.END_TIME_SLOT_OPTION).last.click()
        log.info("Selected end time: 12:30 AM")
        self.pause(1000)

    def click_copy_slot_and_select_day(self):
        self.page.locator(MentorLocators.COPY_SLOT_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.locator(MentorLocators.COPY_SLOT_BUTTON).click()
        log.info("Clicked Copy Slot button")
        self.pause(1000)

        # Wait for the copy panel to open
        self.page.wait_for_selector("//*[contains(text(),'Copy Times to')]", state="visible", timeout=10000)
        log.info("Copy panel opened")
        self.pause(500)

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
        log.info(f"JS click result: {clicked}")
        self.pause(500)

    def click_apply_and_close_slot(self):
        self.click(MentorLocators.SLOT_COPY_APPLY_BUTTON, "slot copy apply button", timeout=10000)
        log.info("Clicked Apply button")
        self.pause(1000)
        # Close 2 slots (Monday + Tuesday created by copy)
        for i in range(2):
            try:
                self.page.locator(MentorLocators.CLOSE_SLOT_BUTTON).wait_for(state="visible", timeout=8000)
                self.page.locator(MentorLocators.CLOSE_SLOT_BUTTON).click()
                log.info(f"Closed slot {i+1}")
                self.pause(1000)
            except Exception as e:
                log.info(f"Close slot {i+1} not found (may be normal): {e}")
                break

    def click_add_override_select_start_and_end_time(self):
        self.click(MentorLocators.ADD_OVERRIDE_BUTTON, "add override button", timeout=15000)
        log.info("Clicked Add an Override button")
        self.pause(1000)

        self.click(MentorLocators.FIRST_DATE_OVERRIDE, "first date override", timeout=10000)
        log.info("Selected first available date for override")
        self.pause(500)

        self.click(MentorLocators.SAVE_DATE_OVERRIDE_BUTTON, "save date override button", timeout=10000)
        log.info("Saved override date selection")
        self.pause(1000)


    def delete_override_slot_and_save(self):
        self.click(MentorLocators.DELETE_ICON, "delete icon", timeout=10000)
        log.info("Clicked Delete icon on override slot")
        self.pause(1000)

        self.click(MentorLocators.SAVE_BUTTON, "save button", timeout=10000)
        log.info("Clicked Save button after deleting override slot")
        self.pause(1500)
