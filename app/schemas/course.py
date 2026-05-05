from pydantic import BaseModel


class Course(BaseModel):
    course_id: int
    course_name: str
    school_name: str
    grade_name: str
    subject_name: str
    version_name: str | None = None
    degree_name: str | None = None
    goal_name: str | None = None
    price: int
    rating: float
    students: int