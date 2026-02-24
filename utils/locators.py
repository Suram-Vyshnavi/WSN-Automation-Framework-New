from utils.config import Config
from operator import contains


class LoginLocators:
    GET_STARTED_BUTTON = "//span[text()='Get Started']"
    LOGIN_BUTTON = "//p[text()='Continue with Email']"
    USERNAME_INPUT="//input[@placeholder='Enter your Email ID']"
    NEXT_BUTTON="//span[text()='Next']"
    PASSWORD_INPUT="//input[@type='password']"
    SUBMIT_BUTTON="//span[text()='Submit']"
    WADHWANI_LOGO="//img[@alt='wadhwani logo white color']"
    HOME_BUTTON="//div[@id='Home']"
    LOGIN_PAGE_HEADER="//h2[contains(text(),'Offered by')]"
    CARD="//div[contains(@class,'program_card__container')]"
    PARAGRAPH_NEW="//p[text()='EN program New']"
    CARRER_ADVISOR="//div[text()='Career Advisor']"
    GOT_IT_BUTTON="//span[text()='Got It']"
    PLACEMENT_PREP="//div[@id='Placement']"
    JOBS_CONNECT="//div[@id='Jobs']"
    CALENDER="(//div[contains(@class,'chat_container')]//img)[1]"
    SUPPORT_ICON="(//div[contains(@class,'chat_container')]//img)[2]"
    CHAT_ICON="(//div[contains(@class,'chat_container')]//img)[3]"
    NOTIFICATIONS_ICON="(//div[contains(@class,'chat_container')]//img)[4]"
    CLOSE_NOTIFICATION="//img[contains(@class,'notification__title__cross')]"
    PROFILE_ICON="//div[@class='header_menu_container']//span[text()='VS']"
    MY_PROFILE="//h1[contains(text(),'My Profile')]"
    EDIT_PROFILE="//span[text()='Edit']"
    FIRST_NAME="//input[@id='first-name']"
    LAST_NAME="//input[@id='last-name']"
    SELECT_COUNTRY="//span[text()='India']"
    SELECT_CITY="//span[text()='Bangalore, Bangalore, Karnataka, India']"
    WHATSAPP_NUMBER="//input[@id='mobile-number']"
    VERIFY_WHATSAPP_NUMBER="//p[text()='Verify']"
    UPDATE_PROFILE="//span[text()='Update']"
    LOGOUT_BUTTON="//h1[normalize-space()='Logout']"

class HomePageLocators:
    HOME_BUTTON="//div[@id='Home']"
    LOGIN_PAGE_HEADER="//h2[contains(text(),'Offered by')]"
    CARD="//div[contains(@class,'program_card__container')]"
    PARAGRAPH_NEW="//p[text()='EN program New']"
    CONTINUE_COURSE="//p[text()='HPS Test-QA2']"
    IN_PROGRESS="//DIV[text()='In Progress']"
    START_COURSE="//span[text()='Start Course']"

