Feature: career buddy
    Scenario: Validate career buddy card on homepage dashboard
        Given user is on the home page
        Then user validates the home icon
        Then user validates the welcome header and wadhwani skilling header
        Then user clicks on Career Buddy card
        Then user clicks on language dropdown and selects the language and click on apply button
        Then user clicks on language close button
        Then user clicks on sector dropdown and selects the sector and click on apply button
        Then user clicks on sector close button
        Then user clicks on location dropdown and selects the location and click on apply button
        Then user clicks on location close button
        Then user clicks on job role dropdown and selects the job role and click on apply button
        Then user clicks on job role close button
        Then user clicks on search mentor and fill the details
        Then user clicks on the recommended mentor card
        Then user validates the sector jobrole and language details
        Then user clicks on the Book a Session button
        Then user selects the available date and clicks on the slot button
        Then user clicks on session purpose label and selects the Job Search Strategy option
        Then user clicks on specific outcome label and fills in the specific outcome fields, selects the checkbox option and clicks on the Book button
        Then user clicks on the Copy Link option and validates the copied link
        Then user clicks on logout