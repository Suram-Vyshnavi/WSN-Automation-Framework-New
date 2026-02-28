class CareerBuddyLocators:
    CAREER_BUDDY_TILE = "//span[contains(text(), 'Career Buddy')]"
    # User requested clicking the 3rd explore button
    EXPLORE_BTN = "(//button[contains(@class, 'explore_btn')])[3]"
    SEARCH_INPUT = "//input[@placeholder='Search Mentors']"
    MENTOR_NAME = "(//h2[contains(text(), 'Leela B')])[1]"
    BOOK_SESSION_BTN = "(//button[contains(., 'Book Session')])[1]"
    AVAILABLE_DATE = "//td[contains(@class, 'ant-picker-cell-in-view') and not(contains(@class, 'ant-picker-cell-disabled'))]"
    NO_SLOTS_MSG = "//div[contains(@class, 'no-slots')]"
    TIME_SLOT = "//button[contains(@class, 'slot')]"
    CLOSE_POPUP = "//span[@class='ant-modal-close-x']"
    # Target dropdown specifically within the modal to avoid hidden/background inputs
    SESSION_PURPOSE_DROPDOWN = "//div[contains(@class, 'ant-modal')]//div[contains(@class, 'ant-select-selector')]" 
    SESSION_PURPOSE_OPTION = "//div[contains(@class, 'ant-select-item-option') and @title='Resume Building']"
    OUTCOME_TEXTAREA = "//textarea[@id='Outcome']"
    CHECKBOX = "//input[@type='checkbox']"
    # Make sure we target the submit button in the modal, not the 'Book Session' button
    BOOK_CONFIRM_BTN = "//button[@type='submit' and contains(., 'Book')]"
    # Use specific class to avoid matching parent container
    MEETING_HEADER = "//span[contains(@class, 'company-name') and not(contains(@class, 'company-name-container'))]"
