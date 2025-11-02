from src.tablero import Tablero
from typing import List, Tuple

ficha1 = "BLANCO"
ficha2 = "NEGRO"

class Jugador:
    def __init__(self, nombre: str, color: str):
        if color not in (ficha1, ficha2):
            raise ValueError("Color inválido. Use 'BLANCO' o 'NEGRO'.")
        self.__nombre__ = nombre
        self.__color__ = color

    @property
    def nombre(self) -> str:
        return self.__nombre__

    @property
    def color(self) -> str:
        return self.__color__
    
    def direccion(self, tablero) -> int:
        return tablero.definir_direccion(self.__color__)
    
    def movimientos_legales(self, tablero, dados: List[int]) -> List[Tuple[int, int, int]]:
        legales: List[Tuple[int, int, int]] = []
        
        print(f"\n=== BUSCANDO MOVIMIENTOS ===")  # DEBUG
        print(f"Color: {self.__color__}, Dados: {dados}")  # DEBUG

        # Si hay fichas en la barra, solo se pueden reingresar
        if tablero.hay_obligacion_reingresar(self.__color__):
            print(f"HAY OBLIGACIÓN DE REINGRESAR")  # DEBUG
            for d in dados:
                if tablero.puede_reingresar(self.__color__, d):
                    destino = tablero.punto_entrada_desde_barra(self.__color__, d)
                    legales.append((-1, destino, d))
                    print(f"  Reingreso posible: barra → {destino} con dado {d}")  # DEBUG
            return legales

        # Movimientos regulares
        puntos = tablero.obtener_puntos()
        print(f"Buscando movimientos regulares...")  # DEBUG
        
        for origen in range(24):
            p = puntos[origen]
            if p["color"] != self.__color__ or p["cantidad"] == 0:
                continue
            
            print(f"  Punto {origen}: {p['cantidad']} fichas {p['color']}")  # DEBUG
            
            for d in dados:
                destino = tablero.lugar_destino(self.__color__, origen, d)
                print(f"    Dado {d}: {origen} → {destino}...", end=" ")  # DEBUG
                if tablero.es_movimiento_bearing_off(self.__color__, origen, d):
                    legales.append((origen, tablero.destino_fuera(self.__color__), d))
                    print(f"✓ BEAR-OFF")  # DEBUG
                    continue


                if tablero.hay_ficha_o_no(self.__color__, origen, d):
                    legales.append((origen, destino, d))
                    print(f"✓ VÁLIDO")  # DEBUG
                else:
                    print(f"✗ INVÁLIDO")  # DEBUG

        print(f"Total movimientos legales: {len(legales)}")  # DEBUG
        return legales

    def puede_mover(self, tablero, dados: List[int]) -> bool:
        return len(self.movimientos_legales(tablero, dados)) > 0
    
    def mover(self, tablero, origen: int, dado: int) -> int:
        if tablero.es_movimiento_bearing_off(self.__color__, origen, dado):
            tablero.aplicar_hay_ficha(self.__color__, origen, dado)
            return tablero.destino_fuera(self.__color__)

        destino = tablero.lugar_destino(self.__color__, origen, dado)
        tablero.aplicar_hay_ficha(self.__color__, origen, dado)
        return destino