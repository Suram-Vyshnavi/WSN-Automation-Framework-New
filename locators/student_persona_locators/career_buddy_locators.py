class CareerBuddyLocators:
    HOME = "//div[text()='Home']"
    CAREER_BUDDY_CARD = "//h6[text()='Career Buddy']"
    SEARCH_MENTORS_INPUT = "//input[@placeholder='Search Mentors']"
    # Prod mentor cards use photo avatars (span.ant-avatar mentor-image-avatar);
    # dev/empty accounts use initials (ant-avatar-string).
    MENTOR_CARD = "//div[@class='mentor-profile-list-card-item']"
    # The card body is not clickable and the button is a sibling of the card,
    # not a child - so it is matched at page level on the filtered listing.
    VIEW_PROFILE_BUTTON = "//button[normalize-space()='View Profile']"
    MENTOR_NAME = "//div[@class='mentor-profile-list-card-item']//h2[contains(@class,'name-text')]"
    _PROFILE_SECTION_TITLE = "//h2[contains(@class,'mentor-profile-section-title')]"
    VALIDATE_SECTORS_HEADER = f"{_PROFILE_SECTION_TITLE}[normalize-space()='Sectors']"
    VALIDATE_JOB_ROLES_HEADER = f"{_PROFILE_SECTION_TITLE}[normalize-space()='Job Roles']"
    VALIDATE_LANGUAGE_HEADER = f"{_PROFILE_SECTION_TITLE}[normalize-space()='Language']"
    # Applying a filter adds a selected-count badge to its button, so match on
    # the label prefix rather than the exact text.
    LANGUAGE_BUTTON = ("//button[contains(@class,'mentor_multi_select-btn')]"
                       "[starts-with(normalize-space(),'Language')]")
    LANGUAGE_OPTION_ENGLISH = "//p[text()='English']"
    # Shared by the Language / Sector / Location / Job Role filter popups.
    APPLY_BUTTON = "//button[text()='Apply']"
    # All four filters open the same Ant modal. It used to be dismissed with
    # positional selectors ((//*[name()='svg'])[1..4]), which broke as soon as
    # the page's icon order changed - the modal itself is the stable hook.
    FILTER_MODAL = "//div[contains(@class,'mentor_multi_select__modal')]"
    FILTER_MODAL_CLOSE = ("//div[contains(@class,'mentor_multi_select__modal')]"
                          "//button[contains(@class,'ant-modal-close')]")
    SECTOR_BUTTON = ("//button[contains(@class,'mentor_multi_select-btn')]"
                     "[starts-with(normalize-space(),'Sector')]")
    SECTOR_OPTION_HEALTHCARE = "//p[text()='Healthcare']"
    LOCATION_BUTTON = ("//button[contains(@class,'mentor_multi_select-btn')]"
                       "[starts-with(normalize-space(),'Location')]")
    LOCATION_OPTION_BENGALURU = "//p[contains(text(),'Bengaluru')]|//p[contains(text(),'bengaluru')]|//li[contains(text(),'Bengaluru')]|//span[contains(text(),'Bengaluru')]|//div[contains(text(),'Bengaluru')]|//a[contains(text(),'Bengaluru')]"
    JOBROLE_BUTTON = ("//button[contains(@class,'job_role-btn')]"
                      "[starts-with(normalize-space(),'Job Role')]")
    JOBROLE_OPTION_SALES_ASSOCIATE = "//p[text()='Sales Associate']"
    # On the mentor profile the button reads "Book a session" (lowercase s) and
    # carries its own class - matching on the class avoids the casing trap.
    BOOK_SESSION_BUTTON = "//button[contains(@class,'mentor-profile-book-btn')]"
    AVAILABLE_SELECT_DATE = "//div[contains(@style,'cursor: pointer')]"
    SLOT_BUTTON = "//button[@class='ant-btn ant-btn-default slot']"
    SESSION_PURPOSE_LABEL = "//label[text()='What is the purpose of this session for you?*']"
    # Ant Design hides the real control behind a styled wrapper, so the session
    # purpose is opened through its container and the outcome box by its id.
    SESSION_PURPOSE_SELECT = ("//label[contains(text(),'purpose of this session')]"
                              "/following::div[contains(@class,'ant-select')][1]")
    JOB_SEARCH_STRATEGY_OPTION = "//div[contains(@class,'ant-select-item-option-content') and contains(.,'Job Search Strategy')]"
    SPECIFIC_OUTCOME_LABEL = "//label[text()='What specific outcome do you want from this session?*']"
    SPECIFIC_OUTCOME_TEXTAREA = "//textarea[@id='Outcome']"
    CHECKBOX_OPTION = "//span[@class='ant-checkbox-inner']"
    BOOK_BUTTON = "//button[text()='Book']"
    COPY_LINK_OPTION = "//span[text()='Copy Link']"

