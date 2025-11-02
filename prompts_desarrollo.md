# 📜 Prompts de Desarrollo – Backgammon Computación 2025  

En este archivo se registran todos los prompts utilizados con herramientas de IA durante el **desarrollo** del proyecto.  
Cada entrada incluye el modelo usado, el prompt original, la respuesta obtenida y cómo se aplicó (si se usó o mse dificó).  

---

## 🔹 Prompt #1 – Funcion para movimientos legales de `Jugador`

**🛠️ Herramienta / Modelo:** ChatGPT (GPT-5)  
**📅 Fecha:** 16/09/2025 – 15:03  
**📂 Archivo relacionado:** `src/jugador.py`  

---

### 📝 Prompt enviado  
```markdown 
Necesito una funcion que me devuela los posibles movimientos legales
que puede hacer un jugador
```
---
### 📝 Respuesta de la IA
```markdown 
def movimientos_legales(self, tablero, dados: List[int]) -> List[Tuple[int, int, int]]:
        """
        Calcula movimientos (origen, destino, dado) legales con el estado actual del tablero.
        Por ahora considera SOLO movimientos regulares (sin barra ni bearing-off).

        Args:
            tablero (Tablero): instancia del tablero actual.
            dados (List[int]): valores disponibles del turno (ej: [3, 5] o [4,4,4,4]).

        Return:
            List[Tuple[int, int, int]]: lista de (origen, destino, dado).
        """
        legales: List[Tuple[int, int, int]] = []

        # Recorremos los 24 puntos y probamos cada dado.
        for origen in range(24):
            punto = tablero._Tablero__puntos__[origen]  # usamos lo que ya tenés
            if punto["color"] != self.__color__ or punto["cantidad"] == 0:
                continue

            for dado in dados:
                destino = tablero.lugar_destino(self.__color__, origen, dado)
                if tablero.hay_ficha_o_no(self.__color__, origen, dado):
                    legales.append((origen, destino, dado))

        return legales
```
---

## 🔹 Prompt #2 – Clase de `pygame`

**🛠️ Herramienta / Modelo:** Claude (Sonnet 4.5)  
**📅 Fecha:** 28/10/2025 – 13:03  
**📂 Archivo relacionado:** `pygame_ui/pygame_ui`  

---

