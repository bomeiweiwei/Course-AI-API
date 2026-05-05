from pydantic import BaseModel


class Course(BaseModel):
    school_id: int
    school_name: str
    grade_id: int
    grade_name: str
    subject_id: int
    subject_name: str
    course_name: str
    version_id: int
    version_name: str
    degree_id: int
    degree_name: str
    goal_id: int
    goal_name: str
    price: int
    preferences: list[int]
    rating: float
    students: int