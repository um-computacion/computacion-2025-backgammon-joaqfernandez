ficha1 = "BLANCO"
ficha2 = "NEGRO"


class Tablero:
    def __init__(self):
        self.__puntos__ = self.tablero_inicial()
        self.__barra__ = {ficha1: 0, ficha2: 0}
        self.__fichas_fuera__ = {ficha1: 0, ficha2: 0}

    def tablero_inicial(self):
        puntos = [{"color": None, "cantidad": 0} for i in range(24)]
        #negras
        puntos[0]  = {"color": ficha2,  "cantidad": 2}   
        puntos[5]  = {"color": ficha1, "cantidad": 5}   
        puntos[7]  = {"color": ficha1, "cantidad": 3}   
        puntos[11] = {"color": ficha2,  "cantidad": 5}  
        #blancas
        puntos[12] = {"color": ficha1, "cantidad": 5}   
        puntos[16] = {"color": ficha2,  "cantidad": 3}  
        puntos[18] = {"color": ficha2,  "cantidad": 5}  
        puntos[23] = {"color": ficha1, "cantidad": 2} 
        return puntos
    
    def definir_direccion(self, color: str) -> int:
        return -1 if color == ficha1 else +1 
    
    def lugar_destino(self, color: str, origen: int, dado: int) -> int:
        return origen + self.definir_direccion(color) * dado
        