ficha1 = "BLANCO"
ficha2 = "NEGRO"


class Tablero:
    def __init__(self):
        self.__puntos__ = self.tablero_inicial()
        self.__barra__ = {ficha1: 0, ficha2: 0}
        self.__fichas_fuera__ = {ficha1: 0, ficha2: 0}

    def tablero_inicial():
        puntos = [{"color": None, "Cantidad": 0} for i in range(24)]
        puntos[0]  = {"color": NEGRO,  "cantidad": 2}   
        puntos[5]  = {"color": BLANCO, "cantidad": 5}   
        puntos[7]  = {"color": BLANCO, "cantidad": 3}   
        puntos[11] = {"color": NEGRO,  "cantidad": 5}  
        puntos[12] = {"color": BLANCO, "cantidad": 5}   
        puntos[16] = {"color": NEGRO,  "cantidad": 3}  
        puntos[18] = {"color": NEGRO,  "cantidad": 5}  
        puntos[23] = {"color": BLANCO, "cantidad": 2} 
        return puntos
    
