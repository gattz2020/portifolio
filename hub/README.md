# 🌐 Portfólio Hub - Vitrine Profissional

Site principal de apresentação profissional focado em conversão de clientes para **Workana**, **99freelas** e visibilidade técnica no **GitHub**.

---

## ✨ Recursos

- **Design Moderno & Responsivo**: Construído com Tailwind CSS e tipografia refinada (*Plus Jakarta Sans* e *JetBrains Mono*).
- **Tema Escuro / Claro**: Alternador automático sincronizado com as preferências do sistema e persistido em `localStorage`.
- **Filtros por Categoria**: Alterna rapidamente entre Landing Pages, Dashboards/SaaS e Automações em Python.
- **Botão Direto de WhatsApp**: Formulário de orçamento que formata e envia a mensagem pronta para o seu WhatsApp.
- **Performance Máxima**: Carregamento instantâneo sem necessidade de etapa complexa de build.

---

## 🚀 Como Executar Localmente

Você pode abrir o arquivo `index.html` diretamente em qualquer navegador, ou usar um servidor local simples:

### Usando extensão Live Server (VS Code):
Basta clicar com o botão direito no `index.html` e selecionar **"Open with Live Server"**.

### Usando Node.js (npx serve):
```bash
npx serve hub
```

### Usando Python:
```bash
python -m http.server 3000 --directory hub
```
Acesse em: `http://localhost:3000`

---

## 🛠️ Como Personalizar

1. **Seu Nome e Contatos**:
   - Abra `index.html` e substitua "DevPortfolio" pelo seu nome ou marca.
   - Atualize os links para o seu perfil no Workana, 99freelas e GitHub.
2. **Seu Número do WhatsApp**:
   - No `index.html` e em `app.js`, substitua `5511999999999` pelo seu DDD + número real do WhatsApp (ex: `5511987654321`).

---

## 📦 Como Publicar Gratuitamente

### 1. GitHub Pages (Recomendado)
- No seu repositório no GitHub, vá em **Settings** > **Pages**.
- Em **Source**, selecione a branch `main` e a pasta `/root` ou configure para a pasta `hub`.

### 2. Vercel / Netlify
- Basta conectar o repositório na [Vercel](https://vercel.com) ou [Netlify](https://netlify.com) e definir o diretório raiz como `hub`.
- A publicação é automática a cada commit!
