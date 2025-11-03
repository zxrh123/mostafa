from functools import lru_cache

from pydantic import AnyHttpUrl, BaseSettings, Field


class Settings(BaseSettings):
    """Centralised application configuration."""

    project_name: str = Field(default="MikroTik AI Control Plane")
    environment: str = Field(default="development")

    api_v1_prefix: str = Field(default="/api/v1")
    websocket_prefix: str = Field(default="/ws")

    # Database configuration
    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_user: str = Field(default="ai_brain")
    postgres_password: str = Field(default="changeme")
    postgres_db: str = Field(default="mikrotik_ai")

    # Cache / pubsub
    redis_url: str = Field(default="redis://localhost:6379/0")

    # AI providers
    openai_api_key: str | None = None
    openai_model: str = Field(default="gpt-4.1")
    gemini_api_key: str | None = None
    gemini_model: str = Field(default="gemini-1.5-pro")

    # RouterOS
    routeros_hosts: list[AnyHttpUrl] = Field(default_factory=list)
    routeros_username: str | None = None
    routeros_password: str | None = None

    # Security / observability
    auth_secret_key: str = Field(default="super-secret-change-me")
    auth_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)

    audit_log_path: str = Field(default="/var/log/mikrotik-ai/audit.log")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
