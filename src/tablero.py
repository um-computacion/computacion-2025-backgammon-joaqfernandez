ficha1 = "BLANCO"
ficha2 = "NEGRO"


class Tablero:
    def __init__(self):
        self.__puntos__ = self.tablero_inicial()
        self.__barra__ = {BLANCO: 0, NEGRO: 0}
        self.__fichas_fuera__ = {BLANCO: 0, NEGRO: 0}

    def tablero_inicial():
        