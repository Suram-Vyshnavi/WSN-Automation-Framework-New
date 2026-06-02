from behave import then
from pages.studentpersona.my_career_advisor_page import MyCareerAdvisorPage
from utils.helpers import attach_screenshot


@then('user clicks on My Career Advisor card')
def click_my_career_advisor_card(context):
    context.current_section = 'career_advisor'
    page = MyCareerAdvisorPage(context.page)
    page._navigate_to_my_career_advisor()
    attach_screenshot(context.page, "My Career Advisor Card Clicked")


@then('user validates the Passion header and clicks on the Review button')
def validate_passion_header_and_click_review(context):
    page = MyCareerAdvisorPage(context.page)
    page.validate_passion_header_and_click_review()
    attach_screenshot(context.page, "Passion Header Validated and Review Clicked")


@then('user selects the passion items and clicks on the Submit button')
def select_passion_items_and_submit(context):
    page = MyCareerAdvisorPage(context.page)
    page.select_passion_items_and_submit()
    attach_screenshot(context.page, "Passion Items Selected and Submitted")


@then('user validates the Questionnaire header')
def validate_questionnaire_header(context):
    page = MyCareerAdvisorPage(context.page)
    page.validate_questionnaire_header()
    attach_screenshot(context.page, "Questionnaire Header Validated")


@then('user clicks on the Review button in the Aptitudes section')
def click_review_in_aptitudes(context):
    page = MyCareerAdvisorPage(context.page)
    page.click_review_in_aptitudes()
    attach_screenshot(context.page, "Aptitudes Review Button Clicked")


@then('user clicks on the Reattempt button')
def click_reattempt_button(context):
    page = MyCareerAdvisorPage(context.page)
    page.click_reattempt_button()
    attach_screenshot(context.page, "Reattempt Button Clicked")


@then('user clicks on the slider choose button')
def click_slider_choose_button(context):
    page = MyCareerAdvisorPage(context.page)
    page.click_slider_choose_button()
    attach_screenshot(context.page, "Slider Choose Button Clicked")


@then('user selects the 1st question option. If the slider sequence is on 9, the user clicks on 10. If the slider sequence is on 10, the user clicks back on 9')
def select_question_slider_option(context):
    page = MyCareerAdvisorPage(context.page)
    page.select_question_slider_option()
    attach_screenshot(context.page, "Slider Option Selected")


@then('user clicks on the Update button')
def click_update_button(context):
    page = MyCareerAdvisorPage(context.page)
    page.click_update_button()
    attach_screenshot(context.page, "Update Button Clicked")


@then('user clicks on the Go to Matched Roles button')
def click_go_to_matched_roles(context):
    page = MyCareerAdvisorPage(context.page)
    page.click_go_to_matched_roles()
    attach_screenshot(context.page, "Go to Matched Roles Clicked")


@then('user clicks on Without College Degree')
def click_without_college_degree(context):
    page = MyCareerAdvisorPage(context.page)
    page.click_without_college_degree()
    attach_screenshot(context.page, "Without College Degree Clicked")


@then('user validates the header count')
def validate_header_count(context):
    page = MyCareerAdvisorPage(context.page)
    page.validate_header_count()
    attach_screenshot(context.page, "Header Count Validated")


@then('user clicks on the searched role')
def click_searched_role(context):
    page = MyCareerAdvisorPage(context.page)
    page.click_searched_role()
    attach_screenshot(context.page, "Searched Role Clicked")


@then('user fills in the job role input field')
def fill_job_role_input(context):
    page = MyCareerAdvisorPage(context.page)
    page.fill_job_role_input()
    attach_screenshot(context.page, "Job Role Input Filled")


@then('user validates the Result header and clicks on Favourite')
def validate_result_and_click_favourite(context):
    page = MyCareerAdvisorPage(context.page)
    page.validate_result_header_and_click_favourite()
    attach_screenshot(context.page, "Result Header Validated and Favourite Clicked")


@then('user clicks on the Favourites header')
def click_favourites_header(context):
    page = MyCareerAdvisorPage(context.page)
    page.click_favourites_header()
    attach_screenshot(context.page, "Favourites Header Clicked")


@then('user clicks on Share Report and clicks on the Share button')
def click_share_report_and_share(context):
    page = MyCareerAdvisorPage(context.page)
    page.click_share_report_and_share()
    attach_screenshot(context.page, "Share Report Clicked and Shared")


@then('user clicks on the Favourite button and removes the favourite')
def click_favourite_and_remove(context):
    page = MyCareerAdvisorPage(context.page)
    page.click_favourite_and_remove()
    attach_screenshot(context.page, "Favourite Removed")


@then('user clicks on the home icon and navigates to home page')
def click_home_icon_and_navigate_home(context):
    page = MyCareerAdvisorPage(context.page)
    page.click_home_icon_and_navigate_home()
    attach_screenshot(context.page, "Home Icon Clicked and Navigated to Home")


@then('user clicks on roles saved card and click on favourites header and validate the favourite role header')
def click_roles_saved_and_validate_favourite_role_header(context):
    page = MyCareerAdvisorPage(context.page)
    page.click_roles_saved_and_validate_favourite_role_header()
    attach_screenshot(context.page, "Roles Saved Card and Favourite Role Header Validated")
