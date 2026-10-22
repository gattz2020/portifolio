let currentOrder = null;
let currentGatewayId = null;
let pollingInterval = null;

document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) {
    lucide.createIcons();
  }
  initCheckout();
});

function initCheckout() {
  const form = document.getElementById('checkout-form');
  form?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('cust-name').value;
    const email = document.getElementById('cust-email').value;
    const cpf = document.getElementById('cust-cpf').value;

    const payload = {
      cliente: { nome: name, email: email, cpf: cpf },
      descricao: "Assinatura CloudPay Nexus Pro",
      valor: 149.90,
      expiracao_minutos: 30
    };

    // Tenta conectar à API FastAPI local ou na nuvem
    try {
      const response = await fetch('http://localhost:8000/api/v1/pagamentos/pix', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Idempotency-Key': 'idemp_' + Date.now()
        },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        const data = await response.json();
        exibirPix(data);
        return;
      }
    } catch (err) {
      console.log("API backend offline. Utilizando motor emulado cliente para visualização estática no GitHub Pages.");
    }

    // Fallback Inteligente (Garante funcionamento mesmo estático no GitHub Pages)
    const mockRef = "ORD-" + Math.random().toString(36).substring(2, 10).toUpperCase();
    const mockGateway = "gw_" + Math.random().toString(36).substring(2, 12);
    const mockPixCopiaCola = "00020126580014br.gov.bcb.pix0136financeiro@minhaempresa.com.br5204000053039865406149.905802BR5925CLOUDPAY SOLUCOES DIGITA6007GOIANIA62190515TX1234567890126304C8A2";
    
    // QR Code visual gerado dinamicamente via API pública QR Code
    const qrImgUrl = `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=${encodeURIComponent(mockPixCopiaCola)}`;

    const mockData = {
      codigo_referencia: mockRef,
      valor_total: 149.90,
      transacao: {
        gateway_id: mockGateway,
        pix_copia_e_cola: mockPixCopiaCola,
        pix_qr_code_base64: qrImgUrl
      }
    };
    exibirPix(mockData);
  });
}

function exibirPix(data) {
  currentOrder = data.codigo_referencia;
  currentGatewayId = data.transacao.gateway_id;

  document.getElementById('label-ref').textContent = currentOrder;
  document.getElementById('pix-copy-input').value = data.transacao.pix_copia_e_cola;
  document.getElementById('pix-qr-img').src = data.transacao.pix_qr_code_base64;

  document.getElementById('step-form').classList.add('hidden');
  document.getElementById('step-pix').classList.remove('hidden');

  if (window.lucide) lucide.createIcons();

  // Inicia polling para verificar se o backend aprovou
  iniciarPolling();
}

function copiarPix() {
  const input = document.getElementById('pix-copy-input');
  input.select();
  input.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(input.value);

  const copyText = document.getElementById('copy-btn-text');
  copyText.textContent = "Copiado!";
  setTimeout(() => {
    copyText.textContent = "Copiar";
  }, 2000);
}

async function simularAprovacao() {
  const btn = document.getElementById('btn-simular');
  btn.disabled = true;
  btn.textContent = "Disparando Webhook no Servidor...";

  try {
    const res = await fetch(`http://localhost:8000/api/v1/pagamentos/simular-aprovacao/${currentGatewayId}`, {
      method: 'POST'
    });
    if (res.ok) {
      finalizarComSucesso();
      return;
    }
  } catch (e) {
    // Modo simulação local / GitHub Pages
  }

  setTimeout(() => {
    finalizarComSucesso();
  }, 800);
}

function iniciarPolling() {
  if (pollingInterval) clearInterval(pollingInterval);

  pollingInterval = setInterval(async () => {
    if (!currentOrder) return;
    try {
      const res = await fetch(`http://localhost:8000/api/v1/pedidos/${currentOrder}`);
      if (res.ok) {
        const orderData = await res.json();
        if (orderData.status === "PAGO") {
          clearInterval(pollingInterval);
          finalizarComSucesso();
        }
      }
    } catch (e) {
      // Ignora erro se estiver em modo offline
    }
  }, 3000);
}

function finalizarComSucesso() {
  if (pollingInterval) clearInterval(pollingInterval);

  document.getElementById('step-pix').classList.add('hidden');
  document.getElementById('step-success').classList.remove('hidden');

  document.getElementById('success-order-id').textContent = currentOrder || "ORD-DEMO99";
  document.getElementById('success-time').textContent = new Date().toLocaleString('pt-BR');

  if (window.lucide) lucide.createIcons();
}

function reiniciarCheckout() {
  document.getElementById('step-success').classList.add('hidden');
  document.getElementById('step-form').classList.remove('hidden');
  document.getElementById('label-ref').textContent = "GERANDO...";
  currentOrder = null;
  currentGatewayId = null;
}
