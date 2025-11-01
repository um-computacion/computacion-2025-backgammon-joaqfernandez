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

    def test_realizar_movimiento_desde_barra_exitoso(self):
        juego = BackgammonGame("Player1", "Player2")
        juego.iniciar_juego()
        
        # Forzar turno a BLANCO y poner ficha en barra
        juego._BackgammonGame__turno_actual__ = juego.jugador1  # BLANCO
        juego.tablero._Tablero__barra__["BLANCO"] = 1
        
        # Tirar dados para tener dados disponibles
        juego._BackgammonGame__dados_disponibles__ = [2, 3]
        
        # Realizar movimiento desde barra (dado 2 -> punto 22)
        resultado = juego.realizar_movimiento(-1, 2)
        
        # Verificaciones
        self.assertTrue(resultado)
        self.assertEqual(juego.tablero.fichas_en_barra("BLANCO"), 0)
        self.assertNotIn(2, juego.dados_disponibles)

    def test_realizar_movimiento_desde_barra_sin_fichas_lanza_error(self):
        juego = BackgammonGame("Player1", "Player2")
        juego.iniciar_juego()
        juego._BackgammonGame__dados_disponibles__ = [3, 4]
        
        # NO hay fichas en la barra
        self.assertEqual(juego.tablero.fichas_en_barra(juego.turno_actual.color), 0)
        
        with self.assertRaises(ValueError) as context:
            juego.realizar_movimiento(-1, 3)
        
        self.assertIn("No hay fichas en la barra", str(context.exception))

    def test_realizar_movimiento_reingreso_bloqueado_lanza_error(self):
        juego = BackgammonGame("Player1", "Player2")
        juego.iniciar_juego()
        
        # Forzar turno a NEGRO y poner ficha en barra
        juego._BackgammonGame__turno_actual__ = juego.jugador2  # NEGRO
        juego.tablero.__barra__["NEGRO"] = 1
        juego._BackgammonGame__dados_disponibles__ = [6]
        
        # Punto 5 tiene 5 fichas BLANCAS (bloqueado para NEGRO)
        # Dado 6 intenta entrar en punto 5 (6-1=5)
        
        with self.assertRaises(ValueError) as context:
            juego.realizar_movimiento(-1, 6)
        
        self.assertIn("No se puede reingresar", str(context.exception))

    def test_realizar_movimiento_regular_exitoso(self):
        juego = BackgammonGame("Player1", "Player2")
        juego.iniciar_juego()
        
        # Forzar turno a BLANCO
        juego._BackgammonGame__turno_actual__ = juego.jugador1  # BLANCO
        juego._BackgammonGame__dados_disponibles__ = [3, 5]
        
        # Verificar estado inicial punto 23 (tiene 2 fichas blancas)
        puntos_antes = juego.tablero.obtener_puntos()
        cantidad_antes = puntos_antes[23]["cantidad"]
        
        # Mover desde punto 23 con dado 3 (23 -> 20)
        resultado = juego.realizar_movimiento(23, 3)
        
        # Verificaciones
        self.assertTrue(resultado)
        puntos_despues = juego.tablero.obtener_puntos()
        self.assertEqual(puntos_despues[23]["cantidad"], cantidad_antes - 1)
        self.assertNotIn(3, juego.dados_disponibles)

    def test_realizar_movimiento_regular_invalido_lanza_error(self):
        juego = BackgammonGame("Player1", "Player2")
        juego.iniciar_juego()
        
        juego._BackgammonGame__dados_disponibles__ = [3, 4]
        
        # Intentar mover desde punto vacío (punto 1 está vacío)
        with self.assertRaises(ValueError) as context:
            juego.realizar_movimiento(1, 3)
        
        self.assertIn("Movimiento inválido", str(context.exception))

    def test_realizar_movimiento_consume_dado_correcto(self):
        juego = BackgammonGame("Player1", "Player2")
        juego.iniciar_juego()
        
        juego._BackgammonGame__turno_actual__ = juego.jugador1  # BLANCO
        juego._BackgammonGame__dados_disponibles__ = [2, 5]
        
        dados_antes = len(juego.dados_disponibles)
        
        # Realizar movimiento con dado 2
        juego.realizar_movimiento(23, 2)
        
        # Verificar que solo se consumió el dado 2
        self.assertEqual(len(juego.dados_disponibles), dados_antes - 1)
        self.assertNotIn(2, juego.dados_disponibles)
        self.assertIn(5, juego.dados_disponibles)

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
        
        color = juego.turno_actual.color
        juego.tablero._set_fichas_fuera_para_test(color, 15)  # ← Método público
        
        self.assertTrue(juego.verificar_victoria())
        self.assertEqual(juego.ganador, juego.turno_actual)
        self.assertTrue(juego.esta_terminado())
        
    def test_esta_terminado_con_ganador_retorna_true(self):
        juego = BackgammonGame("joaquin", "martin")
        juego.iniciar_juego()
        
        # Forzar ganador
        color = juego.turno_actual.color
        juego.tablero._set_fichas_fuera_para_test(color, 15)
        juego.verificar_victoria()
        
        self.assertTrue(juego.esta_terminado())


