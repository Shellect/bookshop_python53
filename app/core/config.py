from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field, SecretStr, field_validator
from typing import Optional

class Settings(BaseSettings):
    # App
    app_name: str = Field("Book Shop")
    debug: bool = True
    testing: bool = False

    # Redis
    redis_host: str
    redis_port: int = 6379
    redis_password: str
    redis_db: int = 0

    # Database
    postgres_host: str
    postgres_port: int = 5432
    postgres_user: str
    postgres_password: SecretStr
    postgres_db: str
    database_url: Optional[PostgresDsn] = None

    @field_validator("database_url", mode="before")
    @classmethod
    def assemble_database_url(cls, v: Optional[str], info) -> PostgresDsn:
        if v:
            return PostgresDsn(v)
        if info.data.get("testing"):
            return PostgresDsn.build(
                scheme="postgresql+psycopg2",
                username=info.data.get("postgres_user"),
                password=info.data.get("postgres_password").get_secret_value(),
                host=info.data.get("postgres_host"),
                port=info.data.get("postgres_port"),
                path=info.data.get("postgres_db")
            )
        else:
            return PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=info.data.get("postgres_user"),
                password=info.data.get("postgres_password").get_secret_value(),
                host=info.data.get("postgres_host"),
                port=info.data.get("postgres_port"),
                path=info.data.get("postgres_db")
            )

settings = Settings()