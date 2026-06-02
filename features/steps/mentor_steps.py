from behave import given, then
from pages.mentor_page import MentorPage
from pages.mentor_profile_page import MentorProfilePage
from utils.helpers import attach_screenshot


@then("user clicks on customize weekly schedule")
def click_customize_weekly_schedule(context):
    mentor = MentorPage(context.page)
    try:
        mentor.click_customize_weekly_schedule()
        attach_screenshot(context.page, "Mentor - Customize Weekly Schedule Clicked")
    except Exception as e:
        attach_screenshot(context.page, "Mentor - Customize Weekly Schedule Error")
        raise


@then("user add slot button selects the start time slot  and end time slot")
def add_slot_select_start_and_end_time(context):
    mentor = MentorPage(context.page)
    try:
        mentor.add_slot_select_start_and_end_time()
        attach_screenshot(context.page, "Mentor - Start and End Time Selected")
    except Exception as e:
        attach_screenshot(context.page, "Mentor - Start End Time Selection Error")
        raise


@then("user clicks on the copy slot button ans selects the day option")
def click_copy_slot_and_select_day_typo(context):
    mentor = MentorPage(context.page)
    try:
        mentor.click_copy_slot_and_select_day()
        attach_screenshot(context.page, "Mentor - Copy Slot Day Selected")
    except Exception as e:
        attach_screenshot(context.page, "Mentor - Copy Slot Day Selection Error")
        raise


@then("user clicks on apply button and closes the slot button")
def click_apply_and_close_slot(context):
    mentor = MentorPage(context.page)
    try:
        mentor.click_apply_and_close_slot()
        attach_screenshot(context.page, "Mentor - Apply and Close Slot")
    except Exception as e:
        attach_screenshot(context.page, "Mentor - Apply Close Slot Error")
        raise


@then("user clicks on add override button and selects the start time slot and end time slot")
def click_add_override_select_times(context):
    mentor = MentorPage(context.page)
    try:
        mentor.click_add_override_select_start_and_end_time()
        attach_screenshot(context.page, "Mentor - Override Start and End Time Selected")
    except Exception as e:
        attach_screenshot(context.page, "Mentor - Override Time Selection Error")
        raise


@then("user clicks on the copy slot button and selects the day option")
def click_copy_slot_and_select_day(context):
    mentor = MentorPage(context.page)
    try:
        mentor.click_copy_slot_and_select_day()
        attach_screenshot(context.page, "Mentor - Override Copy Slot Day Selected")
    except Exception as e:
        attach_screenshot(context.page, "Mentor - Override Copy Slot Day Error")
        raise


@then("user clicks on save button")
def click_save_button(context):
    mentor = MentorPage(context.page)
    try:
        mentor.click_save_button()
        attach_screenshot(context.page, "Mentor - Save Button Clicked")
    except Exception as e:
        attach_screenshot(context.page, "Mentor - Save Button Error")
        raise


@then("user deletes the override slot and clicks on save button")
def delete_override_slot_and_save(context):
    mentor = MentorPage(context.page)
    try:
        mentor.delete_override_slot_and_save()
        attach_screenshot(context.page, "Mentor - Override Slot Deleted and Saved")
    except Exception as e:
        attach_screenshot(context.page, "Mentor - Override Delete Save Error")
        raise


@then("user clicks on the profile icon")
def click_profile_icon(context):
    profile = MentorProfilePage(context.page)
    try:
        profile.click_profile_icon()
        attach_screenshot(context.page, "Mentor - Profile Icon Clicked")
    except Exception as e:
        attach_screenshot(context.page, "Mentor - Profile Icon Click Error")
        raise


@then("user validates profile page")
def validate_profile_page(context):
    profile = MentorProfilePage(context.page)
    try:
        profile.validate_profile_page()
        attach_screenshot(context.page, "Mentor - Profile Page Validated")
    except Exception as e:
        attach_screenshot(context.page, "Mentor - Profile Page Validation Error")
        raise


@then("user changes firstname, lastname, city and saves the profile")
def change_name_city_and_save(context):
    profile = MentorProfilePage(context.page)
    try:
        profile.change_firstname_lastname_city_and_save()
        attach_screenshot(context.page, "Mentor - Name and City Changed and Saved")
    except Exception as e:
        attach_screenshot(context.page, "Mentor - Name City Change Error")
        raise


@then("user reverts the changes and saves the profile")
def revert_name_city_and_save(context):
    profile = MentorProfilePage(context.page)
    try:
        profile.revert_firstname_lastname_city_and_save()
        attach_screenshot(context.page, "Mentor - Name and City Reverted and Saved")
    except Exception as e:
        attach_screenshot(context.page, "Mentor - Name City Revert Error")
        raise


@then("user changes language to spanish and saves the profile")
def change_language_to_spanish_and_save(context):
    profile = MentorProfilePage(context.page)
    try:
        profile.change_language_to_spanish_and_save()
        attach_screenshot(context.page, "Mentor - Language Changed to Spanish and Saved")
    except Exception as e:
        attach_screenshot(context.page, "Mentor - Language Change Error")
        raise


@then("user reverts the language change and saves the profile")
def revert_language_and_save(context):
    profile = MentorProfilePage(context.page)
    try:
        profile.revert_language_to_english_and_save()
        attach_screenshot(context.page, "Mentor - Language Reverted to English and Saved")
    except Exception as e:
        attach_screenshot(context.page, "Mentor - Language Revert Error")
        raise
