import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
OPTIONS_PATH = BASE_DIR / "data" / "options.json"

_options_cache = None


def load_options() -> dict:
    global _options_cache

    if _options_cache is None:
        with open(OPTIONS_PATH, "r", encoding="utf-8") as f:
            _options_cache = json.load(f)

    return _options_cache


def get_all_options() -> dict:
    return load_options()


def get_school_options() -> list[dict]:
    data = load_options()
    return data["school_options"]


def get_grade_options(school_id: int | None = None) -> list[dict]:
    data = load_options()
    options = data["grade_options"]

    if school_id is None:
        return options

    return [
        item for item in options
        if item["parent_id"] == school_id
    ]


def get_subject_options(grade_id: int | None = None) -> list[dict]:
    data = load_options()
    options = data["subject_options"]

    if grade_id is None:
        return options

    return [
        item for item in options
        if item["parent_id"] == grade_id
    ]


def get_version_options(subject_id: int | None = None) -> list[dict]:
    data = load_options()
    options = data["version_options"]

    if subject_id is None:
        return options

    return [
        item for item in options
        if item["parent_id"] == subject_id
    ]


def get_degree_options() -> list[dict]:
    data = load_options()
    return data["degree_options"]


def get_goal_options() -> list[dict]:
    data = load_options()
    return data["goal_options"]


def get_preferences_options() -> list[dict]:
    data = load_options()
    return data["preferences_options"]