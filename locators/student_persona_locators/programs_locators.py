"""Locators for the Programs scenario.

The app merged the Courses and Programs screens into one, so the shared screen
selectors come from `ProgramsAndCoursesLocators`. This class stays separate so
the Programs scenario keeps its own vocabulary and can diverge again later.
"""

from locators.student_persona_locators.programs_and_courses_locators import (
    ProgramsAndCoursesLocators as Merged,
)


class ProgramsLocators:
    HOME = "//div[text()='Home']"

    # --- merged list screen ------------------------------------------------
    PROGRAMS_CARD = Merged.PROGRAMS_AND_COURSES_CARD
    VALIDATE_INPROGRESS_TAB = Merged.IN_PROGRESS_TAB
    VALIDATE_COMPLETED_TAB = Merged.COMPLETED_TAB
    BACK_BUTTON = Merged.BACK_BUTTON

    # --- programs shown on the merged screen -------------------------------
    PROGRAM_CARD = Merged.PROGRAM_CARD
    RECOMMENDED_PROGRAM_CARD = ("//div[contains(@class,'learning-item-card--program')]"
                                "[contains(@class,'learning-item-card--recommended')]")

    # --- recommendation sections ------------------------------------------
    VALIDATE_RECOMMENDED_BY_INSTITUTE = Merged.RECOMMENDED_BY_INSTITUTE
    VALIDATE_OFFERED_BY_WADHWANI_FOUNDATION = Merged.RECOMMENDED_BY_WADHWANI
    RECOMMENDED_SECTION = Merged.RECOMMENDED_SECTION
    JOIN_A_BATCH = Merged.JOIN_A_BATCH
