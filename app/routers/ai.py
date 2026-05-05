from fastapi import APIRouter
from app.schemas.ai import NormalAskRequest, AskRequest, AskResponse
from app.services.ai_service import ask_ai, ask_normal

router = APIRouter()


# @router.post("/normalask", response_model=AskResponse)
# def ask(request: NormalAskRequest):
#     answer = ask_normal(
#         system_prompt=request.system_prompt,
#         user_prompt=request.user_prompt,
#     )

#     return AskResponse(answer=answer)


@router.post("/ask")
def ask(request: AskRequest):
    answer = ask_ai(
        prompt_type=request.prompt_type,
        question=request.question,
        course=request.course,
        courses=request.courses,
    )

    return {"answer": answer}