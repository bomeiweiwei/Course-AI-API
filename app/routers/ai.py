from fastapi import APIRouter
from app.schemas.ai import AskRequest, AskResponse, AskRecommendationRequest
from app.services.ai_service import ask_ai, ask_ai_course_recommendation
from app.prompts.prompt_type import PromptType

router = APIRouter()

# @router.post("/test1")
# def test1(request: AskRequest):
#     answer = ask_ai(
#         prompt_type=PromptType.TEST,
#         question=request.question
#     )
#     return {"answer": answer}

# @router.post("/test2", response_model=AskResponse)
# def test2(request: AskRequest):
#     answer = ask_ai(
#         prompt_type=PromptType.TEST,
#         question=request.question
#     )
#     return AskResponse(answer=answer)

@router.post("/course/recommendation", response_model=AskResponse)
def course_recommendation(request: AskRecommendationRequest):
    answer = ask_ai_course_recommendation(
        # prompt_type=PromptType.RECOMMEND_EXPLANATION,
        data=request.data
    )
    return AskResponse(answer=answer)