class DashboardLocators:
    # Recommended Activities
    RECOMMENDED_ACTIVITIES_SECTION="//p[contains(@class,'recommended_activity_badge') and contains(text(),'Recommended Activities')]"
    RECOMMENDED_ACTIVITY_CARD="//div[contains(@class,'heading_wrapper')]"
    
    # Forums
    MY_FORUMS_SECTION="//h3[contains(text(),'My Forums')]"
    RECOMMENDED_FORUMS_SECTION="//h3[contains(text(),'Recommended Forums')] | //p[contains(@class,'recommended_activity_badge')]"
    FORUM_CARD="//div[contains(@class,'heading_wrapper')]//p[contains(@class,'meeting-badge')]"
    FORUMS_VIEW_ALL="//a[contains(text(),'View All Forums')]"
    
    # Ongoing Course / Learning Progress
    ONGOING_COURSE_SECTION="//h6[contains(@class,'continue-course-text')] | //h5[contains(@class,'my-learning-history-text')]"
    LEARNING_PROGRESS_CARD="//div[contains(@class,'continue-course-container')] | //div[contains(@class,'course_card_container')]"
    COURSE_PROGRESS_BAR="//div[contains(@class,'ant-progress')] | //div[contains(@class,'course_progress_bar')]"
    
    # Institute Specific Courses and Programs
    INSTITUTE_COURSES_SECTION="//h2[contains(@class,'institute_program_course__heading') and contains(text(),'Recommended By Your Institute')]"
    INSTITUTE_PROGRAMS_SUBHEADING="//div[@class='institute_program_course__container']//h4[contains(@class,'institute_program_course__subHeading') and text()='Programs']"
    INSTITUTE_PROGRAM_CARD="//div[@class='institute_program_course__container']//div[@class='program_card__container']"
    INSTITUTE_PROGRAM_NAME="//div[@class='institute_program_course__container']//p[@class='para1 regular program_card__name']"
    INSTITUTE_COURSES_SUBHEADING="//div[@class='institute_program_course__container']//h4[contains(@class,'institute_program_course__courseSubHeading') and text()='Courses']"
    INSTITUTE_COURSE_CARD="//div[@class='institute_program_course__container']//div[@class='popular_class_card_container']"
    INSTITUTE_COURSE_NAME="//div[@class='institute_program_course__container']//p[@class='para1 bold course_name']"
    
    # Default Wadhwani Institute Courses and Programs
    WADHWANI_COURSES_SECTION="//h2[contains(@class,'wadhwani_program_course__heading') and contains(text(),'Offered by')]"
    WADHWANI_PROGRAMS_SUBHEADING="//div[@class='wadhwani_program_course__container']//h4[contains(@class,'wadhwani_program_course__subHeading') and text()='Programs']"
    WADHWANI_PROGRAM_CARD="//div[@class='wadhwani_program_course__container']//div[@class='program_card__container']"
    WADHWANI_PROGRAM_NAME="//div[@class='wadhwani_program_course__container']//p[@class='para1 regular program_card__name']"
    WADHWANI_COURSES_SUBHEADING="//div[@class='wadhwani_program_course__container']//h4[contains(@class,'wadhwani_program_course__subHeading') and text()='Courses']"
    WADHWANI_COURSE_CARD="//div[@class='wadhwani_program_course__container']//div[@class='popular_class_card_container']"
    WADHWANI_COURSE_NAME="//div[@class='wadhwani_program_course__container']//p[@class='para1 bold course_name']"
    
    # Enrol Batch Card
    ENROL_BATCH_SECTION="//div[@class='join-batch-card-container']"
    ENROL_BATCH_TITLE="//div[@class='join-batch-card-container']//h6[contains(@class,'title') and text()='Join a batch']"
    ENROL_BATCH_DESCRIPTION="//div[@class='join-batch-card-container']//p[contains(@class,'description')]"
    ENROL_BATCH_INPUT="//input[@placeholder='Enter code here']"
    ENROL_BUTTON="//button[contains(@class,'join-button')]//span[text()='Enroll']"
    
    # Footer
    FOOTER_SECTION="//div[@class='footer-container']"
    FOOTER_INFO="//span[contains(@class,'more_info') and text()='For more information']"
    FOOTER_WEBSITE_LINK="//a[contains(@class,'website-link')]"
    FOOTER_SOCIAL_MEDIA="//span[contains(@class,'follow_social_media') and text()='Follow us on social media']"
    FOOTER_SOCIAL_ICONS="//div[@class='follow-social-media']//a"
    FOOTER_PRIVACY="//a[contains(@class,'legal-link') and contains(text(),'Privacy policy')]"
    FOOTER_TERMS="//a[contains(@class,'legal-link') and contains(text(),'Terms')]"
    FOOTER_COOKIE="//a[contains(@class,'legal-link') and contains(text(),'Cookie policy')]"
    FOOTER_VERSION="//span[contains(@class,'copyright_text') and contains(text(),'Version')]"
    FOOTER_COPYRIGHT="//span[contains(@class,'copyright_text') and contains(text(),'@2026')]"

