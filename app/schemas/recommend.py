from pydantic import BaseModel
from app.schemas.course import Course


class RecommendRequest(BaseModel):
    school_name: str
    grade_name: str
    subject_name: str
    version_name: str | None = None
    degree_name: str | None = None
    goal_name: str | None = None


class RecommendedCourse(Course):
    score: float
    reason: str