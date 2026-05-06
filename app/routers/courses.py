from fastapi import APIRouter, Query
from app.services.course_service import get_all_courses, filter_courses
from typing import List

router = APIRouter()


@router.get("")
def get_courses():
    """
    取得全部課程（原始資料）
    """   
    return get_all_courses()

@router.get("/filter")
def get_filtered_courses(
    school_id: int = Query(...),
    grade_id: int = Query(...),
    subject_id: int = Query(...),
    version_id: int | None = Query(None),
    degree_id: int | None = Query(None),
    goal_id: int | None = Query(None),
    preference_ids: List[int] | None = Query(None), 
):
    """
    測試用：直接用 query string 做 filter
    """

    courses = get_all_courses()

    filtered = filter_courses(
        courses=courses,
        school_id=school_id,
        grade_id=grade_id,
        subject_id=subject_id,
        version_id=version_id,
        degree_id=degree_id,
        goal_id=goal_id,
        preference_ids=preference_ids,
    )

    return {
        "count": len(filtered),
        "data": filtered
    }