from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Course AI API"
    
    ai_provider: str = "lmstudio"

    gemini_api_key: str | None = None
    gemini_model_name: str = "gemini-1.5-flash"

    lmstudio_base_url: str = "http://localhost:1234/v1"
    lmstudio_model_name: str = "local-model"

    azure_openai_api_key: str | None = None
    azure_openai_endpoint: str | None = None

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()