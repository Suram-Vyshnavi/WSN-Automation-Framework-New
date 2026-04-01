Feature: RM Login

  Scenario: RM login only
    Then current persona login should be successful

  Scenario: RM Homescreen validation
    Then user navigates through dashboard
    Then user clicks on Home menu
    Then user clicks on Batches menu
    Then user clicks on Performance menu
    Then user clicks on Calender
    Then user navigates with Help/support
    Then user checks notifications and chat
    Then user clicks on profile icon
    Then user edits profile details for first name and clicks on the save button
    Then user navigates to home page
    Then user validates recommended activities section
    Then user validates batches section and create new batch button
    Then user validates Active and Inactive tabs under batches section
    Then user clicks on the batches next arrow button
    Then user validates certified courses section and clicks on carousal arrow
    Then user validates My Forums section and validates the recommended forums section

  @faculty_only
  Scenario: Faculty Createbatch validation
    Then user navigates through dashboard
    Then user clicks on craete new batch button
    Then user validates the batch information header section and validates the batch information title
    Then user clicks in Institute selection dropdown and select the "Test National Skill Training Instititute dev" name from list
    Then user validates the faculty pre filled name
    Then user clicks on select course selection dropdown and select the "QA-Emp skill Test-V2" course from list
    Then user clicks on Batch name input filed and enters the "Automation-Batch" name
    Then user validates the start date input field and click on the calendar icon and clicks on the today text
    Then user validates the end date input field and clicks on the calendar icon and clicks on the next year/next month arrow and select "23" from month
    Then user validates the student enrollment note section and validates the prefilled weekly class hours value
    Then user check the confirmation checkbox and clicks on the maximum students allowed input field and enter 200 value and clicks on Next button
    Then user validates the confirm dates popup and clicks on the confirm and proceed button
    Then user validates the assessment details section and click on the next button
    Then user validates the difficulty level 1 , difficulty level 2 , difficulty level 3 and clicks on the difficulty level 2 radio button
    Then user clicks on the "job role or sector" input field and enters the "Automation Engineer" text and clicks on the enter button
    Then user clicks on the save and finish button and validate the batch details card

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

  Scenario: Batch Details validation
    Then user clicks on first batch from Active batches list
    Then user validates the institute name and course name
    Then user validates the course timeline section and batch code section
    Then user clicks on the batch code and copy it
    Then user clicks on the more option and clicks on the edit batch option
    Then user validates the batch details section and edits the batch name and update the details
    Then user clicks on the more option and clicks on the close batch option and clicks on close button
    Then user validates the general info tab and validates the assessment schedule section
    Then user validates the batch activity section and validates the batch faculty section
    Then user clicks on the add faculty button and clicks on the second faculty
    Then user validates the toast message and user clicks on the edit faculty button
    Then user clicks on the faculty2 cross icon and clicks on the faculty delete button
    Then user validates the faculty delete toast message
    Then user validates the upcoming activities section and validates the create meeting button

  Scenario: Create meeting validation
    Then common user navigates to the batch details screen and navigates the upcoming activities section
    Then common user clicks on the create meeting button
    Then common user validates the meeting title and validates the create new meeting card
    Then common user clicks on the meeting input filed and enter the "Automation Meeting"
    Then common user clicks on the select date input field and validate the calendar date picker
    Then common user clicks on the ok button and clicks on the timeslot dropdown and selects the 15min slot
    Then common user validates the meeting agend field and clicks on the meeting agenda input and enters the "Automation Discussion"
    Then common user clicks on the notes input and enters the "We will discuss on automation task latest updates"
    Then common user clicks on the create meeting button and validates the create meeting confirmation card and clicks on the okay button
    Then common user navigates to  batch details screen and refresh the screen
    Then common user validates the meeting card under upcoming activities section and clicks on the meeting on the meeting card
    Then common user validates the meeting check card and notes card
    Then common user clicks on the meeting edit icon and enters the some value to notes and clicks on the update changes
    Then common user clicks on the delete icon and clicks on the delete button on the confirmation popup
    Then common user validates the delete event toast message and lands on the calendar screen

  Scenario: Batch details scorecard validation
    Then user clicks on first batch from Active batches list
    Then user validates the scorecard tab and clicks on it
    Then user validates the Assessment schedule title and validates the Assessment schedule container

  Scenario: Batch details collaboratesetup validation
    Then user clicks on first batch from Active batches list
    Then user validates the collaboratesetup tab and clicks on it
    Then user clicks on edit button and change level from 2 to 1 and clicks on the save button
    Then user navigates to batch details collaborate setup screen and validates the selected career plans section

 Scenario: Batch members validation
   Then common user clicks on "RC2-Final-Batch" batch from Active batches list
   Then common user validates the batch members tab and clicks on it
   Then common user clicks on the manage student button
   Then common user clicks on the invite students button and validated the batch code 
   Then common user clicks on the batchcode copy button and paste it on the enter student email input field
   Then common user removes the batchcode from input field and user enters the email id "stu-webautomation-dev-qa@yopmail.com" and clicks on the send invite button
   Then common user clicks on download template link and clicks on the upload file button and uploads the file and clicks on the file invite button
   Then common user validates the uploaded users status bar and clicks on the uploaded users download button
   Then common user clicks on the invite students back button
   Then common user validates the batch students tab and pending requests tab
   Then common user clicks on the batch students tab and validates the first user view button and download button
   Then common user clicks on the view button and validates the certificate images and cicks on the download certificate button
   Then common user clicks on the close icon and the user clicks on the download certificate download button
   Then common user clicks on the user delete button and validates the remove student popup
   Then common user clicks on the no button from the popup and clicks on the pending requests tab
   Then common user clicks on the first user resend otp button and validates the resend otp popup
   Then common user clicks on the yes button on resend otp popup and clicks on the manage students back button
   Then common user clicks on tha batch members tab and validates the first batch member card and clicks on the chat button
   Then common user clicks on the home menu from header section

 Scenario: Activity insights validation
   Then common user clicks on "RC2-Final-Batch" batch from Active batches list
   Then common user validates the activity insights tab and clicks on it
   Then common user validates the submission insights header section and validates the module column title and lesson name column title
   Then common user clicks on the students submitted i icon and validates the text
   Then common user click on the students scored i icon and validates the text
   Then common user clicks on the pitch trainer pre video arrow icon and validates the heading section and insights table and click on the back arrow
   Then common user clicks on the active listening arrow icon and validates the heading section and insights table and click on the back arrow
   Then common user clicks on the LT and TA arrow icon and validates the heading section and insights table and click on the back arrow
   Then common user clicks on the pitch trainer post video arrow icon and validates the heading section and insights table and click on the back arrow

