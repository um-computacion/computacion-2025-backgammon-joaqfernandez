import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from juego import BackgammonGame
from jugador import Jugador
from tablero import Tablero


class TestBackgammonGameInit(unittest.TestCase):
    
    def test_inicializacion_basica(self):
        juego = BackgammonGame("Alice", "Bob")
        
        self.assertEqual(juego.jugador1.nombre, "Alice")
        self.assertEqual(juego.jugador1.color, "BLANCO")
        self.assertEqual(juego.jugador2.nombre, "Bob")
        self.assertEqual(juego.jugador2.color, "NEGRO")
        self.assertIsNotNone(juego.tablero)
        self.assertIsNone(juego.ganador)
        self.assertIsNone(juego.turno_actual)

    def test_inicializacion_tablero(self):
        juego = BackgammonGame("Player1", "Player2")
        
        self.assertIsInstance(juego.tablero, Tablero)
        puntos = juego.tablero.obtener_puntos()
        self.assertEqual(len(puntos), 24)  

    def test_dados_disponibles_inicialmente_vacio(self):
        juego = BackgammonGame("Player1", "Player2")
        
        self.assertEqual(juego.dados_disponibles, [])
        self.assertFalse(juego.tiene_dados_disponibles())