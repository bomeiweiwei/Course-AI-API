from pydantic import BaseModel, Field
from app.schemas.course import Course


class RecommendRequest(BaseModel):
    school_id: int
    grade_id: int
    subject_id: int

    version_id: int | None = None
    degree_id: int | None = None
    goal_id: int | None = None
    budget: int
    limit: int = Field(default=3, ge=3, le=10)
    preference_ids: list[int] | None = None


class RecommendedCourse(Course):
    score: float
    reason: str