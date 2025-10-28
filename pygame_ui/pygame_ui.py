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
    color_punto_claro = (222, 184, 135)
    color_punto_oscuro = (139, 90, 43)
    color_barra = (70, 50, 30)
    color_ficha_blanca = (240, 240, 240)
    color_ficha_negra = (30, 30, 30)
    color_borde_ficha = (180, 180, 180)
    color_seleccion = (255, 215, 0)
    color_movimiento_posible = (100, 255, 100)
    color_texto = (255, 255, 255)
    color_boton = (52, 152, 219)
    color_boton_hover = (41, 128, 185)
    color_mensaje_error = (231, 76, 60)
    color_mensaje_exito = (46, 204, 113)
    
    # Dimensiones
    ancho_ventana = 1200
    alto_ventana = 800
    marge = 50
    radio_ficha = 20
    
    def __init__(self):
        pygame.init()
        
        self.__ancho__ = self.ancho_ventana
        self.__alto__ = self.alto_ventana
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

    def __calcular_dimensiones_tablero__(self):
        self.__tablero_x__ = self.marge
        self.__tablero_y__ = self.marge + 100
        self.__tablero_ancho__ = self.__ancho__ - 2 * self.marge
        self.__tablero_alto__ = self.__alto__ - 2 * self.marge - 150
        
        # Ancho de cada punto (triángulo)
        self.__ancho_punto__ = self.__tablero_ancho__ // 14  # 12 puntos + 2 para la barra
        self.__alto_punto__ = self.__tablero_alto__ // 2 - 20
    
    def dibujar_fondo(self):
        self.__pantalla__.fill(self.color_fondo)

    def dibujar_tablero(self):
        # Fondo del tablero
        pygame.draw.rect(
            self.__pantalla__,
            self.color_tablero,
            (self.__tablero_x__, self.__tablero_y__, 
             self.__tablero_ancho__, self.__tablero_alto__)
        )
        
        # Dibujar puntos (triángulos)
        for i in range(24):
            self.__dibujar_punto__(i)
        
        # Dibujar barra central
        barra_x = self.__tablero_x__ + 6 * self.__ancho_punto__
        pygame.draw.rect(
            self.__pantalla__,
            self.color_barra,
            (barra_x, self.__tablero_y__, 
             2 * self.__ancho_punto__, self.__tablero_alto__)
        )
        
        # Dibujar bordes
        pygame.draw.rect(
            self.__pantalla__,
            self.color_texto,
            (self.__tablero_x__, self.__tablero_y__, 
             self.__tablero_ancho__, self.__tablero_alto__),
            3
        )