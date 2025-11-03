"""
Configuration settings for the application
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "MikroTik AI Management Platform"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://mikrotik_user:mikrotik_pass@localhost:5432/mikrotik_ai_db"
    )
    
    # AI APIs
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-secret-key-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # MikroTik Default Settings
    MIKROTIK_DEFAULT_HOST: str = os.getenv("MIKROTIK_DEFAULT_HOST", "192.168.88.1")
    MIKROTIK_DEFAULT_USER: str = os.getenv("MIKROTIK_DEFAULT_USER", "admin")
    MIKROTIK_DEFAULT_PASSWORD: str = os.getenv("MIKROTIK_DEFAULT_PASSWORD", "")
    MIKROTIK_DEFAULT_PORT: int = int(os.getenv("MIKROTIK_DEFAULT_PORT", "8728"))
    MIKROTIK_SSH_PORT: int = int(os.getenv("MIKROTIK_SSH_PORT", "22"))
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Security Policies
    AUTO_EXECUTE_ENABLED: bool = os.getenv("AUTO_EXECUTE_ENABLED", "false").lower() == "true"
    REQUIRE_AUTHENTICATION: bool = os.getenv("REQUIRE_AUTHENTICATION", "true").lower() == "true"
    
    # Monitoring
    MONITORING_INTERVAL: int = int(os.getenv("MONITORING_INTERVAL", "30"))
    ALERT_THRESHOLD_CPU: float = float(os.getenv("ALERT_THRESHOLD_CPU", "80"))
    ALERT_THRESHOLD_RAM: float = float(os.getenv("ALERT_THRESHOLD_RAM", "85"))
    ALERT_THRESHOLD_LATENCY: float = float(os.getenv("ALERT_THRESHOLD_LATENCY", "100"))
    
    # Knowledge Base
    KNOWLEDGE_BASE_ENABLED: bool = os.getenv("KNOWLEDGE_BASE_ENABLED", "true").lower() == "true"
    KNOWLEDGE_BASE_UPDATE_INTERVAL: int = int(os.getenv("KNOWLEDGE_BASE_UPDATE_INTERVAL", "3600"))
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
