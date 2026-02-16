"""
Configuration Settings
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # Database
    DATABASE_URL: str = "sqlite:///./toolbox.db"  # Default SQLite voor development
    # Voor productie PostgreSQL:
    # DATABASE_URL: str = "postgresql://user:password@localhost/toolbox_db"

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"  # CHANGE THIS!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dagen

    # Firebase Admin (optioneel)
    FIREBASE_CREDENTIALS_PATH: Optional[str] = None

    # Email
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[str] = "noreply@toolbox.local"
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587

    # App
    APP_NAME: str = "Toolbox Management"
    APP_URL: str = "https://cn7pgf2knn-lab.github.io/toolbox-management/toolbox-app-firebase.html"

    # CORS
    CORS_ORIGINS: list = [
        "https://cn7pgf2knn-lab.github.io",
        "http://localhost:3000",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
