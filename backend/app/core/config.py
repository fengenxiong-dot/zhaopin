from functools import lru_cache

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",
        case_sensitive=False,
        extra="ignore",
    )

    app_env: str = "development"
    app_name: str = "招聘信息管理系统"
    app_secret_key: str = "development-only-secret"
    app_cors_origins: str = "http://localhost:8080"
    database_url: str = "postgresql+asyncpg://recruitment:recruitment@localhost:5432/recruitment"
    attachment_root: str = "/app/storage/attachments"
    max_attachment_size_mb: int = Field(default=20, gt=0, le=200)

    @field_validator("app_env")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        allowed = {"development", "test", "production"}
        if value not in allowed:
            raise ValueError(f"APP_ENV must be one of: {', '.join(sorted(allowed))}")
        return value

    @model_validator(mode="after")
    def validate_production_secret(self) -> "Settings":
        if self.app_env == "production" and len(self.app_secret_key) < 32:
            raise ValueError("APP_SECRET_KEY must be at least 32 characters in production")
        return self

    @property
    def cors_origins(self) -> list[str]:
        return [item.strip() for item in self.app_cors_origins.split(",") if item.strip()]

    @property
    def docs_enabled(self) -> bool:
        return self.app_env != "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
