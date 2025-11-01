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