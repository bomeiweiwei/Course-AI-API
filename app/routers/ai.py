from fastapi import APIRouter
from app.schemas.ai import AskRequest, AskResponse
from app.services.ai_service import ask_ai
from app.prompts.prompt_type import PromptType

router = APIRouter()

@router.post("/test1")
def test1(request: AskRequest):
    answer = ask_ai(
        prompt_type=PromptType.TEST,
        question=request.question
    )
    return {"answer": answer}

@router.post("/test2", response_model=AskResponse)
def test2(request: AskRequest):
    answer = ask_ai(
        prompt_type=PromptType.TEST,
        question=request.question
    )
    return AskResponse(answer=answer)