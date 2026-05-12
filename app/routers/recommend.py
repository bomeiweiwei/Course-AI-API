from fastapi import APIRouter
from app.schemas.recommend import RecommendRequest
from app.services.recommend_service import recommend_courses, export_recommend_csv

router = APIRouter()


@router.post("")
def recommend(request: RecommendRequest):
    return recommend_courses(request)

@router.post("/exportcsv")
def export_csv(request: RecommendRequest):
    courses = recommend_courses(request)
    return export_recommend_csv(courses)