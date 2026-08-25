"""Locators for the Courses scenario.

The app merged the Courses and Programs screens into one, so the shared screen
selectors come from `ProgramsAndCoursesLocators`. This class stays separate so
the Courses scenario keeps its own vocabulary and can diverge again later.
"""

from locators.student_persona_locators.programs_and_courses_locators import (
    ProgramsAndCoursesLocators as Merged,
)


class CoursesLocators:
    HOME = "//div[text()='Home']"

    # --- merged list screen ------------------------------------------------
    COURSES_CARD = Merged.PROGRAMS_AND_COURSES_CARD
    VALIDATE_INPROGRESS_TAB = Merged.IN_PROGRESS_TAB
    VALIDATE_COMPLETED_TAB = Merged.COMPLETED_TAB
    ENROLLED_COURSE_CARD = Merged.ENROLLED_COURSE_CARD
    COMPLETED_COURSE_CARD = Merged.COMPLETED_COURSE_CARD
    COURSE_CARD_TITLE = Merged.COURSE_CARD_TITLE
    RESUME_COURSE_BUTTON = Merged.RESUME_COURSE_BUTTON
    SCORECARD_BUTTON = Merged.SCORECARD_BUTTON
    CERTIFICATE_BUTTON = Merged.CERTIFICATE_BUTTON
    BACK_BUTTON = Merged.BACK_BUTTON

    # --- course detail screen ---------------------------------------------
    COURSE_TITLE = Merged.COURSE_TITLE
    LESSON_ACCORDION = Merged.LESSON_ACCORDION
    CERTIFICATE_PROGRESS = Merged.CERTIFICATE_PROGRESS
    EARNED_MICRO_CERTIFICATES = Merged.EARNED_MICRO_CERTIFICATES
    ASSESSMENT_SCORE_VALUE = Merged.ASSESSMENT_SCORE_VALUE
    ASSESSMENT_SCORE_LABEL = Merged.ASSESSMENT_SCORE_LABEL

    # --- recommendation sections ------------------------------------------
    COURSES_RECOMMENDED_BY_INSTITUTE = Merged.RECOMMENDED_BY_INSTITUTE
    COURSES_OFFERED_BY_WADHWANI_FOUNDATION = Merged.RECOMMENDED_BY_WADHWANI
    VALIDATE_RECOMMENDED_COURSE_CARD = Merged.RECOMMENDED_CARD
