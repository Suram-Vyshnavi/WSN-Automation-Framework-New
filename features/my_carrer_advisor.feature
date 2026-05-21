Feature: My Career Advisor
    Scenario: Validate my career advisor card on homepage dashboard
        Given user is on the home page
        Then user validates the home icon
        Then user validates the welcome header and wadhwani skilling header
        Then user clicks on My Career Advisor card
        Then user validates the Passion header and clicks on the Review button
        Then user selects the passion items and clicks on the Submit button
        Then user validates the Questionnaire header
        Then user clicks on the Review button in the Aptitudes section
        Then user clicks on the Reattempt button
        Then user clicks on the slider choose button
        Then user selects the 1st question option. If the slider sequence is on 9, the user clicks on 10. If the slider sequence is on 10, the user clicks back on 9
        Then user clicks on the Update button
        Then user clicks on the Go to Matched Roles button
        Then user clicks on Without College Degree
        Then user validates the header count
        Then user clicks on the searched role
        Then user fills in the job role input field
        Then user validates the Result header and clicks on Favourite
        Then user clicks on the Favourites header
        Then user clicks on Share Report and clicks on the Share button
        Then user clicks on the Favourite button and removes the favourite
        Then user clicks on logout
