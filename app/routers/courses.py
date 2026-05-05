from fastapi import APIRouter
from app.services.course_service import get_all_courses

router = APIRouter()


@router.get("")
def get_courses():
    return get_all_courses()