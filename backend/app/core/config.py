from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@db:5432/aerotech_db"

    class Config:
        env_file = ".env"

settings = Settings()