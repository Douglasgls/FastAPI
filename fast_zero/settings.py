from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Ler o arquivo env
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_TIME: int
