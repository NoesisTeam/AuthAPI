from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MYSQL_DB_USERNAME: str
    MYSQL_DB_PASSWORD: str
    MYSQL_DB_HOST: str
    MYSQL_DB_PORT: int
    MYSQL_DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    model_config = SettingsConfigDict(env_file="core/.env")

    @property
    def sqlalchemy_database_url(self) -> str:
        return f"mysql+mysqlconnector://{self.MYSQL_DB_USERNAME}:{self.MYSQL_DB_PASSWORD}@{self.MYSQL_DB_HOST}:{self.MYSQL_DB_PORT}/{self.MYSQL_DB_NAME}"


@lru_cache
def get_settings():
    return Settings()
