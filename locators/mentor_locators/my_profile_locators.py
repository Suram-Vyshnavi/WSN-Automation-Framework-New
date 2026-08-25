class MyProfileLocators:
    HOME = "//div[text()='Home']"
    # ant-avatar-string = initials-only avatar; ant-avatar-icon = photo/icon avatar
    PROFILE_ICON = "(//span[contains(@class,'ant-avatar-string') or contains(@class,'ant-avatar-icon')])[1]"
    VALIDATE_PROFILE_INFORMATION_HEADER = "//h4[text()='Profile information']"
    FIRSTNAME = "//input[@id='firstName']"
    LASTNAME = "//input[@id='lastName']"
    SELECT_CITY_INPUT = "//label[text()='Search City']//parent::div//div[@class='ant-select-selection-search']"
    #enters input Hyderabad or Bengaluru accordingly
    HYDERABAD_OPTION = "//span[text()='Hyderabad, Hyderabad, Telangana, India']"
    BENGALURU_OPTION = "//span[text()='Bengaluru, Bengaluru, Karnataka, India']"
    LANGUAGE_DROPDOWN_ENGLISH = "//div[@id='Platform Language-search-input']"
    LANGUAGE_DROPDOWN_SPANISH = "//div[@id='Idioma de la plataforma-search-input']"
    SPANISH_LANGUAGE = "//span[text()='Spanish']"
    SAVE_BUTTON = "//button[text()='Save']"
    GUARDAR_BUTTON = "//button[text()='Guardar']"

