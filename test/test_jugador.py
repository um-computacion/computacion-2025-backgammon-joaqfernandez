import unittest
from src.jugador import Jugador, ficha1, ficha2
from src.tablero import Tablero

class TestJugador(unittest.TestCase):
    def setUp(self):
        self.tablero = Tablero()
        self.blanco = Jugador("Joaquin", ficha1)
        self.negro = Jugador("Profe Walter", ficha2)

    def test_direccion(self):
        self.assertEqual(self.blanco.direccion(self.tablero), -1)
        self.assertEqual(self.negro.direccion(self.tablero), +1)

    def test_movimientos_legales_funcione(self):
        dados = [1, 2]
        movim_jug1 = self.blanco.movimientos_legales(self.tablero, dados)
        movim_jug2 = self.negro.movimientos_legales(self.tablero, dados)
        self.assertIsInstance(movim_jug1, list)
        self.assertIsInstance(movim_jug2, list)


if __name__ == "__main__":
    unittest.main()
