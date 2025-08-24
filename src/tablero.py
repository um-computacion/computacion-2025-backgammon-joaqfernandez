ficha1 = "BLANCO"
ficha2 = "NEGRO"


class Tablero:
    def __init__(self):
        self.__puntos__ = self.tablero_inicial()
        self.__barra__ = {BLANCO: 0, NEGRO: 0}
        self.__fichas_fuera__ = {BLANCO: 0, NEGRO: 0}

    def tablero_inicial():
        puntos = [{"color": None, "Cantidad": 0} for i in range(24)]
        puntos[0]  = {"color": NEGRO,  "cantidad": 2}   # espejo de 23
        puntos[5]  = {"color": BLANCO, "cantidad": 5}   # espejo de 18
        puntos[7]  = {"color": BLANCO, "cantidad": 3}   # espejo de 16
        puntos[11] = {"color": NEGRO,  "cantidad": 5}   # espejo de 12

        puntos[12] = {"color": BLANCO, "cantidad": 5}   # espejo de 11
        puntos[16] = {"color": NEGRO,  "cantidad": 3}   # espejo de 7
        puntos[18] = {"color": NEGRO,  "cantidad": 5}   # espejo de 5
        puntos[23] = {"color": BLANCO, "cantidad": 2} 
        return puntos