class CareerAdvisorLocators:
    CARRER_ADVISOR="//div[text()='Career Advisor']"
    GOT_IT = "//span[text()='Got It']"
    PASSIONS="//h4[text()='Passions']"
    PASSIONS_REVIEW="//h4[normalize-space()='Passions']/following::button[normalize-space()='Review'][1]"
    PASSIONS_SELECTED_ITEMS="//div[@class='selected-items']"
    ################################################################################
    ARTS_DESIGN="//*[contains(text(),'Arts & Design')]"
    DRAWING_ILLUSTRATION_CHECKBOX="//div[text()='Drawing & Illustration']"
    SUBMIT="//button[text()='Submit']"
    BUSINESS_MARKETING="//*[contains(text(),'Business & Marketing')]"
    BUSINESS_MARKETING_CHECKBOX="//button[text()='E‑commerce']"
    QUESTIONNAIRES="//h4[text()='Questionnaires']"
    APTITUDES_REVIEW="//h4[text()='Aptitudes']/ancestor::div[2]//button[text()='Review']"
    APTITUDES_START="//*[normalize-space()='Aptitudes']/following::button[normalize-space()='Start'][1]"
    APTITUDES_REATTEMPT="//button[text()='Reattempt']"
    APTITUDES_SLIDER_CHOOSE="//h3[text()='Slider']/parent::div//button[text()='Choose']"
    START_SLIDER="//button[text()='Start']"
    QUESTION_SEQUENCE="//p[@class='para1 regular slider-sequence' and contains(text(),'1')]"
    #Read the text from the QUESTION_SEQUENCE locator and replace the i value in SLIDER locator with the question number to get the correct slider for that question
    SLIDER_9="//div[@class='questionnaire-slider-container'][1]//span[text()='9']"
    SLIDER_10="//div[@class='questionnaire-slider-container'][1]//span[text()='10']"
    APTITUDES_REATTEMPT_UPDATE="//button[text()='Update']"
    SUBMIT_QUESTIONNAIRE="//button[text()='Submit']"
    INTERESTS_START="//h3[text()='Interests']/ancestor::div[2]//button[text()='Start']"
    VALUES_START="//h3[text()='Values']/ancestor::div[2]//button[text()='Start']"
    GO_TO_MATCHED_ROLES="//button[text()='Go to Matched Roles']"
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
    SHARE_BUTTON="//button[text()='Share']"
    LINK_COPIED_VALIDATION="//h4[contains(text(),'Link copied')]"
