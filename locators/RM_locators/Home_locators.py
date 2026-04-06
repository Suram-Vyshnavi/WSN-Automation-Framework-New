class HomeLocators:
    WADHWANI_LOGO = "//img[@alt='wadhwani logo white color']"
    HOME_MENU="//div[@id='Home']"
    PERFORMANCE_MENU="//div[@id='Performance']"
    ALL_BATCHES_MENU="(//div[@id='All'])[1]"
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
    SAVE_BUTTON="(//button[normalize-space()='Save'])[1]"
    
    #Assigned batches section
    ASSIGNED_BATCHES_TITLE="(//h2[normalize-space()='Assigned Batches'])[1]"
    BATCH_NAME_TITLE="(//div[normalize-space()='Batch Name'])[1]"
    INSTITUTE_NAME_TITLE="(//div[normalize-space()='Institute Name'])[1]"
    COURSE_NAME_TITLE="(//div[normalize-space()='Course Name'])[1]"
    START_DATE_TITLE="(//div[normalize-space()='Start Date'])[1]"
    END_DATE_TITLE="(//div[normalize-space()='End Date'])[1]"
    NO_OF_STUDENTS_TITLE="(//div[normalize-space()='No. of Students'])[1]"
    ACTION_TITLE="(//div[normalize-space()='Action'])[1]"
    ASSIGNED_BATCHES_NEXT_BUTTON="//li[contains(@class,'ant-pagination-next')]/button[not(@disabled)]"
    

