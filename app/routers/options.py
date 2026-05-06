from fastapi import APIRouter, Query
from app.services.option_service import (
    get_all_options,
    get_school_options,
    get_grade_options,
    get_subject_options,
    get_version_options,
    get_degree_options,
    get_goal_options,
    get_preferences_options,
)

router = APIRouter()


@router.get("")
def get_options():
    return get_all_options()


@router.get("/schools")
def get_schools():
    return get_school_options()


@router.get("/grades")
def get_grades(
    school_id: int | None = Query(None)
):
    return get_grade_options(school_id=school_id)


@router.get("/subjects")
def get_subjects(
    grade_id: int | None = Query(None)
):
    return get_subject_options(grade_id=grade_id)


@router.get("/versions")
def get_versions(
    subject_id: int | None = Query(None)
):
    return get_version_options(subject_id=subject_id)


@router.get("/degrees")
def get_degrees():
    return get_degree_options()


@router.get("/goals")
def get_goals():
    return get_goal_options()


@router.get("/preferences")
def get_preferences():
    return get_preferences_options()