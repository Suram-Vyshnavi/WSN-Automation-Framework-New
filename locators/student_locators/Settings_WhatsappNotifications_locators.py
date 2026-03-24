class SettingsWhatsappNotificationsLocators:
    NOTIFICATIONS_MENU="//div[contains(@class,'userSettings_menuItem') and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NOTIFICATIONS')]"
    WHATSAPP_CONTAINER="//div[contains(@class,'section-container') and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'WHATSAPP')]"
    WHATSAPP_CONTAINER_RIGHTARROW="(//img[@alt='right_arrow'])[1]"
    WHATSAPP_SECTION="(//div[@class='detail_container'])"
    WHATSAPP_TOGGLEBUTTON="(//span[@class='ant-switch-handle'])[1]"
    WHATSAPP_SECTION_BACKBUTTON="(//img[@class='wf_image left_icon no-js-arrow-left-dark'])"
