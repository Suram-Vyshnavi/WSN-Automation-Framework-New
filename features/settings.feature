Feature: Settings validations

Background:
  Then user clicks on ZoomConnect profile icon
  Then user clicks on settings menu

Scenario: Settings ZoomConnect validation
  Then user validates the settings sections
  Then user clicks on accounts menu and validates accounts_meetings section
  Then user clicks on sign in with zoom right arrow button
  Then user validates the zoom account delinked popup and closed the popup
  Then user validates the sign in with zoom section and turn on the toggle button
  Then user navigates to meetings section and click on signin button
  Then user navigates to zoom.us signin screen and validates the email address, password, signin buttons
  Then user clicks on email input field and enter the email id
  Then user clicks on password input field and enter the password
  Then user clicks on sigin button
  Then user navigates back to to signin with zoom screen and validates the toggle button status
  Then user click on the toggle button and validates the disconnect section
  Then user clicks on the disconnect button 
  Then user click on back arrow and navigates to settings screen

Scenario: Settings DeleteAccount validation
  Then user validates the settings sections
  Then user clicks on accounts menu and validates delete account section
  Then user clicks on delete account right arrow button
  Then user validates the delete account popup and clicks on the get otp button
  Then user validates the otp input field and clicks on the delete account otp section back arrow
  Then user navigates to delete account section and click on close icon
  Then user navigates to settings screen

Scenario: Settings WhatsappNotifications validation
  Then user validates the settings sections
  Then user clicks on notifications menu and validates whatsapp container section
  Then user clicks on whatsapp container section right arrow button
  Then user validates the whatsapp section and clicks on the toggle button
  Then user clicks on the whatsapp section back arrow and validates the settings section
