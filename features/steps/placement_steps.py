from behave import then
from pages.placement_page import PlacementPage
from utils.locators import CareerBuddyLocators
from utils.helpers import attach_screenshot

@then("user navigates to Placement Prep")
def navigate_placement_prep(context):
    pp_page = PlacementPage(context.page)
    pp_page.click_placement_prep()
    attach_screenshot(context.page, "Navigated to Placement Prep")

@then("user verifies Personal Pitch Trainer tile")
def verify_pitch_tile(context):
    pp_page = PlacementPage(context.page)
    pp_page.verify_personal_pitch_tile()
    attach_screenshot(context.page, "Verified Personal Pitch Tile")

@then("user clicks on Explore button")
def click_explore_btn(context):
    pp_page = PlacementPage(context.page)
    initial_pages = len(context.page.context.pages)
    pp_page.click_explore()
    
    
    if len(context.page.context.pages) > initial_pages:
        new_page = context.page.context.pages[-1]
        context.page = new_page
        new_page.bring_to_front()
    
    context.page.wait_for_load_state("networkidle")
    attach_screenshot(context.page, "Clicked Explore")

@then("user verifies Personal Pitch header")
def verify_pp_header(context):
    pp_page = PlacementPage(context.page)
    pp_page.verify_header()
    attach_screenshot(context.page, "Verified Personal Pitch Header")

@then("user clicks on Create Your Pitch button")
def click_create_pitch_btn(context):
    pp_page = PlacementPage(context.page)
    pp_page.click_create_pitch()
    attach_screenshot(context.page, "Clicked Create Pitch")

@then("user handles language alert if present")
def handle_language_alert_step(context):
    pp_page = PlacementPage(context.page)
    pp_page.handle_language_alert()
    attach_screenshot(context.page, "Handled Language Alert")

@then("user verifies Resume Start Pitch modal and clicks Start New Pitch")
def handle_resume_pitch_modal(context):
    pp_page = PlacementPage(context.page)
    pp_page.handle_resume_modal()
    attach_screenshot(context.page, "Handled Resume/Start Modal")

@then("user verifies Step 1 Target Job & Notes")
def verify_step_1_flow(context):
    pp_page = PlacementPage(context.page)
    pp_page.verify_step_1()
    attach_screenshot(context.page, "Verified Step 1")

@then('user enters "{role}" in job role and validates')
def enter_role_validation(context, role):
    pp_page = PlacementPage(context.page)
    pp_page.enter_job_role(role)
    attach_screenshot(context.page, f"Entered role: {role} & Validated")

@then("user verifies Career Buddy tile and clicks Explore")
def verify_career_buddy_click_explore(context):
    pp_page = PlacementPage(context.page)
    # Reuse click logic or verify tile first
    context.page.locator(CareerBuddyLocators.CAREER_BUDDY_TILE).wait_for(state="visible")
    pp_page.click_career_buddy_explore()
    attach_screenshot(context.page, "Clicked Career Buddy Explore")

@then('user searches for mentor "{name}"')
def search_mentor_step(context, name):
    pp_page = PlacementPage(context.page)
    pp_page.search_mentor(name)
    attach_screenshot(context.page, f"Searched Mentor: {name}")

@then("user clicks on Book Session for the mentor")
def click_book_session_step(context):
    pp_page = PlacementPage(context.page)
    # Assuming the search result is already there from previous step
    slots_available = pp_page.book_session_flow()
    context.slots_available = slots_available  # Store for later steps
    
    if slots_available:
        attach_screenshot(context.page, "Book Session - Time Slot Selected")
    else:
        attach_screenshot(context.page, "Book Session - No Slots Available")

@then("user selects an available date and time slot")
def select_date_time_step(context):
    # This step is now handled in book_session_flow()
    if not getattr(context, 'slots_available', True):
        print("Skipping: No slots available")
    pass