### 📝 Prompt enviado  
```markdown 
generame el pygame, leyendo la documentacion de su pagina https://www.pygame.org/news
```
---
### 📝 Respuesta de la IA
```markdown 
"""
Módulo que contiene la interfaz gráfica con Pygame para Backgammon.
Proporciona una experiencia visual e interactiva del juego.
"""
import pygame
import sys
import os
import math

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from juego import BackgammonGame


class PygameUI:
    """
    Interfaz gráfica del juego de Backgammon usando Pygame.
    
    Atributos:
        __pantalla__ (pygame.Surface): Superficie principal de la ventana.
        __reloj__ (pygame.Clock): Reloj para controlar FPS.
        __juego__ (BackgammonGame): Instancia del juego.
        __ancho__ (int): Ancho de la ventana.
        __alto__ (int): Alto de la ventana.
        __ejecutando__ (bool): Estado de ejecución de la UI.
        __fuente_titulo__ (pygame.font.Font): Fuente para títulos.
        __fuente_texto__ (pygame.font.Font): Fuente para texto normal.
        __fuente_pequeña__ (pygame.font.Font): Fuente para texto pequeño.
        __punto_seleccionado__ (int): Punto actualmente seleccionado.
        __movimientos_posibles__ (list): Lista de movimientos posibles.
        __mensaje__ (str): Mensaje a mostrar al usuario.
        __estado__ (str): Estado actual de la UI (menu, juego, victoria).
    """
    
    # Colores
    COLOR_FONDO = (34, 49, 63)
    COLOR_TABLERO = (101, 67, 33)
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
        """Inicializa Pygame y la interfaz gráfica."""
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
    
    def __calcular_dimensiones_tablero__(self):
        """Calcula las dimensiones y posiciones del tablero."""
        self.__tablero_x__ = self.MARGEN
        self.__tablero_y__ = self.MARGEN + 100
        self.__tablero_ancho__ = self.__ancho__ - 2 * self.MARGEN
        self.__tablero_alto__ = self.__alto__ - 2 * self.MARGEN - 150
        
        # Ancho de cada punto (triángulo)
        self.__ancho_punto__ = self.__tablero_ancho__ // 14  # 12 puntos + 2 para la barra
        self.__alto_punto__ = self.__tablero_alto__ // 2 - 20
    
    def dibujar_fondo(self):
        """Dibuja el fondo de la ventana."""
        self.__pantalla__.fill(self.COLOR_FONDO)
    
    def dibujar_tablero(self):
        """Dibuja el tablero de Backgammon con los 24 puntos."""
        # Fondo del tablero
        pygame.draw.rect(
            self.__pantalla__,
            self.COLOR_TABLERO,
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
            self.COLOR_BARRA,
            (barra_x, self.__tablero_y__, 
             2 * self.__ancho_punto__, self.__tablero_alto__)
        )
        
        # Dibujar bordes
        pygame.draw.rect(
            self.__pantalla__,
            self.COLOR_TEXTO,
            (self.__tablero_x__, self.__tablero_y__, 
             self.__tablero_ancho__, self.__tablero_alto__),
            3
        )
    
    def __dibujar_punto__(self, numero_punto: int):
        """
        Dibuja un punto (triángulo) del tablero.
        
        Args:
            numero_punto (int): Número del punto (0-23).
        """
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
        """Dibuja todas las fichas en el tablero."""
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
        """
        Dibuja las fichas en un punto específico.
        
        Args:
            numero_punto (int): Número del punto.
            color (str): Color de las fichas ("BLANCO" o "NEGRO").
            cantidad (int): Cantidad de fichas.
        """
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
        color_ficha = self.COLOR_FICHA_BLANCA if color == "BLANCO" else self.COLOR_FICHA_NEGRA
        
        # Dibujar fichas (máximo 5 visibles, luego mostrar número)
        fichas_visibles = min(cantidad, 5)
        for i in range(fichas_visibles):
            y = y_inicio + direccion * i * (self.RADIO_FICHA * 2 + 2)
            pygame.draw.circle(self.__pantalla__, color_ficha, (x, y), self.RADIO_FICHA)
            pygame.draw.circle(self.__pantalla__, self.COLOR_BORDE_FICHA, (x, y), self.RADIO_FICHA, 2)
        
        # Si hay más de 5 fichas, mostrar el número
        if cantidad > 5:
            y = y_inicio + direccion * 4 * (self.RADIO_FICHA * 2 + 2)
            texto = self.__fuente_pequeña__.render(str(cantidad), True, self.COLOR_TEXTO)
            texto_rect = texto.get_rect(center=(x, y))
            
            # Fondo para el número
            pygame.draw.circle(self.__pantalla__, color_ficha, (x, y), self.RADIO_FICHA)
            pygame.draw.circle(self.__pantalla__, self.COLOR_BORDE_FICHA, (x, y), self.RADIO_FICHA, 2)
            self.__pantalla__.blit(texto, texto_rect)
    
    def __dibujar_fichas_barra__(self):
        """Dibuja las fichas que están en la barra."""
        if not self.__juego__:
            return
        
        barra_x = self.__tablero_x__ + 6 * self.__ancho_punto__ + self.__ancho_punto__
        
        # Fichas blancas en la barra
        fichas_blanco = self.__juego__.tablero.fichas_en_barra("BLANCO")
        if fichas_blanco > 0:
            y_base = self.__tablero_y__ + self.__tablero_alto__ // 2 + 50
            for i in range(min(fichas_blanco, 5)):
                y = y_base + i * (self.RADIO_FICHA * 2 + 2)
                pygame.draw.circle(self.__pantalla__, self.COLOR_FICHA_BLANCA, (barra_x, y), self.RADIO_FICHA)
                pygame.draw.circle(self.__pantalla__, self.COLOR_BORDE_FICHA, (barra_x, y), self.RADIO_FICHA, 2)
            
            if fichas_blanco > 5:
                texto = self.__fuente_pequeña__.render(str(fichas_blanco), True, self.COLOR_TEXTO)
                self.__pantalla__.blit(texto, (barra_x - 10, y_base - 30))
        
        # Fichas negras en la barra
        fichas_negro = self.__juego__.tablero.fichas_en_barra("NEGRO")
        if fichas_negro > 0:
            y_base = self.__tablero_y__ + self.__tablero_alto__ // 2 - 50
            for i in range(min(fichas_negro, 5)):
                y = y_base - i * (self.RADIO_FICHA * 2 + 2)
                pygame.draw.circle(self.__pantalla__, self.COLOR_FICHA_NEGRA, (barra_x, y), self.RADIO_FICHA)
                pygame.draw.circle(self.__pantalla__, self.COLOR_BORDE_FICHA, (barra_x, y), self.RADIO_FICHA, 2)
            
            if fichas_negro > 5:
                texto = self.__fuente_pequeña__.render(str(fichas_negro), True, self.COLOR_TEXTO)
                self.__pantalla__.blit(texto, (barra_x - 10, y_base + 30))
    
    def __dibujar_fichas_fuera__(self):
        """Dibuja las fichas que están fuera del tablero."""
        if not self.__juego__:
            return
        
        # Área de fichas fuera (derecha del tablero)
        fuera_x = self.__tablero_x__ + self.__tablero_ancho__ + 20
        
        # Fichas blancas fuera
        fichas_blanco = self.__juego__.tablero.fichas_fuera("BLANCO")
        texto = self.__fuente_pequeña__.render(f"Blanco fuera: {fichas_blanco}", True, self.COLOR_TEXTO)
        self.__pantalla__.blit(texto, (fuera_x, self.__tablero_y__ + self.__tablero_alto__ - 50))
        
        # Fichas negras fuera
        fichas_negro = self.__juego__.tablero.fichas_fuera("NEGRO")
        texto = self.__fuente_pequeña__.render(f"Negro fuera: {fichas_negro}", True, self.COLOR_TEXTO)
        self.__pantalla__.blit(texto, (fuera_x, self.__tablero_y__ + 50))
    
    def dibujar_info_turno(self):
        """Dibuja la información del turno actual."""
        if not self.__juego__ or not self.__juego__.turno_actual:
            return
        
        estado = self.__juego__.obtener_estado_juego()
        
        # Nombre del jugador y color
        texto = f"Turno: {estado['turno']} ({estado['color_turno']})"
        superficie_texto = self.__fuente_texto__.render(texto, True, self.COLOR_TEXTO)
        self.__pantalla__.blit(superficie_texto, (self.MARGEN, 20))
        
        # Dados disponibles
        if estado['dados_disponibles']:
            dados_texto = f"Dados: {estado['dados_disponibles']}"
            superficie_dados = self.__fuente_texto__.render(dados_texto, True, self.COLOR_TEXTO)
            self.__pantalla__.blit(superficie_dados, (self.MARGEN, 60))
    
    def dibujar_mensaje(self):
        """Dibuja mensajes temporales al usuario."""
        if self.__mensaje__ and pygame.time.get_ticks() - self.__tiempo_mensaje__ < 3000:
            color = self.COLOR_MENSAJE_EXITO if "✓" in self.__mensaje__ else self.COLOR_MENSAJE_ERROR
            superficie = self.__fuente_texto__.render(self.__mensaje__, True, color)
            rect = superficie.get_rect(center=(self.__ancho__ // 2, self.__alto__ - 50))
            
            # Fondo semi-transparente
            fondo = pygame.Surface((rect.width + 20, rect.height + 10))
            fondo.fill(self.COLOR_FONDO)
            fondo.set_alpha(200)
            self.__pantalla__.blit(fondo, (rect.x - 10, rect.y - 5))
            
            self.__pantalla__.blit(superficie, rect)
    
    def mostrar_mensaje(self, mensaje: str):
        """
        Muestra un mensaje temporal al usuario.
        
        Args:
            mensaje (str): Mensaje a mostrar.
        """
        self.__mensaje__ = mensaje
        self.__tiempo_mensaje__ = pygame.time.get_ticks()
    
    def obtener_punto_desde_posicion(self, pos: tuple) -> int:
        """
        Obtiene el número de punto del tablero desde una posición del mouse.
        
        Args:
            pos (tuple): Posición (x, y) del mouse.
        
        Returns:
            int: Número del punto (0-23) o -1 si no está sobre un punto válido.
        """
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
        """
        Maneja el click del mouse en el tablero.
        
        Args:
            pos (tuple): Posición (x, y) del click.
        """
        if not self.__juego__ or self.__estado__ != "juego":
            return
        
        punto_clickeado = self.obtener_punto_desde_posicion(pos)
        
        if punto_clickeado == -1:
            # Click fuera del tablero, deseleccionar
            self.__punto_seleccionado__ = None
            self.__movimientos_posibles__ = []
            return
        
        # Si no hay punto seleccionado, seleccionar este
        if self.__punto_seleccionado__ is None:
            color_actual = self.__juego__.turno_actual.color
            punto = self.__juego__.tablero.obtener_puntos()[punto_clickeado]
            
            if punto["color"] == color_actual and punto["cantidad"] > 0:
                self.__punto_seleccionado__ = punto_clickeado
                # Obtener movimientos posibles desde este punto
                todos_movimientos = self.__juego__.obtener_movimientos_legales()
                self.__movimientos_posibles__ = [
                    m for m in todos_movimientos if m[0] == punto_clickeado
                ]
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
                    self.mostrar_mensaje("✗ Movimiento inválido")
    
    def dibujar_menu(self):
        """Dibuja el menú principal."""
        self.dibujar_fondo()
        
        # Título
        titulo = self.__fuente_titulo__.render("BACKGAMMON", True, self.COLOR_TEXTO)
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
        color_boton = self.COLOR_BOTON_HOVER if boton_rect.collidepoint(mouse_pos) else self.COLOR_BOTON
        
        pygame.draw.rect(self.__pantalla__, color_boton, boton_rect, border_radius=10)
        pygame.draw.rect(self.__pantalla__, self.COLOR_TEXTO, boton_rect, 2, border_radius=10)
        
        texto_boton = self.__fuente_texto__.render("JUGAR", True, self.COLOR_TEXTO)
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
            superficie = self.__fuente_pequeña__.render(texto, True, self.COLOR_TEXTO)
            rect = superficie.get_rect(center=(self.__ancho__ // 2, y))
            self.__pantalla__.blit(superficie, rect)
            y += 30
        
        return boton_rect
    
    def dibujar_pantalla_victoria(self):
        """Dibuja la pantalla de victoria."""
        self.dibujar_fondo()
        self.dibujar_tablero()
        self.dibujar_fichas()
        
        # Overlay semi-transparente
        overlay = pygame.Surface((self.__ancho__, self.__alto__))
        overlay.fill(self.COLOR_FONDO)
        overlay.set_alpha(200)
        self.__pantalla__.blit(overlay, (0, 0))
        
        # Mensaje de victoria
        if self.__juego__ and self.__juego__.ganador:
            texto_victoria = f"¡{self.__juego__.ganador.nombre} ha ganado!"
            superficie = self.__fuente_titulo__.render(texto_victoria, True, self.COLOR_MENSAJE_EXITO)
            rect = superficie.get_rect(center=(self.__ancho__ // 2, self.__alto__ // 2 - 50))
            self.__pantalla__.blit(superficie, rect)
        
        # Botón volver al menú
        boton_rect = pygame.Rect(
            self.__ancho__ // 2 - 100,
            self.__alto__ // 2 + 50,
            200, 60
        )
        
        mouse_pos = pygame.mouse.get_pos()
        color_boton = self.COLOR_BOTON_HOVER if boton_rect.collidepoint(mouse_pos) else self.COLOR_BOTON
        
        pygame.draw.rect(self.__pantalla__, color_boton, boton_rect, border_radius=10)
        pygame.draw.rect(self.__pantalla__, self.COLOR_TEXTO, boton_rect, 2, border_radius=10)
        
        texto_boton = self.__fuente_texto__.render("MENÚ", True, self.COLOR_TEXTO)
        texto_rect = texto_boton.get_rect(center=boton_rect.center)
        self.__pantalla__.blit(texto_boton, texto_rect)
        
        return boton_rect
    
    def iniciar_juego_nuevo(self):
        """Inicia un nuevo juego."""
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
                if evento.button == 1:  # Click izquierdo
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
                    # Pasar turno (si no puede mover)
                    if not self.__juego__.puede_realizar_movimiento():
                        self.__juego__.cambiar_turno()
                        self.__juego__.tirar_dados()
                        self.mostrar_mensaje("Turno pasado")
    
    def actualizar(self):
        """Actualiza el estado del juego."""
        pass  # Por ahora no hay animaciones
    
    def dibujar(self):
        """Dibuja todos los elementos en pantalla."""
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
        """Bucle principal de la interfaz gráfica."""
        while self.__ejecutando__:
            self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.__reloj__.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()


def main():
    """Función principal para ejecutar la UI de Pygame."""
    ui = PygameUI()
    ui.ejecutar()


if __name__ == "__main__":
    main()
```


