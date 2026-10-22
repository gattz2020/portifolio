import uuid
import hmac
import hashlib
import json
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, Header, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional

from app.config import get_settings
from app.database import engine, get_db, Base
from app.models import Pedido, Transacao, WebhookLog, RegistroIdempotencia, StatusPedido, MetodoPagamento
from app.schemas import (
    HealthResponse,
    CriarCobrancaPixRequest,
    PedidoResponse,
    TransacaoPixResponse,
    NotificacaoWebhookResponse,
    WebhookPayloadMock
)
from app.services.pix_service import PixPayloadEngine

settings = get_settings()

# Criação automática de tabelas (para SQLite e PostgreSQL)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Microserviço em Nuvem para Gateway de Pagamentos, Geração de Pix e Recepção Segura de Webhooks com Idempotência.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Habilita CORS para permitir que frontends e checkouts se comuniquem com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# ROTA DE HEALTHCHECK (Monitoramento Cloud & Kubernetes)
# ==============================================================================
@app.get("/health", response_model=HealthResponse, tags=["Monitoramento"])
def health_check(db: Session = Depends(get_db)):
    """Verifica saúde da aplicação e conectividade com o banco de dados na nuvem."""
    try:
        # Executa uma query leve para confirmar integridade da conexão
        db.execute(Base.metadata.tables["pedidos"].select().limit(1))
        db_status = "ONLINE (Conectado)"
    except Exception as e:
        db_status = f"DEGRADADO ({str(e)})"

    return HealthResponse(
        status="OPERATIONAL",
        versao=settings.APP_VERSION,
        ambiente=settings.ENVIRONMENT,
        banco_dados=db_status,
        timestamp=datetime.utcnow()
    )

# ==============================================================================
# ROTA 1: CRIAR COBRANÇA PIX COM CONTROLE DE IDEMPOTÊNCIA
# ==============================================================================
@app.post(
    "/api/v1/pagamentos/pix",
    response_model=PedidoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Pagamentos"]
)
def criar_cobranca_pix(
    requisicao: CriarCobrancaPixRequest,
    db: Session = Depends(get_db),
    idempotency_key: Optional[str] = Header(None, alias="X-Idempotency-Key")
):
    """
    Cria um novo pedido e gera a cobrança Pix com Payload EMV e QR Code.
    Possui suporte a 'X-Idempotency-Key' para evitar cobranças duplicadas em caso de retry.
    """
    # 1. Verificação de Idempotência
    if idempotency_key:
        registro_existente = db.query(RegistroIdempotencia).filter(
            RegistroIdempotencia.chave == idempotency_key
        ).first()
        if registro_existente:
            # Retorna o resultado previamente computado
            return json.loads(registro_existente.resposta_json)

    # 2. Criação do Pedido
    ref_codigo = f"ORD-{uuid.uuid4().hex[:10].upper()}"
    txid_pix = f"TX{uuid.uuid4().hex[:18].upper()}"
    gateway_id = f"gw_{uuid.uuid4().hex[:16]}"

    novo_pedido = Pedido(
        codigo_referencia=ref_codigo,
        cliente_nome=requisicao.cliente.nome,
        cliente_email=requisicao.cliente.email,
        cliente_cpf=requisicao.cliente.cpf,
        descricao=requisicao.descricao,
        valor_total=requisicao.valor,
        status=StatusPedido.PENDENTE
    )
    db.add(novo_pedido)
    db.flush()  # Obtém o ID do pedido gerado

    # 3. Geração do Pix Padrão Banco Central
    pix_copia_cola = PixPayloadEngine.gerar_pix_copia_e_cola(
        chave_pix=settings.PIX_CHAVE,
        beneficiario=settings.PIX_BENEFICIARIO,
        cidade=settings.PIX_CIDADE,
        valor=requisicao.valor,
        txid=txid_pix
    )

    qr_code_base64 = PixPayloadEngine.gerar_qr_code_base64(pix_copia_cola)
    expira_em = datetime.utcnow() + timedelta(minutes=requisicao.expiracao_minutos)

    # 4. Criação da Transação
    nova_transacao = Transacao(
        pedido_id=novo_pedido.id,
        gateway_id=gateway_id,
        metodo=MetodoPagamento.PIX,
        valor=requisicao.valor,
        status="PENDING",
        pix_copia_e_cola=pix_copia_cola,
        pix_qr_code_base64=qr_code_base64,
        expira_em=expira_em
    )
    db.add(nova_transacao)
    db.commit()
    db.refresh(novo_pedido)

    resposta = PedidoResponse(
        pedido_id=novo_pedido.id,
        codigo_referencia=novo_pedido.codigo_referencia,
        cliente_nome=novo_pedido.cliente_nome,
        cliente_email=novo_pedido.cliente_email,
        descricao=novo_pedido.descricao,
        valor_total=novo_pedido.valor_total,
        status=novo_pedido.status,
        criado_em=novo_pedido.criado_em,
        transacao=TransacaoPixResponse(
            transacao_id=nova_transacao.id,
            gateway_id=nova_transacao.gateway_id,
            status=nova_transacao.status,
            valor=nova_transacao.valor,
            pix_copia_e_cola=nova_transacao.pix_copia_e_cola,
            pix_qr_code_base64=nova_transacao.pix_qr_code_base64,
            expira_em=nova_transacao.expira_em,
            criado_em=nova_transacao.criado_em
        )
    )

    # 5. Salva chave de idempotência se informada
    if idempotency_key:
        registro = RegistroIdempotencia(
            chave=idempotency_key,
            recurso="/api/v1/pagamentos/pix",
            status_code=201,
            resposta_json=resposta.model_dump_json()
        )
        db.add(registro)
        db.commit()

    return resposta

