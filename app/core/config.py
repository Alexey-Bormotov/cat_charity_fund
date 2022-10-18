from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'QRKot_default_title'
    description: str = 'QRKot_default_description'
    database_url: str = 'sqlite+aiosqlite:///./qrkot.db'
    secret: str = 'QRKot_default_secret'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    min_password_length: int = 3

    class Config:
        env_file = '.env'


settings = Settings()
