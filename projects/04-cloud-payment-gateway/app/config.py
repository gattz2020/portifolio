import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Configurações centrais da aplicação carregadas a partir de variáveis de ambiente.
    Segue os princípios de 'Twelve-Factor App'.
    """
    APP_NAME: str = "CloudPay Nexus Engine"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 8000

    # Banco de Dados (PostgreSQL em produção ou SQLite para testes locais)
    DATABASE_URL: str = "sqlite:///./cloudpay.db"

    # Segurança e Validação de Webhooks (HMAC-SHA256)
    WEBHOOK_SECRET: str = "cloudpay_super_secret_webhook_key_2026"
    GATEWAY_API_KEY: str = "mock_sandbox_key_abcdef123456"

    # Dados do Recebedor Pix
    PIX_CHAVE: str = "financeiro@minhaempresa.com.br"
    PIX_BENEFICIARIO: str = "CloudPay Soluções Digitais"
    PIX_CIDADE: str = "Goiania"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Retorna uma instância única em cache das configurações."""
    return Settings()
