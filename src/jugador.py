from tablero import Tablero
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
        #recorre los 24 puntos (casilleros)
        for origen in range(24):
            punto = tablero._Tablero__puntos__[origen] 
            if punto["color"] != self.__color__ or punto["cantidad"] == 0:
                continue

            for dado in dados:
                destino = tablero.lugar_destino(self.__color__, origen, dado)
                if tablero.hay_ficha_o_no(self.__color__, origen, dado):
                    legales.append((origen, destino, dado))

        return legales

    def puede_mover(self, tablero, dados: List[int]) -> bool:
        return len(self.movimientos_legales(tablero, dados)) > 0
    
    def mover(self, tablero, origen: int, dado: int) -> int:
        destino = tablero.lugar_destino(self.__color__, origen, dado)
        tablero.aplicar_hay_ficha(self.__color__, origen, dado)
        return destino