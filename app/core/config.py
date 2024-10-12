import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class GlobalConfig(BaseSettings):
    title: str = os.environ.get("TITLE")
    version: str = "1.0.0"
    description: str = os.environ.get("DESCRIPTION")
    host_url: str = "http://localhost:8000"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"
    api_prefix: str = "/v1"
    debug: bool = os.environ.get("DEBUG")
    postgres_user: str = os.environ.get("POSTGRES_USER")
    postgres_password: str = os.environ.get("POSTGRES_PASSWORD")
    postgres_hostname: str = os.environ.get("DATABASE_HOSTNAME")
    postgres_port: int = int(os.environ.get("POSTGRES_PORT"))
    postgres_db: str = os.environ.get("POSTGRES_DB")
    db_echo_log: bool = True if os.environ.get("DEBUG") is True else False

    @property
    def sync_database_url(self) -> str:
        return (f"postgresql://{self.postgres_user}:{self.postgres_password}@"
                f"{self.postgres_hostname}:{self.postgres_port}/{self.postgres_db}")

    @property
    def async_database_url(self) -> str:
        return (f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@"
                f"{self.postgres_hostname}:{self.postgres_port}/{self.postgres_db}")


settings = GlobalConfig()
