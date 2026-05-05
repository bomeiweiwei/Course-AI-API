from app.core.config import get_settings

settings = get_settings()


def ask_ai(question: str, course_name: str | None = None) -> str:
    if settings.ai_provider == "mock":
        if course_name:
            return f"針對「{course_name}」，你的問題是：{question}。目前這是 mock AI 回答。"

        return f"你的問題是：{question}。目前這是 mock AI 回答。"

    # 之後可以在這裡接 Gemini / Azure OpenAI / LM Studio
    return "尚未設定正式 AI Provider。"