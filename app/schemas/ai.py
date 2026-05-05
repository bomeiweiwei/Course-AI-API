from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
    course_name: str | None = None


class AskResponse(BaseModel):
    answer: str