---

## 🔹 Prompt #3 – Tests `CLI`

**🛠️ Herramienta / Modelo:** Claude (Sonnet 4.5)  
**📅 Fecha:** 1/10/2025 – 13:03  
**📂 Archivo relacionado:** `test/test_cli`  

---

### 📝 Prompt enviado  
```markdown 
Generame un archivo test, con unittest. Te dejo el archivo cli para que lo veas y sepas como esta hecho
```
---
### 📝 Respuesta de la IA
```markdown 

"""
Test suite para la clase CLI del juego Backgammon.
Este archivo contiene tests exhaustivos para lograr >94% de cobertura.

Autor: [Tu Nombre]
Fecha: 2025-11-01
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, call
import sys
import os

# Agregar el path para importar CLI
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cli.cli import CLI


class TestCLI(unittest.TestCase):
    """
    Suite de tests para la clase CLI.
    
    Cobertura objetivo: >94%
    Estrategia: Mockear dependencias externas (BackgammonGame, input, print, os.system)
    """
    
    def setUp(self):
        """
        Configuración inicial antes de cada test.
        Se ejecuta automáticamente antes de cada método test_*.
        """
        self.cli = CLI()
        
        # Mock del juego para evitar dependencias
        self.mock_juego = MagicMock()
        self.cli._CLI__juego__ = self.mock_juego
    
    def tearDown(self):
        """
        Limpieza después de cada test.
        """
        self.cli = None
        self.mock_juego = None
    
    # ==================== TESTS DE INICIALIZACIÓN ====================
    
    def test_init_estado_inicial(self):
        """
        Test 1: Verificar que la inicialización establece correctamente los atributos.
        """
        cli = CLI()
        self.assertIsNone(cli._CLI__juego__)
        self.assertFalse(cli._CLI__ejecutando__)
    
    # ==================== TESTS DE LIMPIAR PANTALLA ====================
    
    @patch('os.system')
    @patch('os.name', 'nt')
    def test_limpiar_pantalla_windows(self, mock_system):
        """
        Test 2: Verificar que en Windows se ejecuta 'cls'.
        
        Explicación:
        - @patch('os.name', 'nt') simula que estamos en Windows
        - @patch('os.system') intercepta la llamada al sistema
        """
        self.cli.limpiar_pantalla()
        mock_system.assert_called_once_with('cls')
    
    @patch('os.system')
    @patch('os.name', 'posix')
    def test_limpiar_pantalla_unix(self, mock_system):
        """
        Test 3: Verificar que en Unix/Linux se ejecuta 'clear'.
        """
        self.cli.limpiar_pantalla()
        mock_system.assert_called_once_with('clear')
    
    # ==================== TESTS DE MOSTRAR BIENVENIDA ====================
    
    @patch('builtins.print')
    def test_mostrar_bienvenida(self, mock_print):
        """
        Test 4: Verificar que se muestra el mensaje de bienvenida.
        
        Explicación:
        - @patch('builtins.print') captura todas las llamadas a print()
        - Verificamos que se imprime el título del juego
        """
        self.cli.mostrar_bienvenida()
        
        # Verificar que se llamó a print varias veces
        self.assertGreater(mock_print.call_count, 0)
        
        # Verificar que se imprimió "BACKGAMMON"
        llamadas = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("BACKGAMMON" in llamada for llamada in llamadas))
    
    # ==================== TESTS DE SOLICITAR NOMBRES ====================
    
    @patch('builtins.input', side_effect=['Joaquin', 'Walter'])
    @patch('builtins.print')
    def test_solicitar_nombres_con_valores(self, mock_print, mock_input):
        """
        Test 5: Verificar que se capturan correctamente los nombres ingresados.
        
        Explicación:
        - side_effect=['Joaquin', 'Walter'] simula dos inputs consecutivos
        - El método debe retornar una tupla con ambos nombres
        """
        nombre1, nombre2 = self.cli.solicitar_nombres()
        
        self.assertEqual(nombre1, 'Joaquin')
        self.assertEqual(nombre2, 'Walter')
        self.assertEqual(mock_input.call_count, 2)
    
    @patch('builtins.input', side_effect=['', ''])
    @patch('builtins.print')
    def test_solicitar_nombres_vacios_usa_defaults(self, mock_print, mock_input):
        """
        Test 6: Verificar que se usan nombres por defecto si no se ingresa nada.
        
        Caso borde: Inputs vacíos
        """
        nombre1, nombre2 = self.cli.solicitar_nombres()
        
        self.assertEqual(nombre1, 'Jugador 1')
        self.assertEqual(nombre2, 'Jugador 2')
    
    @patch('builtins.input', side_effect=['  Juan  ', '  Pedro  '])
    @patch('builtins.print')
    def test_solicitar_nombres_con_espacios(self, mock_print, mock_input):
        """
        Test 7: Verificar que se eliminan espacios en blanco con strip().
        """
        nombre1, nombre2 = self.cli.solicitar_nombres()
        
        self.assertEqual(nombre1, 'Juan')
        self.assertEqual(nombre2, 'Pedro')
    
    # ==================== TESTS DE MOSTRAR TABLERO ====================
    
    @patch('builtins.print')
    def test_mostrar_tablero_basico(self, mock_print):
        """
        Test 8: Verificar que se muestra el tablero sin errores.
        
        Explicación:
        - Necesitamos mockear el tablero del juego
        - Simulamos puntos con fichas
        """
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
        """
        Test 9: Verificar visualización con fichas en la barra.
        """
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

if __name__ == '__main__':
    # Configurar unittest para verbose output
    unittest.main(verbosity=2)
```

