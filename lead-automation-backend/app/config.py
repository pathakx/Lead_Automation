from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str
    
    # Groq AI
    GROQ_API_KEY: str
    
    # Resend Email
    RESEND_API_KEY: str
    RESEND_FROM_EMAIL: str = "leads@yourdomain.com"
    
    # Application
    APP_ENV: str = "development"
    APP_NAME: str = "Lead Automation System"
    CORS_ORIGINS: str = "http://localhost:5173"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Global settings instance
settings = Settings()
