class CareerBuddyLocators:
    CAREER_BUDDY_TILE = "//span[contains(text(), 'Career Buddy')]"
    # User requested clicking the 3rd explore button
    EXPLORE_BTN = "(//button[contains(@class, 'explore_btn')])[3]"
    SEARCH_INPUT = "//input[@placeholder='Search Mentors']"
    SEARCH_NAME_PRIMARY = "Leela B"
    SEARCH_NAME_SECONDARY = "Test shwetha"
    MENTOR_NAME_LEELA = "(//h2[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'leela b')])[1]"
    MENTOR_NAME_TEST_SHWETHA = "(//h2[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'test shwetha')])[1]"
    MENTOR_NAME = MENTOR_NAME_TEST_SHWETHA
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
    LANGUAGE_DROPDOWN="//span[text()='Language  ']"
    SECTOR_DROPDOWN="//span[text()='Sector  ']"
    LOCATION_DROPDOWN="//span[text()='Location  ']"
    JOBROLE_DROPDOWN="//span[text()='Job Role  ']"
    ABOUT="//div[text()='About']"
    CAREER_PATHWAYS="//div[text()='Career Pathways']"
    PERSONAL_TRAITS="//div[text()='Personal Traits']"  
    EMPLOYERS="//div[text()='Employers']" 
    

