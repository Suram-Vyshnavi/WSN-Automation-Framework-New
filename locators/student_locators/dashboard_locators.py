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
