from pages.base_page import BasePage
from locators.Common_locators.common_chat_locators import CommonChatLocators
from locators.Faculty_locators.Home_locators import HomeLocators
from utils.config import Config


class CommonChatPage(BasePage):
	def _set_file_on_available_input(self, file_path, prefer_last=True, timeout=3000, accept_hint=None):
		"""Bind file to an available input[type='file'] if present."""
		selector_candidates = ["input[type='file']"]
		if accept_hint == "image":
			selector_candidates = [
				"input[type='file'][accept*='image']",
				"input[type='file'][accept*='.png']",
				"input[type='file'][accept*='.jpg']",
				"input[type='file'][accept*='.jpeg']",
				"input[type='file']",
			]
		elif accept_hint == "document":
			selector_candidates = [
				"input[type='file'][accept*='pdf']",
				"input[type='file'][accept*='.doc']",
				"input[type='file'][accept*='.docx']",
				"input[type='file'][accept*='file']",
				"input[type='file']",
			]

		frames = [self.page.main_frame] + [f for f in self.page.frames if f != self.page.main_frame]
		for frame in frames:
			for selector in selector_candidates:
				try:
					file_inputs = frame.locator(selector)
					file_inputs.first.wait_for(state="attached", timeout=timeout)
					if prefer_last:
						try:
							file_inputs.last.set_input_files(file_path)
						except Exception:
							file_inputs.first.set_input_files(file_path)
					else:
						try:
							file_inputs.first.set_input_files(file_path)
						except Exception:
							file_inputs.last.set_input_files(file_path)
					return True
				except Exception:
					continue

		for selector in selector_candidates:
			try:
				file_inputs = self.page.locator(selector)
				file_inputs.first.wait_for(state="attached", timeout=timeout)
				if prefer_last:
					try:
						file_inputs.last.set_input_files(file_path)
					except Exception:
						file_inputs.first.set_input_files(file_path)
				else:
					try:
						file_inputs.first.set_input_files(file_path)
					except Exception:
						file_inputs.last.set_input_files(file_path)
				return True
			except Exception:
				continue

		return False

	def _first_visible_in_any_frame(self, selectors, timeout_per_try=2500):
		frames = [self.page.main_frame] + [f for f in self.page.frames if f != self.page.main_frame]
		for frame in frames:
			for selector in selectors:
				locator = frame.locator(selector).first
				try:
					locator.wait_for(state="visible", timeout=timeout_per_try)
					return locator
				except Exception:
					continue
		return None

	def _first_visible(self, selectors, timeout=10000):
		for selector in selectors:
			locator = self.page.locator(selector).first
			try:
				locator.wait_for(state="visible", timeout=timeout)
				return locator
			except Exception:
				continue
		return None

	def _click_first_visible(self, selectors, timeout=10000):
		target = self._first_visible(selectors, timeout=timeout)
		if not target:
			return False
		try:
			target.scroll_into_view_if_needed()
		except Exception:
			pass
		try:
			target.click(timeout=timeout)
		except Exception:
			target.click(timeout=timeout, force=True)
		return True

	def _navigate_to_home(self):
		"""Navigate to home page from any screen."""
		try:
			self.page.locator(HomeLocators.HOME_MENU).first.wait_for(state="visible", timeout=3000)
			self.page.locator(HomeLocators.HOME_MENU).first.click(timeout=3000)
			self.page.wait_for_timeout(800)
		except Exception:
			pass

	def click_chat_icon(self):
		# Navigate to home first so the header icons are visible
		self._navigate_to_home()

		clicked = self._click_first_visible([
			HomeLocators.CHAT_MENU,
			"(//div[contains(@class,'chat_container')]//img)[3]",
			"//img[contains(@alt,'chat') or contains(@alt,'Chat')]",
		])
		assert clicked, "Chat icon is not visible/clickable"

	def click_send_message_button(self):
		clicked = self._click_first_visible([CommonChatLocators.SEND_MESSAGE_BUTTON])
		assert clicked, "Send Message button is not visible/clickable"

	def click_first_contact(self):
		clicked = self._click_first_visible([CommonChatLocators.FIRST_NEW_MESSAGE], timeout=15000)
		assert clicked, "First contact in list is not visible/clickable"

		# Wait for the thread to load after selecting contact
		self.page.wait_for_timeout(2000)

		# Ensure the thread is active; retry click once if composer area is still not present.
		composer_or_send = self._first_visible_in_any_frame([
			"//div[contains(@class,'input_message')]",
			"//img[@alt='send message']",
			"//textarea",
			"//*[@contenteditable='true']",
		], timeout_per_try=2000)
		if not composer_or_send:
			self._click_first_visible([CommonChatLocators.FIRST_NEW_MESSAGE], timeout=10000)

	def send_message(self, message_text=None):
		if message_text is None:
			message_text = Config.MESSAGE_TEXT

		composer_selectors = [
			"//div[contains(@class,'input_message')]//textarea",
			"//div[contains(@class,'input_message')]//*[@contenteditable='true']",
			"//div[contains(@class,'input_message')]//input[not(@type='file') and not(@placeholder='Search...')]",
			"//textarea[contains(@placeholder,'message') or contains(@placeholder,'Message')]",
			"//div[@contenteditable='true' and (@role='textbox' or contains(@class,'input') or contains(@class,'message'))]",
			"//input[contains(@placeholder,'message') and not(@placeholder='Search...')]",
			"//p[contains(@class,'placeholder') and contains(translate(.,'MESSAGE','message'),'message')]",
			"//*[@contenteditable='true']",
			"//textarea",
		]

		composer = self._first_visible_in_any_frame(composer_selectors, timeout_per_try=2500)
		if not composer:
			# One more attempt after re-selecting the first contact.
			self._click_first_visible([CommonChatLocators.FIRST_NEW_MESSAGE], timeout=10000)
			composer = self._first_visible_in_any_frame(composer_selectors, timeout_per_try=2500)
		assert composer, "Message composer is not visible"

		try:
			composer.fill(message_text)
		except Exception:
			try:
				composer.click(timeout=5000)
			except Exception:
				composer.click(timeout=5000, force=True)
			self.page.keyboard.type(message_text)

		send_btn = self._first_visible_in_any_frame([
			CommonChatLocators.SEND_MESSAGE_ICON,
			"//button[contains(@aria-label,'send') or contains(@title,'send')]",
			"//*[contains(@class,'send') and (self::button or self::img or self::span)]",
		], timeout_per_try=3000)
		clicked = False
		if send_btn:
			try:
				send_btn.click(timeout=7000)
				clicked = True
			except Exception:
				try:
					send_btn.click(timeout=7000, force=True)
					clicked = True
				except Exception:
					clicked = False
		assert clicked, "Send message icon is not visible/clickable"

	def validate_latest_message_sent(self, expected_text=None):
		if expected_text is None:
			expected_text = Config.MESSAGE_TEXT

		latest = self._first_visible([
			f"//*[contains(normalize-space(.), '{expected_text}') and not(self::script)]",
			CommonChatLocators.LATEST_SENT_MESSAGE,
		], timeout=15000)
		assert latest, f"Latest message '{expected_text}' is not visible"

	def click_file_upload_button(self):
		clicked = self._click_first_visible([
			"//span[contains(@class,'attachment-popover')]",
			"//div[contains(@class,'input_message')]//*[contains(@class,'attachment')]",
			"//div[contains(@class,'input_message')]//span[@tabindex='0']",
			CommonChatLocators.FILE_UPLOAD_BUTTON,
		], timeout=10000)
		assert clicked, "File upload button is not visible/clickable"

	def upload_photo(self, photo_path):
		# Try to use already opened menu (previous step may have opened it).
		image_option = self._first_visible_in_any_frame([
			CommonChatLocators.IMAGE_OPTION,
			"//*[contains(translate(normalize-space(.),'IMAGEPHOTOGALLERY','imagephotogallery'),'image')]",
			"//*[contains(translate(normalize-space(.),'IMAGEPHOTOGALLERY','imagephotogallery'),'photo')]",
			"//*[contains(translate(normalize-space(.),'IMAGEPHOTOGALLERY','imagephotogallery'),'gallery')]",
		], timeout_per_try=2500)

		# If menu is not open, open it and re-locate the Image option.
		if not image_option:
			self.click_file_upload_button()
			image_option = self._first_visible_in_any_frame([
				CommonChatLocators.IMAGE_OPTION,
				"//*[contains(translate(normalize-space(.),'IMAGEPHOTOGALLERY','imagephotogallery'),'image')]",
				"//*[contains(translate(normalize-space(.),'IMAGEPHOTOGALLERY','imagephotogallery'),'photo')]",
				"//*[contains(translate(normalize-space(.),'IMAGEPHOTOGALLERY','imagephotogallery'),'gallery')]",
			], timeout_per_try=3000)

		bound = False

		# Prefer direct chooser binding on the Image option click.
		if image_option:
			try:
				with self.page.expect_file_chooser(timeout=5000) as chooser_info:
					image_option.click(timeout=5000)
				chooser_info.value.set_files(photo_path)
				bound = True
			except Exception:
				try:
					image_option.click(timeout=5000, force=True)
				except Exception:
					pass
				bound = self._set_file_on_available_input(photo_path, prefer_last=True, timeout=8000, accept_hint="image")

		# Fallback for implementations with direct hidden file input.
		if not bound:
			bound = self._set_file_on_available_input(photo_path, prefer_last=True, timeout=6000, accept_hint="image")

		assert bound, "Unable to attach photo file after selecting image upload option"

		self._click_first_visible([CommonChatLocators.SEND_MESSAGE_ICON], timeout=10000)
		image = self._first_visible([CommonChatLocators.LATEST_SENT_IMAGE], timeout=30000)
		assert image, "Uploaded image is not visible in chat"

	def upload_document(self, document_path):
		# Try to use already opened menu (previous step may have opened it).
		doc_option = self._first_visible_in_any_frame([
			CommonChatLocators.DOCUMENT_OPTION,
			"//*[contains(translate(normalize-space(.),'DOCUMENTDOCFILE','documentdocfile'),'document')]",
			"//*[contains(translate(normalize-space(.),'DOCUMENTDOCFILE','documentdocfile'),'doc')]",
			"//*[contains(translate(normalize-space(.),'DOCUMENTDOCFILE','documentdocfile'),'file')]",
		], timeout_per_try=2500)

		# If menu is not open, open it and re-locate the Document option.
		if not doc_option:
			self.click_file_upload_button()
			doc_option = self._first_visible_in_any_frame([
				CommonChatLocators.DOCUMENT_OPTION,
				"//*[contains(translate(normalize-space(.),'DOCUMENTDOCFILE','documentdocfile'),'document')]",
				"//*[contains(translate(normalize-space(.),'DOCUMENTDOCFILE','documentdocfile'),'doc')]",
				"//*[contains(translate(normalize-space(.),'DOCUMENTDOCFILE','documentdocfile'),'file')]",
			], timeout_per_try=3000)

		bound = False

		# Prefer direct chooser binding on the Document option click.
		if doc_option:
			try:
				with self.page.expect_file_chooser(timeout=5000) as chooser_info:
					doc_option.click(timeout=5000)
				chooser_info.value.set_files(document_path)
				bound = True
			except Exception:
				try:
					doc_option.click(timeout=5000, force=True)
				except Exception:
					pass
				bound = self._set_file_on_available_input(document_path, prefer_last=False, timeout=8000, accept_hint="document")

		# Fallback for implementations with direct hidden file input.
		if not bound:
			bound = self._set_file_on_available_input(document_path, prefer_last=False, timeout=6000, accept_hint="document")

		assert bound, "Unable to attach document file after selecting document upload option"

		self._click_first_visible([CommonChatLocators.SEND_MESSAGE_ICON], timeout=10000)
		document = self._first_visible([CommonChatLocators.LATEST_SENT_DOCUMENT], timeout=30000)
		assert document, "Uploaded document is not visible in chat"

	def navigate_to_home_page(self):
		clicked = self._click_first_visible([
			HomeLocators.HOME_MENU,
			"//div[@id='Home']",
		], timeout=10000)
		assert clicked, "Home menu is not visible/clickable"