class CareerAdvisorLocators:
    CARRER_ADVISOR="//div[text()='Career Advisor']"
    GOT_IT = "//span[text()='Got It']"
    PASSIONS="//h4[text()='Passions']"
    PASSIONS_REVIEW="//h4[text()='Passions']/ancestor::div[2]//span[text()='Review']"
    PASSIONS_SELECTED_ITEMS="//div[@class='selected-items']"
    ################################################################################
    ARTS_DESIGN="//*[contains(text(),'Arts & Design')]"
    DRAWING_ILLUSTRATION_CHECKBOX="//span[text()='Drawing & Illustration']"
    SUBMIT="//span[text()='Submit']"
    BUSINESS_MARKETING="//*[contains(text(),'Business & Marketing')]"
    BUSINESS_MARKETING_CHECKBOX="//div[text()='E‑commerce']"
    QUESTIONNAIRES="//h4[text()='Questionnaires']"
    APTITUDES_REVIEW="//h4[text()='Aptitudes']/ancestor::div[2]//span[text()='Review']"
    APTITUDES_START="//*[normalize-space()='Aptitudes']/following::span[normalize-space()='Start'][1]"
    APTITUDES_REATTEMPT="//span[text()='Reattempt']"
    APTITUDES_SLIDER_CHOOSE="//h3[text()='Slider']/parent::div//span[text()='Choose']"
    START_SLIDER="//span[text()='Start']"
    QUESTION_SEQUENCE="//p[@class='para1 regular slider-sequence' and contains(text(),'1')]"
    #Read the text from the QUESTION_SEQUENCE locator and replace the i value in SLIDER locator with the question number to get the correct slider for that question
    SLIDER_9="//div[@class='questionnaire-slider-container'][1]//span[text()='9']"
    SLIDER_10="//div[@class='questionnaire-slider-container'][1]//span[text()='10']"
    APTITUDES_REATTEMPT_UPDATE="//span[text()='Update']"
    SUBMIT_QUESTIONNAIRE="//span[text()='Submit']"
    INTERESTS_START="//h3[text()='Interests']/ancestor::div[2]//span[text()='Start']"
    VALUES_START="//h3[text()='Values']/ancestor::div[2]//span[text()='Start']"
    GO_TO_MATCHED_ROLES="//span[text()='Go to Matched Roles']"
    WITHOUT_COLLEGE_DEGREE="//span[text()='Without College Degree']"
    VALIDATE_RECOMENDED_ROLES="//span[@class='header-count']"
    #Execute with find elements as validate with all the values in the list and not just the first one
    ##################################################################################################################
    SEARCH_ROLES="//h4[text()='Search Roles']"
    SEARCH_FOR_JOB_ROLE="//input[@placeholder='Search for a Job Role']"
    #Input a job role in the SEARCH_FOR_JOB_ROLE input box and click
    RESULTS_SEARCH="//h4[text()='Results']/following::h4[1]"
    ADD_FAVOURITE_JOB="//h4[text()='Favourite']"
    #################################################################################################################
    FAVOURITES="//h4[text()='Favourites']"
    REMOVE_FAVOURITE_JOB="//h4[text()='Favourite']"
    ##################################################################################################################
    SHARE_REPORT="//h4[text()='Share Report']"
    SHARE_BUTTON="//span[text()='Share']"
    LINK_COPIED_VALIDATION="//h4[contains(text(),'Link copied')]"


class PlacementPrepLocators:
    PLACEMENT_PREP="//div[@id='Placement']"
    PPR_EXPLORE_BUTTON="//span[text()='Personal Pitch Trainer']/parent::div//span[text()='Explore']"
    LANGUAGE_DROPDOWN="//p[text()='English']"
    CREATE_PITCH_BUTTON="//span[text()='Create Your Pitch']"
    POPUP_HEADSUP="//span[text()='Yes, Continue']"
    ###########################################################################################################
    CB_EXPLORE_BUTTON="//span[text()='Career Buddy']/parent::div//span[text()='Explore']"
    CB_START_BUTTON="//span[text()='Start']"
    LANGUAGE_SELECTION="//span[text()='Select Language']"
    ENGLISH_OPTION="//div[text()='English']"
    INTRESTED_SECTOR_OPTION="//div[text()='Healthcare']"
    Next_BUTTON="//span[text()='Next']"
    BOOKSESSION_BUTTON="//span[text()='Book Session']"
    DATE_PICKER_CELL="//td[@class='ant-picker-cell ant-picker-cell-in-view']"
    SLOT_SELECTION_BUTTON="//div[@class='cal-container-right']//button[1]"
    PURPOSE_OF_SESSION="//span[text()='Job Search Strategy']"
    INTERVIEW_PREPARATION_OPTION="//span[text()='Interview Preparation']"
    SPECIFIC_OUTCOME_TEXTAREA="//label[contains(text(),'What specific')]/following::textarea"
    #send some eg text "I need help identifying the right career path based on my background."
    UPLOAD_RESUME_BUTTON="//div[@class='upload_resume_btn']"
    CHECKBOX="//input[@type='checkbox']"
    BOOK_BUTTON="//span[text()='Book']"
    VALIDATE_COPYLINK="//span[text()='Copy Link']"
