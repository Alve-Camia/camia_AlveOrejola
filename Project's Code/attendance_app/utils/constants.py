# constants.py

DATE_FORMAT = "%m-%d-%Y"
TIME_FORMAT = "%H:%M"
DISPLAY_FORMAT = "%m-%d-%Y %H:%M"

AUTH_ERROR = "Authentication Error"

BUTTON_FONT_SIZE = ("Montserrat", 12)
ENTRY_FONT_SIZE = ("Montserrat", 12)
LABEL_FONT_SIZE = ("Arial", 12)
SPINBOX_FONT_SIZE = ("Montserrat", 12)

DEFAULT_STYLE = {
    "foreground": "#0f0f0f",
    "background": "#f0f0f0"
}

GRADE_7_SUBJECTS = sorted((
    "Integrated Science 1", "Computer Science 1", 
    "Mathematics 1", "ADTech 1",
    "English 1", "Filipino 1",
    "Social Science 1", "PEHM 1",
    "Values Education 1"
))

GRADE_8_SUBJECTS = sorted((
    "Biology 1", "Chemistry 1",
    "Physics 1", "Computer Science 2",
    "Mathematics 2", "Mathematics 3",
    "ADTech 2", "English 2",
    "Filipino 2", "Social Science 2",
    "PEHM 2", "Values Education 2", 
    "Earth Science 1"
))

GRADE_9_SUBJECTS = sorted((
    "Biology 2", "Chemistry 2",
    "Physics 2", "Computer Science 3",
    "Mathematics 4", "Statistics 1",
    "ADTech 3", "English 3",
    "Filipino 3", "Social Science 3", 
    "PEHM 3", "Values Education 3"
))

GRADE_10_SUBJECTS = sorted((
    "Biology 3", "Chemistry 3",
    "Physics 3", "Computer Science 4",
    "Mathematics 5", "Statistics 2",
    "English 4", "Filipino 4",
    "Social Science 4", "PEHM 4",
    "Values Education 4", "Elective"
))

GRADE_11_SUBJECTS = sorted((
    "Biology 4", "Chemistry 4",
    "Physics 4", "Mathematics 6",
    "English 5", "Filipino 5",
    "Social Science 5", "Research 1",
    "Elective"
))

GRADE_12_SUBJECTS = sorted((
    "Biology 5", "Chemistry 5",
    "Physics 5", "Mathematics 8",
    "Computer Science 5", "Engineering 1",
    "Engineering 2", "Agriculture 1", 
    "Geology 1", "Climate Science",
    "Mathematics 7", "English 6",
    "Filipino 6", "Social Science 6",
    "Research 2", "Elective"
))

GRADE_SUBJECTS = {
    7: GRADE_7_SUBJECTS,
    8: GRADE_8_SUBJECTS,
    9: GRADE_9_SUBJECTS,
    10: GRADE_10_SUBJECTS,
    11: GRADE_11_SUBJECTS,
    12: GRADE_12_SUBJECTS
}