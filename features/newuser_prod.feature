@prod @newuser_prod
Feature: New_user_Prod
    Scenario: PROD - New user registration with valid details
        Given the user opens the WSN application
        When the user clicks on "Continue with Email"
        And the user enters a valid email address manually
        And the user enters the OTP manually
        And the user completes the registration form
        And the user clicks on "Submit"
        Then the user should be registered successfully

    Scenario: PROD - New user successfully registers and reaches the application
        Then the user should reach the application
        Then the application home page should be displayed

    Scenario: PROD - New user enrolls with the job key
        When the user clicks on accounts menu
        And the user clicks on "join a batch"
        Then user enters the job code in the input field
        And the user clicks on "Enroll"
        Then the user should be enrolled successfully
        
    Scenario: PROD - New user navigates to Courses
        When the user clicks on "Courses"
        Then the Courses page should be displayed

    Scenario: PROD - New user verifies the QA Try Test course
        Then the "QA Try Test" course should be available

    Scenario: PROD - New user enrolls in the QA Try Test course
        When the user selects the "QA Try Test" course
        And the user clicks on the first "Enroll Now" button
        And the user clicks on the second "Enroll Now" button
        Then the course should be enrolled successfully

    Scenario: PROD - New user verifies the enrolled QA Try Test course content
        When the user clicks on "Course Content"
        Then the course content should be displayed

    Scenario: PROD - New user opens and completes the Try Activity
        When the user opens the "Try Activity"
        And the user completes all the required activities
        Then all Try Activity tasks should be completed successfully

    Scenario: PROD - New user starts the first Self-Serve Activity
        When the user opens the "Try Self Serve Activity"
        And the user clicks on the first "Start" button
        And the user clicks on the factory and production work
        Then the first self-serve activity should be started successfully

    Scenario: PROD - New user completes the first Self-Serve Activity
        When the user answers all the available questions
        And the user selects any job category or selects a random job role
        And the user answers all the available questions
        Then the first self-serve activity should be completed successfully

    Scenario: PROD - New user starts the second Self-Serve Activity
        When the user clicks on the second "Start" button
        And the user clicks on the factory and production work
        Then the second self-serve activity should be started successfully

    Scenario: PROD - New user completes the second Self-Serve Activity
        When the user answers all the available questions
        And the user selects any job category or selects a random job role
        And the user answers all the available questions
        Then the second self-serve activity should be completed successfully

    Scenario: PROD - New user verifies that the required activities are completed successfully
        Then all Try Activity tasks should be completed successfully
        And the second self-serve activity should be completed successfully
