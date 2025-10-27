import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from juego import BackgammonGame


class CLI:
    def __init__(self):
        self.__juego__ = None
        self.__ejecutando__ = False
    
    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_bienvenida(self):
        print("=" * 60)
        print(" " * 20 + "BACKGAMMON")
        print("=" * 60)
        print("\n¡Bienvenido al juego de Backgammon!\n")
