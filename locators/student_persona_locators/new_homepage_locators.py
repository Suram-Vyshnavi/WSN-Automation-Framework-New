class NewHomepageLocators:
    # Prod's mobile-new-ui header can hide the desktop #Home div and show a
    # mobile home button instead, so accept either.
    HOME = "//div[@id='Home'] | //div[text()='Home'] | //button[@aria-label='Home']"
    VALIDATE_GENIE_AI_BANNER = "//div[@class='genie-ai-banner']"
    GENIE_AI_SEARCH_INPUT = "//textarea[@placeholder='Type Here']"
    SEND_ICON_ARROW = "//img[@class='wf_image send-icon-arrow no-js-arrow-right-white']"
    SEND_MSG_ICON = "//img[@class='wf_image send-msg-icon no-js-arrow-right-white']"
    SPEAKER_SECTION = "(//div[@class='speaker-section'])[1]"
    GENIE_RATING_BUTTON = "(//button[@class='genie-rating-btn'])[1]"
    # INTERVIEW_COACH = "//span[text()='Interview Coach']"
    ASK_YOUR_QUESTIONS_HERE_TEXTAREA = "//textarea[@placeholder='Ask your questions here']"
    PREVIOUS_CHATS_HEADER = "//*[contains(@class,'genie-sidebar-heading')][normalize-space()='Previous Chats']"
    # The chat-history sidebar collapses once a conversation is open; the toggle
    # carries a stable aria-label in both states.
    GENIE_SIDEBAR_TOGGLE = ("//*[@role='button'][@aria-label='Open conversation history'"
                            " or @aria-label='Expand sidebar']")
    GENIE_CHAT_HISTORY_ITEM = "//*[contains(@class,'genie-chat-item')]"
    SUBPAGE_BACK_BUTTON = "//button[@class='subpage-back-header__back-btn']"
    # The separate "Courses" and "Programs" cards were merged by the app into a
    # single "Programs & Courses" card; both names point at it so the Courses
    # and Programs scenarios can stay independent.
    PROGRAMS_AND_COURSES_CARD = "//h6[text()='Programs & Courses']"
    COURSES_CARD = PROGRAMS_AND_COURSES_CARD
    PROGRAMS_CARD = PROGRAMS_AND_COURSES_CARD
    PERSONAL_PITCH_TRAINER = "//h6[text()='Personal Pitch Trainer']"
    INTERVIEW_COACH = "//h6[text()='Interview Coach']"
    FORUMS_CARD = "//h6[text()='Forums']"
    MY_CAREER_ADVISOR_CARD = "//h6[text()='My Career Advisor']"
    CARRER_BUDDY_CARD = "//h6[text()='Career Buddy']"
    JOBS_CONNECT_CARD = "//h6[text()='Jobs Connect']"
    MENU_HELP_ICON = "//img[@class='wf_image  no-js-MenuHelp']"
    NOTIFICATION_ICON = "//img[@class='notification_icon']"
    # Prod renders the profile avatar as a photo (img.pro_avatar__avatar inside
    # span.ant-avatar-icon); dev/empty accounts render initials (ant-avatar-string).
    PROFILE_ICON = "//img[contains(@class,'pro_avatar__avatar')] | //span[contains(@class,'ant-avatar-string')]"
    # The account menu trigger is a <button aria-label="Accounts menu">. It used
    # to be matched by an exact class on the <img> inside it, which broke as
    # soon as that class changed; the aria-label is the stable, semantic hook.
    HEADER_PROFILE_MENU_ICON = ("//button[@aria-label='Accounts menu']"
                                " | //button[contains(@class,'header_profile_menu_trigger')]")
    # Any entry of the open account dropdown - used to tell whether the menu is
    # already open, because clicking the trigger again would close it.
    ACCOUNT_MENU_ITEM = "//p[contains(@class,'header-user-dropdown__item-label')]"
    CALENDAR = "//p[text()='Calendar']"
    MESSAGES_AND_DISCUSSIONS = "//p[text()='Messages & Discussions']"
    LEARNING_PROGRESS = "//p[text()='Learning Progress']"
    SETTINGS = "//p[text()='Settings']"
    LOG_OUT = "//p[text()='Logout']"

