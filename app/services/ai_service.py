from app.ai.factory import create_ai_langchain
from app.core.config import get_settings
from app.prompts.prompt_type import PromptType
from app.ai.ai_type import AiType


def ask_ai(
    prompt_type: PromptType,
    question: str | None = None
) -> str:

    settings = get_settings()
    # ai_client = create_ai_langchain(settings.ai_provider)
    ai_client = create_ai_langchain(AiType.LMSTUDIO)

    system_prompt, user_prompt = "請簡單回答使用者問題", question

    return ai_client.chat(system_prompt, user_prompt)