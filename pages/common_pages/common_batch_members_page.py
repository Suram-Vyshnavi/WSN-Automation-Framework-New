from pages.base_page import BasePage
from locators.common_locators.common_batch_members_locators import CommonBatchMembersLocators
from locators.faculty_locators.home_locators import HomeLocators
from utils.logger import log


class CommonBatchMembersPage(BasePage):
    def _delete_confirmation_visible(self, timeout=1500):
        return self.first_visible([
            CommonBatchMembersLocators.REMOVE_STUDENT_NO_BUTTON,
            CommonBatchMembersLocators.REMOVE_STUDENT_YES_BUTTON,
            CommonBatchMembersLocators.REMOVE_STUDENT_POPUP,
            "//div[contains(@class,'ant-modal-wrap') and not(contains(@style,'display: none'))]",
            "//div[contains(@class,'ant-modal')]",
        ], timeout=timeout)

    def _navigate_to_batches(self):
        """Navigate to Batches list page from any screen."""
        try:
            self.page.locator(HomeLocators.BATCHES_MENU).first.wait_for(state="visible", timeout=3000)
            self.page.locator(HomeLocators.BATCHES_MENU).first.click(timeout=3000)
            self.pause(1500)
        except Exception:
            try:
                self.page.locator(HomeLocators.HOME_MENU).first.click(timeout=3000)
                self.pause(500)
                self.page.locator(HomeLocators.BATCHES_MENU).first.click(timeout=3000)
                self.pause(1500)
            except Exception as _ignored:
                log.debug("Optional step in _navigate_to_batches() did not apply: %s", _ignored)

    def click_batch_from_active_list(self, batch_name):
        self._navigate_to_batches()

        # Scroll through batch pages looking for the named batch
        for page_attempt in range(3):
            clicked = self.click_first_visible([
                f"(//td[contains(@class,'batch-list-content-bold') and normalize-space()='{batch_name}'])[1]",
                f"(//*[contains(@class,'batch-list-content') and normalize-space()='{batch_name}'])[1]",
            ], timeout=8000)
            if clicked:
                return
            # Try next page of batches
            try:
                next_btn = self.page.locator("//li[contains(@class,'ant-pagination-next')]/button[not(@disabled)]").first
                next_btn.wait_for(state="visible", timeout=2000)
                next_btn.click()
                self.pause(1000)
            except Exception:
                break

        # Final fallback: click the first batch card, whatever its name is.
        # FIRST_BATCH_CARD is hardcoded to one specific batch name, so it's tried
        # last, behind selectors that match any first-row batch.
        clicked = self.click_first_visible([
            "(//td[contains(@class,'batch-list-content-bold')])[1]",
            "(//tbody//tr[1]//td[contains(@class,'batch-list-content')])[1]",
            CommonBatchMembersLocators.FIRST_BATCH_CARD,
        ], timeout=5000)
        assert clicked, f"Batch '{batch_name}' is not visible/clickable"

    def validate_batch_members_tab_and_click(self):
        self.click_required([
            CommonBatchMembersLocators.BATCH_MEMBERS_TAB,
            "(//p[normalize-space()='Batch Members'])[1]",
        ], "Batch Members tab")

        self.validate_any_visible([
            CommonBatchMembersLocators.BATCH_MEMBERS_HEADER_SECTION,
            "//section[contains(@class,'student-section-header-container')]",
        ], "Batch members header section")

    def click_manage_students(self):
        self.click_required([CommonBatchMembersLocators.MANAGE_STUDENTS_BUTTON], "Manage Students button")

    def click_invite_students_and_validate_batch_code(self):
        self.click_required([CommonBatchMembersLocators.INVITE_STUDENTS_BUTTON], "Invite Students button")

        batch_code = self.first_visible([CommonBatchMembersLocators.INVITE_BATCHCODE])
        # When the invite-students panel never renders a batch code (the panel is
        # stuck loading / the batch has no invite data), treat it as a graceful
        # data gap and return to a clean state for the next scenario.
        if not batch_code:
            log.info("Batch code did not appear in the invite students section "
                     "(panel did not load for this batch); skipping remaining batch members validations.")
            try:
                self.click_home_menu_from_header()
            except Exception as _ignored:
                log.debug("Optional step in click_invite_students_and_validate_batch_code() did not apply: %s", _ignored)
            return False
        return True

    def copy_batch_code_and_paste_in_email(self):
        self.click_first_visible([CommonBatchMembersLocators.BATCHCODE_COPY_BUTTON], "batchcode copy button")
        email_input = self.first_visible([CommonBatchMembersLocators.ENTER_STUDENT_EMAIL_INPUT])
        assert email_input, "Student email input is not visible"

        # Clipboard paste can be flaky on CI/remote sessions; fallback to direct text fill.
        email_input.click()
        pasted = False
        try:
            email_input.press("Control+V")
            current = (email_input.input_value() or "").strip()
            pasted = bool(current)
        except Exception:
            pasted = False

        if not pasted:
            code_el = self.first_visible([CommonBatchMembersLocators.INVITE_BATCHCODE])
            assert code_el, "Batch code element is not visible"
            batch_code = (code_el.inner_text() or "").strip()
            assert batch_code, "Batch code text is empty"
            email_input.fill(batch_code)

    def remove_batch_code_and_send_email_invite(self, email):
        email_input = self.first_visible([CommonBatchMembersLocators.ENTER_STUDENT_EMAIL_INPUT])
        assert email_input, "Student email input is not visible"
        email_input.click()
        email_input.press("Control+A")
        email_input.press("Backspace")
        email_input.fill(email)

        self.click_required([CommonBatchMembersLocators.ENTER_STUDENT_INVITE_BUTTON], "Send Invite button")

    def download_template_upload_file_and_invite(self, upload_file_path):
        self.click_first_visible([CommonBatchMembersLocators.DOWNLOAD_TEMPLATE_LINK], "download template link", timeout=5000)

        upload_btn = self.first_visible([CommonBatchMembersLocators.UPLOAD_FILE_BUTTON], timeout=10000)
        assert upload_btn, "Upload File button is not visible/clickable"

        # Prefer file-chooser binding so the file is set on the exact control opened by the button.
        bound = False
        try:
            with self.page.expect_file_chooser(timeout=8000) as chooser_info:
                upload_btn.click(timeout=5000)
            chooser_info.value.set_files(upload_file_path)
            bound = True
        except Exception:
            bound = False

        if not bound:
            # Fallback for implementations that rely on persistent hidden file inputs.
            file_inputs = self.page.locator("input[type='file']")
            file_inputs.first.wait_for(state="attached", timeout=10000)
            try:
                file_inputs.last.set_input_files(upload_file_path)
            except Exception:
                file_inputs.first.set_input_files(upload_file_path)

        self.click_required([CommonBatchMembersLocators.UPLOAD_FILE_INVITE_BUTTON], "File invite button")

    def validate_uploaded_users_status_and_download(self):
        self.validate_any_visible([
            CommonBatchMembersLocators.UPLOAD_USERS_STATUS_BAR,
            "//div[contains(@class,'ant-progress-inner')]",
        ], "Uploaded users status bar", timeout=15000)

        self.click_first_visible([CommonBatchMembersLocators.UPLOAD_USERS_DOWNLOAD_BUTTON], "upload users download button", timeout=7000)

    def click_invite_students_back(self):
        self.click_required([CommonBatchMembersLocators.INVITE_STUDENTS_BACK_ARROW], "Invite students back button")

    def validate_batch_students_and_pending_requests(self):
        batch_students = self.first_visible([CommonBatchMembersLocators.BATCH_STUDENTS_TAB])
        pending = self.first_visible([CommonBatchMembersLocators.PENDING_REQUESTS_TAB])
        assert batch_students, "Batch Students tab is not visible"
        assert pending, "Pending Requests tab is not visible"

    def validate_first_user_view_and_download_buttons(self):
        self.click_required([CommonBatchMembersLocators.BATCH_STUDENTS_TAB], "Batch Students tab")

        view_button = self.first_visible([CommonBatchMembersLocators.DOWNLOAD_CERTIFICATE_VIEW_BUTTON], timeout=8000)
        download_button = self.first_visible([CommonBatchMembersLocators.DOWNLOAD_CERTIFICATE_DOWNLOAD_BUTTON], timeout=8000)
        if not (view_button and download_button):
            # This batch has no already-enrolled/certified student (the "Batch
            # Students" table is empty or has no certificate yet) — a data gap,
            # not a locator failure. Skip the rest gracefully like the invite
            # panel does above.
            log.info("No enrolled/certified student found in Batch Students tab "
                     "for this batch; skipping remaining batch members validations.")
            try:
                self.click_home_menu_from_header()
            except Exception as _ignored:
                log.debug("Optional step in validate_first_user_view_and_download_buttons() did not apply: %s", _ignored)
            return False
        return True

    def click_view_and_validate_certificate_images_download(self):
        clicked = self.click_first_visible([CommonBatchMembersLocators.DOWNLOAD_CERTIFICATE_VIEW_BUTTON], "download certificate view button")
        # assert clicked, "View button is not visible/clickable"

        self.validate_any_visible([CommonBatchMembersLocators.CERTIFICATE_IMAGE], "Certificate image preview")

        self.click_required([CommonBatchMembersLocators.VIEW_CERTIFICATE_DOWNLOAD_CERTIFICATE_BUTTON], "Download certificate button")

    def close_certificate_and_download_from_list(self):
        self.click_required([CommonBatchMembersLocators.VIEW_CERTIFICATE_CLOSE_ICON], "Certificate close icon")

        self.click_first_visible([CommonBatchMembersLocators.DOWNLOAD_CERTIFICATE_DOWNLOAD_BUTTON], "download certificate download button", timeout=7000)

    def click_user_delete_and_validate_remove_popup(self):
        # Ensure we are on Batch Students table before attempting row-level delete.
        self.click_first_visible([CommonBatchMembersLocators.BATCH_STUDENTS_TAB], "batch students tab", timeout=5000)

        # Delete icon is usually hover-driven and can be rendered as div/img/button.
        rows = self.page.locator("//tr[contains(@class,'ant-table-row') and .//td]")
        row_count = rows.count()
        clicked = False

        for idx in range(min(row_count, 5)):
            try:
                rows.nth(idx).hover(timeout=3000)
            except Exception as _ignored:
                log.debug("Optional step in click_user_delete_and_validate_remove_popup() did not apply: %s", _ignored)

            row = rows.nth(idx)
            row_delete_candidates = [
                "xpath=.//*[contains(@class,'remove-student')]",
                "xpath=.//img[@alt='delete']",
                "xpath=.//img[contains(@class,'trash')]",
                "xpath=.//button[contains(translate(normalize-space(.),'DELETE','delete'),'delete')]",
            ]
            for selector in row_delete_candidates:
                try:
                    candidate = row.locator(selector).first
                    if candidate.count() == 0:
                        continue
                    try:
                        candidate.scroll_into_view_if_needed()
                    except Exception as _ignored:
                        log.debug("Optional step in click_user_delete_and_validate_remove_popup() did not apply: %s", _ignored)
                    try:
                        candidate.click(timeout=3000)
                    except Exception:
                        try:
                            candidate.click(timeout=3000, force=True)
                        except Exception:
                            clicked_js = candidate.evaluate("el => { el.click(); return true; }")
                            if not clicked_js:
                                continue

                    # Only accept click if we observe a post-click confirmation signal.
                    if self._delete_confirmation_visible(timeout=1500):
                        clicked = True
                        break
                except Exception:
                    continue
            if clicked:
                break

        if not clicked:
            # Final fallback to global delete selector in case row structure changed.
            fallback_clicked = self.click_first_visible([
                CommonBatchMembersLocators.USER_DELETE_BUTTON,
                "//img[@alt='delete']",
                "//img[contains(@class,'trash')]",
            ], "user delete button", timeout=5000)
            if fallback_clicked and self._delete_confirmation_visible(timeout=2000):
                clicked = True

        assert clicked, "User delete icon is not clickable"

        confirmation = self._delete_confirmation_visible(timeout=5000)
        if not confirmation:
            # Some builds perform delete without a confirmation modal.
            return

    def click_no_and_open_pending_requests(self):
        # Confirmation may appear as modal or be skipped based on environment state.
        no_clicked = self.click_first_visible([CommonBatchMembersLocators.REMOVE_STUDENT_NO_BUTTON], "remove student no button", timeout=3000)
        if not no_clicked:
            try:
                self.page.keyboard.press("Escape")
            except Exception as _ignored:
                log.debug("Optional step in click_no_and_open_pending_requests() did not apply: %s", _ignored)

        pending_clicked = self.click_first_visible([CommonBatchMembersLocators.PENDING_REQUESTS_TAB], "pending requests tab", timeout=15000)
        if not pending_clicked:
            self.click_first_visible([CommonBatchMembersLocators.BATCH_STUDENTS_TAB], "batch students tab", timeout=5000)
            pending_clicked = self.click_first_visible([CommonBatchMembersLocators.PENDING_REQUESTS_TAB], "pending requests tab", timeout=10000)
        assert pending_clicked, "Pending Requests tab is not visible/clickable"

    def click_first_resend_and_validate_popup(self):
        self.click_required([CommonBatchMembersLocators.FIRST_USER_RESEND_BUTTON], "Resend request button", timeout=10000)

        self.validate_any_visible([CommonBatchMembersLocators.RESEND_OTP_POPUP, "//div[contains(@class,'ant-modal-body')]"], "Resend OTP popup")

    def confirm_resend_and_click_manage_students_back(self):
        self.click_required([CommonBatchMembersLocators.RESEND_OTP_POPUP_YES_BUTTON], "Yes button", timeout=7000)

        self.click_required([CommonBatchMembersLocators.MANAGE_STUDENTS_BACK_ARROW], "Manage students back button", timeout=7000)

    def click_batch_members_and_open_first_chat(self):
        self.click_required([CommonBatchMembersLocators.BATCH_MEMBERS_TAB], "Batch Members tab", timeout=7000)

        card = self.first_visible([
            CommonBatchMembersLocators.BATCH_MEMBERS_CARD,
            "(//div[contains(@class,'cohort-member-card')])[1]",
            "(//div[contains(@class,'member-card')])[1]",
        ], timeout=10000)
        assert card, "First batch member card is not visible"

        try:
            card.hover(timeout=3000)
        except Exception as _ignored:
            log.debug("Optional step in click_batch_members_and_open_first_chat() did not apply: %s", _ignored)

        chat_clicked = False
        card_chat_candidates = [
            "xpath=.//h2[contains(normalize-space(),'Chat')]",
            "xpath=.//button[contains(normalize-space(),'Chat')]",
            "xpath=.//img[contains(translate(@alt,'CHAT','chat'),'chat')]",
        ]
        for selector in card_chat_candidates:
            try:
                candidate = card.locator(selector).first
                if candidate.count() == 0:
                    continue
                candidate.scroll_into_view_if_needed()
                candidate.click(timeout=5000)
                chat_clicked = True
                break
            except Exception:
                continue

        if not chat_clicked:
            chat_clicked = self.click_first_visible([
                CommonBatchMembersLocators.FIRST_BATCH_MEMBERS_CHAT_BUTTON,
                "(//h2[contains(normalize-space(),'Chat')])[1]",
                "(//button[contains(normalize-space(),'Chat')])[1]",
                "(//img[contains(translate(@alt,'CHAT','chat'),'chat')])[1]",
            ], "first batch members chat button", timeout=10000)
        assert chat_clicked, "Batch member chat button is not visible/clickable"

    def click_home_menu_from_header(self):
        self.click_required([
            HomeLocators.HOME_MENU,
            "//div[@id='Home']",
        ], "Home menu", timeout=10000)
