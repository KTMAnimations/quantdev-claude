"""
Configuration settings using Pydantic
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # LLM Configuration
    llm_provider: str = "chatmock"  # "chatmock" | "openai"
    llm_base_url: Optional[str] = "http://127.0.0.1:8000/v1"
    llm_api_key: str = "sk-dummy"
    llm_model: str = "gpt-4"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 4096

    # ChromaDB Configuration
    chromadb_persist_directory: str = "./data/chromadb"
    chromadb_collection_name: str = "pine_scripts"

    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/openquant"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # OpenAI (legacy, used if llm_provider is "openai")
    openai_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
        env_prefix = ""
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
