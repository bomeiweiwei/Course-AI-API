from pydantic import BaseModel
from app.prompts.prompt_type import PromptType


class NormalAskRequest(BaseModel):
    system_prompt: str = "簡短的回應使用者的問題"
    user_prompt: str


class AskRequest(BaseModel):
    prompt_type: PromptType
    question: str | None = None
    course: dict | None = None
    courses: list[dict] | None = None


class AskResponse(BaseModel):
    answer: str