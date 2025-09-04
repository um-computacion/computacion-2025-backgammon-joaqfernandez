from src.dados import Dados
import unittest
from unittest.mock import patch


class TestDados(unittest.TestCase):
    def test_dados_alatorios(self):
        dados = Dados()
        self.assertIn(dados.dado1 range(1, 7))
        self.assertIn(dados.dado2, range(1, 7))