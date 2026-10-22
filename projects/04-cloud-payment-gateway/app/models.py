import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class StatusPedido(str, enum.Enum):
    PENDENTE = "PENDENTE"
    PROCESSANDO = "PROCESSANDO"
    PAGO = "PAGO"
    CANCELADO = "CANCELADO"
    ESTORNADO = "ESTORNADO"

class MetodoPagamento(str, enum.Enum):
    PIX = "PIX"
    CARTAO_CREDITO = "CARTAO_CREDITO"
    BOLETO = "BOLETO"

class Pedido(Base):
    """
    Entidade de Negócio: Pedido / Venda
    """
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    codigo_referencia = Column(String(64), unique=True, index=True, nullable=False)
    cliente_nome = Column(String(120), nullable=False)
    cliente_email = Column(String(120), nullable=False, index=True)
    cliente_cpf = Column(String(14), nullable=False)
    descricao = Column(String(255), nullable=False)
    valor_total = Column(Float, nullable=False)
    status = Column(Enum(StatusPedido), default=StatusPedido.PENDENTE, nullable=False, index=True)

    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    transacoes = relationship("Transacao", back_populates="pedido", cascade="all, delete-orphan")

class Transacao(Base):
    """
    Entidade de Integração: Registro da transação financeira no Gateway
    """
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    gateway_id = Column(String(100), unique=True, index=True, nullable=False)
    metodo = Column(Enum(MetodoPagamento), nullable=False)
    valor = Column(Float, nullable=False)
    status = Column(String(50), default="PENDING", nullable=False)

    # Dados específicos do Pix
    pix_copia_e_cola = Column(Text, nullable=True)
    pix_qr_code_base64 = Column(Text, nullable=True)
    expira_em = Column(DateTime, nullable=True)

    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    pago_em = Column(DateTime, nullable=True)

    pedido = relationship("Pedido", back_populates="transacoes")

class WebhookLog(Base):
    """
    Auditoria e Segurança: Armazena cada evento recebido do Gateway na nuvem
    para fins de auditoria forense, idempotência e reprocessamento.
    """
    __tablename__ = "webhook_logs"

    id = Column(Integer, primary_key=True, index=True)
    gateway = Column(String(50), nullable=False)
    event_id = Column(String(100), index=True, nullable=True)
    event_type = Column(String(80), nullable=False)
    assinatura_recebida = Column(String(255), nullable=True)
    assinatura_valida = Column(String(10), nullable=False)  # "TRUE" ou "FALSE"
    payload_bruto = Column(Text, nullable=False)
    status_processamento = Column(String(50), default="PROCESSADO", nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)

class RegistroIdempotencia(Base):
    """
    Controle de Engenharia contra Concorrência e Duplicidade:
    Garante que requisições repetidas com a mesma chave não processem débitos duplicados.
    """
    __tablename__ = "idempotencia_chaves"

    chave = Column(String(128), primary_key=True, index=True)
    recurso = Column(String(100), nullable=False)
    status_code = Column(Integer, nullable=False)
    resposta_json = Column(Text, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
