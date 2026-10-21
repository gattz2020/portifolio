// Dados iniciais de demonstração comercial
const initialClients = [
  { id: 1, nome: "Clínica Bem Estar", segmento: "Saúde & Estética", valor: 3500, status: "Ativo", responsavel: "Lucas Silva" },
  { id: 2, nome: "Distribuidora Alfa", segmento: "Logística / B2B", valor: 7800, status: "Ativo", responsavel: "Marina Rocha" },
  { id: 3, nome: "Soluções Contábeis Silva", segmento: "Serviços", valor: 2100, status: "Negociação", responsavel: "Lucas Silva" },
  { id: 4, nome: "Restaurante Villa Gourmet", segmento: "Gastronomia", valor: 1400, status: "Pendente", responsavel: "Ana Costa" },
  { id: 5, nome: "TechNova E-commerce", segmento: "Tecnologia", valor: 5200, status: "Ativo", responsavel: "Marina Rocha" },
  { id: 6, nome: "Academia Iron Fitness", segmento: "Fitness", valor: 1900, status: "Negociação", responsavel: "Ana Costa" }
];

let clients = JSON.parse(localStorage.getItem('vanguard_clients')) || initialClients;

document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) {
    lucide.createIcons();
  }
  initDashboardTheme();
  initSidebar();
  initCharts();
  renderTable();
  initSearchAndFilter();
  initClientForm();
});

// ==========================================
// TEMA DARK / LIGHT
// ==========================================
function initDashboardTheme() {
  const btn = document.getElementById('theme-btn');
  const icon = document.getElementById('theme-btn-icon');
  const html = document.documentElement;

  const isDark = localStorage.getItem('theme') === 'dark';
  if (isDark) {
    html.classList.add('dark');
    icon?.setAttribute('data-lucide', 'sun');
  } else {
    html.classList.remove('dark');
    icon?.setAttribute('data-lucide', 'moon');
  }
  if (window.lucide) lucide.createIcons();

  btn?.addEventListener('click', () => {
    const currentDark = html.classList.toggle('dark');
    localStorage.setItem('theme', currentDark ? 'dark' : 'light');
    icon?.setAttribute('data-lucide', currentDark ? 'sun' : 'moon');
    if (window.lucide) lucide.createIcons();
  });
}

// ==========================================
// SIDEBAR MOBILE
// ==========================================
function initSidebar() {
  const sidebar = document.getElementById('sidebar');
  const openBtn = document.getElementById('open-sidebar');
  const closeBtn = document.getElementById('close-sidebar');

  openBtn?.addEventListener('click', () => {
    sidebar.classList.toggle('hidden');
  });
  closeBtn?.addEventListener('click', () => {
    sidebar.classList.add('hidden');
  });
}

