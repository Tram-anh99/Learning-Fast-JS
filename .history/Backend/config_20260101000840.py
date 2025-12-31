"""
========== Database Configuration ==========
Cấu hình kết nối PostgreSQL
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Cấu hình ứng dụng từ environment variables"""
    
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5433
    DB_NAME: str = "postgres"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "123456"
    DB_SCHEMA: str = "nongsan"
    
    # API
    API_TITLE: str = "Agriculture Management API"
    API_VERSION: str = "2.0.0"
    API_PREFIX: str = "/api"
    
    # CORS (parse from string to list)
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:5174,http://localhost:3000"
    
    @property
    def cors_origins_list(self) -> list:
        """Convert CORS_ORIGINS string to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def DATABASE_URL(self) -> str:
        """Tạo connection string cho PostgreSQL"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def DATABASE_URL_ASYNC(self) -> str:
        """Async connection string"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()


settings = get_settings()
