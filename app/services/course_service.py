from app.data.fake_courses import COURSES


def get_all_courses():
    return COURSES


def filter_courses(
    school_name: str,
    grade_name: str,
    subject_name: str,
):
    return [
        course for course in COURSES
        if course["school_name"] == school_name
        and course["grade_name"] == grade_name
        and course["subject_name"] == subject_name
    ]