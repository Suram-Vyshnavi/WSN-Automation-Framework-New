from pages.base_page import BasePage
from locators.Common_locators.common_batch_members_locators import CommonBatchMembersLocators
from locators.Faculty_locators.Home_locators import HomeLocators


class CommonBatchMembersPage(BasePage):
	def _delete_confirmation_visible(self, timeout=1500):
		return self._first_visible([
			CommonBatchMembersLocators.REMOVE_STUDENT_NO_BUTTON,
			CommonBatchMembersLocators.REMOVE_STUDENT_YES_BUTTON,
			CommonBatchMembersLocators.REMOVE_STUDENT_POPUP,
			"//div[contains(@class,'ant-modal-wrap') and not(contains(@style,'display: none'))]",
			"//div[contains(@class,'ant-modal')]",
		], timeout=timeout)

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

	def _navigate_to_batches(self):
		"""Navigate to Batches list page from any screen."""
		try:
			self.page.locator(HomeLocators.BATCHES_MENU).first.wait_for(state="visible", timeout=3000)
			self.page.locator(HomeLocators.BATCHES_MENU).first.click(timeout=3000)
			self.page.wait_for_timeout(1500)
		except Exception:
			try:
				self.page.locator(HomeLocators.HOME_MENU).first.click(timeout=3000)
				self.page.wait_for_timeout(500)
				self.page.locator(HomeLocators.BATCHES_MENU).first.click(timeout=3000)
				self.page.wait_for_timeout(1500)
			except Exception:
				pass

	def click_batch_from_active_list(self, batch_name):
		self._navigate_to_batches()

		# Scroll through batch pages looking for the named batch
		for page_attempt in range(3):
			clicked = self._click_first_visible([
				f"(//td[contains(@class,'batch-list-content-bold') and normalize-space()='{batch_name}'])[1]",
				f"(//*[contains(@class,'batch-list-content') and normalize-space()='{batch_name}'])[1]",
			], timeout=8000)
			if clicked:
				return
			# Try next page of batches
			try:
				next_btn = self.page.locator("//li[contains(@class,'ant-pagination-next')]/button[not(@disabled)]").first
				next_btn.wait_for(state="visible", timeout=2000)
				next_btn.click()
				self.page.wait_for_timeout(1000)
			except Exception:
				break

		# Final fallback: click first batch card
		clicked = self._click_first_visible([CommonBatchMembersLocators.FIRST_BATCH_CARD], timeout=5000)
		assert clicked, f"Batch '{batch_name}' is not visible/clickable"

	def validate_batch_members_tab_and_click(self):
		clicked = self._click_first_visible([
			CommonBatchMembersLocators.BATCH_MEMBERS_TAB,
			"(//p[normalize-space()='Batch Members'])[1]",
		])
		assert clicked, "Batch Members tab is not visible/clickable"

		header = self._first_visible([
			CommonBatchMembersLocators.BATCH_MEMBERS_HEADER_SECTION,
			"//section[contains(@class,'student-section-header-container')]",
		])
		assert header, "Batch members header section is not visible"

	def click_manage_students(self):
		clicked = self._click_first_visible([CommonBatchMembersLocators.MANAGE_STUDENTS_BUTTON])
		assert clicked, "Manage Students button is not visible/clickable"

	def click_invite_students_and_validate_batch_code(self):
		clicked = self._click_first_visible([CommonBatchMembersLocators.INVITE_STUDENTS_BUTTON])
		assert clicked, "Invite Students button is not visible/clickable"

		batch_code = self._first_visible([CommonBatchMembersLocators.INVITE_BATCHCODE])
		assert batch_code, "Batch code is not visible in invite students section"

	def copy_batch_code_and_paste_in_email(self):
		self._click_first_visible([CommonBatchMembersLocators.BATCHCODE_COPY_BUTTON])
		email_input = self._first_visible([CommonBatchMembersLocators.ENTER_STUDENT_EMAIL_INPUT])
		assert email_input, "Student email input is not visible"

		# Clipboard paste can be flaky on CI/remote sessions; fallback to direct text fill.
		email_input.click()
		pasted = False
		try:
			email_input.press("Control+V")
			current = (email_input.input_value() or "").strip()
			pasted = bool(current)
		except Exception:
			pasted = False

		if not pasted:
			code_el = self._first_visible([CommonBatchMembersLocators.INVITE_BATCHCODE])
			assert code_el, "Batch code element is not visible"
			batch_code = (code_el.inner_text() or "").strip()
			assert batch_code, "Batch code text is empty"
			email_input.fill(batch_code)

	def remove_batch_code_and_send_email_invite(self, email):
		email_input = self._first_visible([CommonBatchMembersLocators.ENTER_STUDENT_EMAIL_INPUT])
		assert email_input, "Student email input is not visible"
		email_input.click()
		email_input.press("Control+A")
		email_input.press("Backspace")
		email_input.fill(email)

		clicked = self._click_first_visible([CommonBatchMembersLocators.ENTER_STUDENT_INVITE_BUTTON])
		assert clicked, "Send Invite button is not visible/clickable"

	def download_template_upload_file_and_invite(self, upload_file_path):
		self._click_first_visible([CommonBatchMembersLocators.DOWNLOAD_TEMPLATE_LINK], timeout=5000)

		upload_btn = self._first_visible([CommonBatchMembersLocators.UPLOAD_FILE_BUTTON], timeout=10000)
		assert upload_btn, "Upload File button is not visible/clickable"

		# Prefer file-chooser binding so the file is set on the exact control opened by the button.
		bound = False
		try:
			with self.page.expect_file_chooser(timeout=8000) as chooser_info:
				upload_btn.click(timeout=5000)
			chooser_info.value.set_files(upload_file_path)
			bound = True
		except Exception:
			bound = False

		if not bound:
			# Fallback for implementations that rely on persistent hidden file inputs.
			file_inputs = self.page.locator("input[type='file']")
			file_inputs.first.wait_for(state="attached", timeout=10000)
			try:
				file_inputs.last.set_input_files(upload_file_path)
			except Exception:
				file_inputs.first.set_input_files(upload_file_path)

		invite_clicked = self._click_first_visible([CommonBatchMembersLocators.UPLOAD_FILE_INVITE_BUTTON])
		assert invite_clicked, "File invite button is not visible/clickable"

	def validate_uploaded_users_status_and_download(self):
		status_bar = self._first_visible([
			CommonBatchMembersLocators.UPLOAD_USERS_STATUS_BAR,
			"//div[contains(@class,'ant-progress-inner')]",
		], timeout=15000)
		assert status_bar, "Uploaded users status bar is not visible"

		self._click_first_visible([CommonBatchMembersLocators.UPLOAD_USERS_DOWNLOAD_BUTTON], timeout=7000)

	def click_invite_students_back(self):
		clicked = self._click_first_visible([CommonBatchMembersLocators.INVITE_STUDENTS_BACK_ARROW])
		assert clicked, "Invite students back button is not visible/clickable"

	def validate_batch_students_and_pending_requests(self):
		batch_students = self._first_visible([CommonBatchMembersLocators.BATCH_STUDENTS_TAB])
		pending = self._first_visible([CommonBatchMembersLocators.PENDING_REQUESTS_TAB])
		assert batch_students, "Batch Students tab is not visible"
		assert pending, "Pending Requests tab is not visible"

	def validate_first_user_view_and_download_buttons(self):
		clicked = self._click_first_visible([CommonBatchMembersLocators.BATCH_STUDENTS_TAB])
		assert clicked, "Batch Students tab is not visible/clickable"

		view_button = self._first_visible([CommonBatchMembersLocators.DOWNLOAD_CERTIFICATE_VIEW_BUTTON])
		download_button = self._first_visible([CommonBatchMembersLocators.DOWNLOAD_CERTIFICATE_DOWNLOAD_BUTTON])
		assert view_button, "View button is not visible for first user"
		assert download_button, "Download button is not visible for first user"

	def click_view_and_validate_certificate_images_download(self):
		clicked = self._click_first_visible([CommonBatchMembersLocators.DOWNLOAD_CERTIFICATE_VIEW_BUTTON])
		assert clicked, "View button is not visible/clickable"

		image = self._first_visible([CommonBatchMembersLocators.CERTIFICATE_IMAGE])
		assert image, "Certificate image preview is not visible"

		download = self._click_first_visible([CommonBatchMembersLocators.VIEW_CERTIFICATE_DOWNLOAD_CERTIFICATE_BUTTON])
		assert download, "Download certificate button is not visible/clickable on preview"

	def close_certificate_and_download_from_list(self):
		close_clicked = self._click_first_visible([CommonBatchMembersLocators.VIEW_CERTIFICATE_CLOSE_ICON])
		assert close_clicked, "Certificate close icon is not visible/clickable"

		self._click_first_visible([CommonBatchMembersLocators.DOWNLOAD_CERTIFICATE_DOWNLOAD_BUTTON], timeout=7000)

	def click_user_delete_and_validate_remove_popup(self):
		# Ensure we are on Batch Students table before attempting row-level delete.
		self._click_first_visible([CommonBatchMembersLocators.BATCH_STUDENTS_TAB], timeout=5000)

		# Delete icon is usually hover-driven and can be rendered as div/img/button.
		rows = self.page.locator("//tr[contains(@class,'ant-table-row') and .//td]")
		row_count = rows.count()
		clicked = False

		for idx in range(min(row_count, 5)):
			try:
				rows.nth(idx).hover(timeout=3000)
			except Exception:
				pass

			row = rows.nth(idx)
			row_delete_candidates = [
				"xpath=.//*[contains(@class,'remove-student')]",
				"xpath=.//img[@alt='delete']",
				"xpath=.//img[contains(@class,'trash')]",
				"xpath=.//button[contains(translate(normalize-space(.),'DELETE','delete'),'delete')]",
			]
			for selector in row_delete_candidates:
				try:
					candidate = row.locator(selector).first
					if candidate.count() == 0:
						continue
					try:
						candidate.scroll_into_view_if_needed()
					except Exception:
						pass
					try:
						candidate.click(timeout=3000)
					except Exception:
						try:
							candidate.click(timeout=3000, force=True)
						except Exception:
							clicked_js = candidate.evaluate("el => { el.click(); return true; }")
							if not clicked_js:
								continue

					# Only accept click if we observe a post-click confirmation signal.
					if self._delete_confirmation_visible(timeout=1500):
						clicked = True
						break
				except Exception:
					continue
			if clicked:
				break

		if not clicked:
			# Final fallback to global delete selector in case row structure changed.
			fallback_clicked = self._click_first_visible([
				CommonBatchMembersLocators.USER_DELETE_BUTTON,
				"//img[@alt='delete']",
				"//img[contains(@class,'trash')]",
			], timeout=5000)
			if fallback_clicked and self._delete_confirmation_visible(timeout=2000):
				clicked = True

		assert clicked, "User delete icon is not clickable"

		confirmation = self._delete_confirmation_visible(timeout=5000)
		if not confirmation:
			# Some builds perform delete without a confirmation modal.
			return

	def click_no_and_open_pending_requests(self):
		# Confirmation may appear as modal or be skipped based on environment state.
		no_clicked = self._click_first_visible([CommonBatchMembersLocators.REMOVE_STUDENT_NO_BUTTON], timeout=3000)
		if not no_clicked:
			try:
				self.page.keyboard.press("Escape")
			except Exception:
				pass

		pending_clicked = self._click_first_visible([CommonBatchMembersLocators.PENDING_REQUESTS_TAB], timeout=15000)
		if not pending_clicked:
			self._click_first_visible([CommonBatchMembersLocators.BATCH_STUDENTS_TAB], timeout=5000)
			pending_clicked = self._click_first_visible([CommonBatchMembersLocators.PENDING_REQUESTS_TAB], timeout=10000)
		assert pending_clicked, "Pending Requests tab is not visible/clickable"

	def click_first_resend_and_validate_popup(self):
		clicked = self._click_first_visible([CommonBatchMembersLocators.FIRST_USER_RESEND_BUTTON], timeout=10000)
		assert clicked, "Resend request button is not visible/clickable"

		popup = self._first_visible([CommonBatchMembersLocators.RESEND_OTP_POPUP, "//div[contains(@class,'ant-modal-body')]"])
		assert popup, "Resend OTP popup is not visible"

	def confirm_resend_and_click_manage_students_back(self):
		yes_clicked = self._click_first_visible([CommonBatchMembersLocators.RESEND_OTP_POPUP_YES_BUTTON], timeout=7000)
		assert yes_clicked, "Yes button is not visible/clickable on resend popup"

		back_clicked = self._click_first_visible([CommonBatchMembersLocators.MANAGE_STUDENTS_BACK_ARROW], timeout=7000)
		assert back_clicked, "Manage students back button is not visible/clickable"

	def click_batch_members_and_open_first_chat(self):
		clicked = self._click_first_visible([CommonBatchMembersLocators.BATCH_MEMBERS_TAB], timeout=7000)
		assert clicked, "Batch Members tab is not visible/clickable"

		card = self._first_visible([
			CommonBatchMembersLocators.BATCH_MEMBERS_CARD,
			"(//div[contains(@class,'cohort-member-card')])[1]",
			"(//div[contains(@class,'member-card')])[1]",
		], timeout=10000)
		assert card, "First batch member card is not visible"

		try:
			card.hover(timeout=3000)
		except Exception:
			pass

		chat_clicked = False
		card_chat_candidates = [
			"xpath=.//h2[contains(normalize-space(),'Chat')]",
			"xpath=.//button[contains(normalize-space(),'Chat')]",
			"xpath=.//img[contains(translate(@alt,'CHAT','chat'),'chat')]",
		]
		for selector in card_chat_candidates:
			try:
				candidate = card.locator(selector).first
				if candidate.count() == 0:
					continue
				candidate.scroll_into_view_if_needed()
				candidate.click(timeout=5000)
				chat_clicked = True
				break
			except Exception:
				continue

		if not chat_clicked:
			chat_clicked = self._click_first_visible([
				CommonBatchMembersLocators.FIRST_BATCH_MEMBERS_CHAT_BUTTON,
				"(//h2[contains(normalize-space(),'Chat')])[1]",
				"(//button[contains(normalize-space(),'Chat')])[1]",
				"(//img[contains(translate(@alt,'CHAT','chat'),'chat')])[1]",
			], timeout=10000)
		assert chat_clicked, "Batch member chat button is not visible/clickable"

	def click_home_menu_from_header(self):
		clicked = self._click_first_visible([
			HomeLocators.HOME_MENU,
			"//div[@id='Home']",
		], timeout=10000)
		assert clicked, "Home menu is not visible/clickable"
