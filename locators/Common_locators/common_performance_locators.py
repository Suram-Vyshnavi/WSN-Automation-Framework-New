class CommonPerformanceLocators:
    PERFORMANCE_MENU="(//div[@id='Performance'])[1]"
    REPORTS_TITLE="(//span[@class='display2 bold3 reports-title'])[1]"
    COURSE_NAME_CONTAINER="(//div[@class='course-container'])[1]"
    SELECT_COURSE_INPUT_FIELD="(//div[@class='ant-select-selection-overflow'])[1]"
    FIRST_COURSE_IN_DROPDOWN="(//div[@class='ant-select-item-option-content'])[1]"
    STATUS_CONTAINER="(//div[@class='status-container'])[1]"
    SELECT_STATUS_INPUT_FIELD="(//div[@class='ant-select-selection-overflow'])[2]"
    FIRST_STATUS_IN_DROPDOWN="(//div[@class='ant-select-item-option-content'])[1]"
    BATCH_NAME_CONTAINER="(//div[@class='batch-container'])[1]"
    SELECT_BATCH_INPUT_FIELD="(//div[@class='ant-select-selection-overflow'])[3]"
    BATCH_NAME_IN_DROPDOWN="(//span[contains(text(),'RC2-Final-Batch')])[2]"
    #Batch assessment scorecard details assessment status details
    BATCH_ASSESEMENT_TITLE="(//p[contains(text(),'Batch Assessment Scorecard')])"
    BATCH_ASSESSMENT_GRAPH="(//canvas[@role='img'])[1]"
    ASSESSMENT_STATUS_TITLE="(//canvas[@role='img'])[1]"
    SHOW_SCORE_TOGGLE_BUTTON="(//button[@role='switch'])[1]"
    ASSESSMENT_STATUS_NEXTSCREEN_ARROW="(//*[name()='svg'][@class='lucide lucide-chevron-right h-4 w-4'])[1]"
    STUDENT_NAME_LINK="(//button[normalize-space()='TestDemo'])[1]"
    #STUDENT PERFORMANCE DETAILS
    COURSE_NAME_DROPDOWN="(//div[@class='ant-select-selector'])[1]"
    STUDENT_NAME_CARD="(//div[@class='ant-col ant-col-xs-12 ant-col-md-6 profile-image-container'])[1]"
    COURSE_NAME_CARD="(//div[@class='ant-col ant-col-xs-12 ant-col-md-6 course-container'])[1]"
    INSTITUTE_NAME_CARD="(//div[@class='ant-col ant-col-xs-12 ant-col-md-6 course-container'])[2]"
    COMPLETION_STATUS_CARD="(//div[@class='ant-col ant-col-xs-12 ant-col-md-6 course-container'])[3]"
    ASSESSMENT_SCORE_DETAILS_CARD="(//div[@class='section-card-white-container assessment-scores-graph'])[1]"
    HOME_MENU="(//div[@id='Home'])[1]"


# Backward compatibility for any existing imports.
CommonCreateMeetingLocators = CommonPerformanceLocators
    

