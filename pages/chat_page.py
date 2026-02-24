from pages.base_page import BasePage
from utils.locators import LoginLocators, Messages_and_discussionsLocators
from utils.helpers import attach_screenshot
from utils.config import Config
import os


class ChatPage(BasePage):
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
        self.page.locator(Messages_and_discussionsLocators.FIRST_NEW_MESSAGE).wait_for(state="visible", timeout=15000)
        self.page.click(Messages_and_discussionsLocators.FIRST_NEW_MESSAGE)
        attach_screenshot(self.page, "First Contact Selected")

    def send_message(self, message_text=None):
        """Type and send a message in the chat"""
        if message_text is None:
            message_text = Config.MESSAGE_TEXT
        
        # Wait for message textarea to be visible
        self.page.locator(Messages_and_discussionsLocators.MESSAGE_TEXTAREA).wait_for(state="visible", timeout=15000)
        print(f"Typing message: {message_text}")
        
        # Type the message
        self.page.fill(Messages_and_discussionsLocators.MESSAGE_TEXTAREA, message_text)
        attach_screenshot(self.page, "Message Typed")
        
        # Click send icon
        self.page.locator(Messages_and_discussionsLocators.SEND_MESSAGE_ICON).wait_for(state="visible", timeout=10000)
        print("Clicking send message icon...")
        self.page.click(Messages_and_discussionsLocators.SEND_MESSAGE_ICON)
        attach_screenshot(self.page, "Message Sent")

    def validate_latest_text_message(self):
        """Validate that the latest sent text message is visible"""
        try:
            self.page.locator(Messages_and_discussionsLocators.LATEST_SENT_MESSAGE).wait_for(state="visible", timeout=15000)
            latest_message = self.page.locator(Messages_and_discussionsLocators.LATEST_SENT_MESSAGE).first
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
        self.page.locator(Messages_and_discussionsLocators.FILE_UPLOAD_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.click(Messages_and_discussionsLocators.FILE_UPLOAD_BUTTON)
        attach_screenshot(self.page, "File Upload Button Clicked")

    def upload_photo(self, photo_path):
        """Upload a photo to the chat"""
        try:
            # Click on Image option
            self.page.locator(Messages_and_discussionsLocators.IMAGE_OPTION).wait_for(state="visible", timeout=10000)
            print("Clicking Image option...")
            self.page.click(Messages_and_discussionsLocators.IMAGE_OPTION)
            
            # Wait for file input to be available
            
            # Find and interact with the file input element
            file_input = self.page.locator("input[type='file']").last
            print(f"Uploading photo: {photo_path}")
            file_input.set_input_files(photo_path)
            
            # Click send
            self.page.locator(Messages_and_discussionsLocators.SEND_MESSAGE_ICON).wait_for(state="visible", timeout=10000)
            self.page.click(Messages_and_discussionsLocators.SEND_MESSAGE_ICON)
            
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
            # Click on Document option
            self.page.locator(Messages_and_discussionsLocators.DOCUMENT_OPTION).wait_for(state="visible", timeout=10000)
            print("Clicking Document option...")
            self.page.click(Messages_and_discussionsLocators.DOCUMENT_OPTION)
            
            # Wait for file input to be available
            
            # Find and interact with the file input element
            file_input = self.page.locator("input[type='file']").first
            print(f"Uploading document: {document_path}")
            file_input.set_input_files(document_path)
            
            # Click send
            self.page.locator(Messages_and_discussionsLocators.SEND_MESSAGE_ICON).wait_for(state="visible", timeout=10000)
            self.page.click(Messages_and_discussionsLocators.SEND_MESSAGE_ICON)
            
            # Validate document was uploaded
            self.validate_latest_document()
            print("Document uploaded and validated successfully")
        except Exception as e:
            print(f"Failed to upload document: {e}")
            attach_screenshot(self.page, "Document Upload Failed")
            raise
