from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
from app.config import get_settings

settings = get_settings()

# Tratamento para SQLite vs PostgreSQL (pooling e threading)
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True  # Verifica se a conexão com o banco na nuvem ainda está viva
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator:
    """
    Injeção de Dependência do FastAPI para o Ciclo de Vida da Sessão do Banco.
    Garante fechamento correto da conexão para evitar vazamento (connection leak).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
