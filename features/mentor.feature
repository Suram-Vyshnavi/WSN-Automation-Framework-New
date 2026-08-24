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
#     # Scenario: Calendar validation  
#     #     Then user clicks on Accounts menu
#     #     Then user clicks on calendar
#     #     Then user validates the calendar screen
#     #     Then user scroll down the screen and validates the upcoming events/meetings and past meetings if available
#     #     Then user navigates to home screen
    Scenario: Messages and discussions validation
        Then user clicks on Accounts menu
        Then user clicks on Messages & Discussions
        Then user clicks on first chat in the list
        Then user sends a message
        Then user validates the latest message sent
        Then user clicks on file upload button
        Then user uploads document in to the chat and validates
        Then user clicks on file upload button
        Then user uploads photo in to chat and validates
        Then user navigates to home page
    Scenario: Settings ZoomConnect validation
        Then common user clicks on ZoomConnect profile icon
        Then common user clicks on settings menu
        Then common user validates the settings sections
        Then common user clicks on accounts menu and validates accounts_meetings section
        Then common user clicks on sign in with zoom right arrow button
        Then common user validates the zoom account delinked popup and closed the popup
        Then common user validates the sign in with zoom section and turn on the toggle button
        Then common user navigates to meetings section and click on signin button
        Then common user navigates to zoom.us signin screen and validates the email address, password,signin buttons
        Then common user clicks on email input field and enter the email id
        Then common user clicks on password input field and enter the password
        Then common user clicks on sigin button
        Then common user navigates back to to signin with zoom screen and validates the toggle button status
        Then common user click on back arrow and navigates to settings screen
  Scenario: Settings WhatsappNotifications validation
        Then common user clicks on ZoomConnect profile icon
        Then common user clicks on settings menu
        Then common user validates the settings sections
        Then common user clicks on notifications menu and validates whatsapp container section
        Then common user clicks on whatsapp container section right arrow button
        Then common user validates the whatsapp section and clicks on the toggle button
        Then common user clicks on the whatsapp section back arrow and validates the settings section
    