class InterviewPrepLocators:
    INTERVIEW_COACH_CARD="//span[text()='Interview Coach']"
    INTERVIEW_COACH_EXPLORE_BUTTON="//span[text()='Interview Coach']/following::button[1]"
    VALIDATE_INTERVIEW_PREP_MICBUTTON="//img[contains(@class,'mic-on-image')]"
    INTERVIEW_PREP_TEXTBOX="//input[@placeholder='For eg, Retail Sales Associate, Electronics']"
    INTERVIEW_COACH_SEND_ICON="//img[@alt='interviewCoachSendIcon']"
    #loop the above 2 elements to send product manager first time and e-commerce second time
    PRACTISE_INTERVIEWING_FOR_ROLE="//span[text()='Practise Interviewing for the role']"
    VALIDATE_START_BUTTON="//span[contains(text(),'Start')]"
    BACK_ICON="//img[@alt='pitchTrainerBackIcon']"
    YOUR_RECENT_ROLES="//h1[text()='Your Recent Roles']"
    MORE_DETAILS_ICON="//img[@alt='moreDetails']"
    DELETE_ROLE="//p[text()='Delete this role']"
    DELETE_ROLE_CONFIRM_BUTTON="//span[text()='Confirm']"

    

class PlacementLocators:
    PLACEMENT_PREP_MENU = "//div[@id='Placement']"
    PERSONAL_PITCH_TILE = "//span[contains(text(), 'Personal Pitch Trainer')]"
    EXPLORE_BTN = "//span[contains(text(), 'Personal Pitch Trainer')]/ancestor::div[contains(@class, 'placement_prep_landing_page_card')]//button[contains(@class, 'explore_btn')]"
    PERSONAL_PITCH_HEADER = "//h4[contains(text(), 'Personal Pitch')]"
    CREATE_PITCH_BTN = "//button[contains(@class, 'create-your-pitch-button')]"
    RESUME_PITCH_MODAL = "//div[@class='ant-modal-title' and text()='Resume Your Pitch']"
    START_NEW_PITCH_BTN = "//button[contains(@class, 'discard-button')]//span[text()='Start New Pitch']"
    STEP_1_INDICATOR = "//span[@class='ant-steps-icon' and @data-label='1']"
    TARGET_JOB_HEADER = "//h1[contains(@class, 'job-role-heading')]"
    JOB_ROLE_INPUT = "//input[@id='job-role-input']"
    JOB_ROLE_CONTAINER = "//div[contains(@class, 'wf_animated_input')]"
    JOB_ROLE_SUBMIT_BTN = "//div[contains(@class, 'validate-job-role-correct')]"
    UNDERSTAND_BTN = "//button[contains(@class, 'understand-button')]"
    STEP_2_INDICATOR = "//span[@class='ant-steps-icon' and @data-label='2']"
    RECORD_PITCH_HEADER = "//h4[contains(@class, 'record-pitch-heading')]"
    RECORD_BTN = "//p[contains(@class, 'record-button') and text()='Record']"
    LEAVING_PITCH_MODAL = "//div[@class='ant-modal-title' and contains(text(), 'Leaving Pitch Creation')]"
    SAVE_EXIT_BTN = "//button[contains(@class, 'discard-button')]//span[text()='Save & Exit']"
    LANGUAGE_ALERT_HEADER = "//span[contains(text(), 'Heads up!')]"

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
    # Target dropdown specifically within the modal to avoid hidden/background inputs
    SESSION_PURPOSE_DROPDOWN = "//div[contains(@class, 'ant-modal')]//div[contains(@class, 'ant-select-selector')]" 
    SESSION_PURPOSE_OPTION = "//div[contains(@class, 'ant-select-item-option') and @title='Resume Building']"
    OUTCOME_TEXTAREA = "//textarea[@id='Outcome']"
    CHECKBOX = "//input[@type='checkbox']"
    # Make sure we target the submit button in the modal, not the 'Book Session' button
    BOOK_CONFIRM_BTN = "//button[@type='submit' and contains(., 'Book')]"
    # Use specific class to avoid matching parent container
    MEETING_HEADER = "//span[contains(@class, 'company-name') and not(contains(@class, 'company-name-container'))]"


    

