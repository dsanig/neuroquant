from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Investment Control Center API"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str
    redis_url: str
    jwt_secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 10080
    log_level: str = "INFO"


settings = Settings()
