class JobsConnectLocators:
    HOME = "//div[text()='Home']"
    JOBS_CONNECT_CARD = "//h6[text()='Jobs Connect']"
    # Prod Jobs Connect page renders a search-filter-container (no "All Filters"
    # label); keep the old label as a dev fallback.
    VALIDATE_ALL_FILTERS = "//div[contains(@class,'search-filter-container')] | //div[text()='All Filters']"
    # The filters were rebuilt: there are no <a> options any more, the sections
    # are `filter-options-title` headers that expand to checkboxes, and the
    # labels are titlecased ("Full Time", not "Full time"). Options are scoped
    FILTER_SIDEBAR = "//div[contains(@class,'general-filter-sidebar')]"
    _FILTER_TITLE = "//*[contains(@class,'filter-options-title')]"

    JOB_TYPE_FILTER = f"{_FILTER_TITLE}[normalize-space()='Job Type']"
    FULL_TIME_OPTION = f"{FILTER_SIDEBAR}//*[normalize-space()='Full Time']"
    WORK_MODE_FILTER = f"{_FILTER_TITLE}[normalize-space()='Work Mode']"
    OFFICE_OPTION = f"{FILTER_SIDEBAR}//*[normalize-space()='Office']"
    INDUSTRY_SECTOR_FILTER = f"{_FILTER_TITLE}[normalize-space()='Industry/Sector']"
    AUTOMOTIVE_OPTION = f"{FILTER_SIDEBAR}//*[normalize-space()='Automotive']"
    EDUCATION_LEVEL_FILTER = f"{_FILTER_TITLE}[normalize-space()='Education Level']"
    GRADUATE_OPTION = f"{FILTER_SIDEBAR}//*[normalize-space()='Graduate']"
    SEARCH_BY_JOB_TITLE = "//input[@placeholder='Search by job title/roles']"
    # The app ships its own automation hooks on these controls - prefer them.
    FIND_JOBS_BUTTON = "//button[contains(@class,'find-jobs-btn')]"
    # # Prod autocomplete suggestion list that appears while typing in the search box.
    # SEARCH_AUTOCOMPLETE_OPTION = "//li[contains(@class,'jobsfield-option')]"
    FIRST_JOB_CARD = "(//div[@class='job-card-upper-wrapper'])[1]"
    VALIDATE_ABOUT_THE_JOB_BUTTON = "//button[contains(@class,'e2e-tab')][normalize-space()='About the job']"
    VALIDATE_ABOUT_THE_COMPANY_BUTTON = ("//button[contains(@class,'e2e-tab')]"
                                         "[normalize-space()='About the company']")
    VALIDATE_APPLY_BUTTON = "//button[contains(@class,'e2e-primary-btn')][normalize-space()='Apply']"
    RESET_BUTTON = "//button[contains(@class,'job-btn')][normalize-space()='Reset']"
    JOBS_CONNECT_APPLIED_STATUS = "//p[contains(text(), 'Applied')]"
    APPLIED_JOBS_BUTTON = ("//button[contains(@class,'e2e-secondary-btn')]"
                           "[normalize-space()='Applied Jobs']")
    APPLIED_JOB_CARD = "(//div[contains(@class,'job-card-upper-wrapper')])[1]"
    