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
    