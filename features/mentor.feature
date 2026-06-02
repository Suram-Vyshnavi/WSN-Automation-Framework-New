Feature: Mentor
    Scenario: Mentor Validation
        Given user is on the home page
        Then user validates the home icon
        Then user clicks on customize weekly schedule 
        Then user add slot button selects the start time slot  and end time slot
        Then user clicks on the copy slot button and selects the day option
        Then user clicks on apply button and closes the slot button 
        Then user clicks on add override button and selects the start time slot and end time slot
        Then user deletes the override slot and clicks on save button

        
    Scenario: Mentor Profile Validation
        Given user is on the home page
        Then user clicks on the profile icon
        Then user validates profile page
        Then user changes firstname, lastname, city and saves the profile
        Then user reverts the changes and saves the profile
        Then user changes language to spanish and saves the profile
        Then user reverts the language change and saves the profile

        