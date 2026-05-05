from fastapi import APIRouter
from app.schemas.recommend import RecommendRequest
from app.services.recommend_service import recommend_courses

router = APIRouter()


@router.post("")
def recommend(request: RecommendRequest):
    return recommend_courses(request)