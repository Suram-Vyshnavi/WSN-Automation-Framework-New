from utils.config import Config

# Outgoing messages render as:
#   div.message_container.justify_end > div.message_box > span.message_text
#     > (TD for text | SECTION for an image/document)
# Anchoring to that wrapper keeps validation honest: it can never match the
# composer textarea (false text match) or a sidebar avatar (false image match).
_SENT_BUBBLE = ("//div[contains(@class,'message_container') and contains(@class,'justify_end')]"
                "//div[contains(@class,'message_box')]")


class CommonChatLocators:
    HOME = "//div[text()='Home']"
    # The account menu trigger is a <button aria-label="Accounts menu">. It used
    # to be matched by an exact class on the <img> inside it, which broke as
    # soon as that class changed; the aria-label is the stable, semantic hook.
    HEADER_PROFILE_MENU_ICON = ("//button[@aria-label='Accounts menu']"
                                " | //button[contains(@class,'header_profile_menu_trigger')]")

    SEND_MESSAGE_BUTTON = "//button[text()='Send Message']"
    FIRST_NEW_MESSAGE = "(//div[@class='search_result_container']//div)[position()=1]"
    MESSAGE_TEXTAREA = ("//div[contains(@class,'input_message')]//textarea"
                        " | //div[contains(@class,'input_message')]//*[@contenteditable='true']")
    SEND_MESSAGE_ICON = ("//img[@alt='send message'] | //button[contains(@aria-label,'send')]"
                         " | //button[contains(@title,'send')] | //span[contains(@class,'send')]")

    LATEST_SENT_MESSAGE = f"({_SENT_BUBBLE}//td[normalize-space()='{Config.MESSAGE_TEXT}'])[last()]"
    LATEST_SENT_IMAGE = f"({_SENT_BUBBLE}//section//img[contains(@class,'wf_image')])[last()]"
    LATEST_SENT_DOCUMENT = (
        f"({_SENT_BUBBLE}//section[.//*[contains(@class,'chat-File-Icon')]"
        f" or .//span[contains(normalize-space(.),'.pdf')]])[last()]")

    FILE_UPLOAD_BUTTON = ("//div[contains(@class,'input_message')]"
                          "//*[contains(@class,'attachment') or self::button or self::span[@tabindex='0']]")
    IMAGE_OPTION = (
        "//div[contains(@class,'ant-dropdown') and not(contains(@style,'display: none'))]"
        "//*[normalize-space()='Image' or normalize-space()='Photo' or normalize-space()='Gallery']"
        " | //*[normalize-space()='Image' or normalize-space()='Photo' or normalize-space()='Gallery']"
        "[not(ancestor::*[contains(@style,'display: none')])]")
    DOCUMENT_OPTION = (
        "//div[contains(@class,'ant-dropdown') and not(contains(@style,'display: none'))]"
        "//*[normalize-space()='Document' or normalize-space()='File' or normalize-space()='Doc']"
        " | //*[normalize-space()='Document' or normalize-space()='File' or normalize-space()='Doc']"
        "[not(ancestor::*[contains(@style,'display: none')])]")
