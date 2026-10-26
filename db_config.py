"""Load database and JWT authentication settings from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    """Manage database connection settings loaded from environment variables."""

    host: str
    port: int
    name: str
    user: str
    password: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="DB_",
        extra="ignore",
    )


settings = DatabaseConfig()


class AuthConfig(BaseSettings):
    """Manage JWT authentication and token expiration settings."""

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="JWT_",
        extra="ignore",
    )


jwt_config = AuthConfig()
