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
    
    def movimientos_legales(self, tablero, dados: list[int]) -> list[tuple[int,int,int]]:
        legales: list[tuple[int,int,int]] = []

        if tablero.hay_obligacion_reingresar(self.__color__):
            for d in dados:
                if tablero.puede_reingresar(self.__color__, d):
                    destino = tablero.punto_entrada_desde_barra(self.__color__, d)
                    #-1 = desde la barra
                    legales.append((-1, destino, d))
            return legales

        for origen in range(24):
            p = tablero._Tablero.__puntos__[origen]
            if p["color"] != self.__color__ or p["cantidad"] == 0:
                continue
            for d in dados:
                if tablero.hay_ficha_o_no(self.__color__, origen, d):
                    destino = tablero.lugar_destino(self.__color__, origen, d)
                    legales.append((origen, destino, d))

        return legales

    def puede_mover(self, tablero, dados: List[int]) -> bool:
        return len(self.movimientos_legales(tablero, dados)) > 0
    
    def mover(self, tablero, origen: int, dado: int) -> int:
        destino = tablero.lugar_destino(self.__color__, origen, dado)
        tablero.aplicar_hay_ficha(self.__color__, origen, dado)
        return destino