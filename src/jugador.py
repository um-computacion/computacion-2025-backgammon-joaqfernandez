from tablero import Tablero

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
        return [
            (origen, tablero.lugar_destino(self.__color__, origen, dado), dado)
            for (origen, color, cantidad) in tablero.iter_puntos()
            if color == self.__color__ and cantidad > 0
            for dado in dados
            if tablero.hay_ficha_o_no(self.__color__, origen, dado)
    ]
