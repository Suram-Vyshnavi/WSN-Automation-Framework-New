class HomeLocators:
    WADHWANI_LOGO = "//img[@alt='wadhwani logo white color']"
    FACULTY_DASHBOARD_CONTAINER = "//div[contains(@class,'faculty-dashboard-container')]"
    HOME_MENU="//div[@id='Home']"
    BATCHES_MENU="//div[@id='Batches']"
    PERFORMANCE_MENU="//div[@id='Performance']"
    CALENDER_MENU = "//div[@id='Calendar']"
    SUPPORT_MENU = "//img[contains(@class,'no-js-MenuHelp')]"
    NOTIFICATIONS_MENU = "//img[contains(@class,'notification_icon')]"
    # Accounts (hamburger) menu trigger that opens the dropdown containing
    # Calendar / Messages & Discussions / Settings / Logout.
    ACCOUNTS_MENU_TRIGGER = "//button[@aria-label='Accounts menu'] | //img[contains(@class,'header_profile_menu_trigger__icon')]"
    DROPDOWN_MESSAGES_ITEM = "//*[contains(@class,'header-user-dropdown__item-label')][contains(normalize-space(),'Messages')] | //*[normalize-space()='Messages & Discussions']"
    DROPDOWN_SETTINGS_ITEM = "//*[contains(@class,'header-user-dropdown__item-label')][normalize-space()='Settings'] | //p[normalize-space()='Settings']"
    CLOSE_NOTIFICATION = "//img[contains(@class,'notification__title__cross')]"
    # Avatar renders as ant-avatar-icon (photo) or ant-avatar-string (initials) depending on profile photo
    PROFILE_MENU = "(//span[contains(@class,'ant-avatar-icon') or contains(@class,'ant-avatar-string')])[1]"
    MY_PROFILE = "//h1[contains(text(),'My Profile')]"
    EDIT_PROFILE = "//span[text()='Edit']"
    EDIT_BUTTON = "//button[contains(@class,'edit-button') or normalize-space()='Edit' or .//span[normalize-space()='Edit']]"
    FIRST_NAME = "//input[@id='firstName'] | //input[@id='first-name']"
    SAVE_BUTTON="(//button[normalize-space()='Save'])[1]"
    # Recommended Activities
    RECOMMENDED_ACTIVITIES_SECTION="//p[contains(@class,'recommended_activity_badge') and contains(text(),'Recommended Activities')]"
    
     # Forums 
    FORUMS_SECTION="//div[@class='forum-section']"
    MY_FORUMS_TITLE="//h4[contains(text(),'My Forums')]"
    RECOMMENDED_FORUMS_TITLE="(//span[@id='recommended_forum_container'])[1]"
    FORUM_CARD="//div[@class='forum_class_card_container']"
    RECOMMENDED_FORUM_CARD="//div[contains(@class,'heading_wrapper')]//p[contains(@class,'meeting-badge')]"

    #Certified courses
    CERTIFIED_COURSES="//p[contains(@class, 'certified_courses') and text()='Certified Courses']"
    CERTIFIED_COURSES_CARUSOL="(//ul[contains(@class,'react-multi-carousel-track')])[2]"
    CERTIFIED_COURSES_CARUSOL_ARROW ="(//button[contains(@aria-label,'Go to next slide')])[2]"

    #Batches section & Create new batch card
    BATCHES_TITLE="//h2[contains(text(),'Batches')]"
    BATCHES_SECTION="(//div[@class='ant-table-content'])[1]"
    ACTIVE_BATCHES="//button[@role='tab'][.//div[contains(normalize-space(),'Active')]] | (//div[text()='Active'])[1]"
    INACTIVE_BATCHES="//button[@role='tab'][.//div[contains(normalize-space(),'Inactive')]] | (//div[text()='Inactive'])[1]"
    BATCHES_PAGES_ARROW="//li[contains(@class,'ant-pagination-next')]/button[not(@disabled)]"
    CREATE_NEWBATCH_BUTTON="//button[contains(text(),'Create New Batch')]"


