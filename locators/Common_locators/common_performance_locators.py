class CommonPerformanceLocators:
    PERFORMANCE_MENU="(//div[@id='Performance'])[1]"
    VALIDATE_COURSE_PROGRAM_LABEL="//div[text()='Course / Program']"
    SELECT_COURSE_INPUT_FIELD="(//div[@class='ant-select-selection-overflow'])[1]"
    FIRST_COURSE_IN_DROPDOWN="//span[text()=' QA-Emp skill Test-V2-1.0.0']"
    VALIDATE_RISK_CATEGORY_LABEL="//div[text()='Risk Category']"
    SELECT_STATUS_INPUT_FIELD="(//div[@class='ant-select-selection-overflow'])[2]"
    FIRST_STATUS_IN_DROPDOWN="//span[text()='Critical']"
    VALIDATE_BATCH_STATUS_LABEL="//div[text()='Batch Status']"
    # Batch Status is a set of pill buttons (All / Active / Inactive), not a dropdown.
    SELECT_BATCH_INPUT_FIELD="//div[contains(@class,'status-field')]//div[contains(@class,'status-pills')]"
    BATCH_STATUS ="//button[contains(@class,'status-pill') and normalize-space()='Active']"
    CLEAR_BUTTON ="//button[contains(@class,'status-pill-clear') and normalize-space()='Clear']"
    BATCH_DETAILS_ROW_OPTION ="(//tr[@class='batch-row'])[1]"
    # Placeholder the dashboard renders when no batch matches the current filters
    # (e.g. the account has no performance data at all).
    NO_DATA_FOUND="//*[contains(translate(normalize-space(.),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'NO DATA FOUND')]"
    VALIDATE_CERTIFICATION_STATUS_LABEL="//div[text()='Certification Status']"
    VALIDATE_STUDENT_ACTIVITY_LABEL="//div[text()='Student Activity - Pitch Trainer']"
    # Target each plus icon by its row label - clicking one toggles it to a minus and
    # re-indexes positional locators, so positional [1]/[2]/[3] are unreliable here.
    PLUS_ICON_PREVIDEO="//tr[contains(.,'Pre-Video')]//img[contains(@class,'no-js-row-plus')]"
    PLUS_ICON_POSTVIDEO="//tr[contains(.,'Post-Video')]//img[contains(@class,'no-js-row-plus')]"
    VALIDATE_STUDENT_ACTIVITY_ASSESSMENTS_LABEL="//div[text()='Student Activity - Assessments']"
    QUIZ_PLUS_ICON="//tr[contains(.,'Quiz')]//img[contains(@class,'no-js-row-plus')]"
    BACK_TO_DASHBOARD_BUTTON="//button[text()='Back to Dashboard']"
    PAGINATION_BUTTON="//button[text()='1']"
    # The currently selected page is marked with the 'page-active' class.
    ACTIVE_PAGE_BUTTON="//button[contains(@class,'page-active')]"
    NEXT_BUTTON="//button[contains(@class,'page-next')]"
    PER_PAGE_DROPDOWN="//select[@class='per-page-btn']"

# Backward compatibility for any existing imports.
CommonCreateMeetingLocators = CommonPerformanceLocators
    

