import os


def _get_env(name, default):
    value = os.getenv(name)
    return value if value else default


class Config:
    BASE_URL = _get_env("BASE_URL", "https://dev.skilling.wadhwanifoundation.org/")
    USERNAME_INPUT = _get_env("USERNAME", "wadhwani.foundation99@yopmail.com")
    PASSWORD_INPUT = _get_env("PASSWORD", "Demo@123")
    MESSAGE_TEXT = _get_env("MESSAGE_TEXT", "hello")
