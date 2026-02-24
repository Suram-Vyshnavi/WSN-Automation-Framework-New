from behave import given, when, then
from utils.helpers import attach_screenshot, validate_navigation
from utils.locators import LoginLocators
from pages.career_advisor_page import CareerAdvisorPage

# ==================== Career Advisor Complete Validation Steps ====================

@then("user navigates to career advisor")
def navigate_to_career_advisor(context):
    page = context.page
    ca_page = CareerAdvisorPage(page)
    
    try:
        ca_page.navigate_to_career_advisor()
        attach_screenshot(page, "Career Advisor - Landing Page")
    except Exception as e:
        print(f"Error navigating to Career Advisor: {e}")
        attach_screenshot(page, "Career Advisor - Navigation Error")
        raise


@then("user selects passions preferences")
def select_passions_preferences(context):
    page = context.page
    ca_page = CareerAdvisorPage(page)
    
    try:
        ca_page.select_passions_preferences()
        attach_screenshot(page, "Career Advisor - After Passions Click")
    except Exception as e:
        print(f"Error selecting passions preferences: {e}")
        attach_screenshot(page, "Career Advisor - Passions Selection Error")
        raise


@then("user selects review passions preferences")
def select_review_passions(context):
    page = context.page
    ca_page = CareerAdvisorPage(page)
    
    try:
        ca_page.select_review_passions()
        attach_screenshot(page, "Career Advisor - Passions Review")
    except Exception as e:
        print(f"Error clicking review passions: {e}")
        attach_screenshot(page, "Career Advisor - Passions Review Error")
        raise


@then("user validates the selected items in passions review section")
def validate_passions_review(context):
    page = context.page
    ca_page = CareerAdvisorPage(page)
    
    try:
        ca_page.validate_passions_review()
        attach_screenshot(page, "Career Advisor - Passions Review Validated")
    except Exception as e:
        print(f"Error validating passions review: {e}")
        attach_screenshot(page, "Career Advisor - Passions Review Validation Error")
        raise


@then("user click on submit button in passions section")
def click_submit_passions(context):
    page = context.page
    ca_page = CareerAdvisorPage(page)
    
    try:
        ca_page.click_submit_passions()
        attach_screenshot(page, "Career Advisor - Passions Submitted")
    except Exception as e:
        print(f"Error clicking submit in passions: {e}")
        attach_screenshot(page, "Career Advisor - Passions Submit Error")
        raise


@then("user clicks on questionnaires section")
def click_questionnaires_section(context):
    page = context.page
    ca_page = CareerAdvisorPage(page)
    
    try:
        ca_page.click_questionnaires_section()
        attach_screenshot(page, "Career Advisor - Questionnaires Section")
    except Exception as e:
        print(f"Error clicking questionnaires section: {e}")
        attach_screenshot(page, "Career Advisor - Questionnaires Error")
        raise


@then("user clicks on review button in aptitudes section")
def click_aptitudes_review(context):
    page = context.page
    ca_page = CareerAdvisorPage(page)
    
    try:
        ca_page.click_aptitudes_review()
        attach_screenshot(page, "Career Advisor - Aptitudes Review")
    except Exception as e:
        print(f"Error clicking aptitudes review: {e}")
        attach_screenshot(page, "Career Advisor - Aptitudes Review Error")
        raise


@then("user clicks on reattempt")
def click_reattempt(context):
    page = context.page
    ca_page = CareerAdvisorPage(page)
    
    try:
        ca_page.click_reattempt()
        attach_screenshot(page, "Career Advisor - Reattempt Clicked")
    except Exception as e:
        print(f"Error clicking reattempt: {e}")
        attach_screenshot(page, "Career Advisor - Reattempt Error")
        raise


@then("user chooses slider option in aptitudes section")
def choose_slider_option(context):
    page = context.page
    ca_page = CareerAdvisorPage(page)
    
    try:
        ca_page.choose_slider_option()
    except Exception as e:
        print(f"Error choosing slider option: {e}")
        attach_screenshot(page, "Career Advisor - Slider Option Error")
        raise


@then("user clicks on 1st question and changes the slider value to 9 or 10 and clicks on update")
def change_slider_value_and_update(context):
    page = context.page
    ca_page = CareerAdvisorPage(page)
    
    ca_page.change_slider_value_and_update()
    attach_screenshot(page, "Career Advisor - Slider Value Updated")


@then("user clicks on Go to matched roles")
def click_go_to_matched_roles(context):
    page = context.page
    ca_page = CareerAdvisorPage(page)
    
    try:
        ca_page.click_go_to_matched_roles()
        attach_screenshot(page, "Career Advisor - Go to Matched Roles")
    except Exception as e:
        print(f"Error clicking go to matched roles: {e}")
        attach_screenshot(page, "Career Advisor - Go to Matched Roles Error")
        raise

@then("user clicks on search roles")
def click_search_roles(context):
    page = context.page
    ca_page = CareerAdvisorPage(page)
    
    try:
        ca_page.click_search_roles()
        attach_screenshot(page, "Career Advisor - Search Roles")
    except Exception as e:
        print(f"Error clicking search roles: {e}")
        attach_screenshot(page, "Career Advisor - Search Roles Error")
        raise


@then("user enters jobrole and add the first job as favourite")
def enter_jobrole_and_add_favourite(context):
    page = context.page
    ca_page = CareerAdvisorPage(page)
    
    try:
        context.favourite_job_name = ca_page.enter_jobrole_and_add_favourite("Project manager")
        attach_screenshot(page, "Career Advisor - Job Added to Favourites")
    except Exception as e:
        print(f"Error entering job role and adding favourite: {e}")
        attach_screenshot(page, "Career Advisor - Add Favourite Error")
        raise


@then("user clicks Favourites and validates the added job")
def click_favourites_and_validate(context):
    page = context.page
    ca_page = CareerAdvisorPage(page)
    
    try:
        ca_page.click_favourites_and_validate()
        print(f"Validating favourite job: {getattr(context, 'favourite_job_name', 'Unknown')}")
        attach_screenshot(page, "Career Advisor - Favourites Validated")
    except Exception as e:
        print(f"Error validating favourites: {e}")
        attach_screenshot(page, "Career Advisor - Favourites Validation Error")
        raise


@then("user clicks on share report and click and validates the share report options")
def click_share_report_and_validate(context):
    page = context.page
    ca_page = CareerAdvisorPage(page)
    
    try:
        ca_page.click_share_report_and_validate()
        attach_screenshot(page, "Career Advisor - Share Report Options Validated")
    except Exception as e:
        print(f"Error validating share report: {e}")
        attach_screenshot(page, "Career Advisor - Share Report Error")
        raise


@then("user clicks on Favourites and removes the added job from favourites")
def remove_job_from_favourites(context):
    page = context.page
    ca_page = CareerAdvisorPage(page)
    
    try:
        ca_page.remove_job_from_favourites()
        attach_screenshot(page, "Career Advisor - Job Removed from Favourites")
    except Exception as e:
        print(f"Error removing job from favourites: {e}")
        attach_screenshot(page, "Career Advisor - Remove Favourite Error")
        raise