class TestBackgammonGameEstado(unittest.TestCase): 
    def test_obtener_estado_juego_inicial_tiene_claves_requeridas(self):
        juego = BackgammonGame("joaquin", "martin")
        
        estado = juego.obtener_estado_juego()
        self.assertIsInstance(estado, dict)
        self.assertIn("turno", estado)
        self.assertIn("color_turno", estado)
        self.assertIn("dados_disponibles", estado)
        self.assertIn("ganador", estado)
        self.assertIn("fichas_blanco_barra", estado)
        self.assertIn("fichas_negro_barra", estado)
        self.assertIn("fichas_blanco_fuera", estado)
        self.assertIn("fichas_negro_fuera", estado)
    
    def test_obtener_estado_juego_con_turno_iniciado(self):
        juego = BackgammonGame("joaquin", "martin")
        juego.iniciar_juego()
        
        estado = juego.obtener_estado_juego()
        self.assertIn(estado["turno"], ["joaquin", "martin"])
        self.assertIn(estado["color_turno"], ["BLANCO", "NEGRO"])
        self.assertIsNone(estado["ganador"])
    
    def test_obtener_estado_juego_con_dados_tirados(self):
        """Verifica el estado con dados tirados."""
        juego = BackgammonGame("joaquin", "martin")
        juego.iniciar_juego()
        juego.tirar_dados()
        
        estado = juego.obtener_estado_juego()
        self.assertGreater(len(estado["dados_disponibles"]), 0)
        self.assertTrue(all(1 <= d <= 6 for d in estado["dados_disponibles"]))
    
    def test_obtener_estado_fichas_iniciales_en_cero(self):
        juego = BackgammonGame("joaquin", "martin")
        
        estado = juego.obtener_estado_juego()
        self.assertEqual(estado["fichas_blanco_barra"], 0)
        self.assertEqual(estado["fichas_negro_barra"], 0)
        self.assertEqual(estado["fichas_blanco_fuera"], 0)
        self.assertEqual(estado["fichas_negro_fuera"], 0)

class TestBackgammonGameReiniciar(unittest.TestCase):
    """Tests para reiniciar el juego."""
    
    def test_reiniciar_juego_resetea_estado(self):
        juego = BackgammonGame("joaquin", "martin")
        juego.iniciar_juego()
        juego.tirar_dados()
        
        juego.reiniciar_juego()
        
        self.assertIsNone(juego.turno_actual)
        self.assertIsNone(juego.ganador)
        self.assertEqual(juego.dados_disponibles, [])
        self.assertIsInstance(juego.tablero, Tablero)
    
    def test_reiniciar_juego_crea_nuevo_tablero(self):
        juego = BackgammonGame("joaquin", "martin")
        tablero_original = juego.tablero
        
        juego.reiniciar_juego()
        
        self.assertIsNot(juego.tablero, tablero_original)

    def test_reiniciar_juego_con_ganador_establecido(self):
        juego = BackgammonGame("Player1", "Player2")
        juego.iniciar_juego()
        
        # Establecer un ganador
        color = juego.turno_actual.color
        juego.tablero._set_fichas_fuera_para_test(color, 15)
        juego.verificar_victoria()
        
        self.assertIsNotNone(juego.ganador)
        self.assertTrue(juego.esta_terminado())
        
        # Reiniciar
        juego.reiniciar_juego()
        
        # Verificar reset completo
        self.assertIsNone(juego.ganador)
        self.assertFalse(juego.esta_terminado())

    def test_reiniciar_juego_con_turno_y_dados_activos(self):
        juego = BackgammonGame("Player1", "Player2")
        juego.iniciar_juego()
        juego.tirar_dados()
        
        # Estado antes de reiniciar
        self.assertIsNotNone(juego.turno_actual)
        self.assertGreater(len(juego.dados_disponibles), 0)
        
        # Reiniciar
        juego.reiniciar_juego()
        
        # Verificar limpieza
        self.assertIsNone(juego.turno_actual)
        self.assertEqual(juego.dados_disponibles, [])

    def test_reiniciar_juego_restablece_tablero_estado_inicial(self):
        juego = BackgammonGame("Player1", "Player2")
        juego.iniciar_juego()
        juego.tirar_dados()
        
        # Hacer algunos movimientos para alterar el tablero
        if juego.puede_realizar_movimiento():
            movs = juego.obtener_movimientos_legales()
            if movs:
                origen, destino, dado = movs[0]
                try:
                    juego.realizar_movimiento(origen, dado)
                except:
                    pass
        
        # Reiniciar
        tablero_antes_id = id(juego.tablero)
        juego.reiniciar_juego()
        tablero_despues_id = id(juego.tablero)
        
        # Verificar que es un tablero nuevo
        self.assertNotEqual(tablero_antes_id, tablero_despues_id)
        
        # Verificar configuración inicial
        puntos = juego.tablero.obtener_puntos()
        self.assertEqual(puntos[0]["color"], "NEGRO")
        self.assertEqual(puntos[0]["cantidad"], 2)
        self.assertEqual(puntos[23]["color"], "BLANCO")
        self.assertEqual(puntos[23]["cantidad"], 2)

    def test_reiniciar_juego_mantiene_jugadores(self):
        juego = BackgammonGame("Joaquin", "Martin")
        juego.iniciar_juego()
        
        jugador1_antes = juego.jugador1
        jugador2_antes = juego.jugador2
        
        juego.reiniciar_juego()
        
        # Los jugadores deben ser los mismos objetos
        self.assertIs(juego.jugador1, jugador1_antes)
        self.assertIs(juego.jugador2, jugador2_antes)
        self.assertEqual(juego.jugador1.nombre, "Joaquin")
        self.assertEqual(juego.jugador2.nombre, "Martin")