// ==========================================
// GRÁFICOS (CHART.JS)
// ==========================================
function initCharts() {
  // Gráfico de Linha - Receita
  const revCtx = document.getElementById('revenueChart')?.getContext('2d');
  if (revCtx) {
    new Chart(revCtx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out'],
        datasets: [{
          label: 'Faturamento (R$ mil)',
          data: [28, 31, 33, 37, 39, 41, 44, 45, 47, 48.7],
          borderColor: '#2563eb',
          backgroundColor: 'rgba(37, 99, 235, 0.08)',
          fill: true,
          tension: 0.35,
          borderWidth: 2.5,
          pointBackgroundColor: '#2563eb',
          pointRadius: 3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            grid: { color: 'rgba(156, 163, 175, 0.1)' },
            ticks: { font: { size: 10 } }
          },
          x: {
            grid: { display: false },
            ticks: { font: { size: 10 } }
          }
        }
      }
    });
  }

  // Gráfico Rosca - Origem de Clientes
  const chCtx = document.getElementById('channelChart')?.getContext('2d');
  if (chCtx) {
    new Chart(chCtx, {
      type: 'doughnut',
      data: {
        labels: ['Google Ads', 'Indicação', 'Instagram', 'Outros'],
        datasets: [{
          data: [45, 25, 20, 10],
          backgroundColor: ['#3b82f6', '#10b981', '#a855f7', '#f59e0b'],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        cutout: '72%'
      }
    });
  }
}

// ==========================================
// TABELA E FILTROS
// ==========================================
function renderTable(filterText = '', statusFilter = 'Todos') {
  const tbody = document.getElementById('clients-table-body');
  const countEl = document.getElementById('sidebar-badge-count');
  const kpiEl = document.getElementById('kpi-total-clients');
  if (!tbody) return;

  const filtered = clients.filter(c => {
    const matchesText = c.nome.toLowerCase().includes(filterText.toLowerCase()) ||
                        c.segmento.toLowerCase().includes(filterText.toLowerCase()) ||
                        c.responsavel.toLowerCase().includes(filterText.toLowerCase());
    const matchesStatus = statusFilter === 'Todos' || c.status === statusFilter;
    return matchesText && matchesStatus;
  });

  if (countEl) countEl.textContent = clients.length;
  if (kpiEl) kpiEl.textContent = 136 + clients.length;

  tbody.innerHTML = filtered.map(c => {
    let statusClass = "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800";
    if (c.status === "Negociação") {
      statusClass = "bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-400 border border-blue-200 dark:border-blue-800";
    } else if (c.status === "Pendente") {
      statusClass = "bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-400 border border-amber-200 dark:border-amber-800";
    }

    return `
      <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/40 transition-colors">
        <td class="px-6 py-4 font-semibold text-slate-900 dark:text-white flex items-center gap-2">
          <div class="w-7 h-7 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 flex items-center justify-center font-bold text-[11px]">
            ${c.nome.charAt(0)}
          </div>
          <span>${c.nome}</span>
        </td>
        <td class="px-6 py-4 text-slate-500 dark:text-slate-400">${c.segmento}</td>
        <td class="px-6 py-4 font-mono font-bold text-slate-800 dark:text-slate-200">R$ ${c.valor.toLocaleString('pt-BR')},00</td>
        <td class="px-6 py-4">
          <span class="px-2.5 py-1 rounded-full text-[11px] font-semibold ${statusClass}">
            ${c.status}
          </span>
        </td>
        <td class="px-6 py-4 text-slate-600 dark:text-slate-400">${c.responsavel}</td>
        <td class="px-6 py-4 text-right">
          <button onclick="deleteClient(${c.id})" class="text-rose-500 hover:text-rose-700 p-1 rounded-lg hover:bg-rose-50 dark:hover:bg-rose-950/50" title="Remover">
            <i data-lucide="trash-2" class="w-4 h-4"></i>
          </button>
        </td>
      </tr>
    `;
  }).join('');

  if (window.lucide) lucide.createIcons();
}

function initSearchAndFilter() {
  const searchInput = document.getElementById('search-input');
  const statusSelect = document.getElementById('status-filter');

  function handleFilter() {
    renderTable(searchInput.value, statusSelect.value);
  }

  searchInput?.addEventListener('input', handleFilter);
  statusSelect?.addEventListener('change', handleFilter);
}

// ==========================================
// MODAL & ADICIONAR CLIENTE
// ==========================================
function openModal() {
  document.getElementById('client-modal')?.classList.remove('hidden');
}

function closeModal() {
  document.getElementById('client-modal')?.classList.add('hidden');
}

function initClientForm() {
  const form = document.getElementById('new-client-form');
  form?.addEventListener('submit', (e) => {
    e.preventDefault();
    const nome = document.getElementById('m-nome').value;
    const segmento = document.getElementById('m-segmento').value;
    const valor = parseFloat(document.getElementById('m-valor').value) || 0;
    const status = document.getElementById('m-status').value;
    const responsavel = document.getElementById('m-responsavel').value;

    const newClient = {
      id: Date.now(),
      nome,
      segmento,
      valor,
      status,
      responsavel
    };

    clients.unshift(newClient);
    localStorage.setItem('vanguard_clients', JSON.stringify(clients));
    renderTable();
    closeModal();
    form.reset();
  });
}

function deleteClient(id) {
  if (confirm("Deseja realmente remover este registro de cliente?")) {
    clients = clients.filter(c => c.id !== id);
    localStorage.setItem('vanguard_clients', JSON.stringify(clients));
    renderTable();
  }
}

// ==========================================
// EXPORTAÇÃO EM CSV
// ==========================================
function exportToCSV() {
  let csvContent = "data:text/csv;charset=utf-8,";
  csvContent += "ID,Cliente,Segmento,Valor Mensal,Status,Responsavel\n";

  clients.forEach(c => {
    csvContent += `"${c.id}","${c.nome}","${c.segmento}","${c.valor}","${c.status}","${c.responsavel}"\n`;
  });

  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `relatorio_clientes_${new Date().toISOString().slice(0, 10)}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
