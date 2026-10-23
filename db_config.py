"""Load database and JWT authentication settings from environment variables."""
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseConfig(BaseSettings):
    """Manage database connection settings loaded from environment variables."""
    host:str
    port:int
    name:str
    user:str
    password:str

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        env_prefix="DB_",
        extra="ignore",
    )

settings = DatabaseConfig()