---

## 🔹 Prompt #4 – Arreglar crash de `Pygame`

**🛠️ Herramienta / Modelo:** ChatGPT (GPT-5)  
**📅 Fecha:** 16/09/2025 – 22:00
**📂 Archivo relacionado:** `pygame_ui/pygame_ui`  

---

### 📝 Prompt enviado  
```markdown 
Cuando ejecuto el juego, se abre la ventana, aprieto el boton jugar, y se crashea y se cierra la ventana

```
---
### 📝 Respuesta de la IA
```markdown 
def __dibujar_info_fuera__(self, area_rect: pygame.Rect, titulo: str, cantidad: int, color_ficha: tuple):
        if not area_rect:
            return

        titulo_superficie = self.__fuente_texto__.render(titulo, True, self.__color_texto__)
        titulo_rect = titulo_superficie.get_rect(center=(area_rect.centerx, area_rect.top + 25))
        self.__pantalla__.blit(titulo_superficie, titulo_rect)

        cantidad_texto = f"Fichas fuera: {cantidad}"
        cantidad_superficie = self.__fuente_pequeña__.render(cantidad_texto, True, self.__color_texto__)
        cantidad_rect = cantidad_superficie.get_rect(center=(area_rect.centerx, area_rect.bottom - 25))
        self.__pantalla__.blit(cantidad_superficie, cantidad_rect)

        fichas_visibles = min(cantidad, 5)
        if fichas_visibles:
            espacio = self.__radio_ficha__ * 2 + 6
            ancho_total = (fichas_visibles - 1) * espacio
            x_inicio = area_rect.centerx - ancho_total // 2
            y_pos = (area_rect.top + area_rect.bottom) // 2

            for i in range(fichas_visibles):
                x = x_inicio + i * espacio
                pygame.draw.circle(self.__pantalla__, color_ficha, (x, y_pos), self.__radio_ficha__)
                pygame.draw.circle(self.__pantalla__, self.__color_borde_ficha__, (x, y_pos), self.__radio_ficha__, 2)

            if cantidad > fichas_visibles:
                texto_mas = f"+{cantidad - fichas_visibles}"
                superficie_mas = self.__fuente_pequeña__.render(texto_mas, True, self.__color_texto__)
                rect_mas = superficie_mas.get_rect(center=(area_rect.centerx, y_pos + self.__radio_ficha__ + 15))
                self.__pantalla__.blit(superficie_mas, rect_mas)
```

