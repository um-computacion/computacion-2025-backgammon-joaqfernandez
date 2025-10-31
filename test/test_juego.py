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

class TestBackgammonGameTurnos(unittest.TestCase):
    
    def test_determinar_primer_turno(self):
        juego = BackgammonGame("Alice", "Bob")
        
        primer_jugador = juego.determinar_primer_turno()
        self.assertIn(primer_jugador, [juego.jugador1, juego.jugador2])
        self.assertIsInstance(primer_jugador, Jugador)

    def test_iniciar_juego_asigna_turno(self):
        juego = BackgammonGame("Alice", "Bob")
        juego.iniciar_juego()
        
        self.assertIsNotNone(juego.turno_actual)
        self.assertIn(juego.turno_actual, [juego.jugador1, juego.jugador2])
    
    def test_cambiar_turno(self):
        juego = BackgammonGame("Alice", "Bob")
        juego.iniciar_juego()
        
        turno_inicial = juego.turno_actual
        juego.cambiar_turno()
        self.assertNotEqual(juego.turno_actual, turno_inicial)
        
        juego.cambiar_turno()  
        self.assertEqual(juego.turno_actual, turno_inicial)
    
    def test_cambiar_turno_limpia_dados(self):
        juego = BackgammonGame("Alice", "Bob")
        juego.iniciar_juego()
        juego.tirar_dados()
        
        self.assertGreater(len(juego.dados_disponibles), 0)
        
        juego.cambiar_turno()
        
        self.assertEqual(juego.dados_disponibles, [])


class TestBackgammonGameDados(unittest.TestCase):
    
    def test_tirar_dados_normal(self):
        juego = BackgammonGame("Alice", "Bob")
        
        dado1, dado2 = juego.tirar_dados()
        
        self.assertGreaterEqual(dado1, 1)
        self.assertLessEqual(dado1, 6)
        self.assertGreaterEqual(dado2, 1)
        self.assertLessEqual(dado2, 6)
        self.assertIn(len(juego.dados_disponibles), [2, 4])
    

    def test_tirar_dados_dobles_cuatro_movimientos(self):
        juego = BackgammonGame("Alice", "Bob")
        
        # Probar múltiples veces hasta obtener dobles
        encontrado_dobles = False
        for _ in range(100):
            dado1, dado2 = juego.tirar_dados()
            if dado1 == dado2:
                self.assertEqual(len(juego.dados_disponibles), 4)
                self.assertTrue(all(d == dado1 for d in juego.dados_disponibles))
                encontrado_dobles = True
                break
        
        # Si no encontramos dobles, verificar dados normales
        if not encontrado_dobles:
            juego2 = BackgammonGame("Test1", "Test2")
            d1, d2 = juego2.tirar_dados()
            if d1 != d2:
                self.assertEqual(len(juego2.dados_disponibles), 2)
    
    def test_usar_dado_reduce_disponibles(self):
        juego = BackgammonGame("Alice", "Bob")
        juego.tirar_dados()
        
        dados_iniciales = len(juego.dados_disponibles)
        valor_usado = juego.dados_disponibles[0]
        
        juego.usar_dado(valor_usado)
        
        self.assertEqual(len(juego.dados_disponibles), dados_iniciales - 1)
    

    def test_usar_dado_no_disponible_lanza_error(self):
        juego = BackgammonGame("Alice", "Bob")
        
        with self.assertRaises(ValueError) as context:
            juego.usar_dado(7)
        
        self.assertIn("no está disponible", str(context.exception))
    
    def test_tiene_dados_disponibles_con_dados(self):
        juego = BackgammonGame("Alice", "Bob")
        
        self.assertFalse(juego.tiene_dados_disponibles())
        
        juego.tirar_dados()
        self.assertTrue(juego.tiene_dados_disponibles())
    
    def test_usar_todos_los_dados(self):
        juego = BackgammonGame("Alice", "Bob")
        juego.tirar_dados()
        
        # Usar todos los dados
        while juego.tiene_dados_disponibles():
            juego.usar_dado(juego.dados_disponibles[0])
        
        self.assertFalse(juego.tiene_dados_disponibles())
        self.assertEqual(len(juego.dados_disponibles), 0)


if __name__ == "__main__":
    unittest.main()
