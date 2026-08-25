from locators.student_persona_locators.programs_and_courses_locators import (
    ProgramsAndCoursesLocators as Merged,
)

class LearningProgressLocators:
    # The course detail page was redesigned: the Overview / Course Content /
    # Performance tabs were replaced by a certificate-progress panel, lesson
    # accordions and an assessment score. Shared with the Courses scenario.
    COURSE_TITLE = Merged.COURSE_TITLE
    CERTIFICATE_PROGRESS = Merged.CERTIFICATE_PROGRESS
    EARNED_MICRO_CERTIFICATES = Merged.EARNED_MICRO_CERTIFICATES
    LESSON_ACCORDION = Merged.LESSON_ACCORDION
    ASSESSMENT_SCORE_VALUE = Merged.ASSESSMENT_SCORE_VALUE
    ASSESSMENT_SCORE_LABEL = Merged.ASSESSMENT_SCORE_LABEL

    ACCOUNTS_MENU="//button[@aria-label='Accounts menu']//img"
    LEARNING_PROGRESS="//p[contains(text(),'Learning Progress')]"
    VALIDATE_LEARNING_PROGRESS="//h6[text()='Learning Progress']"
    MY_COURSES="//h4[text()='My Courses']"
    ONGOING_COURSES="//h5[contains(text(),'Ongoing')]"
    FIRST_ONGOING_COURSE="(//div[@class='new-enrolled-course-card'])[1]"
    VALIDATE_LEARNING_PROGRESSFIRST_ONGOING_COURSE_HEADING="//h1[contains(@class,'course-title-heading') or contains(@class,'heading-text')]"  
    CERTIFICATE_SHARE_BUTTON="//span[text()='Share']//following::img[1]"
    CERTIFICATE_COPY_LINK="//span[text()='Copy Link']"
    VALIDATE_CERTIFICATE_LINK_COPIED="//span[text()='Certificate link copied']"
    VALIDATE_CERTIFICATE_DOWNLOAD_BUTTON="//span[text()='Download']//following::img[1]"
    BATCH_NAME="//h2[text()='Batch Name : ']/following::h2[1]"
    # "Help us personalize your journey" interstitial popup
    PERSONALIZE_JOURNEY_POPUP="//*[contains(normalize-space(),'personalize your journey') or contains(normalize-space(),'personalise your journey')]"


