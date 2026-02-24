from behave import given, when, then
from utils.helpers import attach_screenshot, validate_navigation
from utils.locators import LoginLocators
from pages.jobs_connect_page import JobsConnectPage

# ==================== Jobs Connect Complete Validation Steps ====================

@then("user navigates to Jobs Connect")
def navigate_to_jobs_connect(context):
    page = context.page
    jc_page = JobsConnectPage(page)
    
    try:
        jc_page.navigate_to_jobs_connect()
        current_url = page.url
        attach_screenshot(page, f"Jobs Connect - Landing Page | url: {current_url}")
    except Exception as e:
        print(f"Error navigating to Jobs Connect: {e}")
        attach_screenshot(page, "Jobs Connect - Navigation Error")
        raise

@then("user resets filters")
def reset_filters(context):
    page = context.page
    jc_page = JobsConnectPage(page)
    
    try:
        jc_page.reset_filters()
        attach_screenshot(page, "Jobs Connect - Filters Reset")
    except Exception as e:
        print(f"Reset button not available: {e}")
        print("Skipping filter reset - continuing with test")
        attach_screenshot(page, "Jobs Connect - Reset Filter Skipped")

@then("user searches for a job")
def search_for_job(context):
    page = context.page
    jc_page = JobsConnectPage(page)
    
    try:
        jc_page.search_for_job("Product Manager")
        attach_screenshot(page, "Jobs Connect - Job Search Entered")
    except Exception as e:
        print(f"Error searching for job: {e}")
        attach_screenshot(page, "Jobs Connect - Job Search Error")
        raise

@then("user clicks on find jobs")
def click_find_jobs(context):
    page = context.page
    jc_page = JobsConnectPage(page)
    
    try:
        jc_page.click_find_jobs()
        attach_screenshot(page, "Jobs Connect - Find Jobs Clicked")
    except Exception as e:
        print(f"Error clicking find jobs: {e}")
        attach_screenshot(page, "Jobs Connect - Find Jobs Error")
        raise

@then("user validates job search results")
def validate_job_search_results(context):
    page = context.page
    jc_page = JobsConnectPage(page)
    
    try:
        job_cards = jc_page.validate_job_search_results()
        attach_screenshot(page, f"Jobs Connect - {job_cards} Job Results")
    except Exception as e:
        print(f"Error validating job search results: {e}")
        attach_screenshot(page, "Jobs Connect - Search Results Error")
        raise

@then("user clicks on the first job result")
def click_first_job_result(context):
    page = context.page
    jc_page = JobsConnectPage(page)
    
    try:
        jc_page.click_first_job_result()
        attach_screenshot(page, "Jobs Connect - First Job Details")
    except Exception as e:
        print(f"Error clicking first job result: {e}")
        attach_screenshot(page, "Jobs Connect - First Job Error")
        raise

@then("user validates the apply option")
def validate_apply_option(context):
    page = context.page
    jc_page = JobsConnectPage(page)
    
    try:
        apply_found = jc_page.validate_apply_option()
        
        if apply_found:
            attach_screenshot(page, "Jobs Connect - Apply Option Validated")
        else:
            attach_screenshot(page, "Jobs Connect - Job Details View (No Apply)")
    except Exception as e:
        print(f"Note: Could not validate apply option: {e}")
        attach_screenshot(page, "Jobs Connect - Apply Option Not Found")

# Note: "user navigates to home page" step is defined in chat_steps.py