class JobsConnectLocators:
    JOBS_CONNECT="//div[@id='Jobs']"
    RESET_FILTER_BUTTON="//div[@class='filter-title']/parent::div//button[text()='Reset']"
    SEARCH_BY_JOB_TITLE_INPUT="//input[@id='search'] | //input[@placeholder='Search by job title/roles']"
    #Input a job title in the SEARCH_BY_JOB_TITLE_INPUT input box and click eg Product Manager
    FIND_JOBS_BUTTON="//button[contains(@class,'find-jobs-btn')] | //button[text()='Find Jobs']"
    GET_STARTED_BUTTON="//button[@id='view-job-openings-btn']"
    EDUCATION_DETAILS="//span[text()='Highest or current education']"
    GRADUATE_OPTION="//div[contains(@class,'ant-select-item-option-content') and normalize-space()='Graduate']"
    COURSE_TYPE_OPTION="//div[contains(@class,'ant-select-item-option-content') and normalize-space()='B.A']"
    SPECILIZATION_OPTION="//div[contains(@class,'ant-select-item-option-content') and normalize-space()='Economics']"
    INSTITUTION_NAME_INPUT="//input[@id='institution-name']"
    #Send institute name
    START_DATE_MONTH_INPUT="//div[@class='start-date-wrapper']//input[@placeholder='Month']"
    #Send month as name of the month like January, February etc
    START_DATE_YEAR_INPUT="//div[@class='start-date-wrapper']//input[@placeholder='Year']"
    #send year as 4 digit number
    END_DATE_MONTH_INPUT="//div[@class='end-date-wrapper']//input[@placeholder='Month']"
    #Send month as name of the month like January, February etc 
    END_DATE_YEAR_INPUT="//div[@class='end-date-wrapper']//input[@placeholder='Year']"
    #send year as 4 digit number
    NEXT_BUTTON="//span[text()='Next']"
    DONT_NEED_JOB_BUTTON="//span[text()='I don’t need a job']"
    CERTIFICATION_YES_BUTTON="//span[text()='Yes']"
    CERTIFICATION_NAME="//span[text()='Certification name']"
    #send certification name in the input box that appears after clicking CERTIFICATION_YES_BUTTON
    SECTOR_OPTION="//div[contains(@class,'ant-select-item-option-content') and normalize-space()='Healthcare']"    
    ISSUING_ORGANIZATION="//span[text()='Issuing Organization']"
    #send issuing organization name in the input box
    CERTIFICATION_MONTH_INPUT="//input[@placeholder='Month']"
    #Send month as name of the month like January, February etc
    CERTIFICATION_YEAR_INPUT="//input[@placeholder='Year']"
    #send year as 4 digit number
    SAVE_BUTTON="//span[text()='Save']"
    ADD_ANOTHERCERTIFICATE="//span[text()='Add certificate']"
    JOB_TITLE="//span[text()='Job title']"
    JOB_TYPE="//span[text()='Job type']"
    JOB_TYPE_OPTION="//div[contains(@class,'ant-select-item-option-content') and normalize-space()='Full time']"
    COMPANY_NAME_INPUT="//input[@id='companyName']"
    ADD_WORK_EXPERIENCE="//span[text()='Add work experience ']"
    PREFFERED_JOB_SECTOR="//span[text()='Preferred sector(s)']"
    PREFFERED_JOB_SECTOR_OPTION="//div[text()='Retail']"
    APPLY_BUTTON="//span[text()='Apply']"
    PREFERRED_JOB_LOCATION="//span[text()='Preferred job location']"
    #send bangalore as preferred job location
    PREFERRED_JOB_LOCATION_OPTION="//div[text()='Bangalore, Bangalore, Karnataka']"
    ADD_PDF_DOCUMENT="//span[text()='Add pdf document']"
    CHECKBOX="//input[@type='checkbox']"
    GIVE_CONSENT_BUTTON="//span[text()='Give Consent']"
    SEARCH_RESULTS_VALIDATION="//div[@class='job-helper-text']//span"
    JOB_RESULT_CARD="//div[contains(@class,'job-card') or contains(@class,'job-listing-card')]"
    FIRST_JOB_RESULT="(//div[contains(@class,'job-card') or contains(@class,'job-listing-card')])[1]"
    APPLY_NOW_BUTTON="//button[contains(text(),'Apply') or contains(text(),'apply')]"
    JOB_DETAILS_APPLY="//span[text()='Apply'] | //button[text()='Apply']"


