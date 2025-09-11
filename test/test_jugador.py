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