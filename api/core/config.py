from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    PROJECT_NAME: str = "Finance App Work Simulation"
    DATABASE_URL: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
