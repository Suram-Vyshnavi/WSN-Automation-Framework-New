import sys
from . import faculty_locators

# Python imports are case-sensitive even on Windows.
# All existing page files import from 'locators.Faculty_locators' (capital F),
# but the directory on disk is 'faculty_locators' (lowercase).
# This alias makes both names resolve to the same package.
sys.modules[__name__ + '.Faculty_locators'] = faculty_locators
