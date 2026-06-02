from behave import then
from pages.studentpersona.jobsconnect_page import JobsConnectPage
from utils.helpers import attach_screenshot


@then("user clicks on jobsconnect card")
def click_jobsconnect_card(context):
    jobsconnect = JobsConnectPage(context.page)
    jobsconnect.click_jobsconnect_card()
    attach_screenshot(context.page, "Jobs Connect Card Clicked")


@then("user clicks on jobtype and selects full time option")
def click_jobtype_and_select_full_time(context):
    jobsconnect = JobsConnectPage(context.page)
    jobsconnect.click_jobtype_and_select_full_time()
    attach_screenshot(context.page, "Full Time Job Type Selected")


@then("user clicks on workmode filter and selects office option")
def click_workmode_and_select_office(context):
    jobsconnect = JobsConnectPage(context.page)
    jobsconnect.click_workmode_and_select_office()
    attach_screenshot(context.page, "Office Work Mode Selected")


@then("user clicks on industry sector filter and selects automotive option")
def click_industry_sector_and_select_automotive(context):
    jobsconnect = JobsConnectPage(context.page)
    jobsconnect.click_industry_sector_and_select_automotive()
    attach_screenshot(context.page, "Automotive Industry Sector Selected")


@then("user clicks on education level filter and selects graduate option")
def click_education_level_and_select_graduate(context):
    jobsconnect = JobsConnectPage(context.page)
    jobsconnect.click_education_level_and_select_graduate()
    attach_screenshot(context.page, "Graduate Education Level Selected")


@then("user clicks on preffered companies filter and selects diatoz option")
def click_preferred_companies_and_select_diatoz(context):
    jobsconnect = JobsConnectPage(context.page)
    jobsconnect.click_preferred_companies_and_select_diatoz()
    attach_screenshot(context.page, "DIATOZ Preferred Company Selected")


@then("user clicks on search by role title and fills product manager and clicks on find jobs")
def search_by_role_title_and_find_jobs(context):
    jobsconnect = JobsConnectPage(context.page)
    new_page = jobsconnect.search_by_role_title_and_find_jobs()
    if new_page:
        context.page = new_page
    attach_screenshot(context.page, "Searched Product Manager and Clicked Find Jobs")


@then("user clicks on first job card")
def click_first_job_card(context):
    jobsconnect = JobsConnectPage(context.page)
    new_page = jobsconnect.click_first_job_card()
    if new_page:
        context.original_page = context.page
        context.page = new_page
    attach_screenshot(context.page, "First Job Card Clicked")


@then("user validates about the job and about the company sections")
def validate_about_job_and_company_sections(context):
    jobsconnect = JobsConnectPage(context.page)
    jobsconnect.validate_about_job_and_company_sections()
    attach_screenshot(context.page, "About the Job and About the Company Sections Validated")


@then("user validates apply button and closes the current tab and navigate to jobs connect page")
def validate_apply_button_and_navigate_back(context):
    original_page = getattr(context, 'original_page', None)
    jobsconnect = JobsConnectPage(context.page)
    jobsconnect.validate_apply_button_and_navigate_back(original_page=original_page)
    if original_page:
        context.page = original_page
        context.original_page = None
    attach_screenshot(context.page, "Apply Button Validated and Navigated Back to Jobs Connect")


@then("user clicks on reset button")
def click_reset_button(context):
    jobsconnect = JobsConnectPage(context.page)
    jobsconnect.click_reset_button()
    attach_screenshot(context.page, "Reset Button Clicked")


@then("user clicks on jobs connect applied status card")
def click_jobs_connect_applied_status_card(context):
    jobsconnect = JobsConnectPage(context.page)
    jobsconnect.click_jobs_connect_applied_status_card()
    attach_screenshot(context.page, "Jobs Connect Applied Status Card Clicked")


@then("user clicks on applied jobs button and validates the applied job card")
def click_applied_jobs_button_and_validate(context):
    jobsconnect = JobsConnectPage(context.page)
    jobsconnect.click_applied_jobs_button_and_validate()
    attach_screenshot(context.page, "Applied Jobs Button Clicked and Applied Job Card Validated")
