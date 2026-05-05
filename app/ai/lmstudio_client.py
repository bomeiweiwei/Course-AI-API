from app.ai.base import BaseAILangchain


class LMStudioLangchain(BaseAILangchain):
    def __init__(self, base_url: str, model_name: str):
        from langchain_openai import ChatOpenAI

        self.llm = ChatOpenAI(
            model=model_name,
            api_key="lm-studio",
            base_url=base_url,
            temperature=0.7,
        )