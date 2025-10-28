import pygame
import sys
import os
import math

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from juego import BackgammonGame

class PygameUI:
    # Colores
    color_fondo = (34, 49, 63)
    color_tablero = (101, 67, 33)
    COLOR_PUNTO_CLARO = (222, 184, 135)
    COLOR_PUNTO_OSCURO = (139, 90, 43)
    COLOR_BARRA = (70, 50, 30)
    COLOR_FICHA_BLANCA = (240, 240, 240)
    COLOR_FICHA_NEGRA = (30, 30, 30)
    COLOR_BORDE_FICHA = (180, 180, 180)
    COLOR_SELECCION = (255, 215, 0)
    COLOR_MOVIMIENTO_POSIBLE = (100, 255, 100)
    COLOR_TEXTO = (255, 255, 255)
    COLOR_BOTON = (52, 152, 219)
    COLOR_BOTON_HOVER = (41, 128, 185)
    COLOR_MENSAJE_ERROR = (231, 76, 60)
    COLOR_MENSAJE_EXITO = (46, 204, 113)
    
    # Dimensiones
    ANCHO_VENTANA = 1200
    ALTO_VENTANA = 800
    MARGEN = 50
    RADIO_FICHA = 20
    
    def __init__(self):
        pygame.init()
        
        self.__ancho__ = self.ANCHO_VENTANA
        self.__alto__ = self.ALTO_VENTANA
        self.__pantalla__ = pygame.display.set_mode((self.__ancho__, self.__alto__))
        pygame.display.set_caption("Backgammon")
        
        self.__reloj__ = pygame.time.Clock()
        self.__juego__ = None
        self.__ejecutando__ = True
        
        # Fuentes
        self.__fuente_titulo__ = pygame.font.Font(None, 60)
        self.__fuente_texto__ = pygame.font.Font(None, 36)
        self.__fuente_pequeña__ = pygame.font.Font(None, 24)
        
        # Estado del juego
        self.__punto_seleccionado__ = None
        self.__movimientos_posibles__ = []
        self.__mensaje__ = ""
        self.__tiempo_mensaje__ = 0
        self.__estado__ = "menu"  # menu, juego, victoria
        
        # Calcular dimensiones del tablero
        self.__calcular_dimensiones_tablero__()