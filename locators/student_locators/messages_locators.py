from utils.config import Config


class Messages_and_discussionsLocators:
    message="hello"
    SEND_MESSAGE_BUTTON="//span[text()='Send Message']"
    FIRST_NEW_MESSAGE="//div[@class='search_result_container']/div[position()=1]"
    MESSAGE_TEXTAREA="//textarea[@placeholder='Type a message']"
    # send hello in the above textarea
    SEND_MESSAGE_ICON="//img[@alt='send message']"
    LATEST_SENT_MESSAGE=f"(//td[text()='{Config.MESSAGE_TEXT}'])[position()=1]"
    LATEST_SENT_IMAGE="(//div[contains(@class,'message_box') and contains(@class,'background_blue')]//img)[1]"
    LATEST_SENT_DOCUMENT="(//span[@class='anticon anticon-download chat-File-Icon'])[position()=1]"
    FILE_UPLOAD_BUTTON="//div[@class='input_message']//span"
    IMAGE_OPTION="//div[text()='Image']"
    DOCUMENT_OPTION="//div[text()='Document']"
