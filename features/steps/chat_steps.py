from behave import given, when, then
from pages.chat_page import ChatPage
from pages.login_page import LoginPage
from utils.config import Config
from utils.helpers import attach_screenshot
import os


@then("user clicks on chat icon")
def click_chat_icon(context):
    chat_page = ChatPage(context.page)
    chat_page.click_chat_icon()


@then("user clicks on send message button")
def click_send_message(context):
    chat_page = ChatPage(context.page)
    chat_page.click_send_message_button()


@then("user clicks on first contact in the list")
def click_first_contact(context):
    chat_page = ChatPage(context.page)
    chat_page.click_first_contact()


@then("user sends a message")
def send_message(context):
    chat_page = ChatPage(context.page)
    message = Config.MESSAGE_TEXT
    chat_page.send_message(message)


@then("user validates the latest message sent")
def validate_latest_message(context):
    chat_page = ChatPage(context.page)
    chat_page.validate_latest_text_message()


@then("user clicks on file upload button")
def click_file_upload(context):
    chat_page = ChatPage(context.page)
    chat_page.click_file_upload_button()


@then("user uploads photo in to chat and validates")
def upload_photo(context):
    # Get the absolute path to the photo file
    workspace_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    photo_path = os.path.join(workspace_path, "files", "Test_Photo_Upload.png")
    
    if not os.path.exists(photo_path):
        raise FileNotFoundError(f"Photo file not found: {photo_path}")
    
    chat_page = ChatPage(context.page)
    chat_page.upload_photo(photo_path)
    
    # Wait for photo upload to complete before opening file menu again
    
    # Click file upload button again for the next upload

@then("user uploads document in to the chat and validates")
def upload_document(context):
    # Get the absolute path to the document file
    
    workspace_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    document_path = os.path.join(workspace_path, "files", "Test_File_Upload.pdf")
    
    if not os.path.exists(document_path):
        raise FileNotFoundError(f"Document file not found: {document_path}")
    
    chat_page = ChatPage(context.page)
    chat_page.upload_document(document_path)


@then("user navigates to home page")
def navigate_to_home(context):
    login_page = LoginPage(context.page)
    login_page.navigate_to_home()
    attach_screenshot(context.page, "Navigated to Home Page")
