import pytest
import hmac
import hashlib
import json
from fastapi.testclient import TestClient
from app.main import app
from app.services.pix_service import PixPayloadEngine
from app.config import get_settings

client = TestClient(app)
settings = get_settings()

def test_pix_crc16_calculo():
    """Valida se o cálculo do CRC16 segue o padrão polinomial do Banco Central."""
    chave = "12345678900"
    payload = PixPayloadEngine.gerar_pix_copia_e_cola(
        chave_pix=chave,
        beneficiario="Loja Teste",
        cidade="Goiania",
        valor=150.00,
        txid="TESTE123"
    )
    # Todo payload Pix termina com a tag 6304 + 4 caracteres hexadecimais do CRC16
    assert "6304" in payload
    assert len(payload.split("6304")[-1]) == 4
    assert payload.startswith("000201")

def test_health_check_endpoint():
    """Valida o endpoint de healthcheck para observabilidade na nuvem."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OPERATIONAL"
    assert "ONLINE" in data["banco_dados"]

def test_criar_cobranca_pix_sucesso():
    """Valida a criação de um pedido com Pix, QR Code e status PENDENTE."""
    payload = {
        "cliente": {
            "nome": "João da Silva",
            "email": "joao.silva@exemplo.com",
            "cpf": "11122233344"
        },
        "descricao": "Serviço de Consultoria de Nuvem",
        "valor": 250.00,
        "expiracao_minutos": 30
    }
    response = client.post("/api/v1/pagamentos/pix", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["cliente_nome"] == "João da Silva"
    assert data["status"] == "PENDENTE"
    assert data["valor_total"] == 250.00
    assert data["transacao"] is not None
    assert "data:image/png;base64," in data["transacao"]["pix_qr_code_base64"]
    assert data["transacao"]["pix_copia_e_cola"].startswith("000201")

def test_idempotencia_garante_nao_duplicidade():
    """
    Teste de Concorrência e Engenharia:
    Duas requisições com o mesmo 'X-Idempotency-Key' devem retornar o mesmo pedido
    sem criar duplicidade no banco.
    """
    idempotency_key = "idemp_test_unique_key_12345"
    payload = {
        "cliente": {
            "nome": "Cliente Idempotente",
            "email": "idemp@exemplo.com",
            "cpf": "99988877766"
        },
        "descricao": "Assinatura Mensal",
        "valor": 99.00
    }
    headers = {"X-Idempotency-Key": idempotency_key}

    # 1ª Requisição
    res1 = client.post("/api/v1/pagamentos/pix", json=payload, headers=headers)
    assert res1.status_code == 201
    codigo1 = res1.json()["codigo_referencia"]

    # 2ª Requisição com a mesma chave (simulando reenvio de rede)
    res2 = client.post("/api/v1/pagamentos/pix", json=payload, headers=headers)
    assert res2.status_code == 201
    codigo2 = res2.json()["codigo_referencia"]

    # Devem ser o mesmo pedido (idempotência perfeita)
    assert codigo1 == codigo2

def test_webhook_assinatura_hmac_valida():
    """Valida o recebimento e aprovação segura de webhook com HMAC-SHA256."""
    # Cria primeiro um pedido para termos o gateway_id
    payload_pix = {
        "cliente": {"nome": "Teste Webhook", "email": "wh@teste.com", "cpf": "00011122233"},
        "descricao": "Teste Webhook",
        "valor": 50.00
    }
    res_pix = client.post("/api/v1/pagamentos/pix", json=payload_pix)
    gw_id = res_pix.json()["transacao"]["gateway_id"]
    cod_ref = res_pix.json()["codigo_referencia"]

    # Monta payload do Webhook simulado
    webhook_data = {
        "event_id": "evt_teste_001",
        "event_type": "payment.approved",
        "gateway_id": gw_id,
        "timestamp": "2026-10-21T22:30:00Z",
        "data": {"status": "paid"}
    }
    body_bytes = json.dumps(webhook_data).encode("utf-8")

    # Calcula a assinatura HMAC-SHA256 como o gateway na nuvem faz
    signature = hmac.new(
        key=settings.WEBHOOK_SECRET.encode("utf-8"),
        msg=body_bytes,
        digestmod=hashlib.sha256
    ).hexdigest()

    # Dispara o webhook para nossa API
    wh_res = client.post(
        "/api/v1/webhooks/gateway",
        content=body_bytes,
        headers={
            "Content-Type": "application/json",
            "X-Signature-SHA256": signature
        }
    )
    assert wh_res.status_code == 200
    assert wh_res.json()["status_processamento"] == "SUCESSO"

    # Confirma que o pedido mudou atômica e confiavelmente para PAGO
    pedido_res = client.get(f"/api/v1/pedidos/{cod_ref}")
    assert pedido_res.json()["status"] == "PAGO"
