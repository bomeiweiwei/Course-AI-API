from app.prompts.prompt_type import PromptType


def build_prompt(
    prompt_type: PromptType,
    question: str | None = None,
    course: dict | None = None,
    courses: list[dict] | None = None,
) -> tuple[str, str]:

    if prompt_type == PromptType.COURSE_QUESTION:
        system_prompt = """
你是線上課程智能推薦顧問。
請根據提供的課程資料回答使用者問題。
不要編造資料，若資料不足請明確說明。
請使用繁體中文。
"""

        user_prompt = f"""
課程資料：
{course}

使用者問題：
{question}
"""
        return system_prompt, user_prompt

    if prompt_type == PromptType.RECOMMEND_EXPLANATION:
        system_prompt = """
你是線上課程智能推薦顧問。
請根據推薦結果，說明推薦原因。
回答要簡潔、具體、適合家長閱讀。
請使用繁體中文。
"""

        user_prompt = f"""
推薦課程清單：
{courses}

請說明這些課程為什麼值得推薦。
"""
        return system_prompt, user_prompt

    if prompt_type == PromptType.GENERAL_ADVISOR:
        system_prompt = """
你是線上課程智能推薦顧問。
請協助使用者釐清選課方向。
回答要用簡單問題引導，不要一次給太多資訊。
請使用繁體中文。
"""

        user_prompt = question or "請協助我選擇適合的課程。"
        return system_prompt, user_prompt

    raise ValueError(f"不支援的 prompt_type：{prompt_type}")