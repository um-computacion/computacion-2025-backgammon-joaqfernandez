ficha1 = "BLANCO"
ficha2 = "NEGRO"


class Tablero:
    def __init__(self):
        self.__puntos__ = self.tablero_inicial()
        self.__barra__ = {ficha1: 0, ficha2: 0}
        self.__fichas_fuera__ = {ficha1: 0, ficha2: 0}
        self._Tablero__puntos__ = self.__puntos__
        self._Tablero__barra__ = self.__barra__
        self._Tablero__fichas_fuera__ = self.__fichas_fuera__

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

        if punto["color"] == color:
            return True

        return punto["cantidad"] == 1
    
    def hay_ficha_o_no(self, color: str, origen: int, dado: int) -> bool:
        if not (0 <= origen < 24):
            return False

        punto_de_origen = self.__puntos__[origen]
        if punto_de_origen["color"] != color or punto_de_origen["cantidad"] == 0:
            return False
        
        if self.es_movimiento_bearing_off(color, origen, dado):
            return True

        destino = self.lugar_destino(color, origen, dado)

        if self.movimiento_regular(color, destino):
            return True

        if not (0 <= destino < 24):
            return False

        punto_destino = self.__puntos__[destino]
        return punto_destino["cantidad"] == 1 and punto_destino["color"] != color
    
    def aplicar_hay_ficha(self, color: str, origen: int, dado: int):
        if not (0 <= origen < 24):
            raise ValueError("Movimiento invalido")

        punto_origen = self.__puntos__[origen]
        if punto_origen["color"] != color or punto_origen["cantidad"] == 0:
            raise ValueError("Movimiento invalido")

        if self.es_movimiento_bearing_off(color, origen, dado):
            punto_origen["cantidad"] -= 1
            if punto_origen["cantidad"] == 0:
                punto_origen["color"] = None
            self.__fichas_fuera__[color] += 1
            return self.destino_fuera(color)

        destino = self.lugar_destino(color, origen, dado)

        if not self.movimiento_regular(color, destino):
            raise ValueError("Movimiento invalido")

        punto_destino = self.__puntos__[destino]

        if punto_destino["cantidad"] == 1 and punto_destino["color"] != color:
            rival = ficha1 if color == ficha2 else ficha2
            self.__barra__[rival] += 1
            punto_destino["color"] = color
            punto_destino["cantidad"] = 1
        else:
            if punto_destino["cantidad"] == 0:
                punto_destino["color"] = color
                punto_destino["cantidad"] = 1
            else:
                punto_destino["cantidad"] += 1

        punto_origen["cantidad"] -= 1
        if punto_origen["cantidad"] == 0:
            punto_origen["color"] = None

        return destino

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

    def _set_fichas_fuera_para_test(self, color: str, cantidad: int):
    #Método auxiliar solo para tests. Modifica fichas fuera.
        self.__fichas_fuera__[color] = cantidad

    def rango_casa(self, color: str):
        return range(0, 6) if color == ficha1 else range(18, 24)

    def todas_fichas_en_casa(self, color: str) -> bool:
        if self.__barra__[color] > 0:
            return False

        rango = self.rango_casa(color)

        for indice, punto in enumerate(self.__puntos__):
            if punto["color"] != color or punto["cantidad"] == 0:
                continue

            if indice not in rango:
                return False

        return True

    def hay_fichas_mas_atras_en_casa(self, color: str, origen: int) -> bool:
        if color == ficha1:
            rango = range(origen + 1, 6)
        else:
            rango = range(18, origen)

        for indice in rango:
            punto = self.__puntos__[indice]
            if punto["color"] == color and punto["cantidad"] > 0:
                return True

        return False

    def distancia_para_salir(self, color: str, origen: int) -> int:
        if color == ficha1:
            return origen + 1
        return 24 - origen

    def destino_fuera(self, color: str) -> int:
        return -1 if color == ficha1 else 24

    def es_movimiento_bearing_off(self, color: str, origen: int, dado: int) -> bool:
        destino = self.lugar_destino(color, origen, dado)

        if color == ficha1 and destino >= 0:
            return False

        if color == ficha2 and destino <= 23:
            return False

        if not self.todas_fichas_en_casa(color):
            return False

        distancia = self.distancia_para_salir(color, origen)

        if dado == distancia:
            return True

        if dado > distancia:
            return not self.hay_fichas_mas_atras_en_casa(color, origen)

        return False