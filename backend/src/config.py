from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(validation_alias="DATABASE_CONNECTION_STRING")
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    app_env: str = "development"

    model_config = {"env_file": ".env", "case_sensitive": False}


settings = Settings()
