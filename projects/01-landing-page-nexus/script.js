document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) {
    lucide.createIcons();
  }
  initRoiCalculator();
  initFaqAccordion();
  initLeadForm();
});

// ==========================================
// SIMULADOR DE ROI DINÂMICO
// ==========================================
function initRoiCalculator() {
  const leadsSlider = document.getElementById('leads-slider');
  const ticketSlider = document.getElementById('ticket-slider');
  const leadsVal = document.getElementById('leads-val');
  const ticketVal = document.getElementById('ticket-val');
  const horasEl = document.getElementById('horas-economizadas');
  const faturamentoEl = document.getElementById('faturamento-extra');

  if (!leadsSlider || !ticketSlider) return;

  function recalculate() {
    const leads = parseInt(leadsSlider.value, 10);
    const ticket = parseInt(ticketSlider.value, 10);

    leadsVal.textContent = `${leads.toLocaleString('pt-BR')} leads`;
    ticketVal.textContent = `R$ ${ticket.toLocaleString('pt-BR')},00`;

    // Cálculo estimado:
    // Média de 15 minutos economizados por lead em triagem/resposta manual = leads * 0.25h
    const horasEconomizadas = Math.round(leads * 0.24);
    
    // Supondo aumento conservador de conversão de 6% sobre os leads com resposta instantânea
    const novosClientes = Math.round(leads * 0.06);
    const faturamentoExtra = novosClientes * ticket;

    horasEl.textContent = `${horasEconomizadas}h`;
    faturamentoEl.textContent = `R$ ${faturamentoExtra.toLocaleString('pt-BR')}`;
  }

  leadsSlider.addEventListener('input', recalculate);
  ticketSlider.addEventListener('input', recalculate);
  recalculate();
}

// ==========================================
// FAQ ACCORDION
// ==========================================
function initFaqAccordion() {
  const faqButtons = document.querySelectorAll('.faq-btn');

  faqButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const content = btn.nextElementSibling;
      const icon = btn.querySelector('i');
      const isHidden = content.classList.contains('hidden');

      // Fecha todos os outros
      document.querySelectorAll('.faq-content').forEach(c => c.classList.add('hidden'));
      document.querySelectorAll('.faq-btn i').forEach(i => i.style.transform = 'rotate(0deg)');

      if (isHidden) {
        content.classList.remove('hidden');
        if (icon) icon.style.transform = 'rotate(180deg)';
      }
    });
  });
}

// ==========================================
// FORMULÁRIO DE CAPTURA RÁPIDA
// ==========================================
function initLeadForm() {
  const form = document.getElementById('lead-form');
  const successMsg = document.getElementById('lead-success');

  form?.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById('lead-email')?.value;
    if (email) {
      form.classList.add('opacity-50', 'pointer-events-none');
      setTimeout(() => {
        form.classList.add('hidden');
        successMsg?.classList.remove('hidden');
      }, 600);
    }
  });
}
