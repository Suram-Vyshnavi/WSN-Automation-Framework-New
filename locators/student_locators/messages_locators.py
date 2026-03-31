from utils.config import Config


class Messages_and_discussionsLocators:
    message="hello"
    SEND_MESSAGE_BUTTON="//button[text()='Send Message']"
    FIRST_NEW_MESSAGE="(//div[@class='search_result_container']//div)[position()=1]"
    MESSAGE_TEXTAREA="//div[contains(@class,'input_message')]//textarea | //div[contains(@class,'input_message')]//*[@contenteditable='true']"
    # send hello in the above textarea
    SEND_MESSAGE_ICON="//img[@alt='send message'] | //button[contains(@aria-label,'send')] | //button[contains(@title,'send')] | //span[contains(@class,'send')]"
    LATEST_SENT_MESSAGE=f"(//td[text()='{Config.MESSAGE_TEXT}'])[position()=1]"
    LATEST_SENT_IMAGE="(//div[contains(@class,'message_box') and contains(@class,'background_blue')]//img)[1]"
    LATEST_SENT_DOCUMENT="(//span[@class='anticon anticon-download chat-File-Icon'])[position()=1]"
    FILE_UPLOAD_BUTTON="//div[contains(@class,'input_message')]//span | //div[contains(@class,'input_message')]//button"
    IMAGE_OPTION="//*[normalize-space()='Image' or normalize-space()='Photo' or normalize-space()='Gallery']"
    DOCUMENT_OPTION="//*[normalize-space()='Document' or normalize-space()='File' or normalize-space()='Doc']"