# ==============================================================================
# ROTA 2: CONSULTAR STATUS DO PEDIDO (Polling pelo Frontend)
# ==============================================================================
@app.get("/api/v1/pedidos/{codigo_referencia}", response_model=PedidoResponse, tags=["Pagamentos"])
def consultar_pedido(codigo_referencia: str, db: Session = Depends(get_db)):
    """Consulta o status em tempo real de um pedido pelo código de referência."""
    pedido = db.query(Pedido).filter(Pedido.codigo_referencia == codigo_referencia).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")

    transacao = db.query(Transacao).filter(Transacao.pedido_id == pedido.id).first()

    transacao_response = None
    if transacao:
        transacao_response = TransacaoPixResponse(
            transacao_id=transacao.id,
            gateway_id=transacao.gateway_id,
            status=transacao.status,
            valor=transacao.valor,
            pix_copia_e_cola=transacao.pix_copia_e_cola,
            pix_qr_code_base64=transacao.pix_qr_code_base64,
            expira_em=transacao.expira_em,
            criado_em=transacao.criado_em
        )

    return PedidoResponse(
        pedido_id=pedido.id,
        codigo_referencia=pedido.codigo_referencia,
        cliente_nome=pedido.cliente_nome,
        cliente_email=pedido.cliente_email,
        descricao=pedido.descricao,
        valor_total=pedido.valor_total,
        status=pedido.status,
        criado_em=pedido.criado_em,
        transacao=transacao_response
    )

# ==============================================================================
# ROTA 3: RECEPTOR DE WEBHOOK COM VALIDAÇÃO HMAC-SHA256
# ==============================================================================
@app.post("/api/v1/webhooks/gateway", response_model=NotificacaoWebhookResponse, tags=["Webhooks"])
async def receber_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_signature: Optional[str] = Header(None, alias="X-Signature-SHA256")
):
    """
    Endpoint de recepção de eventos do Gateway na Nuvem.
    Aplica validação criptográfica HMAC-SHA256 contra adulterações e garante atomicidade.
    """
    raw_body = await request.body()
    body_str = raw_body.decode("utf-8")

    # 1. Validação Criptográfica HMAC-SHA256
    assinatura_valida = False
    if x_signature:
        expected_signature = hmac.new(
            key=settings.WEBHOOK_SECRET.encode("utf-8"),
            msg=raw_body,
            digestmod=hashlib.sha256
        ).hexdigest()
        
        # Uso de hmac.compare_digest para prevenir Timing Attacks
        assinatura_valida = hmac.compare_digest(x_signature, expected_signature)

    if not assinatura_valida and settings.ENVIRONMENT == "production":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Assinatura HMAC de Webhook inválida ou ausente."
        )

    # 2. Parse do Payload
    try:
        data = json.loads(body_str)
        event_id = data.get("event_id", f"evt_{uuid.uuid4().hex[:8]}")
        event_type = data.get("event_type", "unknown")
        gateway_id = data.get("gateway_id")
    except Exception:
        raise HTTPException(status_code=400, detail="Payload JSON inválido.")

    # 3. Auditoria Forense no Banco de Dados
    log = WebhookLog(
        gateway="CloudPay Engine",
        event_id=event_id,
        event_type=event_type,
        assinatura_recebida=x_signature,
        assinatura_valida="TRUE" if assinatura_valida else "FALSE",
        payload_bruto=body_str,
        status_processamento="PROCESSADO"
    )
    db.add(log)

    # 4. Transição de Estado Atômica (Transação ACID)
    if event_type in ["payment.approved", "pix.received"] and gateway_id:
        transacao = db.query(Transacao).filter(Transacao.gateway_id == gateway_id).first()
        if transacao:
            transacao.status = "PAID"
            transacao.pago_em = datetime.utcnow()
            
            # Atualiza o pedido associado
            pedido = db.query(Pedido).filter(Pedido.id == transacao.pedido_id).first()
            if pedido:
                pedido.status = StatusPedido.PAGO

    db.commit()

    return NotificacaoWebhookResponse(
        recebido=True,
        event_id=event_id,
        status_processamento="SUCESSO",
        mensagem="Evento processado e pedido atualizado com sucesso."
    )

# ==============================================================================
# ROTA 4: SIMULADOR DE APROVAÇÃO (Para Demos e Testes de Homologação)
# ==============================================================================
@app.post("/api/v1/pagamentos/simular-aprovacao/{gateway_id}", tags=["Homologação & Demos"])
def simular_aprovacao_pix(gateway_id: str, db: Session = Depends(get_db)):
    """
    Permite aprovar uma transação Pix imediatamente para demonstração visual
    sem necessidade de dinheiro real.
    """
    transacao = db.query(Transacao).filter(Transacao.gateway_id == gateway_id).first()
    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrada.")

    transacao.status = "PAID"
    transacao.pago_em = datetime.utcnow()

    pedido = db.query(Pedido).filter(Pedido.id == transacao.pedido_id).first()
    if pedido:
        pedido.status = StatusPedido.PAGO

    db.commit()
    db.refresh(pedido)

    return {
        "status": "APROVADO",
        "codigo_referencia": pedido.codigo_referencia,
        "pedido_status": pedido.status,
        "mensagem": "Pagamento Pix simulado com sucesso!"
    }
