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
    