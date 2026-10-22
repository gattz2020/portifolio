from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.models import StatusPedido, MetodoPagamento

class HealthResponse(BaseModel):
    status: str
    versao: str
    ambiente: str
    banco_dados: str
    timestamp: datetime

class ClienteSchema(BaseModel):
    nome: str = Field(..., min_length=3, max_length=120, example="Carlos Eduardo Silva")
    email: EmailStr = Field(..., example="carlos.silva@email.com")
    cpf: str = Field(..., min_length=11, max_length=14, example="12345678900")

class CriarCobrancaPixRequest(BaseModel):
    cliente: ClienteSchema
    descricao: str = Field(..., min_length=3, max_length=255, example="Assinatura Plano Pro Anual")
    valor: float = Field(..., gt=0, example=199.90, description="Valor em Reais (BRL), deve ser maior que zero")
    expiracao_minutos: int = Field(default=30, ge=5, le=1440, description="Tempo de expiração do Pix em minutos")

class TransacaoPixResponse(BaseModel):
    transacao_id: int
    gateway_id: str
    status: str
    valor: float
    pix_copia_e_cola: str
    pix_qr_code_base64: Optional[str] = None
    expira_em: datetime
    criado_em: datetime

    class Config:
        from_attributes = True

class PedidoResponse(BaseModel):
    pedido_id: int
    codigo_referencia: str
    cliente_nome: str
    cliente_email: str
    descricao: str
    valor_total: float
    status: StatusPedido
    criado_em: datetime
    transacao: Optional[TransacaoPixResponse] = None

    class Config:
        from_attributes = True

class WebhookPayloadMock(BaseModel):
    event_id: str = Field(..., example="evt_987654321")
    event_type: str = Field(..., example="payment.approved")
    gateway_id: str = Field(..., example="tx_pix_abc123456")
    timestamp: str = Field(..., example="2026-10-21T22:30:00Z")
    data: dict

class NotificacaoWebhookResponse(BaseModel):
    recebido: bool
    event_id: str
    status_processamento: str
    mensagem: str
