from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Investment Control Center API"
    environment: Literal["development", "production", "test"] = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite+pysqlite:///./icc.db"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret_key: str = "change-me"
    jwt_issuer: str = "investment-control-center"
    jwt_audience: str = "investment-control-center-users"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 10080
    log_level: str = "INFO"
    import_storage_dir: str = "./import_storage"
    auth_rate_limit_per_minute: int = 10
    enforce_https_cookies: bool = True
    trust_forwarded_headers: bool = True
    allowed_proxy_hops: int = Field(default=1, ge=0, le=5)

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @model_validator(mode="after")
    def validate_security_posture(self) -> "Settings":
        if self.is_production:
            if self.jwt_secret_key in {"", "change-me"} or len(self.jwt_secret_key) < 32:
                raise ValueError("jwt_secret_key must be set to a strong value in production")
            if self.database_url.startswith("sqlite"):
                raise ValueError("sqlite is not permitted in production")
            if self.access_token_expire_minutes > 60:
                raise ValueError("access_token_expire_minutes must be <= 60 in production")
        return self


settings = Settings()
