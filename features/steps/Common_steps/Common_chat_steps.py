import os

from behave import then

from pages.Common_pages.common_chat_page import CommonChatPage
from utils.config import Config
from utils.helpers import attach_screenshot


@then("common user clicks on chat icon")
def step_click_chat_icon(context):
	page = CommonChatPage(context.page)
	page.click_chat_icon()
	attach_screenshot(context.page, "Clicked chat icon")


@then("common user clicks on send message button")
def step_click_send_message(context):
	page = CommonChatPage(context.page)
	page.click_send_message_button()
	attach_screenshot(context.page, "Clicked send message button")


@then("common user clicks on first contact in the list")
def step_click_first_contact(context):
	page = CommonChatPage(context.page)
	page.click_first_contact()
	attach_screenshot(context.page, "Clicked first contact")


@then("common user sends a message")
def step_send_message(context):
	page = CommonChatPage(context.page)
	page.send_message(Config.MESSAGE_TEXT)
	attach_screenshot(context.page, "Sent message in chat")


@then("common user validates the latest message sent")
def step_validate_latest_message(context):
	page = CommonChatPage(context.page)
	page.validate_latest_message_sent(Config.MESSAGE_TEXT)
	attach_screenshot(context.page, "Validated latest message")


@then("common user clicks on file upload button")
def step_click_file_upload(context):
	page = CommonChatPage(context.page)
	page.click_file_upload_button()
	attach_screenshot(context.page, "Clicked file upload button")


@then("common user uploads photo in to chat and validates")
def step_upload_photo(context):
	import glob
	workspace_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
	files_dir = os.path.join(workspace_path, "files")
	candidates = [
		os.path.join(files_dir, "Test_Photo_Upload.png"),
		os.path.join(files_dir, "Institute-image.jpg"),
	]
	photo_path = None
	for candidate in candidates:
		if os.path.exists(candidate):
			photo_path = candidate
			break
	if photo_path is None:
		image_matches = sorted(glob.glob(os.path.join(files_dir, "*.png")) + glob.glob(os.path.join(files_dir, "*.jpg")) + glob.glob(os.path.join(files_dir, "*.jpeg")))
		if image_matches:
			photo_path = image_matches[0]
	if photo_path is None:
		raise FileNotFoundError(f"No image file found in: {files_dir}")

	page = CommonChatPage(context.page)
	page.upload_photo(photo_path)
	attach_screenshot(context.page, "Uploaded and validated photo in chat")


@then("common user uploads document in to the chat and validates")
def step_upload_document(context):
	workspace_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
	document_path = os.path.join(workspace_path, "files", "Test_File_Upload.pdf")
	if not os.path.exists(document_path):
		raise FileNotFoundError(f"Document file not found: {document_path}")

	page = CommonChatPage(context.page)
	page.upload_document(document_path)
	attach_screenshot(context.page, "Uploaded and validated document in chat")


@then("common user navigates to home page")
def step_navigate_home(context):
	page = CommonChatPage(context.page)
	page.navigate_to_home_page()
	attach_screenshot(context.page, "Navigated to home page")
