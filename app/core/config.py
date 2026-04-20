from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SENDGRID_API_KEY: str
    FROM_EMAIL: str
    FROM_NAME: str

    REDIS_URL: str = "redis://localhost:6379/0"
    DATABASE_URL: str

    RATE_LIMIT_PER_MINUTE: int = 60
    CELERY_TASK_RATE_LIMIT: str = "10/m"

    class Config:
        env_file = ".env"

settings = Settings()