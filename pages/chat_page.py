from pages.base_page import BasePage
from locators.student_locators import LoginLocators, Messages_and_discussionsLocators
from utils.helpers import attach_screenshot
from utils.config import Config
import os


class ChatPage(BasePage):
    def _first_visible_in_any_frame(self, selectors, timeout_per_try=2500):
        frames = [self.page.main_frame] + [f for f in self.page.frames if f != self.page.main_frame]
        for frame in frames:
            for selector in selectors:
                locator = frame.locator(selector).first
                try:
                    locator.wait_for(state="visible", timeout=timeout_per_try)
                    return locator
                except Exception:
                    continue
        return None

    def _click_first_visible(self, selectors, timeout=10000):
        for selector in selectors:
            candidate = self.page.locator(selector).first
            try:
                candidate.wait_for(state="visible", timeout=timeout)
                try:
                    candidate.click(timeout=timeout)
                except Exception:
                    candidate.click(timeout=timeout, force=True)
                return True
            except Exception:
                continue
        return False

    def click_chat_icon(self):
        """Click on chat icon to open messages"""
        self.page.locator(LoginLocators.CHAT_ICON).wait_for(state="visible", timeout=20000)
        self.page.click(LoginLocators.CHAT_ICON)
        attach_screenshot(self.page, "Chat Icon Clicked")

    def click_send_message_button(self):
        """Click on Send Message button"""
        self.page.locator(Messages_and_discussionsLocators.SEND_MESSAGE_BUTTON).wait_for(state="visible", timeout=15000)
        self.page.click(Messages_and_discussionsLocators.SEND_MESSAGE_BUTTON)
        attach_screenshot(self.page, "Send Message Button Clicked")

    def click_first_contact(self):
        """Click on first contact in the search results"""
        self.page.wait_for_timeout(5000)
        self.page.locator(Messages_and_discussionsLocators.FIRST_NEW_MESSAGE).wait_for(state="visible", timeout=15000)
        self.page.click(Messages_and_discussionsLocators.FIRST_NEW_MESSAGE)

        # Ensure thread pane is active; retry once if composer region is not present yet.
        composer_region = self._first_visible_in_any_frame([
            "//div[contains(@class,'input_message')]",
            "//textarea",
            "//*[@contenteditable='true']",
        ], timeout_per_try=2000)
        if not composer_region:
            self.page.click(Messages_and_discussionsLocators.FIRST_NEW_MESSAGE)

        attach_screenshot(self.page, "First Contact Selected")

    def send_message(self, message_text=None):
        """Type and send a message in the chat"""
        if message_text is None:
            message_text = Config.MESSAGE_TEXT

        # Support both textarea and contenteditable message composers.
        composer_candidates = [
            Messages_and_discussionsLocators.MESSAGE_TEXTAREA,
            "//div[@contenteditable='true' and (@role='textbox' or contains(@class,'message') or contains(@class,'input'))]",
            "//div[contains(@class,'input_message')]//input[not(@type='file') and not(@placeholder='Search...')]",
            "//textarea",
        ]
        composer = self._first_visible_in_any_frame(composer_candidates, timeout_per_try=3000)

        if composer is None:
            raise AssertionError("Message composer not visible")

        print(f"Typing message: {message_text}")

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
            Messages_and_discussionsLocators.SEND_MESSAGE_ICON,
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
            print(f"Latest text message validated: {message_text}")
            attach_screenshot(self.page, f"Latest Text Message Validated - {message_text}")
            return True
        except Exception as e:
            print(f"Failed to validate latest text message: {e}")
            attach_screenshot(self.page, "Text Message Validation Failed")
            raise

    def validate_latest_image(self):
        """Validate that the latest sent image is visible"""
        try:
            self.page.locator(Messages_and_discussionsLocators.LATEST_SENT_IMAGE).wait_for(state="visible", timeout=15000)
            latest_image = self.page.locator(Messages_and_discussionsLocators.LATEST_SENT_IMAGE).first
            image_visible = latest_image.is_visible()
            assert image_visible, "Latest sent image is not visible"
            
            print("Latest image validated successfully")
            attach_screenshot(self.page, "Latest Image Validated")
            return True
        except Exception as e:
            print(f"Failed to validate latest image: {e}")
            attach_screenshot(self.page, "Image Validation Failed")
            raise

    def validate_latest_document(self):
        """Validate that the latest sent document is visible"""
        try:
            self.page.locator(Messages_and_discussionsLocators.LATEST_SENT_DOCUMENT).wait_for(state="visible", timeout=15000)
            latest_document = self.page.locator(Messages_and_discussionsLocators.LATEST_SENT_DOCUMENT).first
            document_visible = latest_document.is_visible()
            assert document_visible, "Latest sent document is not visible"
            
            print("Latest document validated successfully")
            attach_screenshot(self.page, "Latest Document Validated")
            return True
        except Exception as e:
            print(f"Failed to validate latest document: {e}")
            attach_screenshot(self.page, "Document Validation Failed")
            raise

    def click_file_upload_button(self):
        """Click on file upload button"""
        clicked = self._click_first_visible([
            Messages_and_discussionsLocators.FILE_UPLOAD_BUTTON,
            "//span[contains(@class,'attachment-popover')]",
            "//div[contains(@class,'input_message')]//span[@tabindex='0']",
        ], timeout=10000)
        assert clicked, "File upload button is not visible/clickable"
        attach_screenshot(self.page, "File Upload Button Clicked")

    def upload_photo(self, photo_path):
        """Upload a photo to the chat"""
        try:
            # Re-open upload trigger because transient menu might close between steps.
            self.click_file_upload_button()

            option_clicked = self._click_first_visible([
                Messages_and_discussionsLocators.IMAGE_OPTION,
                "//*[normalize-space()='Image' or normalize-space()='Photo' or normalize-space()='Gallery']",
            ], timeout=4000)

            if option_clicked:
                file_input = self.page.locator("input[type='file']").last
                file_input.wait_for(state="attached", timeout=10000)
                print(f"Uploading photo: {photo_path}")
                file_input.set_input_files(photo_path)
            else:
                # Direct chooser/file-input variant.
                bound = False
                try:
                    file_input = self.page.locator("input[type='file']").last
                    file_input.wait_for(state="attached", timeout=3000)
                    file_input.set_input_files(photo_path)
                    bound = True
                except Exception:
                    bound = False
                if not bound:
                    with self.page.expect_file_chooser(timeout=8000) as chooser_info:
                        self.click_file_upload_button()
                    chooser_info.value.set_files(photo_path)
            
            # Click send
            send_clicked = self._click_first_visible([
                Messages_and_discussionsLocators.SEND_MESSAGE_ICON,
                "//img[@alt='send message']",
                "//button[contains(@aria-label,'send') or contains(@title,'send')]",
            ], timeout=10000)
            assert send_clicked, "Send message icon/button is not visible after photo upload"
            
            # Validate photo was uploaded
            self.validate_latest_image()
            print("Photo uploaded and validated successfully")
        except Exception as e:
            print(f"Failed to upload photo: {e}")
            attach_screenshot(self.page, "Photo Upload Failed")
            raise

    def upload_document(self, document_path):
        """Upload a document to the chat"""
        try:
            self.click_file_upload_button()

            option_clicked = self._click_first_visible([
                Messages_and_discussionsLocators.DOCUMENT_OPTION,
                "//*[normalize-space()='Document' or normalize-space()='File' or normalize-space()='Doc']",
            ], timeout=4000)

            if option_clicked:
                file_input = self.page.locator("input[type='file']").first
                file_input.wait_for(state="attached", timeout=10000)
                print(f"Uploading document: {document_path}")
                file_input.set_input_files(document_path)
            else:
                bound = False
                try:
                    file_input = self.page.locator("input[type='file']").first
                    file_input.wait_for(state="attached", timeout=3000)
                    file_input.set_input_files(document_path)
                    bound = True
                except Exception:
                    bound = False
                if not bound:
                    with self.page.expect_file_chooser(timeout=8000) as chooser_info:
                        self.click_file_upload_button()
                    chooser_info.value.set_files(document_path)
            
            # Click send
            send_clicked = self._click_first_visible([
                Messages_and_discussionsLocators.SEND_MESSAGE_ICON,
                "//img[@alt='send message']",
                "//button[contains(@aria-label,'send') or contains(@title,'send')]",
            ], timeout=10000)
            assert send_clicked, "Send message icon/button is not visible after document upload"
            
            # Validate document was uploaded
            self.validate_latest_document()
            print("Document uploaded and validated successfully")
        except Exception as e:
            print(f"Failed to upload document: {e}")
            attach_screenshot(self.page, "Document Upload Failed")
            raise