## 🔹 Prompt #5 – Arreglar crash de `Pygame`

**🛠️ Herramienta / Modelo:** ChatGPT (GPT-5)  
**📅 Fecha:** 16/09/2025 – 22:28  
**📂 Archivo relacionado:** `pygame_ui/pygame_ui`  

---

### 📝 Prompt enviado  
```markdown 
al poner una ficha comida en el medio, despues ese color no funciona, no se puede hacer nada

```
---
### 📝 Respuesta de la IA
```markdown 
    barra_x = self.__tablero_x__ + 6 * self.__ancho_punto__
        barra_ancho = 2 * self.__ancho_punto__
        barra_alto = self.__tablero_alto__ // 2

        self.__rect_barra_superior__ = pygame.Rect(
            barra_x,
            self.__tablero_y__,
            barra_ancho,
            barra_alto
        )

        self.__rect_barra_inferior__ = pygame.Rect(
            barra_x,
            self.__tablero_y__ + barra_alto,
            barra_ancho,
            barra_alto
        )

```

```markdown

        if hasattr(self, "__rect_barra_inferior__"):
            if self.__punto_seleccionado__ == "barra_blanco":
                pygame.draw.rect(
                    self.__pantalla__,
                    self.__color_seleccion__,
                    self.__rect_barra_inferior__,
                    3,
                    border_radius=12
                )
            if self.__punto_seleccionado__ == "barra_negro":
                pygame.draw.rect(
                    self.__pantalla__,
                    self.__color_seleccion__,
                    self.__rect_barra_superior__,
                    3,
                    border_radius=12
                )

```

