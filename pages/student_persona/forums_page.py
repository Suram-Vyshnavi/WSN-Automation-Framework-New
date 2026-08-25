from locators.student_persona_locators.forums_locators import ForumsLocators
from pages.student_persona.student_persona_page import CARD_TIMEOUT, StudentPersonaPage
from pages.base_page import LONG_TIMEOUT


class ForumsPage(StudentPersonaPage):
    """The student Forums list."""

    def click_forums_card(self):
        self.click(ForumsLocators.FORUMS_CARD, "Forums card", timeout=CARD_TIMEOUT)

    def validate_my_forums_header(self):
        self.wait_for_load("domcontentloaded", timeout=LONG_TIMEOUT)
        self.validate_visible(ForumsLocators.VALIDATE_MY_FORUMS_HEADER, "My Forums header",
                              timeout=LONG_TIMEOUT)

    def click_view_forum_button(self):
        """Open the first forum, then return to the list."""
        self.click(ForumsLocators.VIEW_FORUM_BUTTON, "View Forum button", timeout=CARD_TIMEOUT)
        self.go_back()
