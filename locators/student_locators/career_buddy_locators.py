class CareerBuddyLocators:
    CAREER_BUDDY_TILE = "//span[contains(text(), 'Career Buddy')]"
    # User requested clicking the 3rd explore button
    EXPLORE_BTN = "(//button[contains(@class, 'explore_btn')])[3]"
    SEARCH_INPUT = "//input[@placeholder='Search Mentors']"
    SEARCH_NAME_PRIMARY = "Leela B"
    SEARCH_NAME_SECONDARY = "Test shwetha"
    MENTOR_NAME_LEELA = "(//h2[contains(normalize-space(), 'Leela B')])[1]"
    MENTOR_NAME_TEST_SHWETHA = "(//h2[contains(normalize-space(), 'Test Shwetha')])[1]"
    MENTOR_NAME = MENTOR_NAME_TEST_SHWETHA
    BOOK_SESSION_BTN = "(//button[contains(., 'Book Session')])[1]"
    AVAILABLE_DATE = "//td[contains(@class, 'ant-picker-cell-in-view') and not(contains(@class, 'ant-picker-cell-disabled'))]"
    NO_SLOTS_MSG = "//div[contains(@class, 'no-slots')]"
    TIME_SLOT = "//button[contains(@class, 'slot')]"
    CLOSE_POPUP = "//span[@class='ant-modal-close-x']"
    # Target dropdown specifically within the modal to avoid hidden/background inputs
    SESSION_PURPOSE_DROPDOWN = "//div[contains(@class, 'ant-modal')]//div[contains(@class, 'ant-select-selector')]" 
    SESSION_PURPOSE_OPTION = "//div[contains(@class,'ant-select-item-option')]//span[normalize-space()='Resume Building']"
    OUTCOME_TEXTAREA = "//textarea[@id='Outcome']"
    CHECKBOX = "//span[@class='ant-checkbox-inner']"
    # Make sure we target the submit button in the modal, not the 'Book Session' button
    BOOK_CONFIRM_BTN = "//button[@type='submit' and contains(., 'Book')]"
    # Use specific class to avoid matching parent container
    MEETING_HEADER = "//span[contains(@class, 'company-name') and not(contains(@class, 'company-name-container'))]"
    LANGUAGE_DROPDOWN="//button[text()='Language  ']"
    SECTOR_DROPDOWN="//button[text()='Sector  ']"
    LOCATION_DROPDOWN="//button[text()='Location  ']"
    JOBROLE_DROPDOWN="//button[text()='Job Role  ']"
    ABOUT="//p[text()='About Me']"
    CAREER_PATHWAYS="//div[text()='Career Pathways']"
    PERSONAL_TRAITS="//div[text()='Personal Traits']"  
    EMPLOYERS="//div[text()='Employers']" 
    

