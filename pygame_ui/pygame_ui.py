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

    def __dibujar_punto__(self, numero_punto: int):
        # Determinar posición
        if numero_punto < 12:
            # Parte inferior
            fila = 1
            columna = 11 - numero_punto
        else:
            # Parte superior
            fila = 0
            columna = numero_punto - 12
        
        # Ajustar por la barra central
        if columna >= 6:
            columna += 2
        
        # Calcular posición x
        x = self.__tablero_x__ + columna * self.__ancho_punto__
        
        # Calcular posición y y dirección del triángulo
        if fila == 0:
            # Triángulo hacia abajo (parte superior)
            y_base = self.__tablero_y__
            y_punta = y_base + self.__alto_punto__
        else:
            # Triángulo hacia arriba (parte inferior)
            y_base = self.__tablero_y__ + self.__tablero_alto__
            y_punta = y_base - self.__alto_punto__
        
        # Color alternado
        color = self.COLOR_PUNTO_CLARO if numero_punto % 2 == 0 else self.COLOR_PUNTO_OSCURO
        
        # Resaltar si está seleccionado
        if numero_punto == self.__punto_seleccionado__:
            color = self.COLOR_SELECCION
        
        # Resaltar si es movimiento posible
        if any(destino == numero_punto for _, destino, _ in self.__movimientos_posibles__):
            # Mezclar con color de movimiento posible
            color = tuple((c + g) // 2 for c, g in zip(color, self.COLOR_MOVIMIENTO_POSIBLE))
        
        # Dibujar triángulo
        puntos = [
            (x + self.__ancho_punto__ // 2, y_punta),
            (x, y_base),
            (x + self.__ancho_punto__, y_base)
        ]
        pygame.draw.polygon(self.__pantalla__, color, puntos)
        pygame.draw.polygon(self.__pantalla__, self.COLOR_TEXTO, puntos, 1)
        
        # Dibujar número del punto
        texto = self.__fuente_pequeña__.render(str(numero_punto), True, self.COLOR_TEXTO)
        texto_rect = texto.get_rect(center=(x + self.__ancho_punto__ // 2, y_base + (10 if fila == 0 else -10)))
        self.__pantalla__.blit(texto, texto_rect)

    def dibujar_fichas(self):
        if not self.__juego__:
            return
        
        puntos = self.__juego__.tablero.obtener_puntos()
        
        for i, punto in enumerate(puntos):
            if punto["cantidad"] > 0:
                self.__dibujar_fichas_en_punto__(i, punto["color"], punto["cantidad"])
        
        # Dibujar fichas en la barra
        self.__dibujar_fichas_barra__()
        
        # Dibujar fichas fuera
        self.__dibujar_fichas_fuera__()

    def __dibujar_fichas_en_punto__(self, numero_punto: int, color: str, cantidad: int):
        # Determinar posición del punto
        if numero_punto < 12:
            fila = 1
            columna = 11 - numero_punto
        else:
            fila = 0
            columna = numero_punto - 12
        
        if columna >= 6:
            columna += 2
        
        x = self.__tablero_x__ + columna * self.__ancho_punto__ + self.__ancho_punto__ // 2
        
        if fila == 0:
            y_inicio = self.__tablero_y__ + 20
            direccion = 1
        else:
            y_inicio = self.__tablero_y__ + self.__tablero_alto__ - 20
            direccion = -1
        
        # Color de la ficha
        color_ficha = self.color_ficha_blanca if color == "BLANCO" else self.color_ficha_negra
        
        # Dibujar fichas (máximo 5 visibles, luego mostrar número)
        fichas_visibles = min(cantidad, 5)
        for i in range(fichas_visibles):
            y = y_inicio + direccion * i * (self.radio_ficha * 2 + 2)
            pygame.draw.circle(self.__pantalla__, color_ficha, (x, y), self.radio_ficha)
            pygame.draw.circle(self.__pantalla__, self.color_borde_ficha, (x, y), self.radio_ficha, 2)
        
        # Si hay más de 5 fichas, mostrar el número
        if cantidad > 5:
            y = y_inicio + direccion * 4 * (self.radio_ficha * 2 + 2)
            texto = self.__fuente_pequeña__.render(str(cantidad), True, self.color_texto)
            texto_rect = texto.get_rect(center=(x, y))
            
            # Fondo para el número
            pygame.draw.circle(self.__pantalla__, color_ficha, (x, y), self.radio_ficha)
            pygame.draw.circle(self.__pantalla__, self.color_borde_ficha, (x, y), self.radio_ficha, 2)
            self.__pantalla__.blit(texto, texto_rect)
    
    def __dibujar_fichas_barra__(self):
        if not self.__juego__:
            return
        
        barra_x = self.__tablero_x__ + 6 * self.__ancho_punto__ + self.__ancho_punto__
        
        # Fichas blancas en la barra
        fichas_blanco = self.__juego__.tablero.fichas_en_barra("BLANCO")
        if fichas_blanco > 0:
            y_base = self.__tablero_y__ + self.__tablero_alto__ // 2 + 50
            for i in range(min(fichas_blanco, 5)):
                y = y_base + i * (self.radio_ficha * 2 + 2)
                pygame.draw.circle(self.__pantalla__, self.color_ficha_blanca, (barra_x, y), self.radio_ficha)
                pygame.draw.circle(self.__pantalla__, self.color_borde_ficha, (barra_x, y), self.radio_ficha, 2)
            
            if fichas_blanco > 5:
                texto = self.__fuente_pequeña__.render(str(fichas_blanco), True, self.color_texto)
                self.__pantalla__.blit(texto, (barra_x - 10, y_base - 30))
        
        # Fichas negras en la barra
        fichas_negro = self.__juego__.tablero.fichas_en_barra("NEGRO")
        if fichas_negro > 0:
            y_base = self.__tablero_y__ + self.__tablero_alto__ // 2 - 50
            for i in range(min(fichas_negro, 5)):
                y = y_base - i * (self.radio_ficha * 2 + 2)
                pygame.draw.circle(self.__pantalla__, self.color_ficha_negra, (barra_x, y), self.radio_ficha)
                pygame.draw.circle(self.__pantalla__, self.color_borde_ficha, (barra_x, y), self.radio_ficha, 2)
            
            if fichas_negro > 5:
                texto = self.__fuente_pequeña__.render(str(fichas_negro), True, self.color_texto)
                self.__pantalla__.blit(texto, (barra_x - 10, y_base + 30))

    def __dibujar_fichas_fuera__(self):
        if not self.__juego__:
            return
        
        # Área de fichas fuera (derecha del tablero)
        fuera_x = self.__tablero_x__ + self.__tablero_ancho__ + 20
        
        # Fichas blancas fuera
        fichas_blanco = self.__juego__.tablero.fichas_fuera("BLANCO")
        texto = self.__fuente_pequeña__.render(f"Blanco fuera: {fichas_blanco}", True, self.color_texto)
        self.__pantalla__.blit(texto, (fuera_x, self.__tablero_y__ + self.__tablero_alto__ - 50))
        
        # Fichas negras fuera
        fichas_negro = self.__juego__.tablero.fichas_fuera("NEGRO")
        texto = self.__fuente_pequeña__.render(f"Negro fuera: {fichas_negro}", True, self.color_texto)
        self.__pantalla__.blit(texto, (fuera_x, self.__tablero_y__ + 50))

    def dibujar_info_turno(self):
        if not self.__juego__ or not self.__juego__.turno_actual:
            return
        
        estado = self.__juego__.obtener_estado_juego()
        
        # Nombre del jugador y color
        texto = f"Turno: {estado['turno']} ({estado['color_turno']})"
        superficie_texto = self.__fuente_texto__.render(texto, True, self.color_texto)
        self.__pantalla__.blit(superficie_texto, (self.marge, 20))
        
        # Dados disponibles
        if estado['dados_disponibles']:
            dados_texto = f"Dados: {estado['dados_disponibles']}"
            superficie_dados = self.__fuente_texto__.render(dados_texto, True, self.color_texto)
            self.__pantalla__.blit(superficie_dados, (self.MARGEN, 60))