from pydantic_settings import BaseSettings, SettingConfigDict

class Setting(BaseSettings):

    host:str
    port:int
    name:str
    user:str
    password:str

    model_config = SettingConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        env_prefix="DB_"
        extra="ignore"
    )

settings = Setting()