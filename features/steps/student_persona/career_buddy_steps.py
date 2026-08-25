from behave import then
from pages.student_persona.career_buddy_page import CareerBuddyPage
from utils.helpers import attach_screenshot


@then("user clicks on Career Buddy card")
def click_career_buddy_card(context):
    career_buddy = CareerBuddyPage(context.page)
    career_buddy.click_career_buddy_card()
    attach_screenshot(context.page, "Career Buddy Card Clicked")


@then("user clicks on language dropdown and selects the language and click on apply button")
def click_language_dropdown_and_apply(context):
    career_buddy = CareerBuddyPage(context.page)
    career_buddy.click_language_dropdown_and_apply()
    attach_screenshot(context.page, "Language Dropdown - Applied")


@then("user clicks on language close button")
def click_language_close_button(context):
    career_buddy = CareerBuddyPage(context.page)
    career_buddy.click_language_close_button()
    attach_screenshot(context.page, "Language Close Button Clicked")


@then("user clicks on sector dropdown and selects the sector and click on apply button")
def click_sector_dropdown_and_apply(context):
    career_buddy = CareerBuddyPage(context.page)
    career_buddy.click_sector_dropdown_and_apply()
    attach_screenshot(context.page, "Sector Dropdown - Applied")


@then("user clicks on sector close button")
def click_sector_close_button(context):
    career_buddy = CareerBuddyPage(context.page)
    career_buddy.click_sector_close_button()
    attach_screenshot(context.page, "Sector Close Button Clicked")


@then("user clicks on location dropdown and selects the location and click on apply button")
def click_location_dropdown_and_apply(context):
    career_buddy = CareerBuddyPage(context.page)
    career_buddy.click_location_dropdown_and_apply()
    attach_screenshot(context.page, "Location Dropdown - Applied")


@then("user clicks on location close button")
def click_location_close_button(context):
    career_buddy = CareerBuddyPage(context.page)
    career_buddy.click_location_close_button()
    attach_screenshot(context.page, "Location Close Button Clicked")


@then("user clicks on job role dropdown and selects the job role and click on apply button")
def click_job_role_dropdown_and_apply(context):
    career_buddy = CareerBuddyPage(context.page)
    career_buddy.click_job_role_dropdown_and_apply()
    attach_screenshot(context.page, "Job Role Dropdown - Applied")


@then("user clicks on job role close button")
def click_job_role_close_button(context):
    career_buddy = CareerBuddyPage(context.page)
    career_buddy.click_job_role_close_button()
    attach_screenshot(context.page, "Job Role Close Button Clicked")


@then("user clicks on search mentor and fill the details")
def search_mentor_and_fill_details(context):
    career_buddy = CareerBuddyPage(context.page)
    career_buddy.search_mentor_and_fill_details()
    attach_screenshot(context.page, "Mentor Search Filled")


@then("user clicks on the recommended mentor card")
def click_recommended_mentor_card(context):
    career_buddy = CareerBuddyPage(context.page)
    career_buddy.click_recommended_mentor_card()
    attach_screenshot(context.page, "Recommended Mentor Card Clicked")


@then("user validates the sector jobrole and language details")
def validate_sector_jobrole_language_details(context):
    career_buddy = CareerBuddyPage(context.page)
    career_buddy.validate_sector_jobrole_language_details()
    attach_screenshot(context.page, "Sector, Job Role and Language Validated")


@then("user clicks on the Book a Session button")
def click_book_session_button(context):
    career_buddy = CareerBuddyPage(context.page)
    career_buddy.click_book_session_button()
    attach_screenshot(context.page, "Book Session Button Clicked")


@then("user selects the available date and clicks on the slot button")
def select_available_date_and_slot(context):
    career_buddy = CareerBuddyPage(context.page)
    career_buddy.select_available_date_and_slot()
    attach_screenshot(context.page, "Date Selected and Slot Clicked")


@then("user clicks on session purpose label and selects the Job Search Strategy option")
def click_session_purpose_and_select_job_search_strategy(context):
    career_buddy = CareerBuddyPage(context.page)
    career_buddy.click_session_purpose_and_select_job_search_strategy()
    attach_screenshot(context.page, "Session Purpose Selected")


@then("user clicks on specific outcome label and fills in the specific outcome fields, selects the checkbox option and clicks on the Book button")
def fill_specific_outcome_and_book(context):
    career_buddy = CareerBuddyPage(context.page)
    career_buddy.fill_specific_outcome_and_book()
    attach_screenshot(context.page, "Specific Outcome Filled and Booked")


@then("user clicks on the Copy Link option and validates the copied link")
def click_copy_link_and_validate(context):
    career_buddy = CareerBuddyPage(context.page)
    career_buddy.click_copy_link_and_validate()
    attach_screenshot(context.page, "Copy Link Clicked and Validated")
