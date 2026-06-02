from behave import given, when, then
from pages.chat_page import ChatPage
from pages.login_page import LoginPage
from utils.config import Config
from utils.helpers import attach_screenshot
import os


def _project_root_from_here():
    """Resolve repo root by walking up until behave.ini is found."""
    current = os.path.abspath(os.path.dirname(__file__))
    while True:
        if os.path.exists(os.path.join(current, "behave.ini")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            raise FileNotFoundError("Could not locate project root (behave.ini not found)")
        current = parent


@then("user clicks on Accounts menu")
def click_accounts_menu(context):
    chat_page = ChatPage(context.page)
    chat_page.click_accounts_menu()


@then("user clicks on Messages & Discussions")
def click_messages_and_discussions(context):
    chat_page = ChatPage(context.page)
    chat_page.click_messages_and_discussions()


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
    project_root = _project_root_from_here()
    photo_candidates = [
        os.path.join(project_root, "files", "Test_Photo_Upload.png"),
        os.path.join(project_root, "files", "Institute-image.jpg"),
    ]
    photo_path = next((p for p in photo_candidates if os.path.exists(p)), None)
    if photo_path is None:
        raise FileNotFoundError(f"Photo file not found. Checked: {photo_candidates}")
    
    chat_page = ChatPage(context.page)
    chat_page.upload_photo(photo_path)
    
    # Wait for photo upload to complete before opening file menu again
    
    # Click file upload button again for the next upload

@then("user uploads document in to the chat and validates")
def upload_document(context):
    project_root = _project_root_from_here()
    document_path = os.path.join(project_root, "files", "Test_File_Upload.pdf")

    if not os.path.exists(document_path):
        raise FileNotFoundError(f"Document file not found: {document_path}")
    
    chat_page = ChatPage(context.page)
    chat_page.upload_document(document_path)


@then("user navigates to home page")
def navigate_to_home(context):
    persona = getattr(context, "persona", "student")
    if persona == "faculty":
        from pages.Faculty_pages.Home_page import FacultyHomePage

        faculty_home_page = FacultyHomePage(context.page)
        faculty_home_page.navigate_to_home()
    else:
        chat_page = ChatPage(context.page)
        chat_page.navigate_to_home_page()
    attach_screenshot(context.page, "Navigated to Home Page")
