from pages.base_page import BasePage
from locators.student_persona_locators.forums_locators import forumsLocators
from utils.helpers import attach_screenshot, highlight_element


class ForumsPage(BasePage):

    def click_forums_card(self):
        self.page.locator(forumsLocators.FORUMS_CARD).wait_for(state="visible", timeout=15000)
        highlight_element(self.page, forumsLocators.FORUMS_CARD)
        self.page.locator(forumsLocators.FORUMS_CARD).click()
        print("Clicked Forums card")

    def validate_my_forums_header(self):
        header = self.page.locator(forumsLocators.VALIDATE_MY_FORUMS_HEADER)
        header.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, forumsLocators.VALIDATE_MY_FORUMS_HEADER)
        assert header.count() > 0, "My Forums header not found"
        print("My Forums header validated")

    def click_view_forum_button(self):
        self.page.locator(forumsLocators.VIEW_FORUM_BUTTON).first.wait_for(state="visible", timeout=15000)
        highlight_element(self.page, forumsLocators.VIEW_FORUM_BUTTON)
        self.page.locator(forumsLocators.VIEW_FORUM_BUTTON).first.click()
        self.page.go_back()
        print("View Forum button clicked")
