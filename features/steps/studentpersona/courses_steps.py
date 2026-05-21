from behave import then
from pages.studentpersona.courses_page import CoursesPage
from utils.helpers import attach_screenshot


@then('user validates Inprogress tab and Completed tab')
def validate_inprogress_and_completed_tabs(context):
    if getattr(context, 'current_section', 'courses') == 'programs':
        from pages.studentpersona.programs_page import ProgramsPage
        page_obj = ProgramsPage(context.page)
    else:
        page_obj = CoursesPage(context.page)
    page_obj.validate_inprogress_and_completed_tabs()
    attach_screenshot(context.page, "In Progress and Completed Tabs Validated")


@then('user clicks on Inprogress tab')
def click_inprogress_tab(context):
    if getattr(context, 'current_section', 'courses') == 'programs':
        from pages.studentpersona.programs_page import ProgramsPage
        page_obj = ProgramsPage(context.page)
    else:
        page_obj = CoursesPage(context.page)
    page_obj.click_inprogress_tab()
    attach_screenshot(context.page, "In Progress Tab Clicked")


@then('user clicks on Completed tab')
def click_completed_tab(context):
    if getattr(context, 'current_section', 'courses') == 'programs':
        from pages.studentpersona.programs_page import ProgramsPage
        page_obj = ProgramsPage(context.page)
    else:
        page_obj = CoursesPage(context.page)
    page_obj.click_completed_tab()
    attach_screenshot(context.page, "Completed Tab Clicked")


@then('user validates enrolled course card')
def validate_enrolled_course_card(context):
    courses_page = CoursesPage(context.page)
    courses_page.validate_enrolled_course_card()
    attach_screenshot(context.page, "Enrolled Course Card Validated")


@then('user clicks on view details button')
def click_view_details_button(context):
    courses_page = CoursesPage(context.page)
    courses_page.click_view_details_button()
    attach_screenshot(context.page, "View Details Button Clicked")


@then('user validates overview course content and performance tabs')
def validate_overview_course_content_performance_tabs(context):
    courses_page = CoursesPage(context.page)
    courses_page.validate_overview_course_content_performance_tabs()
    attach_screenshot(context.page, "Overview Course Content Performance Tabs Validated")


@then('user clicks on performance tab')
def click_performance_tab(context):
    courses_page = CoursesPage(context.page)
    courses_page.click_performance_tab()
    attach_screenshot(context.page, "Performance Tab Clicked")


@then('user validates final score certificate and performance tab')
def validate_final_score_certificate_performance(context):
    courses_page = CoursesPage(context.page)
    courses_page.validate_final_score_certificate_performance()
    attach_screenshot(context.page, "Final Score Certificate Performance Validated")


@then('user clicks on view analysis button')
def click_view_analysis_button(context):
    courses_page = CoursesPage(context.page)
    courses_page.click_view_analysis_button()
    attach_screenshot(context.page, "View Analysis Button Clicked")


@then('user clciks on view pitch button')
def click_view_pitch_button(context):
    courses_page = CoursesPage(context.page)
    courses_page.click_view_pitch_button()
    attach_screenshot(context.page, "View Pitch Button Clicked")


@then('user clicks on video play button')
def click_video_play_button(context):
    if getattr(context, 'current_section', 'courses') == 'personal_pitch':
        from pages.studentpersona.personal_pitch_page import PersonalPitchPage
        page_obj = PersonalPitchPage(context.page)
    else:
        page_obj = CoursesPage(context.page)
    page_obj.click_video_play_button()
    attach_screenshot(context.page, "Video Play Button Clicked")


@then('user clicks on video close button')
def click_video_close_button(context):
    if getattr(context, 'current_section', 'courses') == 'personal_pitch':
        from pages.studentpersona.personal_pitch_page import PersonalPitchPage
        page_obj = PersonalPitchPage(context.page)
    else:
        page_obj = CoursesPage(context.page)
    page_obj.click_video_close_button()
    attach_screenshot(context.page, "Video Close Button Clicked")


@then('user clicks on share pitch button')
def click_share_pitch_button(context):
    if getattr(context, 'current_section', 'courses') == 'personal_pitch':
        from pages.studentpersona.personal_pitch_page import PersonalPitchPage
        page_obj = PersonalPitchPage(context.page)
    else:
        page_obj = CoursesPage(context.page)
    page_obj.click_share_pitch_button()
    attach_screenshot(context.page, "Share Pitch Button Clicked")


@then('user clicks on copy pitch button')
def click_copy_pitch_button(context):
    if getattr(context, 'current_section', 'courses') == 'personal_pitch':
        from pages.studentpersona.personal_pitch_page import PersonalPitchPage
        page_obj = PersonalPitchPage(context.page)
    else:
        page_obj = CoursesPage(context.page)
    page_obj.click_copy_pitch_button()
    attach_screenshot(context.page, "Copy Pitch Button Clicked")


@then('user clicks on share pitch close button')
def click_share_pitch_close_button(context):
    if getattr(context, 'current_section', 'courses') == 'personal_pitch':
        from pages.studentpersona.personal_pitch_page import PersonalPitchPage
        page_obj = PersonalPitchPage(context.page)
    else:
        page_obj = CoursesPage(context.page)
    page_obj.click_share_pitch_close_button()
    attach_screenshot(context.page, "Share Pitch Close Button Clicked")


@then('user clicks on back arrow button')
def click_back_arrow_button(context):
    courses_page = CoursesPage(context.page)
    courses_page.click_back_arrow_button()
    attach_screenshot(context.page, "Back Arrow Button Clicked")


@then('user clicks on create post-video button')
def click_create_post_video_button(context):
    courses_page = CoursesPage(context.page)
    courses_page.click_create_post_video_button()
    attach_screenshot(context.page, "Create Post-Video Button Clicked")


@then('user clicks on pitch trainer back arrow button')
def click_pitch_trainer_back_arrow_button(context):
    courses_page = CoursesPage(context.page)
    courses_page.click_pitch_trainer_back_arrow_button()
    attach_screenshot(context.page, "Pitch Trainer Back Arrow Button Clicked")


@then('user validates courses recommended by institute')
def validate_courses_recommended_by_institute(context):
    courses_page = CoursesPage(context.page)
    courses_page.validate_courses_recommended_by_institute()
    attach_screenshot(context.page, "Courses Recommended by Institute Validated")


@then('user validates recommended course card')
def validate_recommended_course_card(context):
    courses_page = CoursesPage(context.page)
    courses_page.validate_recommended_course_card()
    attach_screenshot(context.page, "Recommended Course Card Validated")


@then('user validates courses offered by wadhwani foundation')
def validate_courses_offered_by_wadhwani_foundation(context):
    courses_page = CoursesPage(context.page)
    courses_page.validate_courses_offered_by_wadhwani_foundation()
    attach_screenshot(context.page, "Courses Offered by Wadhwani Foundation Validated")


@then('user validates offered course card')
def validate_offered_course_card(context):
    courses_page = CoursesPage(context.page)
    courses_page.validate_offered_course_card()
    attach_screenshot(context.page, "Offered Course Card Validated")
