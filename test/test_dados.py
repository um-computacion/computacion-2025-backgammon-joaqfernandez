from src.dados import Dados
import unittest
from unittest.mock import patch


class TestDados(unittest.TestCase):
    def test_dados_alatorios(self):
        dados = Dados()
        self.assertIn(dados.dado1, range(1, 7))
        self.assertIn(dados.dado2, range(1, 7))

    def test_tirar_dado_actualiza_valores(self):
        dados = Dados()
        antes = (dados.dado1, dados.dado2)
        despues = dados.tirar_dado()
        self.assertIn(despues[0], range(1, 7))
        self.assertIn(despues[1], range(1, 7))


if __name__ == "__main__":
    unittest.main()