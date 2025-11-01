import unittest
from unittest.mock import Mock, patch, MagicMock, call
import sys
import os

# Agregar el path para importar CLI
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cli.cli import CLI


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.cli = CLI()
        
        # Mock del juego para evitar dependencias
        self.mock_juego = MagicMock()
        self.cli._CLI__juego__ = self.mock_juego
    
    def tearDown(self):
        self.cli = None
        self.mock_juego = None

# ==================== TESTS DE INICIALIZACIÓN ====================
    
    def test_init_estado_inicial(self):
        cli = CLI()
        self.assertIsNone(cli._CLI__juego__)
        self.assertFalse(cli._CLI__ejecutando__)

 # ==================== TESTS DE LIMPIAR PANTALLA ====================
    
    @patch('os.system')
    @patch('os.name', 'nt')
    def test_limpiar_pantalla_windows(self, mock_system):
        self.cli.limpiar_pantalla()
        mock_system.assert_called_once_with('cls')
    
    @patch('os.system')
    @patch('os.name', 'posix')
    def test_limpiar_pantalla_unix(self, mock_system):
        self.cli.limpiar_pantalla()
        mock_system.assert_called_once_with('clear')
    
# ==================== TESTS DE MOSTRAR TABLERO ====================
    @patch('builtins.print')
    def test_mostrar_tablero_basico(self, mock_print):
        # Configurar mock del tablero
        puntos_mock = [{"color": None, "cantidad": 0} for _ in range(24)]
        puntos_mock[0] = {"color": "NEGRO", "cantidad": 2}
        puntos_mock[23] = {"color": "BLANCO", "cantidad": 2}
        
        self.mock_juego.tablero.obtener_puntos.return_value = puntos_mock
        self.mock_juego.tablero.fichas_en_barra.return_value = 0
        self.mock_juego.tablero.fichas_fuera.return_value = 0
        
        # Ejecutar
        self.cli.mostrar_tablero()
        
        # Verificar que se llamó a print múltiples veces
        self.assertGreater(mock_print.call_count, 10)
    
    @patch('builtins.print')
    def test_mostrar_tablero_con_fichas_en_barra(self, mock_print):
        puntos_mock = [{"color": None, "cantidad": 0} for _ in range(24)]
        
        self.mock_juego.tablero.obtener_puntos.return_value = puntos_mock
        self.mock_juego.tablero.fichas_en_barra.side_effect = [2, 1]  # BLANCO=2, NEGRO=1
        self.mock_juego.tablero.fichas_fuera.return_value = 0
        
        self.cli.mostrar_tablero()
        
        # Verificar que se mencionan fichas en barra
        llamadas = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("BARRA" in llamada for llamada in llamadas))
    
