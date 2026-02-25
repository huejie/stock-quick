# core/config.py
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用配置"""

    # 环境
    ENV: str = "development"
    DEBUG: bool = True

    # API 配置
    API_PREFIX: str = "/api"
    APP_NAME: str = "智投助手 API"
    VERSION: str = "1.0.0"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:7777",
        "http://localhost:7780",
        "http://localhost:8000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:7777",
        "http://127.0.0.1:7780",
    ]

    # 数据库配置
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "stock_quick"

    # Redis 配置
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False  # 本地开发先关闭

    # 数据源配置
    AKSHARE_TIMEOUT: int = 10
    CACHE_EXPIRE_DEFAULT: int = 30
    CACHE_EXPIRE_SECTORS: int = 60
    CACHE_EXPIRE_NEWS: int = 300

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
