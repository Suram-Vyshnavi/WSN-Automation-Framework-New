from pages.base_page import BasePage
from locators.Faculty_locators.Batch_details_scorecard_locators import BatchDetailsScorecardLocators
from utils.helpers import highlight_element


class BatchDetailsScorecardPage(BasePage):

	def _show_element(self, locator, duration=1200):
		try:
			locator.scroll_into_view_if_needed()
		except Exception:
			pass
		try:
			highlight_element(self.page, locator, duration=duration)
		except Exception:
			pass

	def _first_visible(self, selectors, timeout=5000):
		for selector in selectors:
			locator = self.page.locator(selector).first
			try:
				locator.wait_for(state="visible", timeout=timeout)
				self._show_element(locator, duration=500)
				return locator
			except Exception:
				continue
		return None

	def _click_first_visible(self, selectors, timeout=5000):
		locator = self._first_visible(selectors, timeout=timeout)
		if not locator:
			return False
		try:
			locator.click(timeout=timeout)
		except Exception:
			locator.click(timeout=timeout, force=True)
		return True

	def _scroll_assessment_container_fully(self, container):
		try:
			container.scroll_into_view_if_needed()
		except Exception:
			pass

		try:
			self.page.wait_for_timeout(80)
			self.page.evaluate("""
				(el) => {
					el.scrollIntoView({ behavior: 'instant', block: 'center', inline: 'nearest' });
					if (el.scrollHeight > el.clientHeight) {
						el.scrollTop = el.scrollHeight;
						el.dispatchEvent(new Event('scroll', { bubbles: true }));
						el.scrollTop = 0;
						el.dispatchEvent(new Event('scroll', { bubbles: true }));
					}
				}
			""", container)
			self.page.wait_for_timeout(80)
		except Exception:
			pass

	def validate_scorecard_tab_and_click(self):
		scorecard_tab = self._first_visible([
			BatchDetailsScorecardLocators.SCORECARD_TAB,
			"//p[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SCORECARD')]",
			"//*[contains(@class,'tab') and contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SCORECARD')]",
		], timeout=10000)
		assert scorecard_tab, "Scorecard tab is not visible"

		clicked = self._click_first_visible([
			BatchDetailsScorecardLocators.SCORECARD_TAB,
			"//p[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SCORECARD')]",
		], timeout=8000)
		assert clicked, "Scorecard tab is not clickable"

		try:
			self.page.wait_for_load_state("networkidle", timeout=5000)
		except Exception:
			pass
		try:
			self.page.wait_for_timeout(120)
		except Exception:
			pass

	def validate_assessment_schedule_title_and_container(self):
		title = self._first_visible([
			BatchDetailsScorecardLocators.ASSESSMENT_SCHEDULE_TITLE,
			"//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ASSESSMENT SCHEDULE')]",
		], timeout=15000)
		assert title, "Assessment Schedule title is not visible"

		container = self._first_visible([
			BatchDetailsScorecardLocators.COURSE_ASSESSMENTS_CONTAINER,
			"//div[contains(@class,'course-assessments-container')]",
		], timeout=15000)
		assert container, "Assessment Schedule container is not visible"
		self._scroll_assessment_container_fully(container)
		self._show_element(container, duration=700)
