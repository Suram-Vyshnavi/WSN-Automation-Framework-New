"""Single logging entry point for the whole framework.

Every page object, step definition and hook logs through `log` so that the
output format is identical everywhere and so that Behave/Allure capture the
same stream for the report.

Handlers write to stdout (not stderr) on purpose: Behave captures stdout per
step and embeds it in the Allure report, which is where testers read it.
"""

import logging
import os
import sys

LOGGER_NAME = "wsn"

_SENSITIVE_KEYS = ("password", "passwd", "otp", "secret", "token", "api_key", "apikey")
MASKED = "***"


def _build_logger():
    logger = logging.getLogger(LOGGER_NAME)
    if logger.handlers:
        return logger

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())
    logger.propagate = False
    return logger


log = _build_logger()


def mask(value):
    """Return a masked placeholder so credentials never reach the report."""
    return MASKED if value else MASKED


def is_sensitive(name):
    """True when a field name looks like it holds a credential."""
    lowered = (name or "").lower()
    return any(key in lowered for key in _SENSITIVE_KEYS)
