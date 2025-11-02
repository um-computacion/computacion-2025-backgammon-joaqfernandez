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

## 🔹 Prompt #2 – Funcion para movimientos legales de `Jugador`

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