class Messages_and_discussionsLocators:
    message="hello"
    SEND_MESSAGE_BUTTON="//span[text()='Send Message']"
    FIRST_NEW_MESSAGE="//div[@class='search_result_container']/div[position()=1]"
    MESSAGE_TEXTAREA="//textarea[@placeholder='Type a message']"
    # send hello in the above textarea
    SEND_MESSAGE_ICON="//img[@alt='send message']"
    LATEST_SENT_MESSAGE=f"(//td[text()='{Config.MESSAGE_TEXT}'])[position()=1]"
    LATEST_SENT_IMAGE="(//div[contains(@class,'message_box') and contains(@class,'background_blue')]//img)[1]"
    LATEST_SENT_DOCUMENT="(//span[@class='anticon anticon-download chat-File-Icon'])[position()=1]"
    FILE_UPLOAD_BUTTON="//div[@class='input_message']//span"
    IMAGE_OPTION="//div[text()='Image']"
    DOCUMENT_OPTION="//div[text()='Document']"

class Learning_Progress_Locators:
    PROFILE_ICON="//div[@class='header_menu_container']//span[text()='VS']"
    LEARNING_PROGRESS="//h1[text()='Learning Progress']"
    VALIDATE_LEARNING_PROGRESS="//h6[text()='Learning Progress']"
    MY_COURSES="//h4[text()='My Courses']"
    ONGOING_COURSES="//P[contains(text(),'Ongoing')]"
    FIRST_ONGOING_COURSE="(//div[@class='course_card_container'])[position()=1]"
    VALIDATE_LEARNING_PROGRESSFIRST_ONGOING_COURSE_HEADING="//h1[@class='typography-text page-title heading-text']"  
    FIRST_ONGOING_COURSE_OVERVIEW="//p[text()='Overview']"
    FIRST_ONGOING_COURSE_CONTENT="//p[text()='Course Content']"
    FIRST_ONGOING_COURSE_PERFORMANCE="//p[text()='Performance']"
    COMPLETED_COURSES="//P[contains(text(),'Completed')]"
    FIRST_COMPLETED_COURSE="//div[@class='course_card_container']//div[text()='Completed'][1]"
    VALIDATE_LEARNING_PROGRESSFIRST_COMPLETED_COURSE_HEADING="//h1[@class='typography-text page-title heading-text']"
    FIRST_COMPLETED_COURSE_OVERVIEW="//p[text()='Overview']"
    FIRST_COMPLETED_COURSE_CONTENT="//p[text()='Course Content']"
    FIRST_COMPLETED_COURSE_PERFORMANCE="//p[text()='Performance']"
    VALIDATE_SCORE_VALUE="//div[@class='score_info']//span[@class='score_value']"
    VALIDATE_OVERALL_PROGRESS="//span[text()='Overall Progress']"

class NotificationLocators:
    NOTIFICATIONS_ICON="(//div[contains(@class,'chat_container')]//img)[4]"   
    VALIDATE_NOTIFICATION_CONTAINER="//div[@class='notification__scroll']"
    FIRST_NOTIFICATION="//div[@class='notification__scroll']//div[1]//span[1]"
