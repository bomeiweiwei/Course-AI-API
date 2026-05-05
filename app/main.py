from fastapi import FastAPI
from app.core.config import get_settings
from app.routers import courses, recommend, ai

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0"
)

app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(recommend.router, prefix="/api/recommend", tags=["Recommend"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])


@app.get("/")
def root():
    return {
        "message": "Course AI API is running"
    }