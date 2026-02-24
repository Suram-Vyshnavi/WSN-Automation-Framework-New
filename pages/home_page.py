from xml.sax.xmlreader import Locator
from pages.base_page import BasePage
from utils.locators import LoginLocators


class HomePage(BasePage):

    def open_url(self, url):
        self.page.goto(url)

    def dismiss_popup_if_present(self):
        # Playwright auto-waits, no EC, no is_displayed
        try:
            self.page.locator(LoginLocators.DISMISS_BTN).click(timeout=3000)
        except:
            pass

    def click_get_started(self):
        self.page.locator(LoginLocators.GET_STARTED_BUTTON).click()

