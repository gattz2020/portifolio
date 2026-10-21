// Inicia ícones do Lucide
document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) {
    lucide.createIcons();
  }
  initTheme();
  initFilters();
  initMobileMenu();
  initContactForm();
});

// ==========================================
// THEME CONTROLLER (Dark / Light Mode)
// ==========================================
function initTheme() {
  const themeToggle = document.getElementById('theme-toggle');
  const themeIcon = document.getElementById('theme-icon');
  const html = document.documentElement;

  // Check saved or system preference
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    html.classList.add('dark');
    updateThemeIcon(true);
  } else {
    html.classList.remove('dark');
    updateThemeIcon(false);
  }

  themeToggle?.addEventListener('click', () => {
    const isDark = html.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    updateThemeIcon(isDark);
  });
}

function updateThemeIcon(isDark) {
  const themeIcon = document.getElementById('theme-icon');
  if (!themeIcon) return;
  themeIcon.setAttribute('data-lucide', isDark ? 'sun' : 'moon');
  if (window.lucide) {
    lucide.createIcons();
  }
}

// ==========================================
// FILTROS DE PROJETOS
// ==========================================
function initFilters() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const cards = document.querySelectorAll('.project-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Toggle active style
      filterBtns.forEach(b => {
        b.classList.remove('active', 'bg-brand-600', 'text-white');
        b.classList.add('text-slate-600', 'dark:text-slate-300');
      });

      btn.classList.add('active', 'bg-brand-600', 'text-white');
      btn.classList.remove('text-slate-600', 'dark:text-slate-300');

      const category = btn.getAttribute('data-category');

      cards.forEach(card => {
        if (category === 'all' || card.getAttribute('data-category') === category) {
          card.classList.remove('hidden');
        } else {
          card.classList.add('hidden');
        }
      });
    });
  });
}

// ==========================================
// MOBILE MENU
// ==========================================
function initMobileMenu() {
  const btn = document.getElementById('mobile-menu-btn');
  const menu = document.getElementById('mobile-menu');

  btn?.addEventListener('click', () => {
    menu?.classList.toggle('hidden');
  });

  menu?.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      menu?.classList.add('hidden');
    });
  });
}

// ==========================================
// FORMULÁRIO DE CONTATO DIRETO VIA WHATSAPP
// ==========================================
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const name = document.getElementById('contact-name')?.value || '';
    const detail = document.getElementById('contact-detail')?.value || '';
    const service = document.getElementById('contact-service')?.value || '';
    const msg = document.getElementById('contact-msg')?.value || '';

    // Telefone configurado do desenvolvedor
    const telefoneDestino = '5562985099185';

    const texto = `Olá! Meu nome é ${encodeURIComponent(name)}.
Contato: ${encodeURIComponent(detail)}
Interesse: ${encodeURIComponent(service)}
Detalhes: ${encodeURIComponent(msg)}
(Enviado através do Portfólio Hub)`;

    const whatsappUrl = `https://api.whatsapp.com/send?phone=${telefoneDestino}&text=${texto}`;
    window.open(whatsappUrl, '_blank');
  });
}

// ==========================================
// MODAL DE AUTOMAÇÃO / PYTHON
// ==========================================
function openPythonModal() {
  const modal = document.getElementById('python-modal');
  modal?.classList.remove('hidden');
}

function closePythonModal() {
  const modal = document.getElementById('python-modal');
  modal?.classList.add('hidden');
}