```markdown
def __dibujar_info_fuera__(self, area_rect: pygame.Rect, titulo: str, cantidad: int, color_ficha: tuple):
        if not area_rect:
            return

        titulo_superficie = self.__fuente_texto__.render(titulo, True, self.__color_texto__)
        titulo_rect = titulo_superficie.get_rect(center=(area_rect.centerx, area_rect.top + 25))
        self.__pantalla__.blit(titulo_superficie, titulo_rect)

        cantidad_texto = f"Fichas fuera: {cantidad}"
        cantidad_superficie = self.__fuente_pequeña__.render(cantidad_texto, True, self.__color_texto__)
        cantidad_rect = cantidad_superficie.get_rect(center=(area_rect.centerx, area_rect.bottom - 25))
        self.__pantalla__.blit(cantidad_superficie, cantidad_rect)

        fichas_visibles = min(cantidad, 5)
        if fichas_visibles:
            espacio = self.__radio_ficha__ * 2 + 6
            ancho_total = (fichas_visibles - 1) * espacio
            x_inicio = area_rect.centerx - ancho_total // 2
            y_pos = (area_rect.top + area_rect.bottom) // 2

            for i in range(fichas_visibles):
                x = x_inicio + i * espacio
                pygame.draw.circle(self.__pantalla__, color_ficha, (x, y_pos), self.__radio_ficha__)
                pygame.draw.circle(self.__pantalla__, self.__color_borde_ficha__, (x, y_pos), self.__radio_ficha__, 2)

            if cantidad > fichas_visibles:
                texto_mas = f"+{cantidad - fichas_visibles}"
                superficie_mas = self.__fuente_pequeña__.render(texto_mas, True, self.__color_texto__)
                rect_mas = superficie_mas.get_rect(center=(area_rect.centerx, y_pos + self.__radio_ficha__ + 15))
                self.__pantalla__.blit(superficie_mas, rect_mas)
```
```markdown
def obtener_punto_desde_posicion(self, pos: tuple):
        x, y = pos

        if hasattr(self, "__area_fuera_blanco__"):
            if self.__area_fuera_blanco__.collidepoint(pos):
                return self.__destino_fuera_blanco__
            if self.__area_fuera_negro__.collidepoint(pos):
                return self.__destino_fuera_negro__

        if self.__juego__ and hasattr(self, "__rect_barra_inferior__"):
            if self.__rect_barra_inferior__.collidepoint(pos):
                return "barra_blanco"
            if self.__rect_barra_superior__.collidepoint(pos):
                return "barra_negro"


```
```markdown

        if isinstance(punto_clickeado, str) and punto_clickeado.startswith("barra"):
            if self.__punto_seleccionado__ == punto_clickeado:
                self.__punto_seleccionado__ = None
                self.__movimientos_posibles__ = []
                return
            self.__seleccionar_barra__(punto_clickeado)
            return

```
```markdown
              if isinstance(punto_clickeado, str) and punto_clickeado.startswith("barra"):
                    self.__seleccionar_barra__(punto_clickeado)
                else:
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

    def __seleccionar_barra__(self, identificador: str):
        if not self.__juego__ or not self.__juego__.turno_actual:
            return

        color_barra = "BLANCO" if identificador == "barra_blanco" else "NEGRO"

        if self.__juego__.turno_actual.color != color_barra:
            self.mostrar_mensaje("Es el turno del otro color")
            return

        if self.__juego__.tablero.fichas_en_barra(color_barra) == 0:
            self.mostrar_mensaje("No hay fichas en la barra")
            return

        movimientos = self.__juego__.obtener_movimientos_legales()
        movimientos_barra = [m for m in movimientos if m[0] == -1]

        if not movimientos_barra:
            self.mostrar_mensaje("No hay movimientos disponibles desde la barra")
            return

        self.__punto_seleccionado__ = identificador
        self.__movimientos_posibles__ = movimientos_barra

        color_texto = "blanca" if color_barra == "BLANCO" else "negra"
        self.mostrar_mensaje(f"Barra {color_texto} seleccionada")

```
