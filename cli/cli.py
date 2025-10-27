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

    def solicitar_nombres(self) -> tuple:
        print("Configuración de jugadores:")
        nombre1 = input("Nombre del Jugador 1 (fichas BLANCAS): ").strip()
        if not nombre1:
            nombre1 = "Jugador 1"
        
        nombre2 = input("Nombre del Jugador 2 (fichas NEGRAS): ").strip()
        if not nombre2:
            nombre2 = "Jugador 2"
        
        return nombre1, nombre2