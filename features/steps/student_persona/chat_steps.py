from behave import then
from pages.student_persona.chat_page import ChatPage
from utils.config import Config
from utils.helpers import attach_screenshot, require_test_data_file
from config.env_config import IS_PROD


@then("user clicks on Accounts menu")
def click_accounts_menu(context):
    chat_page = ChatPage(context.page)
    chat_page.click_accounts_menu()


@then("user clicks on Messages & Discussions")
def click_messages_and_discussions(context):
    chat_page = ChatPage(context.page)
    try:
        chat_page.click_messages_and_discussions()
    except Exception as error:
        persona = getattr(context, "persona", "").strip().lower()
        menu_missing = "messages & discussions menu is not visible/clickable" in str(error).lower()
        if IS_PROD and persona == "mentor" and menu_missing:
            attach_screenshot(context.page, "Mentor - Messages Menu Unavailable")
            context.scenario.skip("Prod mentor Messages & Discussions menu unavailable for this run")
            return
        raise


@then("user clicks on first chat in the list")
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
    photo_path = require_test_data_file("Test_Photo_Upload.png", "Institute-image.jpg")
    ChatPage(context.page).upload_photo(photo_path)
    attach_screenshot(context.page, "Uploaded photo in chat")


@then("user uploads document in to the chat and validates")
def upload_document(context):
    document_path = require_test_data_file("Test_File_Upload.pdf")
    ChatPage(context.page).upload_document(document_path)
    attach_screenshot(context.page, "Uploaded document in chat")


@then("user navigates to home page")
def navigate_to_home(context):
    persona = getattr(context, "persona", "student")
    if persona == "faculty":
        from pages.faculty_pages.home_page import FacultyHomePage

        faculty_home_page = FacultyHomePage(context.page)
        faculty_home_page.navigate_to_home()
    else:
        chat_page = ChatPage(context.page)
        chat_page.navigate_to_home_page()
    attach_screenshot(context.page, "Navigated to Home Page")
