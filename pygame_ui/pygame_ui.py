import pygame
import sys
import os
import math

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from juego import BackgammonGame

class PygameUI:
    def __init__(self):
        pygame.init()
        
        self.__color_fondo__ = (34, 49, 63)
        self.__color_tablero__ = (101, 67, 33)
        self.__color_punto_claro__ = (222, 184, 135)
        self.__color_punto_oscuro__ = (139, 90, 43)
        self.__color_barra__ = (70, 50, 30)
        self.__color_ficha_blanca__ = (240, 240, 240)
        self.__color_ficha_negra__ = (30, 30, 30)
        self.__color_borde_ficha__ = (180, 180, 180)
        self.__color_seleccion__ = (255, 215, 0)
        self.__color_movimiento_posible__ = (100, 255, 100)
        self.__color_texto__ = (255, 255, 255)
        self.__color_boton__ = (52, 152, 219)
        self.__color_boton_hover__ = (41, 128, 185)
        self.__color_mensaje_error__ = (231, 76, 60)
        self.__color_mensaje_exito__ = (46, 204, 113)
        
        # Dimensiones
        self.__ancho_ventana__ = 1200
        self.__alto_ventana__ = 800
        self.__marge__ = 50
        self.__radio_ficha__ = 20
        
        self.__ancho__ = self.__ancho_ventana__
        self.__alto__ = self.__alto_ventana__
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
        self.__tablero_x__ = self.__marge__
        self.__tablero_y__ = self.__marge__ + 100
        self.__tablero_ancho__ = self.__ancho__ - 2 * self.__marge__
        self.__tablero_alto__ = self.__alto__ - 2 * self.__marge__ - 150
        
        # Ancho de cada punto (triángulo)
        self.__ancho_punto__ = self.__tablero_ancho__ // 14  # 12 puntos + 2 para la barra
        self.__alto_punto__ = self.__tablero_alto__ // 2 - 20
    
    def dibujar_fondo(self):
        self.__pantalla__.fill(self.__color_fondo__)

    def dibujar_tablero(self):
        # Fondo del tablero
        pygame.draw.rect(
            self.__pantalla__,
            self.__color_tablero__,
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
            self.__color_barra__,
            (barra_x, self.__tablero_y__, 
             2 * self.__ancho_punto__, self.__tablero_alto__)
        )
        
        # Dibujar bordes
        pygame.draw.rect(
            self.__pantalla__,
            self.__color_texto__,
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
        color = self.__color_punto_claro__ if numero_punto % 2 == 0 else self.__color_punto_oscuro__
        
        # Resaltar si está seleccionado
        if numero_punto == self.__punto_seleccionado__:
            color = self.__color_seleccion__
        
        # Resaltar si es movimiento posible
        if any(destino == numero_punto for _, destino, _ in self.__movimientos_posibles__):
            # Mezclar con color de movimiento posible
            color = tuple((c + g) // 2 for c, g in zip(color, self.__color_movimiento_posible__))
        
        # Dibujar triángulo
        puntos = [
            (x + self.__ancho_punto__ // 2, y_punta),
            (x, y_base),
            (x + self.__ancho_punto__, y_base)
        ]
        pygame.draw.polygon(self.__pantalla__, color, puntos)
        pygame.draw.polygon(self.__pantalla__, self.__color_texto__, puntos, 1)
        
        # Dibujar número del punto
        texto = self.__fuente_pequeña__.render(str(numero_punto), True, self.__color_texto__)
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
        color_ficha = self.__color_ficha_blanca__ if color == "BLANCO" else self.__color_ficha_negra__
        
        # Dibujar fichas (máximo 5 visibles, luego mostrar número)
        fichas_visibles = min(cantidad, 5)
        for i in range(fichas_visibles):
            y = y_inicio + direccion * i * (self.__radio_ficha__ * 2 + 2)
            pygame.draw.circle(self.__pantalla__, color_ficha, (x, y), self.__radio_ficha__)
            pygame.draw.circle(self.__pantalla__, self.__color_borde_ficha__, (x, y), self.__radio_ficha__, 2)
        
        # Si hay más de 5 fichas, mostrar el número
        if cantidad > 5:
            y = y_inicio + direccion * 4 * (self.__radio_ficha__ * 2 + 2)
            texto = self.__fuente_pequeña__.render(str(cantidad), True, self.__color_texto__)
            texto_rect = texto.get_rect(center=(x, y))
            
            # Fondo para el número
            pygame.draw.circle(self.__pantalla__, color_ficha, (x, y), self.__radio_ficha__)
            pygame.draw.circle(self.__pantalla__, self.__color_borde_ficha__, (x, y), self.__radio_ficha__, 2)
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
                y = y_base + i * (self.__radio_ficha__ * 2 + 2)
                pygame.draw.circle(self.__pantalla__, self.__color_ficha_blanca__, (barra_x, y), self.__radio_ficha__)
                pygame.draw.circle(self.__pantalla__, self.__color_borde_ficha__, (barra_x, y), self.__radio_ficha__, 2)
            
            if fichas_blanco > 5:
                texto = self.__fuente_pequeña__.render(str(fichas_blanco), True, self.__color_texto__)
                self.__pantalla__.blit(texto, (barra_x - 10, y_base - 30))
        
        # Fichas negras en la barra
        fichas_negro = self.__juego__.tablero.fichas_en_barra("NEGRO")
        if fichas_negro > 0:
            y_base = self.__tablero_y__ + self.__tablero_alto__ // 2 - 50
            for i in range(min(fichas_negro, 5)):
                y = y_base - i * (self.__radio_ficha__ * 2 + 2)
                pygame.draw.circle(self.__pantalla__, self.__color_ficha_negra__, (barra_x, y), self.__radio_ficha__)
                pygame.draw.circle(self.__pantalla__, self.__color_borde_ficha__, (barra_x, y), self.__radio_ficha__, 2)
            
            if fichas_negro > 5:
                texto = self.__fuente_pequeña__.render(str(fichas_negro), True, self.__color_texto__)
                self.__pantalla__.blit(texto, (barra_x - 10, y_base + 30))

    def __dibujar_fichas_fuera__(self):
        if not self.__juego__:
            return
        
        # Área de fichas fuera (derecha del tablero)
        fuera_x = self.__tablero_x__ + self.__tablero_ancho__ + 20
        
        # Fichas blancas fuera
        fichas_blanco = self.__juego__.tablero.fichas_fuera("BLANCO")
        texto = self.__fuente_pequeña__.render(f"Blanco fuera: {fichas_blanco}", True, self.__color_texto__)
        self.__pantalla__.blit(texto, (fuera_x, self.__tablero_y__ + self.__tablero_alto__ - 50))
        
        # Fichas negras fuera
        fichas_negro = self.__juego__.tablero.fichas_fuera("NEGRO")
        texto = self.__fuente_pequeña__.render(f"Negro fuera: {fichas_negro}", True, self.__color_texto__)
        self.__pantalla__.blit(texto, (fuera_x, self.__tablero_y__ + 50))

    def dibujar_info_turno(self):
        if not self.__juego__ or not self.__juego__.turno_actual:
            return
        
        estado = self.__juego__.obtener_estado_juego()
        
        # Nombre del jugador y color
        texto = f"Turno: {estado['turno']} ({estado['color_turno']})"
        superficie_texto = self.__fuente_texto__.render(texto, True, self.__color_texto__)
        self.__pantalla__.blit(superficie_texto, (self.__marge__, 20))
        
        # Dados disponibles
        if estado['dados_disponibles']:
            dados_texto = f"Dados: {estado['dados_disponibles']}"
            superficie_dados = self.__fuente_texto__.render(dados_texto, True, self.__color_texto__)
            self.__pantalla__.blit(superficie_dados, (self.__marge__, 60))

    def dibujar_mensaje(self):
        if self.__mensaje__ and pygame.time.get_ticks() - self.__tiempo_mensaje__ < 3000:
            color = self.__color_mensaje_exito__ if "✓" in self.__mensaje__ else self.__color_mensaje_error__
            superficie = self.__fuente_texto__.render(self.__mensaje__, True, color)
            rect = superficie.get_rect(center=(self.__ancho__ // 2, self.__alto__ - 50))
            
            # Fondo semi-transparente
            fondo = pygame.Surface((rect.width + 20, rect.height + 10))
            fondo.fill(self.__color_fondo__)
            fondo.set_alpha(200)
            self.__pantalla__.blit(fondo, (rect.x - 10, rect.y - 5))
            
            self.__pantalla__.blit(superficie, rect)
    
    def mostrar_mensaje(self, mensaje: str):
        self.__mensaje__ = mensaje
        self.__tiempo_mensaje__ = pygame.time.get_ticks()

    def obtener_punto_desde_posicion(self, pos: tuple) -> int:
        x, y = pos
        
        # Verificar si está dentro del tablero
        if not (self.__tablero_x__ <= x <= self.__tablero_x__ + self.__tablero_ancho__ and
                self.__tablero_y__ <= y <= self.__tablero_y__ + self.__tablero_alto__):
            return -1
        
        # Calcular columna
        x_rel = x - self.__tablero_x__
        columna = x_rel // self.__ancho_punto__
        
        # Ajustar por la barra
        if columna >= 6 and columna < 8:
            return -1  # Click en la barra
        if columna >= 8:
            columna -= 2
        
        # Determinar si es parte superior o inferior
        y_rel = y - self.__tablero_y__
        if y_rel < self.__tablero_alto__ // 2:
            # Parte superior (puntos 12-23)
            numero_punto = columna + 12
        else:
            # Parte inferior (puntos 0-11)
            numero_punto = 11 - columna
        
        return numero_punto if 0 <= numero_punto < 24 else -1
    
    def manejar_click(self, pos: tuple):

        if not self.__juego__ or self.__estado__ != "juego":
            return
        
        punto_clickeado = self.obtener_punto_desde_posicion(pos)
        print(f"Click en punto: {punto_clickeado}")
        
        if punto_clickeado == -1:
            # Click fuera del tablero, deseleccionar
            self.__punto_seleccionado__ = None
            self.__movimientos_posibles__ = []
            return
        
        # Si no hay punto seleccionado, seleccionar este
        if self.__punto_seleccionado__ is None:
            color_actual = self.__juego__.turno_actual.color
            punto = self.__juego__.tablero.obtener_puntos()[punto_clickeado]
            
            print(f"Color actual: {color_actual}")  # DEBUG
            print(f"Punto info: {punto}")  # DEBUG
            
            if punto["color"] == color_actual and punto["cantidad"] > 0:
                self.__punto_seleccionado__ = punto_clickeado
                todos_movimientos = self.__juego__.obtener_movimientos_legales()
                print(f"Movimientos legales TODOS: {todos_movimientos}")  # DEBUG
                self.__movimientos_posibles__ = [
                    m for m in todos_movimientos if m[0] == punto_clickeado
                ]
                print(f"Movimientos desde {punto_clickeado}: {self.__movimientos_posibles__}")  # DEBUG
                self.mostrar_mensaje(f"Punto {punto_clickeado} seleccionado")
        else:
            # Ya hay un punto seleccionado, intentar mover
            # Buscar si este destino es válido
            movimiento_valido = None
            for origen, destino, dado in self.__movimientos_posibles__:
                if destino == punto_clickeado:
                    movimiento_valido = (origen, destino, dado)
                    break
            
            if movimiento_valido:
                origen, destino, dado = movimiento_valido
                try:
                    self.__juego__.realizar_movimiento(origen, dado)
                    self.mostrar_mensaje(f"✓ Movimiento realizado: {origen} → {destino}")
                    
                    # Verificar victoria
                    if self.__juego__.verificar_victoria():
                        self.__estado__ = "victoria"
                    
                    # Deseleccionar
                    self.__punto_seleccionado__ = None
                    self.__movimientos_posibles__ = []
                    
                    # Si no quedan dados o no puede mover, cambiar turno
                    if not self.__juego__.tiene_dados_disponibles() or \
                       not self.__juego__.puede_realizar_movimiento():
                        self.__juego__.cambiar_turno()
                        if self.__juego__.tiene_dados_disponibles() == False:
                            self.__juego__.tirar_dados()
                
                except Exception as e:
                    self.mostrar_mensaje(f"✗ Error: {e}")
            else:
                # Cambiar selección a este punto si es del jugador actual
                color_actual = self.__juego__.turno_actual.color
                punto = self.__juego__.tablero.obtener_puntos()[punto_clickeado]
                
                if punto["color"] == color_actual and punto["cantidad"] > 0:
                    self.__punto_seleccionado__ = punto_clickeado
                    todos_movimientos = self.__juego__.obtener_movimientos_legales()
                    self.__movimientos_posibles__ = [
                        m for m in todos_movimientos if m[0] == punto_clickeado
                    ]
                else:
                    self.mostrar_mensaje("Movimiento inválido")
    
    def dibujar_menu(self):
        self.dibujar_fondo()
        
        # Título
        titulo = self.__fuente_titulo__.render("BACKGAMMON", True, self.__color_texto__)
        titulo_rect = titulo.get_rect(center=(self.__ancho__ // 2, 150))
        self.__pantalla__.blit(titulo, titulo_rect)
        
        # Botón Jugar
        boton_rect = pygame.Rect(
            self.__ancho__ // 2 - 100,
            self.__alto__ // 2 - 50,
            200, 60
        )
        
        # Verificar hover
        mouse_pos = pygame.mouse.get_pos()
        __color_boton__ = self.__color_boton_hover__ if boton_rect.collidepoint(mouse_pos) else self.__color_boton__
        
        pygame.draw.rect(self.__pantalla__, __color_boton__, boton_rect, border_radius=10)
        pygame.draw.rect(self.__pantalla__, self.__color_texto__, boton_rect, 2, border_radius=10)
        
        texto_boton = self.__fuente_texto__.render("JUGAR", True, self.__color_texto__)
        texto_rect = texto_boton.get_rect(center=boton_rect.center)
        self.__pantalla__.blit(texto_boton, texto_rect)
        
        # Instrucciones
        instrucciones = [
            "Click en una ficha tuya para seleccionarla",
            "Click en un punto válido para mover",
            "El juego tira los dados automáticamente"
        ]
        
        y = self.__alto__ // 2 + 100
        for texto in instrucciones:
            superficie = self.__fuente_pequeña__.render(texto, True, self.__color_texto__)
            rect = superficie.get_rect(center=(self.__ancho__ // 2, y))
            self.__pantalla__.blit(superficie, rect)
            y += 30
        
        return boton_rect
    
    def dibujar_pantalla_victoria(self):
        self.dibujar_fondo()
        self.dibujar_tablero()
        self.dibujar_fichas()
        
        # Overlay semi-transparente
        overlay = pygame.Surface((self.__ancho__, self.__alto__))
        overlay.fill(self.__color_fondo__)
        overlay.set_alpha(200)
        self.__pantalla__.blit(overlay, (0, 0))
        
        # Mensaje de victoria
        if self.__juego__ and self.__juego__.ganador:
            texto_victoria = f"¡{self.__juego__.ganador.nombre} ha ganado!"
            superficie = self.__fuente_titulo__.render(texto_victoria, True, self.__color_mensaje_exito__)
            rect = superficie.get_rect(center=(self.__ancho__ // 2, self.__alto__ // 2 - 50))
            self.__pantalla__.blit(superficie, rect)
        
        # Botón volver al menú
        boton_rect = pygame.Rect(
            self.__ancho__ // 2 - 100,
            self.__alto__ // 2 + 50,
            200, 60
        )
        
        mouse_pos = pygame.mouse.get_pos()
        __color_boton__ = self.__color_boton_hover__ if boton_rect.collidepoint(mouse_pos) else self.__color_boton__
        
        pygame.draw.rect(self.__pantalla__, __color_boton__.boton_rect, border_radius=10)
        pygame.draw.rect(self.__pantalla__, self.__color_texto__, boton_rect, 2, border_radius=10)
        
        texto_boton = self.__fuente_texto__.render("MENÚ", True, self.__color_texto__)
        texto_rect = texto_boton.get_rect(center=boton_rect.center)
        self.__pantalla__.blit(texto_boton, texto_rect)
        
        return boton_rect
    
    def iniciar_juego_nuevo(self):
        # Por ahora nombres fijos, pero podrías agregar input
        self.__juego__ = BackgammonGame("Jugador 1", "Jugador 2")
        self.__juego__.iniciar_juego()
        self.__juego__.tirar_dados()
        self.__estado__ = "juego"
        self.__punto_seleccionado__ = None
        self.__movimientos_posibles__ = []
    
    def manejar_eventos(self):
        """Maneja los eventos de Pygame."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.__ejecutando__ = False
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if self.__estado__ == "menu":
                        boton_rect = self.dibujar_menu()
                        if boton_rect.collidepoint(evento.pos):
                            self.iniciar_juego_nuevo()
                    
                    elif self.__estado__ == "juego":
                        self.manejar_click(evento.pos)
                    
                    elif self.__estado__ == "victoria":
                        boton_rect = self.dibujar_pantalla_victoria()
                        if boton_rect.collidepoint(evento.pos):
                            self.__estado__ = "menu"
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if self.__estado__ == "juego":
                        self.__estado__ = "menu"
                    else:
                        self.__ejecutando__ = False
                
                elif evento.key == pygame.K_SPACE and self.__estado__ == "juego":
                    if not self.__juego__.puede_realizar_movimiento():
                        self.__juego__.cambiar_turno()
                        self.__juego__.tirar_dados()
                        self.mostrar_mensaje("Turno pasado")
    
    def dibujar(self):
        if self.__estado__ == "menu":
            self.dibujar_menu()
        
        elif self.__estado__ == "juego":
            self.dibujar_fondo()
            self.dibujar_tablero()
            self.dibujar_fichas()
            self.dibujar_info_turno()
            self.dibujar_mensaje()
        
        elif self.__estado__ == "victoria":
            self.dibujar_pantalla_victoria()
        
        pygame.display.flip()
    
    def ejecutar(self):
        while self.__ejecutando__:
            self.manejar_eventos()
            self.dibujar()
            self.__reloj__.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()


def main():
    ui = PygameUI()
    ui.ejecutar()


if __name__ == "__main__":
    main()