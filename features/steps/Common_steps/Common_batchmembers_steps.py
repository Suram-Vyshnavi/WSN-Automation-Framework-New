import os

from behave import then

from pages.Common_pages.common_batchmembers_page import CommonBatchMembersPage
from utils.helpers import attach_screenshot


@then('common user clicks on "{batch_name}" batch from Active batches list')
def step_click_batch_from_active_list(context, batch_name):
	page = CommonBatchMembersPage(context.page)
	page.click_batch_from_active_list(batch_name)
	attach_screenshot(context.page, f"Clicked batch {batch_name} from Active list")


@then("common user validates the batch members tab and clicks on it")
def step_validate_batch_members_tab_and_click(context):
	page = CommonBatchMembersPage(context.page)
	page.validate_batch_members_tab_and_click()
	attach_screenshot(context.page, "Validated and clicked Batch Members tab")


@then("common user clicks on the manage student button")
def step_click_manage_student(context):
	page = CommonBatchMembersPage(context.page)
	page.click_manage_students()
	attach_screenshot(context.page, "Clicked Manage Students button")


@then("common user clicks on the invite students button and validated the batch code")
def step_click_invite_and_validate_batch_code(context):
	page = CommonBatchMembersPage(context.page)
	page.click_invite_students_and_validate_batch_code()
	attach_screenshot(context.page, "Clicked Invite Students and validated batch code")


@then("common user clicks on the batchcode copy button and paste it on the enter student email input field")
def step_copy_batchcode_and_paste(context):
	page = CommonBatchMembersPage(context.page)
	page.copy_batch_code_and_paste_in_email()
	attach_screenshot(context.page, "Copied batch code and pasted into email input")


@then('common user removes the batchcode from input field and user enters the email id "{email_id}" and clicks on the send invite button')
def step_remove_batchcode_and_send_email(context, email_id):
	page = CommonBatchMembersPage(context.page)
	page.remove_batch_code_and_send_email_invite(email_id)
	attach_screenshot(context.page, f"Entered {email_id} and clicked Send Invite")


@then("common user clicks on download template link and clicks on the upload file button and uploads the file and clicks on the file invite button")
def step_download_template_upload_and_invite(context):
	import glob
	workspace_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
	files_dir = os.path.join(workspace_path, "files")
	exact_file = os.path.join(files_dir, "WO-Student-bulk.xlsx")
	if os.path.exists(exact_file):
		upload_file_path = exact_file
	else:
		matches = sorted(glob.glob(os.path.join(files_dir, "WO-Student-bulk*")))
		if not matches:
			raise FileNotFoundError(f"No file matching 'WO-Student-bulk*' found in: {files_dir}")
		upload_file_path = matches[0]

	page = CommonBatchMembersPage(context.page)
	page.download_template_upload_file_and_invite(upload_file_path)
	attach_screenshot(context.page, "Downloaded template, uploaded file and clicked file invite")


@then("common user validates the uploaded users status bar and clicks on the uploaded users download button")
def step_validate_uploaded_users_status_and_download(context):
	page = CommonBatchMembersPage(context.page)
	page.validate_uploaded_users_status_and_download()
	attach_screenshot(context.page, "Validated uploaded users status and clicked download")


@then("common user clicks on the invite students back button")
def step_click_invite_students_back(context):
	page = CommonBatchMembersPage(context.page)
	page.click_invite_students_back()
	attach_screenshot(context.page, "Clicked Invite Students back button")


@then("common user validates the batch students tab and pending requests tab")
def step_validate_batch_students_and_pending(context):
	page = CommonBatchMembersPage(context.page)
	page.validate_batch_students_and_pending_requests()
	attach_screenshot(context.page, "Validated Batch Students and Pending Requests tabs")


@then("common user clicks on the batch students tab and validates the first user view button and download button")
def step_validate_first_user_view_and_download(context):
	page = CommonBatchMembersPage(context.page)
	page.validate_first_user_view_and_download_buttons()
	attach_screenshot(context.page, "Validated first user View and Download buttons")


@then("common user clicks on the view button and validates the certificate images and cicks on the download certificate button")
def step_view_and_validate_certificate(context):
	page = CommonBatchMembersPage(context.page)
	page.click_view_and_validate_certificate_images_download()
	attach_screenshot(context.page, "Validated certificate image and clicked download certificate")


@then("common user clicks on the close icon and the user clicks on the download certificate download button")
def step_close_certificate_and_download(context):
	page = CommonBatchMembersPage(context.page)
	page.close_certificate_and_download_from_list()
	attach_screenshot(context.page, "Closed certificate modal and clicked download")


@then("common user clicks on the user delete button and validates the remove student popup")
def step_delete_user_and_validate_popup(context):
	page = CommonBatchMembersPage(context.page)
	page.click_user_delete_and_validate_remove_popup()
	attach_screenshot(context.page, "Validated remove student popup")


@then("common user clicks on the no button from the popup and clicks on the pending requests tab")
def step_click_no_and_pending_tab(context):
	page = CommonBatchMembersPage(context.page)
	page.click_no_and_open_pending_requests()
	attach_screenshot(context.page, "Clicked No on popup and opened Pending Requests tab")


@then("common user clicks on the first user resend otp button and validates the resend otp popup")
def step_first_resend_and_validate_popup(context):
	page = CommonBatchMembersPage(context.page)
	page.click_first_resend_and_validate_popup()
	attach_screenshot(context.page, "Validated resend OTP popup")


@then("common user clicks on the yes button on resend otp popup and clicks on the manage students back button")
def step_confirm_resend_and_back(context):
	page = CommonBatchMembersPage(context.page)
	page.confirm_resend_and_click_manage_students_back()
	attach_screenshot(context.page, "Confirmed resend OTP and clicked manage students back")


@then("common user clicks on tha batch members tab and validates the first batch member card and clicks on the chat button")
def step_batch_member_card_and_chat(context):
	page = CommonBatchMembersPage(context.page)
	page.click_batch_members_and_open_first_chat()
	attach_screenshot(context.page, "Validated batch member card and clicked chat")


@then("common user clicks on the home menu from header section")
def step_click_home_menu_from_header(context):
	page = CommonBatchMembersPage(context.page)
	page.click_home_menu_from_header()
	attach_screenshot(context.page, "Clicked Home menu from header section")
