Feature: Login
  Scenario: Valid login
    Then user navigates through dashboard
    Then user clicks on Career Advisor
    Then user clicks on Placement Prep
    Then user clicks on Jobs Connect
    Then user clicks on Calender
    Then user navigates with support
    Then user checks notifications and chat
    Then user clicks on profile icon
    Then profile fields should be visible
    Then user edits profile details
    Then user navigates to home page

  Scenario: Dashboard sections validation
    Then user validates recommended activities section
    Then user validates ongoing course section
    Then user validates institute specific courses
    Then user validates wadhwani courses and programs
    Then user validates enrol batch card
    Then user validates footer section

  Scenario: Verify Placement Prep Personal Pitch Flow
    Then user navigates to Placement Prep
    Then user verifies Personal Pitch Trainer tile
    Then user clicks on Explore button
    Then user verifies Personal Pitch header
    Then user clicks on Create Your Pitch button
    Then user handles language alert if present
    Then user verifies Resume Start Pitch modal and clicks Start New Pitch
    Then user verifies Step 1 Target Job & Notes
    Then user enters "Automation Tester" in job role and validates
    Then user clicks on Create Your Pitch
    Then user handles "I understood" popup if present
    Then user verifies Step 2 Record Pitch
    Then user verifies Record Pitch header and Record button
    Then user clicks on Placement Prep menu
    Then user handles Leaving Pitch Creation modal by clicking Save & Exit
    Then user navigates to home page

  Scenario: Verify Placement Prep Interview coach Flow
    Then user navigates to Placement Prep
    Then user verifies Interview Coach tile and clicks Explore
    Then user validates textbox and mic button in Interview Coach page
    Then user sends required details for the interview coaching
    Then user clicks on Practise Interviewing for the role
    Then user validates questions using start button
    Then user navigates back from the questions page and deletes the created interview coaching
    Then user navigates to home page

  Scenario: Verify Placement Prep Career Buddy Flow
    Then user navigates to Placement Prep
    Then user verifies Career Buddy tile and clicks Explore
    Then user searches for mentor "Leela B"
    Then user clicks on Book Session for the mentor
    Then user selects an available date and time slot
    Then user enters booking details and confirms
    Then user verifies the meeting details page
    Then user navigates to home page

  Scenario: Career Advisor complete validation
    Then user navigates to career advisor
    Then user selects passions preferences
    Then user selects review passions preferences
    Then user validates the selected items in passions review section
    Then user click on submit button in passions section
    Then user clicks on questionnaires section
    Then user clicks on review button in aptitudes section
    Then user clicks on reattempt
    Then user chooses slider option in aptitudes section
    Then user clicks on 1st question and changes the slider value to 9 or 10 and clicks on update
    Then user clicks on Go to matched roles
    Then user clicks on search roles
    Then user enters jobrole and add the first job as favourite
    Then user clicks Favourites and validates the added job
    Then user clicks on share report and click and validates the share report options
    Then user clicks on Favourites and removes the added job from favourites
    Then user navigates to home page

  Scenario: Jobs Connect complete validation
    Then user navigates to Jobs Connect
    Then user resets filters
    Then user searches for a job
    Then user clicks on find jobs
    Then user validates job search results
    Then user clicks on the first job result
    Then user validates the apply option
    Then user navigates to home page
  
  Scenario: Messages and discussions validation
    Then user clicks on chat icon
    Then user clicks on send message button
    Then user clicks on first contact in the list
    Then user sends a message
    Then user validates the latest message sent
    Then user clicks on file upload button
    Then user uploads photo in to chat and validates
    Then user clicks on file upload button
    Then user uploads document in to the chat and validates
    Then user navigates to home page

  Scenario: Notifications validation
    Then user clicks on notification icon
    Then user validates the notifications
    Then user clicks on first notification
    Then user navigates to home page

  Scenario: Learning progress validation
    Then user clicks on profile icon
    Then user clicks on learning progress
    Then user validates the learning progress
    Then user navigates to learning progress page and clicks on completed courses
    Then user clicks on a completed course and validates overview, content, performance sections, score value and overall progress
    Then user clicks on share certificate button and validates download certificate option
    Then user clicks on ongoing courses and validates overview section
    Then user clicks on content section and clicks on resume
    Then user clicks on performance section and validates final score
    Then user clicks on overview section and clicks on view batch and validates
    Then user clicks on general info and validates upcoming activities
    Then user clicks on batch members and validates students added count and maximum allowed and batch member list
    Then user clicks on chat button
    Then user sends a message
    Then user validates the latest message sent
    Then user navigates to home page
  
    
