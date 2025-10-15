from pydantic_settings import BaseSettings
from typing import List, Union
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://nlq_user:nlq_password@localhost:5432/nlq_app"
    REDIS_URL: str = "redis://localhost:6379"
    
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4"
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: Union[str, List[str]] = ["http://localhost:3000"]
    
    # Optional
    ENABLE_METRICS: bool = True
    ENABLE_TRACING: bool = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Convert CORS_ORIGINS to list if it's a string
        if isinstance(self.CORS_ORIGINS, str):
            self.CORS_ORIGINS = [self.CORS_ORIGINS]
    
    class Config:
        env_file = "../.env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env

# Global settings instance
settings = Settings()
