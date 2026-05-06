from pydantic import BaseModel
from app.prompts.prompt_type import PromptType


class AskRequest(BaseModel):
    prompt_type: PromptType
    question: str | None = None


class AskResponse(BaseModel):
    answer: str


class AskRecommendationRequest(AskRequest):
    data: dict | None = None