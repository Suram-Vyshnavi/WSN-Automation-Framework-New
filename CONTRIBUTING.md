# Framework conventions

Read this before adding a scenario, a page object or a locator. The point of
these rules is that any tester can open any file and find the same shapes.

## Layout

```
features/                 Gherkin feature files + Behave hooks
  environment.py          browser lifecycle, shared pre-login, per-scenario reset
  steps/
    _load_nested_steps.py bootstrap that imports every nested step module
    common_steps/         steps shared by all personas ("common user ...")
    faculty_steps/  rm_steps/  student_persona/
pages/                    page objects - one class per screen
  base_page.py            THE single implementation of every UI operation
  common_pages/  faculty_pages/  rm_pages/  student_persona/
locators/                 selectors only, one class per screen
  xpath.py                shared XPath building blocks
utils/                    logger, config, reporting helpers
config/                   env_config.py + config.yaml (no secrets)
files/                    test-data files used by upload steps
```

## Naming

| Thing | Convention | Example |
|---|---|---|
| Modules, packages, feature files | `snake_case` | `batch_details_page.py`, `faculty_all.feature` |
| Classes | `PascalCase` | `BatchDetailsPage`, `CoursesLocators` |
| Methods, functions, variables | `snake_case` | `click_view_details_button` |
| Locator constants, module constants | `UPPER_SNAKE_CASE` | `COURSES_CARD`, `CARD_TIMEOUT` |
| Page-object methods | `click_*` / `enter_*` / `select_*` / `validate_*` / `get_*` | `validate_my_forums_header` |

Indentation is 4 spaces everywhere.

## UI operations go through `BasePage`

Page objects must not call `self.page.locator(...)`, `self.page.click(...)` or
`self.page.wait_for_timeout(...)` for a normal interaction. Use the `BasePage`
API so waiting, highlighting, retrying and logging stay identical everywhere:

| Operation | Use |
|---|---|
| Click | `self.click(LOCATOR, "description")` |
| Click one of several | `self.click_first_visible([...], "description")` / `self.click_required(...)` |
| Enter text | `self.enter_text(LOCATOR, value, "description")` |
| Dropdown | `self.select_dropdown_option(...)` / `self.open_dropdown_and_select(...)` |
| Checkbox / radio | `self.set_checkbox(LOCATOR, checked=True)` |
| Read text | `self.get_text(LOCATOR)` / `self.get_value(LOCATOR)` |
| Wait | `self.wait_for_visible(...)`, `self.wait_for_load(...)`, `self.pause(ms)` |
| Scroll | `self.scroll_into_view(...)`, `self.scroll_to_bottom()`, `self.click_arrow_until_end(...)` |
| Navigate | `self.open_url(url)`, `self.reload()`, `self.go_back()` |
| Popups / tabs | `self.dismiss_if_present([...])`, `self.open_in_new_tab_and_close(...)`, `self.press_escape()`, `self.close_extra_tabs()` |
| Assertions | `self.validate_visible(...)`, `self.validate_any_visible(...)`, `self.validate_text(...)` |

Dropping to the raw Playwright API is acceptable only for genuinely special
cases (iframes, `filter(has_text=...)`, JS evaluation) - add a comment saying why.

`self.pause(ms)` is a deliberate fixed wait. Only use it when the app exposes
no observable end state (CSS animation, debounce). Prefer an explicit wait.

## Timeouts

Import them from `pages.base_page`: `DEFAULT_TIMEOUT` (10s), `SHORT_TIMEOUT`
(5s), `LONG_TIMEOUT` (20s), `NAVIGATION_TIMEOUT` (60s). Student-persona pages
also have `CARD_TIMEOUT` (15s). A page whose screen is consistently slower
overrides `DEFAULT_TIMEOUT` on the class rather than passing a literal
everywhere.

## Locators

* Live in `locators/`, never inline in a page object - except short generic
  fallbacks inside a `first_visible([...])` list.
* Prefer stable hooks: `id`, `data-testid`, `aria-label`, then text, then class.
* Avoid positional indexes: the helpers already resolve `.first`.
* For case-insensitive text use `from locators.xpath import UPPER`:
  `f"//button[contains({UPPER}, 'SAVE')]"`.

## Step definitions

Thin wrappers only: build the page object, call one or two methods, attach a
screenshot. No UI logic. Persona-dependent behaviour belongs in
`common_steps/common_home_steps.py`. Steps shared by faculty/RM are worded
`common user ...`; student-only steps are worded `user ...`.

## Logging

`from utils.logger import log` - `log.info` for actions, `log.warning` for a
graceful skip, `log.error` for a real problem, `log.debug` for best-effort
detail. Never `print()`. Never log a password, OTP or token - `BasePage`
provides `enter_text(..., sensitive=True)`.

## Configuration and secrets

Everything environment-specific comes from `config/env_config.py`, which reads
env vars / `.env` first and falls back to `config/config.yaml`. Credentials
only ever come from the environment - see `.env.example`. Nothing sensitive is
committed, and `.env` is git-ignored.

## Running

```bash
ENV=dev PERSONA=student python -m behave features/student.feature
./run-report.ps1 -Persona faculty          # single persona + Allure report
./run-combined-report.ps1                  # every persona x dev/prod
```
