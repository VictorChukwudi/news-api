from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    database_url: str
    jwt_secret_key: str

    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60
    
settings = Settings()