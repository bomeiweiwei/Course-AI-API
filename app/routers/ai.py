from fastapi import APIRouter
from app.schemas.ai import AskRequest, AskResponse
from app.services.ai_service import ask_ai

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    answer = ask_ai(
        question=request.question,
        course_name=request.course_name
    )

    return AskResponse(answer=answer)