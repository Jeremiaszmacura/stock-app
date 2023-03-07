"""Backend app configuration file."""
from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    """Class contains backend app settings."""

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:3000",
    ]

    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str

    # JWT access token
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    CLIENT_ORIGIN: str

    ALPHA_VANTAGE_API_KEY: str

    class Config:
        env_file = "../.env"


settings = Settings()
