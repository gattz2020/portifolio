# 💼 Portfólio Profissional de Desenvolvimento & Automação

Bem-vindo ao repositório central de projetos desenvolvidos para demonstração comercial em plataformas freelance (**Workana**, **99freelas**) e visibilidade técnica no **GitHub**.

---

## 🚀 Vitrine dos Projetos Desenvolvidos

| Projeto | Categoria | Tecnologias | Demonstração |
| :--- | :--- | :--- | :--- |
| **[Portfólio Hub](./hub/)** | Vitrine Central / Pessoal | Tailwind CSS, Lucide, JS ES6+ | [Abrir Hub](./hub/index.html) |
| **[01. NexusFlow](./projects/01-landing-page-nexus/)** | Landing Page de Alta Conversão | Tailwind CSS, Lucide, Simulador ROI | [Abrir Demo](./projects/01-landing-page-nexus/index.html) |
| **[02. Vanguard CRM](./projects/02-dashboard-gestao/)** | Dashboard Comercial & SaaS | Tailwind, Chart.js, LocalStorage, Export CSV | [Abrir Demo](./projects/02-dashboard-gestao/index.html) |
| **[03. LeadHunter Bot](./projects/03-automacao-scraper-bot/)** | Automação & Web Scraping | Python 3.12, CSV/JSON, Webhooks | [Ver Código & Testes](./projects/03-automacao-scraper-bot/) |

---

## 📂 Estrutura do Repositório

```text
portifolio/
├── hub/                          # 🌐 Site Principal de Portfólio com apresentação, contato e filtros
│   ├── index.html
│   ├── app.js
│   └── README.md
├── projects/
│   ├── 01-landing-page-nexus/    # 🚀 Landing page de produto SaaS com calculadora de ROI e FAQ
│   │   ├── index.html
│   │   ├── script.js
│   │   └── README.md
│   ├── 02-dashboard-gestao/      # 📊 Dashboard gerencial e CRM com gráficos interativos e tabela
│   │   ├── index.html
│   │   ├── dashboard.js
│   │   └── README.md
│   └── 03-automacao-scraper-bot/ # 🤖 Automação em Python para extração de leads, exportação e alertas
│       ├── main.py
│       ├── scraper.py
│       ├── exporter.py
│       ├── notifier.py
│       ├── test_automation.py
│       └── requirements.txt
├── docs/                         # 📝 Modelos de propostas comerciais para Workana e 99freelas
│   └── propostas-freelance.md
├── PORTFOLIO-STATUS.md           # 📌 Resumo de status, próximos passos e checklist para amanhã
└── .gitignore                    # Arquivos ignorados pelo Git
```

---

## ⚡ Como Visualizar Localmente Agora Mesmo

Não é necessária nenhuma instalação complexa para testar os projetos visuais:

1. **Pelo Navegador Direto**:
   - Dê um duplo clique no arquivo [`hub/index.html`](./hub/index.html) para abrir o portal completo.
   - A partir dele, você pode navegar e testar todas as páginas e demonstrações.

2. **Via Servidor Local (Node ou Python)**:
   ```bash
   # Com Python:
   python -m http.server 3000
   
   # Ou com npx:
   npx serve .
   ```
   Acesse: `http://localhost:3000/hub/`

3. **Executando a Automação Python**:
   ```bash
   cd projects/03-automacao-scraper-bot
   python main.py --segmento "Clínicas" --cidade "Curitiba" --limite 5 --notificar
   ```
   E para rodar os testes unitários:
   ```bash
   python test_automation.py
   ```

---

## 🎯 Próximos Passos (Checklist de Publicação)

- [ ] Ajustar o número do WhatsApp e links sociais nos arquivos `hub/index.html` e `hub/app.js`.
- [ ] Criar o repositório no seu GitHub (`git remote add origin ...`).
- [ ] Ativar o **GitHub Pages** para o repositório ficar online gratuitamente na internet.
- [ ] Cadastrar os links nas propostas do **Workana** e **99freelas** utilizando os modelos na pasta `docs/`.
