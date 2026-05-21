from behave import then
from pages.studentpersona.forums_page import ForumsPage
from utils.helpers import attach_screenshot


@then("user validates the my forums header")
def validate_my_forums_header(context):
    forums = ForumsPage(context.page)
    forums.validate_my_forums_header()
    attach_screenshot(context.page, "My Forums Header Validated")


@then("user clicks on view forum button")
def click_view_forum_button(context):
    forums = ForumsPage(context.page)
    forums.click_view_forum_button()
    attach_screenshot(context.page, "View Forum Button Clicked")
