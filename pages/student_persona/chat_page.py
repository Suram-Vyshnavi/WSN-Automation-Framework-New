from pages.student_persona.student_persona_page import StudentPersonaPage
from locators.student_persona_locators import MessagesAndDiscussionsLocators
from utils.helpers import attach_screenshot
from utils.config import Config
from utils.logger import log


class ChatPage(StudentPersonaPage):
    def _dismiss_marketing_overlay(self):
        """Dismiss transient marketing/pop-up overlays that block header clicks."""
        for selector in [
            "#wzrk-cancel",
            "#wzrk-close",
            "//*[@id='wzrkImageOnlyDiv']//button[contains(@aria-label,'close') or contains(@class,'close')]",
            "//*[@id='wzrkImageOnlyDiv']//*[contains(@class,'close')]",
        ]:
            try:
                close_btn = self.page.locator(selector).first
                close_btn.wait_for(state="visible", timeout=900)
                close_btn.click(timeout=1500, force=True)
                self.pause(250)
            except Exception:
                continue

        try:
            self.page.evaluate(
                """() => {
                    const ids = ['wzrkImageOnlyDiv', 'wzrk_wrapper', 'wzrk_popup'];
                    ids.forEach(id => {
                        const el = document.getElementById(id);
                        if (el) el.remove();
                    });
                    document.querySelectorAll('ct-web-popup-imageonly, [id*="wzrk"], [class*="wzrk"]').forEach(el => {
                        try { el.remove(); } catch (_) {}
                    });
                }"""
            )
        except Exception as _ignored:
            log.debug("Optional step in _dismiss_marketing_overlay() did not apply: %s", _ignored)

    def _set_file_on_available_input(self, file_path, prefer_last=True, timeout=3000, accept_hint=None):
        """Bind file to any available input[type='file'] across frames."""
        selector_candidates = ["input[type='file']"]
        if accept_hint == "image":
            selector_candidates = [
                "input[type='file'][accept*='image']",
                "input[type='file'][accept*='.png']",
                "input[type='file'][accept*='.jpg']",
                "input[type='file'][accept*='.jpeg']",
                "input[type='file']",
            ]
        elif accept_hint == "document":
            selector_candidates = [
                "input[type='file'][accept*='pdf']",
                "input[type='file'][accept*='.doc']",
                "input[type='file'][accept*='.docx']",
                "input[type='file'][accept*='file']",
                "input[type='file']",
            ]

        frames = [self.page.main_frame] + [f for f in self.page.frames if f != self.page.main_frame]
        for frame in frames:
            for selector in selector_candidates:
                try:
                    file_inputs = frame.locator(selector)
                    file_inputs.first.wait_for(state="attached", timeout=timeout)
                    if prefer_last:
                        try:
                            file_inputs.last.set_input_files(file_path)
                        except Exception:
                            file_inputs.first.set_input_files(file_path)
                    else:
                        try:
                            file_inputs.first.set_input_files(file_path)
                        except Exception:
                            file_inputs.last.set_input_files(file_path)
                    return True
                except Exception:
                    continue
        return False

    def _click_send_when_ready(self, wait_ready_timeout=12000, confirm_timeout=10000):
        ready_selector = (
            "//div[contains(@class,'input_message_send') "
            "and not(contains(@class,'disable_button'))]"
        )
        disabled_selector = (
            "//div[contains(@class,'input_message_send') "
            "and contains(@class,'disable_button')]"
        )

        ready_wrapper = self.page.locator(ready_selector).first
        try:
            ready_wrapper.wait_for(state="visible", timeout=wait_ready_timeout)
        except Exception:
            attach_screenshot(self.page, "Send Button Not Ready (attachment not staged)")
            raise AssertionError("Send button never became ready - attachment was not staged")

        send_img = self.page.locator(ready_selector + "//img").first
        clicked = False
        for attempt in range(3):
            try:
                send_img.wait_for(state="visible", timeout=4000)
                try:
                    send_img.click(timeout=4000)
                except Exception:
                    send_img.click(timeout=4000, force=True)
                clicked = True
            except Exception as _ignored:
                log.debug("Optional step in _click_send_when_ready() did not apply: %s", _ignored)

            # Confirm the send consumed the staged content: the wrapper goes
            # back to the disabled state once nothing is left to send.
            try:
                self.page.locator(disabled_selector).first.wait_for(state="visible", timeout=confirm_timeout)
                attach_screenshot(self.page, "Send Confirmed (composer cleared)")
                return True
            except Exception:
                # Still staged - the click may not have registered; retry.
                continue

        assert clicked, "Send button is not visible/clickable"
        # Clicked but couldn't confirm clearing; let downstream validation decide.
        attach_screenshot(self.page, "Send Clicked (clear not confirmed)")
        return clicked

    def _close_visible_modal_if_any(self):
        """Close any blocking modal that may intercept menu clicks."""
        for selector in [
            "//div[contains(@class,'ant-modal-wrap') and not(contains(@style,'display: none'))]//button[contains(@aria-label,'close')]",
            "//div[contains(@class,'ant-modal-wrap') and not(contains(@style,'display: none'))]//span[contains(@class,'close')]",
            "//div[contains(@class,'ant-modal-wrap') and not(contains(@style,'display: none'))]//button[.='Close' or .='Cancel']",
        ]:
            try:
                close_btn = self.page.locator(selector).first
                close_btn.wait_for(state="visible", timeout=1200)
                close_btn.click(timeout=2000, force=True)
                self.pause(500)
                return
            except Exception:
                continue

    def click_accounts_menu(self):
        """Open Accounts menu from the student home screen."""
        # A modal left open by a preceding scenario (e.g. Validate Programs'
        # enroll-confirmation popup) can still have its mask in the DOM. A
        # force=True click then "succeeds" with no exception but actually
        # lands on the mask instead of the button underneath, so the dropdown
        # silently never opens - clear any such leftover modal first.
        self._close_visible_modal_if_any()
        self._dismiss_marketing_overlay()
        self.click_required([
            MessagesAndDiscussionsLocators.ACCOUNTS_MENU,
            "//button[@aria-label='Accounts menu']",
        ], "Accounts menu", timeout=30000)
        attach_screenshot(self.page, "Accounts Menu Clicked")

    def click_messages_and_discussions(self):
        """Click Messages & Discussions from the Accounts menu."""
        self._dismiss_marketing_overlay()
        clicked = self.click_first_visible([
            MessagesAndDiscussionsLocators.CHAT_ICON,
            "//p[contains(normalize-space(),'Messages & Discussions')]",
            "//*[contains(normalize-space(),'Messages') and contains(normalize-space(),'Discussions')]",
        ], "chat icon", timeout=20000)
        if not clicked:
            # Retry once: overlay may have closed the dropdown before selection,
            # or the accounts-menu click above landed on a leftover modal mask
            # instead of actually opening the dropdown.
            self._dismiss_marketing_overlay()
            self.click_accounts_menu()
            clicked = self.click_first_visible([
                MessagesAndDiscussionsLocators.CHAT_ICON,
                "//p[contains(normalize-space(),'Messages & Discussions')]",
                "//*[contains(normalize-space(),'Messages') and contains(normalize-space(),'Discussions')]",
            ], "chat icon", timeout=10000)
        assert clicked, "Messages & Discussions menu is not visible/clickable"
        attach_screenshot(self.page, "Messages And Discussions Opened")

    def click_chat_icon(self):
        """Backward-compatible alias for opening Messages & Discussions."""
        self.click_messages_and_discussions()
        attach_screenshot(self.page, "Chat Icon Clicked")

    def click_send_message_button(self):
        """Click on Send Message button"""
        clicked = self.click_first_visible([
            MessagesAndDiscussionsLocators.SEND_MESSAGE_BUTTON,
            "//button[normalize-space()='Send Message']",
            "//*[contains(normalize-space(),'Send Message')]",
        ], "send message button", timeout=8000)

        if clicked:
            attach_screenshot(self.page, "Send Message Button Clicked")
            return

        # Revamped UI may open the thread list directly without an explicit button.
        fallback_visible = self.first_visible_in_any_frame([
            MessagesAndDiscussionsLocators.FIRST_NEW_MESSAGE,
            "(//*[contains(@class,'search_result') and normalize-space(.)])[1]",
            "(//*[contains(@class,'conversation') and normalize-space(.)])[1]",
            MessagesAndDiscussionsLocators.MESSAGE_TEXTAREA,
        ], timeout_per_try=2500)
        assert fallback_visible is not None, "Send Message entry point is not visible"
        attach_screenshot(self.page, "Send Message Button Not Required In Current UI")

    def click_first_contact(self):
        """Open the first existing chat/conversation in the Messages list."""
        self.pause(2000)

        self.click_required([
            MessagesAndDiscussionsLocators.FIRST_CHAT_IN_LIST,
            "(//div[contains(@class,'conversation_card_container')])[1]",
            "(//div[contains(@class,'conversation__card__container')])[1]",
            MessagesAndDiscussionsLocators.FIRST_NEW_MESSAGE,
            "(//*[contains(@class,'search_result') and normalize-space(.)])[1]",
            "(//*[contains(@class,'chat') and contains(@class,'item') and normalize-space(.)])[1]",
            "(//li[normalize-space(.)])[1]",
        ], "First chat in the list", timeout=15000)

        attach_screenshot(self.page, "First Chat Selected")

    def send_message(self, message_text=None):
        """Type and send a message in the chat"""
        if message_text is None:
            message_text = Config.MESSAGE_TEXT

        # Support both textarea and contenteditable message composers.
        composer_candidates = [
            MessagesAndDiscussionsLocators.MESSAGE_TEXTAREA,
            "//*[@role='textbox' and not(contains(@aria-label,'Search')) and not(contains(@placeholder,'Search'))]",
            "//div[@contenteditable='true' and (@role='textbox' or contains(@class,'message') or contains(@class,'input'))]",
            "//textarea[not(contains(@placeholder,'Search'))]",
            "//div[contains(@class,'input_message')]//input[not(@type='file') and not(@placeholder='Search...')]",
            "//input[contains(translate(@placeholder,'MESSAGE','message'),'message')]",
            "//textarea",
        ]
        # The conversation pane + composer load asynchronously after the
        # contact is selected, so poll over a few attempts. If the composer
        # still hasn't rendered, re-select the contact and keep trying. This
        # guards against a timing race where the composer isn't yet attached.
        composer = None
        for attempt in range(4):
            # Let any in-flight conversation load settle before searching.
            try:
                self.page.wait_for_load_state("networkidle", timeout=4000)
            except Exception as _ignored:
                log.debug("Optional step in send_message() did not apply: %s", _ignored)

            composer = self.first_visible_in_any_frame(composer_candidates, timeout_per_try=3000)
            if composer is not None:
                break

            # Re-select the thread once more before retrying; some revamped
            # flows only render the composer after a second selection.
            try:
                self.click_first_contact()
            except Exception as _ignored:
                log.debug("Optional step in send_message() did not apply: %s", _ignored)

        if composer is None:
            attach_screenshot(self.page, "Message Composer Not Visible")
            raise AssertionError("Message composer not visible")

        log.info(f"Typing message: {message_text}")

        # Fill works for textarea; fall back to click+type for contenteditable.
        try:
            composer.fill(message_text)
        except Exception:
            composer.click()
            self.page.keyboard.type(message_text)

        attach_screenshot(self.page, "Message Typed")
        
        # Click send icon with fallbacks; some variants only send on Enter.
        send_clicked = False
        send_candidates = [
            MessagesAndDiscussionsLocators.SEND_MESSAGE_ICON,
            "//img[@alt='send message']",
            "//button[contains(@aria-label,'send') or contains(@title,'send')]",
            "//span[contains(@class,'send')]",
        ]
        for selector in send_candidates:
            candidate = self.page.locator(selector).first
            try:
                candidate.wait_for(state="visible", timeout=2500)
                try:
                    candidate.click(timeout=3000)
                except Exception:
                    candidate.click(timeout=3000, force=True)
                send_clicked = True
                break
            except Exception:
                continue

        if not send_clicked:
            try:
                composer.press("Enter")
                send_clicked = True
            except Exception:
                send_clicked = False

        assert send_clicked, "Send message icon/button is not visible/clickable"
        attach_screenshot(self.page, "Message Sent")

    def validate_latest_text_message(self):
        """Validate that the latest sent text message is visible"""
        try:
            latest_locator = self.page.locator(
                f"//*[contains(normalize-space(.), '{Config.MESSAGE_TEXT}') and not(self::script)]"
            ).first
            latest_locator.wait_for(state="visible", timeout=15000)
            latest_message = latest_locator
            message_visible = latest_message.is_visible()
            assert message_visible, f"Latest sent text message '{Config.MESSAGE_TEXT}' is not visible"
            
            # Get and print message text
            message_text = latest_message.inner_text()
            log.info(f"Latest text message validated: {message_text}")
            attach_screenshot(self.page, f"Latest Text Message Validated - {message_text}")
            return True
        except Exception as e:
            log.warning(f"Failed to validate latest text message: {e}")
            attach_screenshot(self.page, "Text Message Validation Failed")
            raise

    def validate_latest_image(self):
        """Validate that the latest sent image is visible"""
        try:
            self.page.locator(MessagesAndDiscussionsLocators.LATEST_SENT_IMAGE).wait_for(state="visible", timeout=15000)
            latest_image = self.page.locator(MessagesAndDiscussionsLocators.LATEST_SENT_IMAGE).first
            image_visible = latest_image.is_visible()
            assert image_visible, "Latest sent image is not visible"
            
            log.info("Latest image validated successfully")
            attach_screenshot(self.page, "Latest Image Validated")
            return True
        except Exception as e:
            log.warning(f"Failed to validate latest image: {e}")
            attach_screenshot(self.page, "Image Validation Failed")
            raise

    def validate_latest_document(self):
        """Validate that the latest sent document is visible"""
        try:
            latest_document = self.first_visible_in_any_frame([
                MessagesAndDiscussionsLocators.LATEST_SENT_DOCUMENT,
                "(//span[contains(@class,'download') and contains(@class,'chat-File-Icon')] | //a[contains(@href,'.pdf')] | //span[contains(normalize-space(.),'.pdf')])[last()]",
                "(//*[contains(normalize-space(.),'Test_File_Upload')])[last()]",
            ], timeout_per_try=6000)
            assert latest_document is not None, "Latest sent document is not visible"
            document_visible = latest_document.is_visible()
            assert document_visible, "Latest sent document is not visible"
            
            log.info("Latest document validated successfully")
            attach_screenshot(self.page, "Latest Document Validated")
            return True
        except Exception as e:
            log.warning(f"Failed to validate latest document: {e}")
            attach_screenshot(self.page, "Document Validation Failed")
            raise

    def click_file_upload_button(self):
        """Click on file upload button"""
        self.click_required([
            MessagesAndDiscussionsLocators.FILE_UPLOAD_BUTTON,
            "//span[contains(@class,'attachment-popover')]",
            "//div[contains(@class,'input_message')]//span[@tabindex='0']",
        ], "File upload button", timeout=10000)
        attach_screenshot(self.page, "File Upload Button Clicked")

    def upload_photo(self, photo_path):
        """Upload a photo to the chat"""
        try:
            image_option = self.first_visible_in_any_frame([
                MessagesAndDiscussionsLocators.IMAGE_OPTION,
                "//*[normalize-space()='Image' or normalize-space()='Photo' or normalize-space()='Gallery']",
            ], timeout_per_try=2500)

            if not image_option:
                self.click_file_upload_button()
                image_option = self.first_visible_in_any_frame([
                    MessagesAndDiscussionsLocators.IMAGE_OPTION,
                    "//*[normalize-space()='Image' or normalize-space()='Photo' or normalize-space()='Gallery']",
                ], timeout_per_try=3000)

            bound = False
            if image_option:
                try:
                    with self.page.expect_file_chooser(timeout=5000) as chooser_info:
                        image_option.click(timeout=5000)
                    chooser_info.value.set_files(photo_path)
                    bound = True
                except Exception:
                    try:
                        image_option.click(timeout=5000, force=True)
                    except Exception as _ignored:
                        log.debug("Optional step in upload_photo() did not apply: %s", _ignored)
                    bound = self._set_file_on_available_input(photo_path, prefer_last=True, timeout=8000, accept_hint="image")

            if not bound:
                bound = self._set_file_on_available_input(photo_path, prefer_last=True, timeout=6000, accept_hint="image")

            assert bound, "Unable to attach photo file after selecting image upload option"

            # Wait for the photo to actually register in the composer before
            # sending; the image attaches asynchronously and an early send click
            # would otherwise be a no-op.
            attached = self.first_visible_in_any_frame([
                "//div[contains(@class,'input_message')]//*[contains(@class,'attached-image')]",
                "//div[contains(@class,'input_message')]//*[contains(@class,'attached')]",
            ], timeout_per_try=10000)
            if attached is None:
                attach_screenshot(self.page, "Photo Attachment Indicator Not Found")

            # Click send only once ready, then confirm it was sent.
            self._click_send_when_ready()

            # Validate photo was uploaded
            self.validate_latest_image()
            log.info("Photo uploaded and validated successfully")
        except Exception as e:
            log.warning(f"Failed to upload photo: {e}")
            attach_screenshot(self.page, "Photo Upload Failed")
            raise

    def upload_document(self, document_path):
        """Upload a document to the chat"""
        try:
            doc_option = self.first_visible_in_any_frame([
                MessagesAndDiscussionsLocators.DOCUMENT_OPTION,
                "//*[normalize-space()='Document' or normalize-space()='File' or normalize-space()='Doc']",
            ], timeout_per_try=2500)

            if not doc_option:
                self.click_file_upload_button()
                doc_option = self.first_visible_in_any_frame([
                    MessagesAndDiscussionsLocators.DOCUMENT_OPTION,
                    "//*[normalize-space()='Document' or normalize-space()='File' or normalize-space()='Doc']",
                ], timeout_per_try=3000)

            bound = False
            if doc_option:
                try:
                    with self.page.expect_file_chooser(timeout=5000) as chooser_info:
                        doc_option.click(timeout=5000)
                    chooser_info.value.set_files(document_path)
                    bound = True
                except Exception:
                    try:
                        doc_option.click(timeout=5000, force=True)
                    except Exception as _ignored:
                        log.debug("Optional step in upload_document() did not apply: %s", _ignored)
                    bound = self._set_file_on_available_input(document_path, prefer_last=False, timeout=8000, accept_hint="document")

            if not bound:
                bound = self._set_file_on_available_input(document_path, prefer_last=False, timeout=6000, accept_hint="document")

            assert bound, "Unable to attach document file after selecting document upload option"

            # Wait for the document to register in the composer before sending.
            attached = self.first_visible_in_any_frame([
                "//div[contains(@class,'input_message')]//*[contains(@class,'attached-file')]",
                "//div[contains(@class,'input_message')]//*[contains(@class,'attached')]",
            ], timeout_per_try=10000)
            if attached is None:
                attach_screenshot(self.page, "Document Attachment Indicator Not Found")

            # Click send only once ready, then confirm it was sent.
            self._click_send_when_ready()

            # Validate document was uploaded
            self.validate_latest_document()
            log.info("Document uploaded and validated successfully")
        except Exception as e:
            log.warning(f"Failed to upload document: {e}")
            attach_screenshot(self.page, "Document Upload Failed")
            raise

    def navigate_to_home_page(self):
        """Navigate back to Home from chat screens."""
        self._close_visible_modal_if_any()
        self.click_required([
            "//div[@id='Home']",
            "//p[normalize-space()='Home']",
            "//button[@aria-label='Home menu']",
            # Prod's mobile-new-ui header hides the desktop #Home and shows a
            # mobile home button labelled just 'Home'.
            "//button[@aria-label='Home']",
        ], "Home menu", timeout=15000)
        self.pause(1500)
        attach_screenshot(self.page, "Navigated To Home From Chat")
