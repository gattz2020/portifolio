"""
LeadHunter & Data Scraper v1.0.0
Aplicação CLI de Automação Comercial e Web Scraping em Python 3.12
"""

import argparse
import sys
import os
from scraper import LeadScraper
from exporter import DataExporter
from notifier import Notifier

def exibir_banner():
    banner = """
========================================================================
   __                     _ _   _             _             
  / /  ___  __ _  __| | | | |_   _ _ __ | |_ ___ _ __ 
 / /  / _ \/ _` |/ _` | |_| | | | | '_ \| __/ _ \ '__|
/ /__|  __/ (_| | (_| |  _  | |_| | | | | ||  __/ |   
\____/\___|\__,_|\__,_|_| |_|\__,_|_| |_|\__\___|_|   
          Robô de Prospecção & Automação B2B (Python 3.12)
========================================================================
"""
    print(banner)

def main():
    exibir_banner()

    parser = argparse.ArgumentParser(
        description="LeadHunter CLI - Automação de Coleta e Qualificação de Contatos Comerciais"
    )
    parser.add_argument(
        "--segmento", "-s",
        type=str,
        default="Clínicas Odontológicas",
        help="Nicho de atuação das empresas desejadas (Ex: 'Advogados', 'Restaurantes', 'Clínicas')"
    )
    parser.add_argument(
        "--cidade", "-c",
        type=str,
        default="Sao Paulo",
        help="Cidade/região da busca (Ex: 'Sao Paulo', 'Rio de Janeiro', 'Curitiba')"
    )
    parser.add_argument(
        "--limite", "-l",
        type=int,
        default=5,
        help="Quantidade de leads a coletar (Padrão: 5)"
    )
    parser.add_argument(
        "--formato", "-f",
        choices=["csv", "json", "ambos"],
        default="ambos",
        help="Formato de exportação dos dados (csv, json ou ambos)"
    )
    parser.add_argument(
        "--notificar", "-n",
        action="store_true",
        help="Simula o disparo de webhook de notificação para canal comercial"
    )

    args = parser.parse_args()

    # 1. Coleta
    scraper = LeadScraper(delay_segundos=0.3)
    leads = scraper.coletar_leads(
        segmento=args.segmento,
        cidade=args.cidade,
        limite=args.limite
    )

    if not leads:
        print("[AVISO] Nenhum lead encontrado com os filtros fornecidos.")
        sys.exit(0)

    # 2. Exportação
    pasta_saida = os.path.join(os.path.dirname(__file__), "output")
    nome_base = f"leads_{args.segmento.lower().replace(' ', '_')}_{args.cidade.lower().replace(' ', '_')}"
    arquivo_gerado = ""

    if args.formato in ["csv", "ambos"]:
        caminho_csv = os.path.join(pasta_saida, f"{nome_base}.csv")
        arquivo_gerado = DataExporter.para_csv(leads, caminho_csv)

    if args.formato in ["json", "ambos"]:
        caminho_json = os.path.join(pasta_saida, f"{nome_base}.json")
        DataExporter.para_json(leads, caminho_json)

    # 3. Notificação
    if args.notificar:
        Notifier.simular_envio_telegram(
            segmento=args.segmento,
            cidade=args.cidade,
            total_leads=len(leads),
            arquivo_gerado=arquivo_gerado
        )

    print("========================================================================")
    print("✓ Pipeline de automação concluído com êxito!")
    print(f"✓ Arquivos disponíveis na pasta: {pasta_saida}")
    print("========================================================================")

if __name__ == "__main__":
    main()
