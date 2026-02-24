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
    DONT_NEED_JOB_BUTTON="//span[text()='I don't need a job']"
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