# ==================== TESTS DE MOSTRAR ESTADO TURNO ====================
    
    @patch('builtins.print')
    def test_mostrar_estado_turno(self, mock_print):
        """
        Test 10: Verificar que se muestra el estado del turno actual.
        """
        # Configurar estado del juego
        estado_mock = {
            'turno': 'Joaquin',
            'color_turno': 'BLANCO',
            'dados_disponibles': [3, 5]
        }
        self.mock_juego.obtener_estado_juego.return_value = estado_mock
        self.mock_juego.obtener_movimientos_legales.return_value = [(23, 20, 3)]
        
        self.cli.mostrar_estado_turno()
        
        # Verificar que se imprimió información del turno
        self.assertGreater(mock_print.call_count, 0)
    
    @patch('builtins.print')
    def test_mostrar_estado_turno_sin_dados(self, mock_print):
        """
        Test 11: Verificar comportamiento cuando no hay dados disponibles.
        """
        estado_mock = {
            'turno': 'Walter',
            'color_turno': 'NEGRO',
            'dados_disponibles': []
        }
        self.mock_juego.obtener_estado_juego.return_value = estado_mock
        self.mock_juego.obtener_movimientos_legales.return_value = []
        
        self.cli.mostrar_estado_turno()
        
        # Solo debe mostrar turno, no dados
        self.assertGreater(mock_print.call_count, 0)
    
    # ==================== TESTS DE MOSTRAR COMANDOS ====================
    
    @patch('builtins.print')
    def test_mostrar_comandos(self, mock_print):
        """
        Test 12: Verificar que se muestran todos los comandos disponibles.
        """
        self.cli.mostrar_comandos()
        
        # Verificar que se imprimieron comandos
        llamadas = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("mover" in llamada for llamada in llamadas))
        self.assertTrue(any("barra" in llamada for llamada in llamadas))
        self.assertTrue(any("pasar" in llamada for llamada in llamadas))
    
    # ==================== TESTS DE PROCESAR COMANDO ====================
    
    def test_procesar_comando_vacio(self):
        """
        Test 13: Verificar que comando vacío retorna False.
        
        Caso borde: Input vacío
        """
        resultado = self.cli.procesar_comando("")
        self.assertFalse(resultado)
    
    def test_procesar_comando_solo_espacios(self):
        """
        Test 14: Verificar que comando con solo espacios retorna False.
        """
        resultado = self.cli.procesar_comando("   ")
        self.assertFalse(resultado)
    
    @patch('builtins.print')
    def test_procesar_comando_mover_valido(self, mock_print):
        """
        Test 15: Verificar comando 'mover' con parámetros válidos.
        
        Explicación:
        - Formato: "mover <origen> <dado>"
        - Debe llamar a realizar_movimiento del juego
        """
        self.mock_juego.realizar_movimiento.return_value = True
        
        resultado = self.cli.procesar_comando("mover 5 3")
        
        self.assertTrue(resultado)
        self.mock_juego.realizar_movimiento.assert_called_once_with(5, 3)
    
    @patch('builtins.print')
    def test_procesar_comando_mover_invalido_pocos_parametros(self, mock_print):
        """
        Test 16: Verificar que 'mover' sin suficientes parámetros retorna False.
        """
        resultado = self.cli.procesar_comando("mover 5")
        self.assertFalse(resultado)
    
    @patch('builtins.print')
    def test_procesar_comando_mover_con_value_error(self, mock_print):
        """
        Test 17: Verificar manejo de ValueError en movimiento.
        
        Explicación:
        - Simula que el juego lanza ValueError (movimiento inválido)
        - El CLI debe capturarlo y mostrar error
        """
        self.mock_juego.realizar_movimiento.side_effect = ValueError("Movimiento inválido")
        
        resultado = self.cli.procesar_comando("mover 5 3")
        
        self.assertFalse(resultado)
        # Verificar que se imprimió el error
        mock_print.assert_called()
    
    @patch('builtins.print')
    def test_procesar_comando_mover_con_excepcion_generica(self, mock_print):
        """
        Test 18: Verificar manejo de Exception genérica.
        """
        self.mock_juego.realizar_movimiento.side_effect = Exception("Error inesperado")
        
        resultado = self.cli.procesar_comando("mover 5 3")
        
        self.assertFalse(resultado)
    
    @patch('builtins.print')
    def test_procesar_comando_barra_valido(self, mock_print):
        """
        Test 19: Verificar comando 'barra' con parámetro válido.
        """
        self.mock_juego.realizar_movimiento.return_value = True
        
        resultado = self.cli.procesar_comando("barra 4")
        
        self.assertTrue(resultado)
        # Verificar que se llamó con origen=-1 (convención para barra)
        self.mock_juego.realizar_movimiento.assert_called_once_with(-1, 4)
    
    @patch('builtins.print')
    def test_procesar_comando_barra_invalido(self, mock_print):
        """
        Test 20: Verificar que 'barra' sin parámetro retorna False.
        """
        resultado = self.cli.procesar_comando("barra")
        self.assertFalse(resultado)
    
    @patch('builtins.print')
    def test_procesar_comando_pasar_cuando_no_puede_mover(self, mock_print):
        """
        Test 21: Verificar comando 'pasar' cuando no hay movimientos disponibles.
        
        Explicación:
        - Si no puede mover, debe cambiar de turno
        - Retorna True indicando acción válida
        """
        self.mock_juego.puede_realizar_movimiento.return_value = False
        
        resultado = self.cli.procesar_comando("pasar")
        
        self.assertTrue(resultado)
        self.mock_juego.cambiar_turno.assert_called_once()
    
    @patch('builtins.print')
    def test_procesar_comando_pasar_cuando_si_puede_mover(self, mock_print):
        """
        Test 22: Verificar que 'pasar' falla si aún hay movimientos posibles.
        
        Caso: Jugador intenta pasar pero tiene movimientos disponibles
        """
        self.mock_juego.puede_realizar_movimiento.return_value = True
        
        resultado = self.cli.procesar_comando("pasar")
        
        self.assertFalse(resultado)
        self.mock_juego.cambiar_turno.assert_not_called()
    
    @patch('builtins.print')
    def test_procesar_comando_ayuda(self, mock_print):
        """
        Test 23: Verificar comando 'ayuda'.
        """
        resultado = self.cli.procesar_comando("ayuda")
        
        self.assertTrue(resultado)
        # Verificar que se mostraron los comandos
        self.assertGreater(mock_print.call_count, 0)
    
    def test_procesar_comando_salir(self):
        """
        Test 24: Verificar comando 'salir'.
        
        Explicación:
        - Debe cambiar el flag __ejecutando__ a False
        - Esto hará que el bucle principal termine
        """
        self.cli._CLI__ejecutando__ = True
        
        resultado = self.cli.procesar_comando("salir")
        
        self.assertTrue(resultado)
        self.assertFalse(self.cli._CLI__ejecutando__)
    
    @patch('builtins.print')
    def test_procesar_comando_no_reconocido(self, mock_print):
        """
        Test 25: Verificar comando no reconocido.
        
        Caso borde: Comando que no existe
        """
        resultado = self.cli.procesar_comando("comando_invalido")
        
        self.assertFalse(resultado)
        # Verificar que se imprimió mensaje de error
        self.assertGreater(mock_print.call_count, 0)
    
    @patch('builtins.print')
    def test_procesar_comando_mover_con_parametros_no_numericos(self, mock_print):
        """
        Test 26: Verificar que parámetros no numéricos generan error.
        
        Caso: "mover abc xyz"
        """
        resultado = self.cli.procesar_comando("mover abc xyz")
        
        self.assertFalse(resultado)
    
    # ==================== TESTS DE JUGAR TURNO ====================
    
    @patch('builtins.input', return_value='salir')
    @patch('builtins.print')
    def test_jugar_turno_salir_inmediatamente(self, mock_print, mock_input):
        """
        Test 27: Verificar que se puede salir durante un turno.
        """
        self.mock_juego.jugar_turno.return_value = True
        self.mock_juego.tiene_dados_disponibles.return_value = True
        self.mock_juego.puede_realizar_movimiento.return_value = True
        
        # Configurar tablero y estado
        puntos_mock = [{"color": None, "cantidad": 0} for _ in range(24)]
        self.mock_juego.tablero.obtener_puntos.return_value = puntos_mock
        self.mock_juego.tablero.fichas_en_barra.return_value = 0
        self.mock_juego.tablero.fichas_fuera.return_value = 0
        self.mock_juego.obtener_estado_juego.return_value = {
            'turno': 'Test',
            'color_turno': 'BLANCO',
            'dados_disponibles': [3]
        }
        
        self.cli._CLI__ejecutando__ = True
        self.cli.jugar_turno()
        
        # Verificar que se detuvo la ejecución
        self.assertFalse(self.cli._CLI__ejecutando__)
    
    @patch('builtins.print')
    def test_jugar_turno_no_puede_mover(self, mock_print):
        """
        Test 28: Verificar turno cuando no puede mover desde el inicio.
        """
        self.mock_juego.jugar_turno.return_value = False
        
        self.cli.jugar_turno()
        
        # No debe intentar mostrar tablero ni pedir comandos
        self.mock_juego.tiene_dados_disponibles.assert_not_called()
    
    @patch('builtins.input', side_effect=['mover 5 3', 'pasar'])
    @patch('builtins.print')
    def test_jugar_turno_movimiento_seguido_sin_dados(self, mock_print, mock_input):
        """
        Test 29: Verificar flujo completo de turno con movimiento y sin más dados.
        """
        self.mock_juego.jugar_turno.return_value = True
        
        # Primera iteración: tiene dados y puede mover
        # Segunda iteración: no tiene dados
        self.mock_juego.tiene_dados_disponibles.side_effect = [True, False]
        self.mock_juego.puede_realizar_movimiento.return_value = True
        self.mock_juego.realizar_movimiento.return_value = True
        self.mock_juego.verificar_victoria.return_value = False
        
        # Configurar mocks necesarios
        puntos_mock = [{"color": None, "cantidad": 0} for _ in range(24)]
        self.mock_juego.tablero.obtener_puntos.return_value = puntos_mock
        self.mock_juego.tablero.fichas_en_barra.return_value = 0
        self.mock_juego.tablero.fichas_fuera.return_value = 0
        self.mock_juego.obtener_estado_juego.return_value = {
            'turno': 'Test',
            'color_turno': 'BLANCO',
            'dados_disponibles': [3]
        }
        self.mock_juego.obtener_movimientos_legales.return_value = []
        
        self.cli.jugar_turno()
        
        # Verificar que se cambió de turno
        self.mock_juego.cambiar_turno.assert_called()
    
    @patch('builtins.input', return_value='mover 5 3')
    @patch('builtins.print')
    def test_jugar_turno_con_victoria(self, mock_print, mock_input):
        """
        Test 30: Verificar que se detecta victoria durante el turno.
        """
        self.mock_juego.jugar_turno.return_value = True
        self.mock_juego.tiene_dados_disponibles.return_value = True
        self.mock_juego.puede_realizar_movimiento.return_value = True
        self.mock_juego.realizar_movimiento.return_value = True
        self.mock_juego.verificar_victoria.return_value = True  # ¡Victoria!
        
        # Mock del ganador
        mock_ganador = Mock()
        mock_ganador.nombre = "Joaquin"
        mock_ganador.color = "BLANCO"
        self.mock_juego.ganador = mock_ganador
        
        # Configurar mocks necesarios
        puntos_mock = [{"color": None, "cantidad": 0} for _ in range(24)]
        self.mock_juego.tablero.obtener_puntos.return_value = puntos_mock
        self.mock_juego.tablero.fichas_en_barra.return_value = 0
        self.mock_juego.tablero.fichas_fuera.return_value = 15  # ¡Todas las fichas fuera!
        self.mock_juego.obtener_estado_juego.return_value = {
            'turno': 'Joaquin',
            'color_turno': 'BLANCO',
            'dados_disponibles': [3]
        }
        self.mock_juego.obtener_movimientos_legales.return_value = []
        
        self.cli.jugar_turno()
        
        # Verificar que se llamó a verificar_victoria
        self.mock_juego.verificar_victoria.assert_called()
    
    @patch('builtins.input', return_value='mover 5 3')
    @patch('builtins.print')
    def test_jugar_turno_sin_movimientos_disponibles(self, mock_print, mock_input):
        """
        Test 31: Verificar que se sale del turno cuando no puede mover más.
        """
        self.mock_juego.jugar_turno.return_value = True
        self.mock_juego.tiene_dados_disponibles.return_value = True
        self.mock_juego.puede_realizar_movimiento.return_value = False  # No puede mover
        
        # Configurar mocks necesarios
        puntos_mock = [{"color": None, "cantidad": 0} for _ in range(24)]
        self.mock_juego.tablero.obtener_puntos.return_value = puntos_mock
        self.mock_juego.tablero.fichas_en_barra.return_value = 0
        self.mock_juego.tablero.fichas_fuera.return_value = 0
        self.mock_juego.obtener_estado_juego.return_value = {
            'turno': 'Test',
            'color_turno': 'BLANCO',
            'dados_disponibles': [3]
        }
        
        self.cli.jugar_turno()
        
        # Debe cambiar turno porque no puede mover
        self.mock_juego.cambiar_turno.assert_called()
    
    # ==================== TESTS DE MOSTRAR VICTORIA ====================
    
    @patch('builtins.print')
    def test_mostrar_victoria(self, mock_print):
        """
        Test 32: Verificar que se muestra mensaje de victoria correctamente.
        """
        # Mock del ganador
        mock_ganador = Mock()
        mock_ganador.nombre = "Joaquin"
        mock_ganador.color = "BLANCO"
        self.mock_juego.ganador = mock_ganador
        
        # Configurar tablero
        puntos_mock = [{"color": None, "cantidad": 0} for _ in range(24)]
        self.mock_juego.tablero.obtener_puntos.return_value = puntos_mock
        self.mock_juego.tablero.fichas_en_barra.return_value = 0
        self.mock_juego.tablero.fichas_fuera.return_value = 15
        
        self.cli.mostrar_victoria()
        
        # Verificar que se imprimió mensaje de victoria
        llamadas = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("VICTORIA" in llamada for llamada in llamadas))
        self.assertTrue(any("Joaquin" in llamada for llamada in llamadas))
    
    # ==================== TESTS DE JUGAR DE NUEVO ====================
    
    @patch('builtins.input', return_value='s')
    def test_jugar_de_nuevo_afirmativo_s(self, mock_input):
        """
        Test 33: Verificar que 's' retorna True.
        """
        resultado = self.cli.jugar_de_nuevo()
        self.assertTrue(resultado)
    
    @patch('builtins.input', return_value='si')
    def test_jugar_de_nuevo_afirmativo_si(self, mock_input):
        """
        Test 34: Verificar que 'si' retorna True.
        """
        resultado = self.cli.jugar_de_nuevo()
        self.assertTrue(resultado)
    
    @patch('builtins.input', return_value='sí')
    def test_jugar_de_nuevo_afirmativo_si_con_tilde(self, mock_input):
        """
        Test 35: Verificar que 'sí' (con tilde) retorna True.
        """
        resultado = self.cli.jugar_de_nuevo()
        self.assertTrue(resultado)
    
    @patch('builtins.input', return_value='yes')
    def test_jugar_de_nuevo_afirmativo_yes(self, mock_input):
        """
        Test 36: Verificar que 'yes' retorna True.
        """
        resultado = self.cli.jugar_de_nuevo()
        self.assertTrue(resultado)
    
    @patch('builtins.input', return_value='y')
    def test_jugar_de_nuevo_afirmativo_y(self, mock_input):
        """
        Test 37: Verificar que 'y' retorna True.
        """
        resultado = self.cli.jugar_de_nuevo()
        self.assertTrue(resultado)
    
    @patch('builtins.input', return_value='n')
    def test_jugar_de_nuevo_negativo(self, mock_input):
        """
        Test 38: Verificar que 'n' retorna False.
        """
        resultado = self.cli.jugar_de_nuevo()
        self.assertFalse(resultado)
    
    @patch('builtins.input', return_value='no')
    def test_jugar_de_nuevo_negativo_no(self, mock_input):
        """
        Test 39: Verificar que 'no' retorna False.
        """
        resultado = self.cli.jugar_de_nuevo()
        self.assertFalse(resultado)
    
    @patch('builtins.input', return_value='cualquier_cosa')
    def test_jugar_de_nuevo_respuesta_invalida(self, mock_input):
        """
        Test 40: Verificar que respuesta inválida retorna False.
        """
        resultado = self.cli.jugar_de_nuevo()
        self.assertFalse(resultado)
    
    # ==================== TESTS DE INICIAR (Flujo completo) ====================
    
    @patch('builtins.input', side_effect=['Joaquin', 'Walter', 'salir'])
    @patch('builtins.print')
    @patch.object(CLI, 'limpiar_pantalla')
    def test_iniciar_salir_inmediatamente(self, mock_limpiar, mock_print, mock_input):
        """
        Test 41: Verificar flujo de iniciar y salir inmediatamente.
        
        Explicación:
        - Simula ingreso de nombres
        - Luego ejecuta comando 'salir'
        - El bucle debe terminar
        """
        # Configurar mock del juego
        with patch('cli.cli.BackgammonGame') as MockGame:
            mock_game_instance = MockGame.return_value
            mock_game_instance.iniciar_juego.return_value = None
            mock_game_instance.esta_terminado.return_value = False
            mock_game_instance.jugar_turno.return_value = True
            mock_game_instance.tiene_dados_disponibles.return_value = True
            mock_game_instance.puede_realizar_movimiento.return_value = True
            
            # Configurar tablero
            puntos_mock = [{"color": None, "cantidad": 0} for _ in range(24)]
            mock_game_instance.tablero.obtener_puntos.return_value = puntos_mock
            mock_game_instance.tablero.fichas_en_barra.return_value = 0
            mock_game_instance.tablero.fichas_fuera.return_value = 0
            mock_game_instance.obtener_estado_juego.return_value = {
                'turno': 'Joaquin',
                'color_turno': 'BLANCO',
                'dados_disponibles': [3]
            }
            mock_game_instance.obtener_movimientos_legales.return_value = []
            
            cli = CLI()
            cli.iniciar()
            
            # Verificar que se creó el juego
            MockGame.assert_called_once_with('Joaquin', 'Walter')
    
    @patch('builtins.input', side_effect=['Joaquin', 'Walter', 'mover 5 3', 'n'])
    @patch('builtins.print')
    @patch.object(CLI, 'limpiar_pantalla')
    def test_iniciar_juego_completo_y_no_repetir(self, mock_limpiar, mock_print, mock_input):
        """
        Test 42: Verificar flujo completo: jugar una partida y no repetir.
        """
        with patch('cli.cli.BackgammonGame') as MockGame:
            mock_game_instance = MockGame.return_value
            mock_game_instance.iniciar_juego.return_value = None
            
            # Simular que el juego termina rápidamente
            mock_game_instance.esta_terminado.side_effect = [False, True]
            mock_game_instance.jugar_turno.return_value = False  # No puede mover
            
            cli = CLI()
            cli.iniciar()
            
            # Verificar que se preguntó si quiere jugar de nuevo
            # y que se imprimió mensaje de despedida
            llamadas = [str(call) for call in mock_print.call_args_list]
            self.assertTrue(any("Gracias por jugar" in llamada for llamada in llamadas))
    
    @patch('builtins.input', side_effect=[
        'Joaquin', 'Walter',  # Nombres primera partida
        'mover 5 3',          # Movimiento
        's',                  # Jugar de nuevo = SÍ
        'Juan', 'Pedro',      # Nombres segunda partida
        'salir'               # Salir en segunda partida
    ])
    @patch('builtins.print')
    @patch.object(CLI, 'limpiar_pantalla')
    def test_iniciar_multiples_partidas(self, mock_limpiar, mock_print, mock_input):
        """
        Test 43: Verificar que se pueden jugar múltiples partidas.
        
        Flujo:
        1. Primera partida (Joaquin vs Walter)
        2. Termina y dice que sí quiere jugar de nuevo
        3. Segunda partida (Juan vs Pedro)
        4. Sale
        """
        with patch('cli.cli.BackgammonGame') as MockGame:
            mock_game_instance = MockGame.return_value
            mock_game_instance.iniciar_juego.return_value = None
            
            # Primera partida termina, segunda partida se interrumpe con salir
            mock_game_instance.esta_terminado.side_effect = [
                False, True,  # Primera partida
                False         # Segunda partida
            ]
            mock_game_instance.jugar_turno.return_value = True
            mock_game_instance.tiene_dados_disponibles.return_value = True
            mock_game_instance.puede_realizar_movimiento.return_value = True
            
            # Configurar mocks necesarios para renderizado
            puntos_mock = [{"color": None, "cantidad": 0} for _ in range(24)]
            mock_game_instance.tablero.obtener_puntos.return_value = puntos_mock
            mock_game_instance.tablero.fichas_en_barra.return_value = 0
            mock_game_instance.tablero.fichas_fuera.return_value = 0
            mock_game_instance.obtener_estado_juego.return_value = {
                'turno': 'Test',
                'color_turno': 'BLANCO',
                'dados_disponibles': [3]
            }
            mock_game_instance.obtener_movimientos_legales.return_value = []
            
            cli = CLI()
            cli.iniciar()
            
            # Verificar que se creó el juego dos veces
            self.assertEqual(MockGame.call_count, 2)
    
    # ==================== TESTS ADICIONALES PARA COBERTURA ====================
    
    @patch('builtins.print')
    def test_mostrar_tablero_multiples_fichas_en_punto(self, mock_print):
        """
        Test 44: Verificar visualización con múltiples fichas en un punto.
        """
        puntos_mock = [{"color": None, "cantidad": 0} for _ in range(24)]
        puntos_mock[5] = {"color": "BLANCO", "cantidad": 5}
        puntos_mock[16] = {"color": "NEGRO", "cantidad": 3}
        
        self.mock_juego.tablero.obtener_puntos.return_value = puntos_mock
        self.mock_juego.tablero.fichas_en_barra.return_value = 0
        self.mock_juego.tablero.fichas_fuera.return_value = 0
        
        self.cli.mostrar_tablero()
        
        # Verificar que se renderizó sin errores
        self.assertGreater(mock_print.call_count, 0)
    
    @patch('builtins.input', return_value='MOVER 5 3')  # Mayúsculas
    @patch('builtins.print')
    def test_procesar_comando_case_insensitive(self, mock_print, mock_input):
        """
        Test 45: Verificar que comandos funcionan en mayúsculas.
        
        Explicación:
        - Los comandos deben ser case-insensitive gracias a .lower()
        """
        self.mock_juego.jugar_turno.return_value = True
        self.mock_juego.tiene_dados_disponibles.return_value = True
        self.mock_juego.puede_realizar_movimiento.return_value = True
        self.mock_juego.realizar_movimiento.return_value = True
        
        # Configurar mocks
        puntos_mock = [{"color": None, "cantidad": 0} for _ in range(24)]
        self.mock_juego.tablero.obtener_puntos.return_value = puntos_mock
        self.mock_juego.tablero.fichas_en_barra.return_value = 0
        self.mock_juego.tablero.fichas_fuera.return_value = 0
        self.mock_juego.obtener_estado_juego.return_value = {
            'turno': 'Test',
            'color_turno': 'BLANCO',
            'dados_disponibles': [3]
        }
        self.mock_juego.obtener_movimientos_legales.return_value = []
        self.mock_juego.verificar_victoria.return_value = False
        
        # Simular un solo ciclo del turno
        self.mock_juego.tiene_dados_disponibles.side_effect = [True, False]
        
        self.cli.jugar_turno()
        
        # Verificar que se procesó el comando correctamente
        self.mock_juego.realizar_movimiento.assert_called_with(5, 3)


# ==================== EJECUCIÓN DE TESTS ====================

if __name__ == "__main__":
    unittest.main()