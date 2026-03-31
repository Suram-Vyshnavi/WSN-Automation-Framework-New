from utils.config import Config


class CommonChatLocators:
    message="hello"
    SEND_MESSAGE_BUTTON="//button[text()='Send Message']"
    FIRST_NEW_MESSAGE="(//div[@class='search_result_container']//div)[position()=1]"
    MESSAGE_TEXTAREA="//div[contains(@class,'input_message')]//textarea | //div[contains(@class,'input_message')]//*[@contenteditable='true']"
    # send hello in the above textarea
    SEND_MESSAGE_ICON="//img[@alt='send message'] | //button[contains(@aria-label,'send')] | //button[contains(@title,'send')] | //span[contains(@class,'send')]"
    LATEST_SENT_MESSAGE=f"(//td[text()='{Config.MESSAGE_TEXT}'])[position()=1]"
    LATEST_SENT_IMAGE="(//div[contains(@class,'message') or contains(@class,'chat')]//img[not(contains(@class,'avatar')) and not(contains(@src,'profile'))])[last()]"
    LATEST_SENT_DOCUMENT="(//span[contains(@class,'download') and contains(@class,'chat-File-Icon')] | //a[contains(@href,'.pdf')] | //span[contains(normalize-space(.),'.pdf')])[last()]"
    FILE_UPLOAD_BUTTON="//div[contains(@class,'input_message')]//*[contains(@class,'attachment') or self::button or self::span[@tabindex='0']]"
    IMAGE_OPTION="//div[contains(@class,'ant-dropdown') and not(contains(@style,'display: none'))]//*[normalize-space()='Image' or normalize-space()='Photo' or normalize-space()='Gallery'] | //*[normalize-space()='Image' or normalize-space()='Photo' or normalize-space()='Gallery'][not(ancestor::*[contains(@style,'display: none')])]"
    DOCUMENT_OPTION="//div[contains(@class,'ant-dropdown') and not(contains(@style,'display: none'))]//*[normalize-space()='Document' or normalize-space()='File' or normalize-space()='Doc'] | //*[normalize-space()='Document' or normalize-space()='File' or normalize-space()='Doc'][not(ancestor::*[contains(@style,'display: none')])]"