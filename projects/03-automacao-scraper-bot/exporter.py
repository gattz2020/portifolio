"""
Módulo de Exportação de Dados
Exporta os dados higienizados para CSV, JSON e relatórios de auditoria.
"""

import csv
import json
import os
from dataclasses import asdict
from typing import List
from scraper import LeadData

class DataExporter:
    @staticmethod
    def para_csv(leads: List[LeadData], caminho_arquivo: str) -> str:
        """Exporta a lista de leads para um arquivo CSV formatado em UTF-8 com delimitador ponto e vírgula (padrão Excel BR)."""
        os.makedirs(os.path.dirname(os.path.abspath(caminho_arquivo)), exist_ok=True)
        
        campos = [
            "Razao Social", "Nome Fantasia", "Segmento", "Cidade", "Estado",
            "Telefone", "Email", "Website", "Status Validacao"
        ]

        with open(caminho_arquivo, mode="w", newline="", encoding="utf-8-sig") as f:
            escritor = csv.writer(f, delimiter=";")
            escritor.writerow(campos)

            for lead in leads:
                escritor.writerow([
                    lead.razao_social,
                    lead.nome_fantasia,
                    lead.segmento,
                    lead.cidade,
                    lead.estado,
                    lead.telefone,
                    lead.email,
                    lead.website,
                    lead.status_validacao
                ])

        print(f"[EXPORTER] Arquivo CSV salvo com sucesso em: {caminho_arquivo}")
        return caminho_arquivo

    @staticmethod
    def para_json(leads: List[LeadData], caminho_arquivo: str) -> str:
        """Exporta os leads como array JSON estruturado."""
        os.makedirs(os.path.dirname(os.path.abspath(caminho_arquivo)), exist_ok=True)
        
        dados = [asdict(lead) for lead in leads]
        with open(caminho_arquivo, mode="w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

        print(f"[EXPORTER] Arquivo JSON estruturado salvo em: {caminho_arquivo}")
        return caminho_arquivo
