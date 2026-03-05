class SettingsDeleteAccountLocators:
    DELETE_ACCOUNT="(//div[@class='delete-account-menu-item'])[1]"
    DELETE_ACCOUNT_ARROW="(//div[contains(@class,'delete-account-menu-item')]//img[@alt='right_arrow'])[1]"
    DELETE_ACCOUNT_POPUP="(//div[@class='login-card-details-section'])[1]"
    DELETE_ACCOUNT_CLOSEICON="(//img[@class='wf_image unified-card-arrow no-js-svg%3e'])"
    DELETE_ACCOUNT_GETOTP="//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'OTP') or .//span[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'OTP')]]"
    DELETE_ACCOUNT_OTP_INPUT="//input[contains(translate(@id,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'OTP') or contains(translate(@name,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'OTP') or contains(translate(@placeholder,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'OTP')]"
    DELETE_ACCOUNT_BACKARROW="(//img[@alt='arrow'])[1]"