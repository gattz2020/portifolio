"""
Testes Unitários do Robô de Automação e Scraping
Executa validações sobre formatação de dados, coleta e exportação.
"""

import unittest
import os
import shutil
from scraper import LeadScraper
from exporter import DataExporter

class TestLeadHunter(unittest.TestCase):
    def setUp(self):
        self.scraper = LeadScraper(delay_segundos=0.01)
        self.test_dir = os.path.join(os.path.dirname(__file__), "test_output")
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_limpeza_telefone(self):
        tel_11_digitos = "11988887777"
        formatado = self.scraper._limpar_telefone(tel_11_digitos)
        self.assertEqual(formatado, "(11) 98888-7777")

    def test_validacao_email(self):
        self.assertTrue(self.scraper._validar_email("contato@empresa.com.br"))
        self.assertFalse(self.scraper._validar_email("email-invalido-sem-arroba.com"))

    def test_coleta_leads(self):
        leads = self.scraper.coletar_leads(segmento="Tecnologia", cidade="Sao Paulo", limite=3)
        self.assertEqual(len(leads), 3)
        self.assertEqual(leads[0].segmento, "Tecnologia")
        self.assertEqual(leads[0].cidade, "Sao Paulo")

    def test_exportacao_csv_e_json(self):
        leads = self.scraper.coletar_leads(segmento="Teste", cidade="Curitiba", limite=2)
        
        csv_path = os.path.join(self.test_dir, "teste.csv")
        json_path = os.path.join(self.test_dir, "teste.json")

        DataExporter.para_csv(leads, csv_path)
        DataExporter.para_json(leads, json_path)

        self.assertTrue(os.path.exists(csv_path))
        self.assertTrue(os.path.exists(json_path))
        self.assertGreater(os.path.getsize(csv_path), 0)
        self.assertGreater(os.path.getsize(json_path), 0)

if __name__ == "__main__":
    unittest.main()
