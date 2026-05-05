from app.ai.factory import create_ai_langchain
from app.core.config import get_settings
from app.prompts.prompt_builder import build_prompt
from app.prompts.prompt_type import PromptType
from app.ai.ai_type import AiType


def ask_normal(
    system_prompt: str,
    user_prompt: str,
    ai_type: AiType = AiType.LMSTUDIO,
) -> str:
    settings = get_settings()
    llm = create_ai_langchain(settings.ai_provider)

    result = llm.chat(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    return result


def ask_ai(
    prompt_type: PromptType,
    question: str | None = None,
    course: dict | None = None,
    courses: list[dict] | None = None,
) -> str:
    settings = get_settings()
    ai_client = create_ai_langchain(settings.ai_provider)

    system_prompt, user_prompt = build_prompt(
        prompt_type=prompt_type,
        question=question,
        course=course,
        courses=courses,
    )

    return ai_client.chat(system_prompt, user_prompt)