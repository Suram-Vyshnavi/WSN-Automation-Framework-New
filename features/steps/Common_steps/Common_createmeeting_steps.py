from behave import then

from pages.Common_pages.common_createmeeting_page import CommonCreateMeetingPage
from utils.helpers import attach_screenshot


@then("common user navigates to the batch details screen and navigates the upcoming activities section")
@then("user navigates to the batch details screen and navigates the upcoming activities section")
def step_navigate_to_batch_details_and_upcoming(context):
	page = CommonCreateMeetingPage(context.page)
	page.navigate_to_batch_details_and_upcoming_activities()
	attach_screenshot(context.page, "Navigated to batch details and upcoming activities")


@then("common user clicks on the create meeting button")
@then("user clicks on the create meeting button")
def step_click_create_meeting(context):
	page = CommonCreateMeetingPage(context.page)
	page.click_create_meeting_button()
	attach_screenshot(context.page, "Clicked create meeting button")


@then("common user validates the meeting title and validates the create new meeting card")
@then("user validates the meeting title and validates the create new meeting card")
def step_validate_meeting_title_and_card(context):
	page = CommonCreateMeetingPage(context.page)
	page.validate_meeting_title_and_new_meeting_card()
	attach_screenshot(context.page, "Validated meeting title and create new meeting card")


@then('common user clicks on the meeting input filed and enter the "{meeting_title}"')
@then('user clicks on the meeting input filed and enter the "{meeting_title}"')
def step_enter_meeting_title(context, meeting_title):
	page = CommonCreateMeetingPage(context.page)
	page.enter_meeting_title(meeting_title)
	attach_screenshot(context.page, f"Entered meeting title: {meeting_title}")


@then("common user clicks on the select date input field and validate the calendar date picker")
@then("user clicks on the select date input field and validate the calendar date picker")
def step_validate_calendar_picker(context):
	page = CommonCreateMeetingPage(context.page)
	page.click_date_and_validate_calendar()
	attach_screenshot(context.page, "Validated calendar date picker")


@then("common user clicks on the ok button and clicks on the timeslot dropdown and selects the 15min slot")
@then("user clicks on the ok button and clicks on the timeslot dropdown and selects the 15min slot")
def step_select_timeslot(context):
	page = CommonCreateMeetingPage(context.page)
	page.confirm_date_and_select_15min_slot()
	attach_screenshot(context.page, "Selected 15 min time slot")


@then('common user validates the meeting agend field and clicks on the meeting agenda input and enters the "{agenda_text}"')
@then('user validates the meeting agend field and clicks on the meeting agenda input and enters the "{agenda_text}"')
def step_enter_meeting_agenda(context, agenda_text):
	page = CommonCreateMeetingPage(context.page)
	page.validate_agenda_field_and_enter(agenda_text)
	attach_screenshot(context.page, f"Validated agenda field and entered: {agenda_text}")


@then('common user clicks on the notes input and enters the "{notes_text}"')
@then('user clicks on the notes input and enters the "{notes_text}"')
def step_enter_notes(context, notes_text):
	page = CommonCreateMeetingPage(context.page)
	page.enter_notes(notes_text)
	attach_screenshot(context.page, "Entered meeting notes")


@then("common user clicks on the create meeting button and go to the batch details screen")
@then("user clicks on the create meeting button and go to the batch details screen")
def step_create_meeting(context):
	page = CommonCreateMeetingPage(context.page)
	page.create_meeting_and_return_to_batch_details()
	attach_screenshot(context.page, "Created meeting and returned to batch details")


@then("common user clicks on the create meeting button and validates the create meeting confirmation card and clicks on the okay button")
@then("user clicks on the create meeting button and validates the create meeting confirmation card and clicks on the okay button")
def step_create_meeting_with_confirmation(context):
	page = CommonCreateMeetingPage(context.page)
	page.create_meeting_and_return_to_batch_details()
	page.validate_create_confirmation_and_click_okay()
	attach_screenshot(context.page, "Validated create meeting confirmation and clicked Okay")


@then("common user navigates to  batch details screen and refresh the screen")
@then("user navigates to  batch details screen and refresh the screen")
def step_refresh_batch_details_screen(context):
	page = CommonCreateMeetingPage(context.page)
	page.refresh_batch_details_screen()
	attach_screenshot(context.page, "Refreshed batch details screen after meeting creation")


@then("common user validates the meeting card under upcoming activities section and clicks on the meeting on the meeting card")
@then("user validates the meeting card under upcoming activities section and clicks on the meeting on the meeting card")
def step_open_meeting_card(context):
	page = CommonCreateMeetingPage(context.page)
	page.validate_meeting_card_and_open()
	attach_screenshot(context.page, "Validated and opened meeting card")


@then("common user validates the meeting check card and notes card")
@then("user validates the meeting check card and notes card")
def step_validate_meeting_check_and_notes(context):
	page = CommonCreateMeetingPage(context.page)
	page.validate_meeting_check_and_notes_cards()
	attach_screenshot(context.page, "Validated meeting check card and notes card")


@then("common user clicks on the meeting edit icon and enters the some value to notes and clicks on the update changes")
@then("user clicks on the meeting edit icon and enters the some value to notes and clicks on the update changes")
def step_edit_meeting_and_update(context):
	page = CommonCreateMeetingPage(context.page)
	page.edit_meeting_notes_and_update("Updated automation notes after review")
	attach_screenshot(context.page, "Edited meeting notes and updated changes")


@then("common user clicks on the delete icon and clicks on the delete button on the confirmation popup")
@then("user clicks on the delete icon and clicks on the delete button on the confirmation popup")
def step_delete_meeting(context):
	page = CommonCreateMeetingPage(context.page)
	page.delete_meeting_and_confirm()
	attach_screenshot(context.page, "Deleted meeting from confirmation popup")


@then("common user validates the delete event toast message and lands on the calendar screen")
@then("user validates the delete event toast message and lands on the calendar screen")
def step_validate_delete_event_toast(context):
	page = CommonCreateMeetingPage(context.page)
	page.validate_delete_event_toast_and_land_on_calendar()
	attach_screenshot(context.page, "Validated delete event flow and calendar landing")
