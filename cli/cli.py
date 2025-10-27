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

    def mostrar_tablero(self):
        print("\n" + "=" * 60)
        print(" " * 22 + "TABLERO")
        print("=" * 60)
        
        # Parte superior (puntos 12-23)
        print("\n  12  11  10   9   8   7  |  6   5   4   3   2   1")
        print("  " + "-" * 54)
        
        # Mostrar fichas en parte superior
        linea_superior = "  "
        for i in range(12, 24):
            punto = self.__juego__.tablero.obtener_puntos()[i]
            if punto["cantidad"] > 0:
                simbolo = "B" if punto["color"] == "BLANCO" else "N"
                linea_superior += f"{simbolo}{punto['cantidad']:1d}  "
            else:
                linea_superior += "··  "
            
            if i == 17:  # Separador en medio
                linea_superior += "| "
        
        print(linea_superior)
        print("  " + "-" * 54)
        
        # Mostrar barra y fichas fuera
        barra_blanco = self.__juego__.tablero.fichas_en_barra("BLANCO")
        barra_negro = self.__juego__.tablero.fichas_en_barra("NEGRO")
        fuera_blanco = self.__juego__.tablero.fichas_fuera("BLANCO")
        fuera_negro = self.__juego__.tablero.fichas_fuera("NEGRO")
        
        print(f"\n  BARRA: Blanco={barra_blanco}, Negro={barra_negro}")
        print(f"  FUERA: Blanco={fuera_blanco}, Negro={fuera_negro}")
        
        print("\n  " + "-" * 54)
        
        # Mostrar fichas en parte inferior
        linea_inferior = "  "
        for i in range(11, -1, -1):
            punto = self.__juego__.tablero.obtener_puntos()[i]
            if punto["cantidad"] > 0:
                simbolo = "B" if punto["color"] == "BLANCO" else "N"
                linea_inferior += f"{simbolo}{punto['cantidad']:1d}  "
            else:
                linea_inferior += "··  "
            
            if i == 6:
                linea_inferior += "| "
        
        print(linea_inferior)
        print("  " + "-" * 54)
        
        # Parte inferior (puntos 11-0)
        print("  11  10   9   8   7   6  |  5   4   3   2   1   0")
        print("=" * 60 + "\n")

    def mostrar_estado_turno(self):
        estado = self.__juego__.obtener_estado_juego()
        
        print(f"Turno de: {estado['turno']} ({estado['color_turno']})")
        
        if estado['dados_disponibles']:
            print(f"Dados disponibles: {estado['dados_disponibles']}")
        
        # Mostrar movimientos legales
        movimientos = self.__juego__.obtener_movimientos_legales()
        if movimientos:
            print(f"\nMovimientos posibles: {len(movimientos)}")