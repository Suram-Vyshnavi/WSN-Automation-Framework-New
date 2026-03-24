class HomeLocators:
    WADHWANI_LOGO = "//img[@alt='wadhwani logo white color']"
    FACULTY_DASHBOARD_CONTAINER = "//div[contains(@class,'faculty-dashboard-container')]"
    HOME_MENU="//div[@id='Home']"
    BATCHES_MENU="//div[@id='Batches']"
    PERFORMANCE_MENU="//div[@id='Performance']"
    CALENDER_MENU = "(//div[contains(@class,'chat_container')]//img)[1]"
    SUPPORT_MENU = "(//div[contains(@class,'chat_container')]//img)[2]"
    CHAT_MENU = "(//div[contains(@class,'chat_container')]//img)[3]"
    NOTIFICATIONS_MENU = "(//div[contains(@class,'chat_container')]//img)[4]"
    CLOSE_NOTIFICATION = "//img[contains(@class,'notification__title__cross')]"
    PROFILE_MENU = "(//div[@class='profile_container_wrapper'])[1]"
    MY_PROFILE = "//h1[contains(text(),'My Profile')]"
    EDIT_PROFILE = "//span[text()='Edit']"
    EDIT_BUTTON = "//button[contains(@class,'edit-button') or normalize-space()='Edit' or .//span[normalize-space()='Edit']]"
    FIRST_NAME = "//input[@id='firstName'] | //input[@id='first-name']"

    # Recommended Activities
    RECOMMENDED_ACTIVITIES_SECTION="//p[contains(@class,'recommended_activity_badge') and contains(text(),'Recommended Activities')]"
    RECOMMENDED_ACTIVITY_CARD="//div[contains(@class,'heading_wrapper')]"
    
     # Forums 
    FORUMS_SECTION="//div[@class='forum-section']"
    MY_FORUMS_TITLE="//h4[contains(text(),'My Forums')]"
    FORUM_CARD="//div[@class='forum_class_card_container']"

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


