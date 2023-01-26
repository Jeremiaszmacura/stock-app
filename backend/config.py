from pydantic import AnyHttpUrl, BaseSettings

class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8080",
    ]
    
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str

    class Config:
        env_file = ".env"


settings = Settings()