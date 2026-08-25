class AllBatchesLocators:
    ALL_BATCHES_TITLE = "(//h2[normalize-space()='All Batches'])[1]"
    SEARCHBAR = "(//input[@placeholder='Search Batch'])[1]"
    STATUS_TITLE = "//span[normalize-space()='Status']"
    STATUS_DROPDOWN = "//button[@class='ant-btn ant-btn-default dropdown-btn']"
    ACTIVE_OPTION_IN_DROPDOWN = "//div[contains(@class,'ant-dropdown')]//span[normalize-space(text())='Active']"
    INACTIVE_OPTION_IN_DROPDOWN = "//div[contains(@class,'ant-dropdown')]//span[normalize-space(text())='Inactive']"
    ALL_BATCHES_CONTAINER = "(//div[@class='site-content'])[1]"

    