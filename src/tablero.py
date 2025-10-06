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
        
    def movimiento_regular(self, color: str, numero_destino: int) -> bool:
        if not (0 <= numero_destino < 24):
            return False
        punto = self.__puntos__[numero_destino]
        if punto["cantidad"] == 0:
            return True
        return punto["color"] == color
    
    def hay_ficha_o_no(self, color: str, origen: int, dado: int)->bool:
        if not (0 <= origen < 24):
            False
        punto_de_origen = self.__puntos__[origen]
        if punto_de_origen["color"] != color or punto_de_origen["cantidad"] == 0:
            return False
        destino = self.lugar_destino(color, origen, dado)
        return self.movimiento_regular(color, destino)
    
    def aplicar_hay_ficha(self, color: str, origen: int, dado: int):
        if not self.hay_ficha_o_no(color, origen, dado):
            raise ValueError("Movimiento invalido")
        destino = self.lugar_destino(color, origen, dado)

        self.__puntos__[origen]["cantidad"] -= 1
        if self.__puntos__[origen]["cantidad"] == 0:
            self.__puntos__[origen]["color"] = None

        if self.__puntos__[destino]["cantidad"] == 0:
            self.__puntos__[destino]["color"] = color
            self.__puntos__[destino]["cantidad"] = 1
        else:
            self.__puntos__[destino]["cantidad"] += 1

    def iter_puntos(self):
        for i, p in enumerate(self.__puntos__):
            yield i, p["color"], p["cantidad"]
        
    def obtener_puntos(self):
        return self.__puntos__

    def fichas_en_barra(self, color: str) -> int:
        return self.__barra__[color]

    def fichas_fuera(self, color: str) -> int:
        return self.__fichas_fuera__[color]
    
    def hay_obligacion_reingresar(self, color: str) -> bool:
        return self.__barra__[color] > 0
    
    def punto_entrada_desde_barra(self, color: str, dado: int) -> int:
        if not (1 <= dado <= 6):
            raise ValueError("Dado inválido para reingreso")
        if color == ficha1:  
            return 24 - dado
        else:                 
            return dado - 1
        
    def puede_reingresar(self, color: str, dado: int) -> bool:
        destino = self.punto_entrada_desde_barra(color, dado)
        punto = self.__puntos__[destino]
        if punto["cantidad"] == 0:
                return True
        if punto["color"] == color:
                return True
        return punto["cantidad"] == 1 and punto["color"] != color

    def aplicar_reingreso(self, color: str, dado: int) -> int:
        if self.__barra__[color] <= 0:
            raise ValueError("No hay fichas en barra para reingresar")
        if not self.puede_reingresar(color, dado):
            raise ValueError("No se puede reingresar con este dado")

        destino = self.punto_entrada_desde_barra(color, dado)
        punto = self.__puntos__[destino]


        if punto["cantidad"] == 1 and punto["color"] != color:
            rival = ficha1 if color == ficha2 else ficha2
            self.__barra__[rival] += 1
            punto["color"] = color
            punto["cantidad"] = 1
        else:
            if punto["cantidad"] == 0:
                punto["color"] = color
                punto["cantidad"] = 1
            else:
                punto["cantidad"] += 1

        self.__barra__[color] -= 1
        return destino