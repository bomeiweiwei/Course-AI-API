from app.ai.base import BaseAILangchain


class AzureLangchain(BaseAILangchain):
    def __init__(self, api_key: str, endpoint: str, deployment_name: str, api_version: str):
        from langchain_openai import AzureChatOpenAI
        self.llm = AzureChatOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            azure_deployment=deployment_name,
            api_version=api_version,
        )
