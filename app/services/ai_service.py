from app.ai.factory import create_ai_langchain
from app.core.config import get_settings
from app.prompts.prompt_type import PromptType
from app.ai.ai_type import AiType
from app.prompts.recommend_prompt_builder import build_prompt as build_recommend_prompt


def ask_ai(
    prompt_type: PromptType,
    question: str | None = None
) -> str:

    settings = get_settings()
    # ai_client = create_ai_langchain(settings.ai_provider)
    ai_client = create_ai_langchain(AiType.LMSTUDIO)

    system_prompt, user_prompt = "請簡單回答使用者問題", question

    return ai_client.chat(system_prompt, user_prompt)

def ask_ai_course_recommendation(
    data: dict
) -> str:
    final_ai_provider = AiType.LMSTUDIO

    ai_client = create_ai_langchain(final_ai_provider)

    system_prompt, user_prompt = build_recommend_prompt(
        data=data
    )

    if final_ai_provider == AiType.LMSTUDIO:
        return ai_client.chat(system_prompt, user_prompt)
    elif final_ai_provider == AiType.GEMINI:
        return ai_client.chat(system_prompt, user_prompt)[0]["text"]
    else:
        return "無"