class TestBackgammonGameIntegracion(unittest.TestCase):
    def test_flujo_basico_juego_completo(self):
        juego = BackgammonGame("Player1", "Player2")
        
        # Iniciar juego
        juego.iniciar_juego()
        self.assertIsNotNone(juego.turno_actual)
        # Tirar dados
        dado1, dado2 = juego.tirar_dados()
        self.assertGreater(len(juego.dados_disponibles), 0)
        # Obtener movimientos
        movimientos = juego.obtener_movimientos_legales()
        self.assertIsInstance(movimientos, list)
        # Estado del juego
        estado = juego.obtener_estado_juego()
        self.assertIsNotNone(estado["turno"])
    
    def test_jugar_turno_ejecuta_correctamente(self):
        juego = BackgammonGame("Player1", "Player2")
        juego.iniciar_juego()
        
        turno_inicial = juego.turno_actual
        resultado = juego.jugar_turno()
        
        self.assertIsInstance(resultado, bool)
        self.assertTrue(len(juego.dados_disponibles) > 0 or resultado is False)

    def test_multiples_cambios_de_turno(self):
        juego = BackgammonGame("Player1", "Player2")
        juego.iniciar_juego()
        
        turnos_vistos = set()
        for _ in range(10):
            turnos_vistos.add(juego.turno_actual)
            juego.cambiar_turno()
        
        # Ambos jugadores deberían haber tenido turno
        self.assertEqual(len(turnos_vistos), 2)
    
    def test_secuencia_tirar_usar_cambiar(self):
        juego = BackgammonGame("Player1", "Player2")
        juego.iniciar_juego()
        
        turno1 = juego.turno_actual
        
        # Tirar dados
        juego.tirar_dados()
        self.assertTrue(juego.tiene_dados_disponibles())
        # Usar todos los dados
        while juego.tiene_dados_disponibles():
            juego.usar_dado(juego.dados_disponibles[0])
        # Cambiar turno
        juego.cambiar_turno()
        turno2 = juego.turno_actual
        
        self.assertNotEqual(turno1, turno2)
        self.assertFalse(juego.tiene_dados_disponibles())

class TestBackgammonGameProperties(unittest.TestCase):
    def test_property_tablero_retorna_instancia_correcta(self):
        juego = BackgammonGame("joaquin", "martin")
        
        self.assertIsInstance(juego.tablero, Tablero)
        self.assertIsInstance(juego.tablero, Tablero)
    
    def test_property_jugadores_retornan_instancias_correctas(self):
        juego = BackgammonGame("joaquin", "martin")
        
        self.assertIsInstance(juego.jugador1, Jugador)
        self.assertIsInstance(juego.jugador2, Jugador)
        self.assertEqual(juego.jugador1.nombre, "joaquin")
        self.assertEqual(juego.jugador2.nombre, "martin")
    
    def test_property_turno_actual_inicialmente_none(self):
        juego = BackgammonGame("joaquin", "martin")
        
        self.assertIsNone(juego.turno_actual)
        
        juego.iniciar_juego()
        self.assertIn(juego.turno_actual, [juego.jugador1, juego.jugador2])
    
    def test_property_ganador_inicialmente_none(self):
        juego = BackgammonGame("joaquin", "martin")
        
        self.assertIsNone(juego.ganador)
    
    def test_property_dados_disponibles_retorna_lista(self):
        juego = BackgammonGame("joaquin", "martin")
        
        self.assertEqual(juego.dados_disponibles, [])
        
        juego.tirar_dados()
        self.assertIsInstance(juego.dados_disponibles, list)
        self.assertIn(len(juego.dados_disponibles), [2, 4])
    
    def test_properties_son_readonly(self):
        juego = BackgammonGame("joaquin", "martin")
        
        # Intentar asignar a properties debería fallar
        with self.assertRaises(AttributeError):
            juego.tablero = None
        
        with self.assertRaises(AttributeError):
            juego.jugador1 = None



if __name__ == "__main__":
    unittest.main()
