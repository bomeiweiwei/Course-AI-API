import json
from pathlib import Path
from typing import List

# 取得專案根目錄
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "courses.json"


def load_courses() -> list[dict]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["COURSES"]


def get_all_courses():
    return load_courses()


def filter_courses(
    courses: list[dict],
    school_id: int,
    grade_id: int,
    subject_id: int,
    version_id: int | None = None,
    degree_id: int | None = None,
    goal_id: int | None = None,
    preference_ids: list[int] | None = None,
):
    results = []

    for course in courses:

        if course["school_id"] != school_id:
            continue

        if course["grade_id"] != grade_id:
            continue

        if course["subject_id"] != subject_id:
            continue

        if version_id is not None and course["version_id"] != version_id:
            continue

        if degree_id is not None and course["degree_id"] != degree_id:
            continue

        if goal_id is not None and course["goal_id"] != goal_id:
            continue

        if preference_ids is not None:
            if not any(pid in course["preferences"] for pid in preference_ids):
                continue

        results.append(course)

    return results