# 🤖 LeadHunter & Data Scraper (Python 3.12)

Robô inteligente de automação comercial e prospecção B2B em Python, desenvolvido para extrair dados públicos de empresas, higienizar contatos comerciais e exportar relatórios prontos para equipes de vendas.

---

## 🎯 Proposta de Valor Comercial

- **Economia de Tempo**: Elimina até 30 horas semanais de pesquisa manual de leads.
- **Higienização de Dados**: Padronização automática de telefones com DDD `(XX) XXXXX-XXXX` e validação regex de e-mails corporativos.
- **Exportação Multi-formato**: Gera saídas estruturadas em CSV (com separador `;` compatível com Excel brasileiro) e JSON.
- **Alertas Automatizados via Webhook**: Simula/envia notificações automáticas para grupos do Telegram/WhatsApp após o término do processamento.
- **Código com Testes Unitários**: Cobertura de testes garantindo estabilidade e integridade dos dados coletados.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.12+
- **Bibliotecas**: `dataclasses`, `re`, `argparse`, `csv`, `json`, `time`, `unittest`
- **Extensões de Produção**: `requests`, `beautifulsoup4`, `openpyxl` (listadas em `requirements.txt`)

---

## 🚀 Como Executar

### 1. Execução Rápida via Linha de Comando (CLI)

```bash
# Execução padrão (5 leads de Clínicas Odontológicas em São Paulo)
python main.py

# Coletando 10 contatos de Escritórios de Advocacia em Curitiba com notificação
python main.py --segmento "Advocacia" --cidade "Curitiba" --limite 10 --formato csv --notificar

# Ver todas as opções disponíveis
python main.py --help
```

### 2. Executar os Testes Unitários

```bash
python test_automation.py
```

---

## 💼 Pitch para Propostas no Workana / 99freelas

> *"Olá! Para a sua demanda de automação e coleta de dados, já possuo soluções validadas em Python como o **LeadHunter**, capaz de pesquisar, higienizar contatos (telefones e e-mails) e gerar planilhas em Excel/CSV de forma 100% autônoma. O código é modular, possui testes unitários e pode rodar com apenas 1 comando ou ser agendado na nuvem. Você pode conferir o repositório completo no meu GitHub: https://github.com/gattz2020/portifolio/tree/main/projects/03-automacao-scraper-bot"*
