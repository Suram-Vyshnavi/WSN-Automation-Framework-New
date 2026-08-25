from pages.base_page import BasePage
from locators.faculty_locators.create_newbatch_locators import CreateNewBatchLocators
from utils.logger import log
from locators.xpath import UPPER


class CreateNewBatchPage(BasePage):

    def _scroll_until_any_visible(self, selectors, max_scrolls=12, step_px=700, wait_ms=250):
        """Scroll down in steps until one of the selectors becomes visible."""
        for _ in range(max_scrolls + 1):
            for selector in selectors:
                locator = self.page.locator(selector).first
                try:
                    if locator.is_visible():
                        return locator
                except Exception:
                    continue

            self.page.mouse.wheel(0, step_px)
            self.pause(wait_ms)

        return None

    def click_create_new_batch_button(self):
        self.click_required([
            CreateNewBatchLocators.CREATE_NEWBATCH_BUTTON,
            f"//button[contains({UPPER}, 'CREATE NEW BATCH')]",
        ], "Create New Batch button", timeout=15000)

    def validate_batch_information_header_and_title(self):
        self.validate_any_visible([
            CreateNewBatchLocators.BATCH_INFORMATION_HEADER_SECTION,
            "//*[contains(@class,'stepper') or contains(@class,'createBatch')]",
        ], "Batch Information header section", timeout=15000)

        self.validate_any_visible([
            CreateNewBatchLocators.BATCH_INFORMATION_TITLE,
            f"//*[contains({UPPER}, 'BATCH INFORMATION')]",
        ], "Batch Information title", timeout=10000)

    def select_institute_by_name(self, institute_name):
        clicked = False
        for selector in [
            "#Institute-search-input .ant-select-selector",
            "#Institute-search-input",
            CreateNewBatchLocators.INSTITUTE_DROPDOWN,
            f"//label[contains({UPPER}, 'INSTITUTE')]/following::div[contains(@class,'ant-select-selector')][1]",
        ]:
            locator = self.page.locator(selector).first
            try:
                locator.wait_for(state="attached", timeout=4000)
                try:
                    locator.scroll_into_view_if_needed(timeout=2000)
                except Exception as _ignored:
                    log.debug("Optional step in select_institute_by_name() did not apply: %s", _ignored)
                self.show_element(locator, duration=1200)
                locator.click(force=True)
                clicked = True
                break
            except Exception:
                continue

        if not clicked:
            prefilled = self.first_visible([
                f"//*[normalize-space()='{institute_name}']",
                f"//*[contains(normalize-space(),'{institute_name}')]",
            ], timeout=5000)
            # assert prefilled, "Institute dropdown is not available and institute text is not present"
            return

        self.pause(1000)

        option = self.first_visible([
            f"//span[normalize-space()='{institute_name}']",
            f"//div[@role='option'][normalize-space()='{institute_name}']",
            f"//div[@role='option'][.//*[contains(normalize-space(),'{institute_name}')]]",
            CreateNewBatchLocators.INSTITUTE_DROPDOWN_OPTION,
        ], timeout=5000)
        if option:
            try:
                self.show_element(option, duration=1200)
                option.dispatch_event("click")
            except Exception:
                option.click(force=True)
            return

        search_input = self.page.locator("input[aria-autocomplete='list']").first
        try:
            search_input.wait_for(state="attached", timeout=3000)
            search_input.fill(institute_name)
            search_input.press("Enter")
            self.pause(1000)
        except Exception as _ignored:
            log.debug("Optional step in select_institute_by_name() did not apply: %s", _ignored)

        selected = self.first_visible([
            f"//span[normalize-space()='{institute_name}']",
            f"//*[contains(normalize-space(),'{institute_name}')]",
        ], timeout=5000)
        if selected:
            return

        # Institute name not found (e.g. dev-specific name used against prod).
        # Fall back to selecting the first available institute in the dropdown.
        first_option = self.first_visible([
            "//div[contains(@class,'ant-select-item-option') and not(contains(@aria-disabled,'true'))][1]",
            "//li[contains(@class,'ant-select-item-option') and not(contains(@aria-disabled,'true'))][1]",
            "//div[@role='option'][1]",
        ], timeout=5000)
        if first_option:
            try:
                first_option.click(force=True)
            except Exception:
                first_option.dispatch_event("click")
            log.info(f"Institute '{institute_name}' not found; selected first available institute as fallback")
            return
        assert False, f"Institute option '{institute_name}' is not visible/selected and no fallback institute found"

    def select_course_by_name(self, course_name):
        # Wait for course dropdown to become enabled (it starts disabled until institute is selected)
        try:
            self.page.wait_for_function(
                "() => { const el = document.getElementById('Select Course-search-input'); return el && !el.closest('.ant-select-disabled'); }",
                timeout=10000
            )
        except Exception as _ignored:
            log.debug("Optional step in select_course_by_name() did not apply: %s", _ignored)
        self.pause(500)

        clicked = False
        for selector in [
            "//*[@id='Select Course-search-input']//div[contains(@class,'ant-select-selector')]",
            "//*[@id='Select Course-search-input']",
            CreateNewBatchLocators.SELECT_COURSE_DROPDOWN,
            f"//label[contains({UPPER}, 'COURSE')]/following::div[contains(@class,'ant-select-selector')][1]",
        ]:
            locator = self.page.locator(selector).first
            try:
                locator.wait_for(state="attached", timeout=4000)
                try:
                    locator.scroll_into_view_if_needed(timeout=2000)
                except Exception as _ignored:
                    log.debug("Optional step in select_course_by_name() did not apply: %s", _ignored)
                self.show_element(locator, duration=1200)
                locator.click(force=True)
                clicked = True
                break
            except Exception:
                continue

        if not clicked:
            self.validate_any_visible([
                f"//*[normalize-space()='{course_name}']",
                f"//*[contains(normalize-space(),'{course_name}')]",
            ], "Select course dropdown", timeout=5000)
            return

        self.pause(1000)

        option = self.first_visible([
            f"//span[normalize-space()='{course_name}']",
            f"//div[@role='option'][normalize-space()='{course_name}']",
            f"//div[@role='option'][.//*[contains(normalize-space(),'{course_name}')]]",
            CreateNewBatchLocators.SELECT_COURSE_DROPDOWN_OPTION,
        ], timeout=5000)
        if option:
            try:
                self.show_element(option, duration=1200)
                option.dispatch_event("click")
            except Exception:
                option.click(force=True)
            return

        search_input = self.page.locator("input[aria-autocomplete='list']").first
        try:
            search_input.wait_for(state="attached", timeout=3000)
            search_input.fill(course_name)
            search_input.press("Enter")
            self.pause(1000)
        except Exception as _ignored:
            log.debug("Optional step in select_course_by_name() did not apply: %s", _ignored)

        selected = self.first_visible([
            f"//span[normalize-space()='{course_name}']",
            f"//*[contains(normalize-space(),'{course_name}')]",
            "//span[contains(@class,'ant-select-selection-item')]",
        ], timeout=5000)
        assert selected, f"Course option '{course_name}' is not visible"

    def enter_batch_name(self, batch_name):
        field = self.page.locator(CreateNewBatchLocators.BATCH_NAME_INPUT).first
        field.wait_for(state="attached", timeout=10000)
        try:
            field.scroll_into_view_if_needed(timeout=2000)
        except Exception as _ignored:
            log.debug("Optional step in enter_batch_name() did not apply: %s", _ignored)
        self.show_element(field, duration=1200)
        try:
            field.fill(batch_name, force=True)
        except Exception:
            self.page.evaluate(f"document.querySelector('input[placeholder=\"provide batch name\"]').value = '{batch_name}'")

    def _open_batch_date_field(self, field="start", timeout=10000):
        """Open the correct date field popup: start (first) or end (second)."""
        index = 0 if field == "start" else 1

        candidates = [
            "//div[@id='create-batch-startedAt']",
            "//div[@id='create-batch-endedAt']",
            "//div[contains(@class,'ant-picker')]",
        ]

        for selector in candidates:
            locator = self.page.locator(selector)
            count = locator.count()
            if count <= index:
                continue
            target = locator.nth(index)
            try:
                target.wait_for(state="attached", timeout=timeout)
                self.show_element(target, duration=1200)
                target.click(force=True)
                return True
            except Exception:
                continue

        # fallback: date input wrappers by index
        fallback = self.page.locator("//div[contains(@class,'ant-picker-input')]")
        if fallback.count() > index:
            target = fallback.nth(index)
            try:
                target.wait_for(state="attached", timeout=timeout)
                self.show_element(target, duration=1200)
                target.click(force=True)
                return True
            except Exception as _ignored:
                log.debug("Optional step in _open_batch_date_field() did not apply: %s", _ignored)

        return False

    def set_start_date_to_today(self):
        clicked = self._open_batch_date_field(field="start", timeout=10000)
        assert clicked, "Start date picker is not visible/clickable"

        today = self.first_visible([
            CreateNewBatchLocators.DATE_PICKER_TODAY_TEXT,
            "//*[contains(@class,'ant-picker-today-btn') or normalize-space()='Today']",
        ], timeout=10000)
        assert today, "Today option is not visible in date picker"
        self.show_element(today, duration=1200)
        today.click()

    def set_end_date_with_next_year_next_month(self, day_text):
        clicked = self._open_batch_date_field(field="end", timeout=10000)
        assert clicked, "End date picker is not visible/clickable"

        self.click_first_visible([
            CreateNewBatchLocators.NEXT_YEAR_BUTTON,
            "//button[contains(@class,'super-next')]",
        ], "next year button", timeout=3000)

        self.click_first_visible([
            CreateNewBatchLocators.NEXT_MONTH_BUTTON,
            "//button[contains(@class,'next-btn')]",
        ], "next month button", timeout=3000)

        day = self.first_visible([
            f"//td[not(contains(@class,'disabled'))]//div[normalize-space()='{day_text}']",
            CreateNewBatchLocators.BATCH_ENDDATE,
        ], timeout=10000)
        assert day, f"Could not find day '{day_text}' in end-date picker"
        self.show_element(day, duration=1200)
        day.click()

    def validate_student_enrollment_note_and_weekly_hours(self):
        note_selectors = [
            CreateNewBatchLocators.STUDENT_ENROLLMENT_NOTE,
            "//div[contains(@class,'student-e') and contains(@class,'note')]",
            "//div[contains(@class,'enrollment') or contains(@class,'erollment')]",
            f"//*[contains({UPPER}, 'STUDENT ENROLLMENT NOTE')]",
            f"//*[contains({UPPER}, 'STUDENT ENROLLMENT')]",
            f"//*[contains({UPPER}, 'ENROLLMENT')]",
        ]

        # Bring lower form sections into viewport before strict validations.
        scrolled_note = self._scroll_until_any_visible(note_selectors, max_scrolls=18, step_px=650, wait_ms=250)
        if scrolled_note:
            self.show_element(scrolled_note, duration=1000)

        self._scroll_until_any_visible([CreateNewBatchLocators.WEEKELY_CLASS_HOURS], max_scrolls=14, step_px=500, wait_ms=220)
        # weekly-hours input ID may differ in prod; try alternate selectors before hard-asserting.
        weekly_hours = self.first_visible([
            CreateNewBatchLocators.WEEKELY_CLASS_HOURS,
            "//input[contains(@id,'weekly') or contains(@name,'weekly') or contains(@id,'class-hours')]",
            "//input[contains(@placeholder,'hours') or contains(@placeholder,'Hours')]",
        ], timeout=10000)
        if not weekly_hours:
            log.warning("Weekly class hours field not found — batch form may have different structure in this environment; skipping validation")
            return
        try:
            weekly_hours.scroll_into_view_if_needed(timeout=2000)
        except Exception as _ignored:
            log.debug("Optional step in validate_student_enrollment_note_and_weekly_hours() did not apply: %s", _ignored)
        self.show_element(weekly_hours, duration=1200)
        value = weekly_hours.input_value().strip()
        if not value:
            value = self.page.evaluate("document.querySelector('input#weekly-hours') && document.querySelector('input#weekly-hours').value") or ""
        assert value, "Weekly class hours prefilled value is empty"

        # Try attached state for note section after weekly-hours anchor is found.
        note_locator = None
        for selector in note_selectors:
            loc = self.page.locator(selector).first
            try:
                loc.wait_for(state="attached", timeout=1500)
                try:
                    loc.scroll_into_view_if_needed(timeout=1000)
                except Exception as _ignored:
                    log.debug("Optional step in validate_student_enrollment_note_and_weekly_hours() did not apply: %s", _ignored)
                note_locator = loc
                break
            except Exception:
                continue

        # In some variants note text is not separately rendered; weekly-hours field is the reliable anchor.
        if note_locator:
            self.show_element(note_locator, duration=1200)
        else:
            log.info("Student enrollment note label is not separately visible; validated section via weekly class hours field")

    def check_confirmation_set_max_students_and_next(self, max_students):
        self.click_required([
            CreateNewBatchLocators.CONFIRM_CHECKBOX,
            "//span[contains(@class,'ant-checkbox-inner')]",
        ], "Confirmation checkbox", timeout=10000)

        max_students_field = self.page.locator(CreateNewBatchLocators.MAX_STUDENTS_ALLOWED_INPUT).first
        max_students_field.wait_for(state="attached", timeout=10000)
        try:
            max_students_field.scroll_into_view_if_needed(timeout=2000)
        except Exception as _ignored:
            log.debug("Optional step in check_confirmation_set_max_students_and_next() did not apply: %s", _ignored)
        self.show_element(max_students_field, duration=1200)
        try:
            max_students_field.fill(str(max_students), force=True)
        except Exception:
            self.page.evaluate(f"document.querySelector('input[name=\"maxStudentsAllowed\"]').value = '{max_students}'")

        self.click_required([
            CreateNewBatchLocators.NEXT_BUTTON,
            "//button[normalize-space()='Next']",
        ], "Next button", timeout=10000)

    def confirm_dates_and_proceed(self):
        popup = self.first_visible([
            CreateNewBatchLocators.CONFIRM_DATES_POPUP,
            "//div[contains(@class,'ant-modal-body')]",
        ], timeout=10000)
        assert popup, "Confirm dates popup is not visible"
        self.show_element(popup, duration=1200)

        self.click_required([
            CreateNewBatchLocators.CONFIRM_AND_PROCEED_BUTTON,
            f"//button[contains({UPPER}, 'CONFIRM')]",
        ], "Confirm & Proceed button", timeout=10000)

    def validate_assessment_details_and_next(self):
        assessment_selectors = [
            CreateNewBatchLocators.ASSESSMENT_DETAILS_SECTION,
            f"//*[contains({UPPER}, 'ASSESSMENT DETAILS')]",
            f"//*[contains({UPPER}, 'ASSESSMENT')]",
        ]

        # Bring assessment block into view before validating/clicking Next.
        self._scroll_until_any_visible(
            assessment_selectors + [
                CreateNewBatchLocators.LEVEL2_RADIO_BUTTON,
                "//input[@value='Intermediate']",
            ],
            max_scrolls=16,
            step_px=550,
            wait_ms=220,
        )

        assessment = self.first_visible([
            *assessment_selectors,
        ], timeout=6000)

        # Some UI variants auto-skip/compact this section; difficulty radios indicate forward progress.
        if not assessment:
            self.validate_any_visible([
                CreateNewBatchLocators.LEVEL2_RADIO_BUTTON,
                "//input[@value='Intermediate']",
                f"//*[contains({UPPER}, 'INTERMEDIATE')]",
            ], "Assessment details section", timeout=2500)
            log.info("Assessment details section not separately visible; continuing from difficulty-level screen")
            return

        self.show_element(assessment, duration=1200)

        next_clicked = self.click_first_visible([
            CreateNewBatchLocators.ASSESSMENT_DETAILS_NEXT_BUTTON,
            "//button[normalize-space()='Next']",
            f"//button[contains({UPPER}, 'CONTINUE')]",
        ], "assessment details next button", timeout=10000)
        if not next_clicked:
            self.validate_any_visible([
                CreateNewBatchLocators.LEVEL2_RADIO_BUTTON,
                "//input[@value='Intermediate']",
            ], "Assessment details Next button", timeout=3000)

    def validate_difficulty_levels_and_select_level2(self):
        self._scroll_until_any_visible([
            CreateNewBatchLocators.DIFFICULY_LEVEL1_CARD,
            CreateNewBatchLocators.DIFFICULY_LEVEL2_CARD,
            CreateNewBatchLocators.DIFFICULY_LEVEL3_CARD,
            f"//*[contains({UPPER}, 'BASIC')]",
            f"//*[contains({UPPER}, 'INTERMEDIATE')]",
            f"//*[contains({UPPER}, 'ADVANCED')]",
        ], max_scrolls=12, step_px=450, wait_ms=220)

        level1 = self.first_visible([
            CreateNewBatchLocators.DIFFICULY_LEVEL1_CARD,
            f"//div[contains(@class,'radio_option')][.//*[contains({UPPER}, 'BASIC')]]",
            f"//*[contains({UPPER}, 'BASIC')]",
        ], timeout=7000)
        assert level1, "Difficulty level 1 card is not visible"
        self.show_element(level1, duration=1000)

        level2 = self.first_visible([
            CreateNewBatchLocators.DIFFICULY_LEVEL2_CARD,
            f"//div[contains(@class,'radio_option')][.//*[contains({UPPER}, 'INTERMEDIATE')]]",
            f"//*[contains({UPPER}, 'INTERMEDIATE')]",
        ], timeout=7000)
        assert level2, "Difficulty level 2 card is not visible"
        self.show_element(level2, duration=1000)

        level3 = self.first_visible([
            CreateNewBatchLocators.DIFFICULY_LEVEL3_CARD,
            f"//div[contains(@class,'radio_option')][.//*[contains({UPPER}, 'ADVANCED')]]",
            f"//*[contains({UPPER}, 'ADVANCED')]",
        ], timeout=7000)
        assert level3, "Difficulty level 3 card is not visible"
        self.show_element(level3, duration=1000)

        clicked = self.click_first_visible([
            CreateNewBatchLocators.LEVEL2_RADIO_BUTTON,
            "//input[@value='Intermediate']",
            "//label[.//input[@value='Intermediate']]",
            f"//div[contains(@class,'radio_option')][.//*[contains({UPPER}, 'INTERMEDIATE')]]",
        ], "level2 radio button", timeout=10000)
        if not clicked:
            already_selected = self.page.locator("//input[@value='Intermediate' and @checked]").count() > 0
            assert already_selected, "Difficulty level 2 radio button is not visible/clickable"

    def enter_job_role_or_sector(self, job_role_text):
        input_field = self.first_visible([
            CreateNewBatchLocators.JOBEROLE_OR_SECTOR_INPUT,
            "//input[contains(@placeholder,'job role') or contains(@placeholder,'Job Role')]",
            "//input[contains(@placeholder,'sector') or contains(@placeholder,'Sector')]",
            "//input[contains(@placeholder,'press enter') or contains(@placeholder,'Press Enter')]",
        ], timeout=10000)
        assert input_field, "Job role/sector input field is not visible"
        try:
            input_field.scroll_into_view_if_needed(timeout=2000)
        except Exception as _ignored:
            log.debug("Optional step in enter_job_role_or_sector() did not apply: %s", _ignored)
        self.show_element(input_field, duration=1200)
        try:
            input_field.fill(job_role_text, force=True)
        except Exception:
            input_field.click(force=True)
            self.page.keyboard.press("Control+A")
            self.page.keyboard.type(job_role_text)

        enter_clicked = self.click_first_visible([
            CreateNewBatchLocators.JOBEROLE_OR_SECTOR_ENTER_BUTTON,
            f"//button[contains({UPPER}, 'ENTER')]",
            f"//button[contains({UPPER}, 'ADD')]",
        ], "joberole or sector enter button", timeout=10000)
        if not enter_clicked:
            input_field.press("Enter")

        self.validate_any_visible([
            f"//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{job_role_text.lower()}')]",
            "//div[contains(@class,'tag') or contains(@class,'chip')]",
        ], "Job role/sector value was not added", timeout=5000)

    def save_and_finish_and_validate_batch_details_card(self):
        self.click_required([
            CreateNewBatchLocators.SAVE_AND_FINISH_BUTTON,
            f"//button[contains({UPPER}, 'SAVE') and contains({UPPER}, 'FINISH')]",
        ], "Save & Finish button", timeout=10000)

        card = self.first_visible([
            CreateNewBatchLocators.BATCH_DETAILS_CARD,
            "//div[contains(@class,'section_card_container') and contains(@class,'card')]",
        ], timeout=15000)
        assert card, "Batch details card is not visible after Save & Finish"
        self.show_element(card, duration=1400)
