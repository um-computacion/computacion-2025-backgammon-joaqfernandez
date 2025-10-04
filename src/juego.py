from dados import Dados
from tablero import Tablero
from jugador import Jugador

ficha1 = "BLANCO"
ficha2 = "NEGRO"


class BackgammonGame:
    def __init__(self, nombre_j1: str, nombre_j2: str):
        self.__tablero__ = Tablero()
        self.__jugador1__ = Jugador(nombre_j1, ficha1)
        self.__jugador2__ = Jugador(nombre_j2, ficha2)
        self.__dados__ = Dados()
        self.__turno_actual__ = None
        self.__ganador__ = None
        self.__dados_disponibles__ = []
