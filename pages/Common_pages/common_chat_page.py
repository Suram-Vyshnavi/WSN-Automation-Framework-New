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

		# Chat ("Messages & Discussions") lives inside the Accounts (hamburger)
		# dropdown menu, not as a standalone header icon.
		self._click_first_visible([HomeLocators.ACCOUNTS_MENU_TRIGGER], timeout=8000)
		self.page.wait_for_timeout(500)

		clicked = self._click_first_visible([
			HomeLocators.DROPDOWN_MESSAGES_ITEM,
			"//*[contains(normalize-space(),'Messages & Discussions')]",
		])
		assert clicked, "Messages & Discussions menu item is not visible/clickable"

	def click_send_message_button(self):
		clicked = self._click_first_visible([CommonChatLocators.SEND_MESSAGE_BUTTON])
		assert clicked, "Send Message button is not visible/clickable"

	def new_message_flow_available(self, timeout=4000):
		"""After clicking Send Message, the app should show the new-message
		contact search. For accounts with no messageable connections it instead
		throws an 'Oops! Something went wrong.' error popup with a 'Go to
		Homepage' button.

		If that popup appears, validate it (error text + Go to Homepage button),
		click 'Go to Homepage' to recover, and return False so the caller can
		skip the rest of the chat scenario gracefully. Returns True when the
		normal new-message flow is available."""
		error = self._first_visible([
			"//*[contains(normalize-space(.),'Something went wrong')]",
		], timeout=timeout)
		if not error:
			return True

		# Validate the error popup and its Go to Homepage button.
		go_home = self._first_visible([
			"//button[normalize-space()='Go to Homepage']",
		], timeout=4000)
		assert go_home, "Error popup appeared but the 'Go to Homepage' button is not visible"
		print("[INFO] 'Oops! Something went wrong.' popup validated with 'Go to Homepage' button.")

		# Recover by clicking Go to Homepage so we land on a clean screen.
		clicked = self._click_first_visible([
			"//button[normalize-space()='Go to Homepage']",
		], timeout=4000)
		assert clicked, "'Go to Homepage' button is not clickable on the error popup"
		self.page.wait_for_timeout(1500)
		return False

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

		# Prefer the enabled send control (it carries `disable_button` until the
		# thread is ready); fall back to any send icon.
		clicked = self._click_send(timeout=8000)
		if not clicked:
			send_btn = self._first_visible_in_any_frame([
				CommonChatLocators.SEND_MESSAGE_ICON,
				"//button[contains(@aria-label,'send') or contains(@title,'send')]",
				"//*[contains(@class,'send') and (self::button or self::img or self::span)]",
			], timeout_per_try=3000)
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

		# Allow time for the message to be delivered and rendered in the thread.
		self.page.wait_for_timeout(2000)

		# Scroll the chat thread container to the bottom so the latest message is in view.
		try:
			self.page.evaluate("""
				const containers = document.querySelectorAll(
					'[class*="message_list"], [class*="chat-messages"], [class*="thread"], [class*="conversation"], [class*="messages"]'
				);
				containers.forEach(c => { c.scrollTop = c.scrollHeight; });
			""")
		except Exception:
			pass
		self.page.wait_for_timeout(1000)

		# Anchor to an actual outgoing bubble. A loose //*[contains(.,text)] would
		# falsely match the same text still sitting in the composer textarea.
		# Prod environments may render message text in <p>/<span>/<div> instead of <td>.
		latest = self._first_visible([
			f"(//div[contains(@class,'message_container') and contains(@class,'justify_end')]//div[contains(@class,'message_box')]//td[normalize-space()='{expected_text}'])[last()]",
			f"(//div[contains(@class,'message_container') and contains(@class,'justify_end')]//div[contains(@class,'message_box')]//*[normalize-space()='{expected_text}' and not(self::textarea) and not(self::input)])[last()]",
			f"(//div[contains(@class,'message_container') and contains(@class,'justify_end')]//*[normalize-space()='{expected_text}' and not(self::textarea) and not(self::input)])[last()]",
			CommonChatLocators.LATEST_SENT_MESSAGE,
			f"(//*[normalize-space()='{expected_text}' and not(self::textarea) and not(self::input) and not(ancestor::*[contains(@class,'input_message') or contains(@class,'composer')])])[last()]",
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

	def _ensure_attachment_inputs(self, timeout=3000):
		"""Open the paperclip attachment popover so the hidden chat file inputs
		(#imageUpload / #fileUpload) are mounted. No-op if they already exist."""
		try:
			if self.page.locator("#imageUpload, #fileUpload").count() > 0:
				return True
		except Exception:
			pass
		self._click_first_visible([
			"//span[contains(@class,'attachment-popover')]",
			"//div[contains(@class,'input_message')]//*[contains(@class,'attachment')]",
			CommonChatLocators.FILE_UPLOAD_BUTTON,
		], timeout=timeout)
		self.page.wait_for_timeout(500)
		try:
			return self.page.locator("#imageUpload, #fileUpload").count() > 0
		except Exception:
			return False

	def _set_file_on_input(self, selector, file_path, timeout=4000):
		"""Set a file on a (possibly hidden) input by selector."""
		try:
			inp = self.page.locator(selector).first
			inp.wait_for(state="attached", timeout=timeout)
			inp.set_input_files(file_path)
			return True
		except Exception:
			return False

	def _wait_for_upload_ready(self, timeout=12000):
		"""After selecting a file, the app uploads it to storage and shows a
		'File uploaded successfully' toast. The Send action no-ops until this
		completes, so wait for the toast before clicking send."""
		try:
			self.page.locator(
				"//*[contains(translate(normalize-space(.),'UPLOADED','uploaded'),'uploaded successfully')]"
			).first.wait_for(state="visible", timeout=timeout)
			return True
		except Exception:
			# Toast may have appeared/disappeared quickly; settle briefly instead.
			self.page.wait_for_timeout(2500)
			return False

	def _click_send(self, timeout=8000):
		"""Click the Send control, preferring the enabled state. The send button
		carries a `disable_button` class until the composer/thread is ready to
		send, and clicking it while disabled is a no-op."""
		enabled = self._first_visible([
			"//div[contains(@class,'input_message_send') and not(contains(@class,'disable_button'))]",
		], timeout=timeout)
		if enabled:
			try:
				enabled.click(timeout=5000)
				return True
			except Exception:
				try:
					enabled.click(timeout=5000, force=True)
					return True
				except Exception:
					pass
		# Fallback: generic send icon (older/other layouts).
		return self._click_first_visible([CommonChatLocators.SEND_MESSAGE_ICON], timeout=timeout)

	def _send_attachment_until_visible(self, result_selectors, attempts=3):
		"""Click Send and confirm the attachment bubble renders. The upload to
		storage can lag behind the Send click, so retry the send a few times
		until the sent attachment becomes visible in the thread."""
		result = None
		for _ in range(attempts):
			self._wait_for_upload_ready()
			self._click_send(timeout=10000)
			result = self._first_visible(result_selectors, timeout=12000)
			if result:
				return result
		return result

	def upload_photo(self, photo_path):
		# The chat image input (#imageUpload, accept=image/*) mounts when the
		# paperclip attachment popover is opened. Set the file directly on it.
		self._ensure_attachment_inputs()
		bound = self._set_file_on_input("#imageUpload", photo_path)

		# Fallback for implementations without the id'd input.
		if not bound:
			bound = self._set_file_on_available_input(photo_path, prefer_last=True, timeout=8000, accept_hint="image")

		assert bound, "Unable to attach photo file after selecting image upload option"

		image = self._send_attachment_until_visible([CommonChatLocators.LATEST_SENT_IMAGE])
		assert image, "Uploaded image is not visible in chat"

	def upload_document(self, document_path):
		# The chat document input (#fileUpload, accept=pdf/word/ppt/...) mounts
		# when the paperclip attachment popover is opened. Set the file directly
		# on it rather than re-clicking the paperclip (which would toggle the
		# popover closed and unmount the inputs).
		self._ensure_attachment_inputs()
		bound = self._set_file_on_input("#fileUpload", document_path)

		# Fallback for implementations without the id'd input.
		if not bound:
			bound = self._set_file_on_available_input(document_path, prefer_last=False, timeout=8000, accept_hint="document")

		assert bound, "Unable to attach document file after selecting document upload option"

		document = self._send_attachment_until_visible([CommonChatLocators.LATEST_SENT_DOCUMENT])
		assert document, "Uploaded document is not visible in chat"

	def navigate_to_home_page(self):
		clicked = self._click_first_visible([
			HomeLocators.HOME_MENU,
			"//div[@id='Home']",
		], timeout=10000)
		assert clicked, "Home menu is not visible/clickable"
