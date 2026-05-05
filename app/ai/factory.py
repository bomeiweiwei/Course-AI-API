from app.ai.ai_type import AiType
from app.ai.base import BaseAILangchain
from app.ai.gemini_client import GeminiLangchain
from app.ai.lmstudio_client import LMStudioLangchain
from app.core.config import get_settings


def create_ai_langchain(ai_type: AiType | str) -> BaseAILangchain:
    settings = get_settings()

    ai_type = AiType(ai_type)

    if ai_type == AiType.GEMINI:
        return GeminiLangchain(
            api_key=settings.gemini_api_key,
            model_name=settings.gemini_model_name,
        )

    if ai_type == AiType.LMSTUDIO:
        return LMStudioLangchain(
            base_url=settings.lmstudio_base_url,
            model_name=settings.lmstudio_model_name,
        )

    raise ValueError(f"不支援的 AI 類型：{ai_type}")