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