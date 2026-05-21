Feature:jobsconnect
  Scenario:Validate jobsconnect card on homepage dashboard
    Given user is on the home page
        Then user validates the home icon
        Then user validates the welcome header and wadhwani skilling header
        Then user clicks on jobsconnect card
        Then user clicks on jobtype and selects full time option
        Then user clicks on workmode filter and selects office option
        Then user clicks on industry sector filter and selects automotive option
        Then user clicks on education level filter and selects graduate option
        Then user clicks on preffered companies filter and selects diatoz option
        Then user clicks on search by role title and fills product manager and clicks on find jobs
        Then user clicks on first job card
        Then user validates about the job and about the company sections
        Then user validates apply button and closes the current tab and navigate to jobs connect page
        Then user clicks on reset button
        Then user clicks on logout