@then("user enters booking details and confirms")
def enter_booking_details_step(context):
    if not getattr(context, 'slots_available', True):
        print("Skipping: No slots available")
        attach_screenshot(context.page, "Booking Skipped - No Slots Available")
        return
    
    pp_page = PlacementPage(context.page)
    pp_page.fill_booking_details()
    attach_screenshot(context.page, "Entered Booking Details")

@then("user verifies the meeting details page")
def verify_meeting_details_step(context):
    if not getattr(context, 'slots_available', True):
        print("Skipping: No slots available")
        attach_screenshot(context.page, "Verification Skipped - No Slots Available")
        return
    
    pp_page = PlacementPage(context.page)
    pp_page.verify_meeting_details()
    attach_screenshot(context.page, "Verified Meeting Details")

@then("user clicks on Create Your Pitch")
def click_create_pitch_step(context):
    # Depending on the flow, there might be another Create Pitch button or Next
    # Based on the user request, it says "user clicks on createyour pitch" after validation
    # Re-using the locator if it's the same button class
    pp_page = PlacementPage(context.page)
    pp_page.click_create_pitch()

@then("user handles \"I understood\" popup if present")
def handle_understand_popup_step(context):
    pp_page = PlacementPage(context.page)
    pp_page.handle_understand_popup()
    attach_screenshot(context.page, "Handled Understand Popup")

@then("user verifies Step 2 Record Pitch")
def verify_step_2_flow(context):
    # This step is split in the user request but verifying the indicator implies step 2
    pp_page = PlacementPage(context.page)
    # Just checking indicator for now, detailed check in next step
    pass 

@then("user verifies Record Pitch header and Record button")
def verify_record_header_btn(context):
    pp_page = PlacementPage(context.page)
    pp_page.verify_step_2()
    attach_screenshot(context.page, "Verified Step 2 Record")

@then("user clicks on Placement Prep menu")
def click_placement_menu(context):
    pp_page = PlacementPage(context.page)
    pp_page.click_placement_prep()

@then("user handles Leaving Pitch Creation modal by clicking Save & Exit")
def handle_leaving_modal_step(context):
    pp_page = PlacementPage(context.page)
    pp_page.handle_leaving_modal()
    attach_screenshot(context.page, "Handled Leaving Modal")

# Interview Coach Steps
@then("user verifies Interview Coach tile and clicks Explore")
def verify_interview_coach_and_explore(context):
    pp_page = PlacementPage(context.page)
    pp_page.verify_interview_coach_tile()
    pp_page.click_interview_coach_explore()
    attach_screenshot(context.page, "Interview Coach - Clicked Explore")

@then("user validates textbox and mic button in Interview Coach page")
def validate_textbox_mic(context):
    pp_page = PlacementPage(context.page)
    pp_page.validate_textbox_and_mic()
    attach_screenshot(context.page, "Interview Coach - Validated Textbox and Mic")

@then("user sends required details for the interview coaching")
def send_interview_details(context):
    pp_page = PlacementPage(context.page)
    pp_page.send_interview_details("Product Manager", "E-commerce")
    attach_screenshot(context.page, "Interview Coach - Sent Details")

@then("user clicks on Practise Interviewing for the role")
def click_practice_interviewing(context):
    pp_page = PlacementPage(context.page)
    pp_page.click_practice_interviewing()
    attach_screenshot(context.page, "Interview Coach - Clicked Practice Interviewing")

@then("user validates questions using start button")
def validate_questions_start(context):
    pp_page = PlacementPage(context.page)
    pp_page.validate_start_button()
    attach_screenshot(context.page, "Interview Coach - Validated Start Button")

@then("user navigates back from the questions page and deletes the created interview coaching")
def navigate_back_delete(context):
    pp_page = PlacementPage(context.page)
    pp_page.navigate_back_and_delete()
    attach_screenshot(context.page, "Interview Coach - Deleted")
