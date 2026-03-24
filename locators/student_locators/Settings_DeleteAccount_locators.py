class SettingsDeleteAccountLocators:
    DELETE_ACCOUNT="(//div[@class='delete-account-menu-item'])[1]"
    DELETE_ACCOUNT_ARROW="(//div[contains(@class,'delete-account-menu-item')]//img[@alt='right_arrow'])[1]"
    DELETE_ACCOUNT_POPUP="(//div[@class='login-card-details-section'])[1]"
    DELETE_ACCOUNT_CLOSEICON="(//img[@alt='arrow'])"
    DELETE_ACCOUNT_GETOTP="//button[contains(normalize-space(), 'Get OTP')]"
    DELETE_ACCOUNT_OTP_INPUT="//input[contains(@placeholder,'Enter the OTP')]"
    DELETE_ACCOUNT_BACKARROW="(//img[@alt='arrow'])[1]"