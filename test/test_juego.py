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
        juego = BackgammonGame("joaquin", "martin")
        
        self.assertEqual(juego.jugador1.nombre, "joaquin")
        self.assertEqual(juego.jugador1.color, "BLANCO")
        self.assertEqual(juego.jugador2.nombre, "martin")
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
        juego = BackgammonGame("joaquin", "martin")
        
        primer_jugador = juego.determinar_primer_turno()
        self.assertIn(primer_jugador, [juego.jugador1, juego.jugador2])
        self.assertIsInstance(primer_jugador, Jugador)

    def test_iniciar_juego_asigna_turno(self):
        juego = BackgammonGame("joaquin", "martin")
        juego.iniciar_juego()
        
        self.assertIsNotNone(juego.turno_actual)
        self.assertIn(juego.turno_actual, [juego.jugador1, juego.jugador2])
    
    def test_cambiar_turno(self):
        juego = BackgammonGame("joaquin", "martin")
        juego.iniciar_juego()
        
        turno_inicial = juego.turno_actual
        juego.cambiar_turno()
        self.assertNotEqual(juego.turno_actual, turno_inicial)
        
        juego.cambiar_turno()  
        self.assertEqual(juego.turno_actual, turno_inicial)
    
    def test_cambiar_turno_limpia_dados(self):
        juego = BackgammonGame("joaquin", "martin")
        juego.iniciar_juego()
        juego.tirar_dados()
        
        self.assertGreater(len(juego.dados_disponibles), 0)
        
        juego.cambiar_turno()
        
        self.assertEqual(juego.dados_disponibles, [])


class TestBackgammonGameDados(unittest.TestCase):
    
    def test_tirar_dados_normal(self):
        juego = BackgammonGame("joaquin", "martin")
        
        dado1, dado2 = juego.tirar_dados()
        
        self.assertGreaterEqual(dado1, 1)
        self.assertLessEqual(dado1, 6)
        self.assertGreaterEqual(dado2, 1)
        self.assertLessEqual(dado2, 6)
        self.assertIn(len(juego.dados_disponibles), [2, 4])
    

    def test_tirar_dados_dobles_cuatro_movimientos(self):
        juego = BackgammonGame("joaquin", "martin")
        
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
        juego = BackgammonGame("joaquin", "martin")
        juego.tirar_dados()
        
        dados_iniciales = len(juego.dados_disponibles)
        valor_usado = juego.dados_disponibles[0]
        
        juego.usar_dado(valor_usado)
        
        self.assertEqual(len(juego.dados_disponibles), dados_iniciales - 1)
    

    def test_usar_dado_no_disponible_lanza_error(self):
        juego = BackgammonGame("joaquin", "martin")
        
        with self.assertRaises(ValueError) as context:
            juego.usar_dado(7)
        
        self.assertIn("no está disponible", str(context.exception))
    
    def test_tiene_dados_disponibles_con_dados(self):
        juego = BackgammonGame("joaquin", "martin")
        
        self.assertFalse(juego.tiene_dados_disponibles())
        
        juego.tirar_dados()
        self.assertTrue(juego.tiene_dados_disponibles())
    
    def test_usar_todos_los_dados(self):
        juego = BackgammonGame("joaquin", "martin")
        juego.tirar_dados()
        
        # Usar todos los dados
        while juego.tiene_dados_disponibles():
            juego.usar_dado(juego.dados_disponibles[0])
        
        self.assertFalse(juego.tiene_dados_disponibles())
        self.assertEqual(len(juego.dados_disponibles), 0)

class TestBackgammonGameMovimientos(unittest.TestCase):
    
    def test_realizar_movimiento_sin_dados_lanza_error(self):
        juego = BackgammonGame("joaquin", "martin")
        juego.iniciar_juego()
        
        with self.assertRaises(ValueError):
            juego.realizar_movimiento(0, 3)
    
    def test_obtener_movimientos_legales_sin_dados_retorna_vacio(self):
        juego = BackgammonGame("joaquin", "martin")
        juego.iniciar_juego()
        
        movimientos = juego.obtener_movimientos_legales()
        self.assertEqual(movimientos, [])
    
    def test_obtener_movimientos_legales_con_dados_retorna_lista(self):
        juego = BackgammonGame("joaquin", "martin")
        juego.iniciar_juego()
        juego.tirar_dados()
        
        movimientos = juego.obtener_movimientos_legales()
        self.assertIsInstance(movimientos, list)

    def test_puede_realizar_movimiento_sin_dados_retorna_false(self):
        juego = BackgammonGame("joaquin", "martin")
        juego.iniciar_juego()
        
        self.assertFalse(juego.puede_realizar_movimiento())
    
    def test_puede_realizar_movimiento_con_dados_retorna_bool(self):
        juego = BackgammonGame("joaquin", "martin")
        juego.iniciar_juego()
        juego.tirar_dados()
        
        puede_mover = juego.puede_realizar_movimiento()
        self.assertIsInstance(puede_mover, bool)
    
    def test_realizar_movimiento_dado_no_disponible(self):
        juego = BackgammonGame("joaquin", "martin")
        juego.iniciar_juego()
        juego.tirar_dados()
        
        # Intentar usar un dado que definitivamente no está
        dado_invalido = 10
        
        with self.assertRaises(ValueError) as context:
            juego.realizar_movimiento(0, dado_invalido)
        
        self.assertIn("no está disponible", str(context.exception))


class TestBackgammonGameVictoria(unittest.TestCase):    
    def test_verificar_victoria_inicial_sin_ganador(self):
        juego = BackgammonGame("joaquin", "martin")
        juego.iniciar_juego()
        
        self.assertFalse(juego.verificar_victoria())
        self.assertIsNone(juego.ganador)
    
    def test_esta_terminado_inicial_retorna_false(self):
        juego = BackgammonGame("joaquin", "martin")
        
        self.assertFalse(juego.esta_terminado())
    
    def test_verificar_victoria_con_15_fichas_fuera(self):
        juego = BackgammonGame("joaquin", "martin")
        juego.iniciar_juego()
        
        # Simular que un jugador sacó todas las fichas
        color = juego.turno_actual.color
        juego.tablero._Tablero__fichas_fuera__[color] = 15
        
        self.assertTrue(juego.verificar_victoria())
        self.assertEqual(juego.ganador, juego.turno_actual)
        self.assertTrue(juego.esta_terminado())
    
    def test_esta_terminado_con_ganador_retorna_true(self):
        juego = BackgammonGame("joaquin", "martin")
        juego.iniciar_juego()
        
        # Forzar ganador
        color = juego.turno_actual.color
        juego.tablero._Tablero__fichas_fuera__[color] = 15
        juego.verificar_victoria()
        
        self.assertTrue(juego.esta_terminado())

if __name__ == "__main__":
    unittest.main()
