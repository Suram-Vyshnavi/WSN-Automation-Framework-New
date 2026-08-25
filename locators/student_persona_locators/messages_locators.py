from utils.config import Config


class MessagesAndDiscussionsLocators:
    ACCOUNTS_MENU="//img[@class='wf_image header_profile_menu_trigger__icon no-js-svg%3e']"
    CHAT_ICON = "//p[contains(text(),'Messages & Discussions')]"
    SEND_MESSAGE_BUTTON="//button[normalize-space()='Send Message']"
    FIRST_NEW_MESSAGE="(//div[@class='search_result_container']//div)[position()=1]"
    FIRST_CHAT_IN_LIST="(//div[contains(@class,'chat_list_overflow')]//div[contains(@class,'conversation_card_container')])[1]"
    MESSAGE_TEXTAREA="//div[contains(@class,'input_message')]//textarea | //div[contains(@class,'input_message')]//*[@contenteditable='true']"
    # send hello in the above textarea
    SEND_MESSAGE_ICON="//div[contains(@class,'input_message_send')]//img"
    LATEST_SENT_MESSAGE=f"(//td[text()='{Config.MESSAGE_TEXT}'])[position()=1]"
    LATEST_SENT_IMAGE="(//div[contains(@class,'message_box') and contains(@class,'background_blue')]//img)[1]"
    LATEST_SENT_DOCUMENT="(//span[@class='anticon anticon-download chat-File-Icon'])[position()=1]"
    FILE_UPLOAD_BUTTON="//span[contains(@class,'attachment-popover')]//*[name()='svg']"
    IMAGE_OPTION="//*[normalize-space()='Image' or normalize-space()='Photo' or normalize-space()='Gallery']"
    DOCUMENT_OPTION="//*[normalize-space()='Document' or normalize-space()='File' or normalize-space()='Doc']"
