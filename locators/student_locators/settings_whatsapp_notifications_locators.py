from locators.xpath import UPPER
class SettingsWhatsappNotificationsLocators:
    NOTIFICATIONS_MENU=f"//div[contains(@class,'userSettings_menuItem') and contains({UPPER}, 'NOTIFICATIONS')]"
    WHATSAPP_CONTAINER=f"//div[contains(@class,'section-container') and contains({UPPER}, 'WHATSAPP')]"
    WHATSAPP_CONTAINER_RIGHTARROW="(//img[@alt='right_arrow'])[1]"
    WHATSAPP_SECTION="(//div[@class='detail_container'])"
    WHATSAPP_TOGGLEBUTTON="(//span[@class='ant-switch-handle'])[1]"
    WHATSAPP_SECTION_BACKBUTTON="(//img[@class='wf_image left_icon no-js-arrow-left-dark'])"
