"""Small XPath building blocks shared by locators and page objects.

The application's labels differ in casing between environments, so many
selectors match text case-insensitively. XPath 1.0 has no `lower-case()`, which
is why the `translate()` dance below is needed - it lives here once instead of
being retyped in every fallback selector.

Usage:
    from locators.xpath import UPPER
    f"//button[contains({UPPER}, 'SAVE')]"
"""

LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#: Upper-cases an element's normalised text, for case-insensitive matching.
UPPER = f"translate(normalize-space(.), '{LOWERCASE}', '{UPPERCASE}')"

#: Upper-cases an attribute value, e.g. f"//input[contains({attr_upper('@placeholder')}, 'EMAIL')]".
def attr_upper(attribute):
    """Upper-case an attribute value for case-insensitive matching."""
    return f"translate({attribute}, '{LOWERCASE}', '{UPPERCASE}')"


def attr_lower(attribute):
    """Lower-case an attribute value for case-insensitive matching."""
    return f"translate({attribute}, '{UPPERCASE}', '{LOWERCASE}')"