Scenario: Performance screen validation
  Then common user clicks on the performance menu
  Then common user validates the reports title 
  Then common user validate the course name container and clicks on the select course name input field and clicks on the first course from dropdown
  Then common user validates the status container and clicks on the select satus input field and clicks on the first status from the dropdown
  Then common user validates the batch name container and clicks on the select batch input field and clicks on the "RC2-Final-Batch" from dropdown
  Then common user validates the batch assessment title and batch assessment graph
  Then common user validates the assessment status title and validates the show score toggle button
  Then common user clicks on the score toggle button and clicks on the assessment status next arrow button 
  Then common user clicks on the student name link from second screen
  Then common user validates the course name dropdown and validates the student name card
  Then common user validates the course name card , institute name card , completion status card  and assessment score details card
  Then common user clicks on the home menu from header section


 Scenario: Chat Messages and discussions validation
   Then common user clicks on chat icon
   Then common user clicks on send message button
   Then common user clicks on first contact in the list
   Then common user sends a message
   Then common user validates the latest message sent
   Then common user clicks on file upload button
   Then common user uploads photo in to chat and validates
   Then common user clicks on file upload button
   Then common user uploads document in to the chat and validates
   Then common user navigates to home page

Scenario: Notifications validation
  Then common user clicks on notification icon
  Then common user validates the notifications
  Then common user clicks on first notification
  Then common user navigates to home page