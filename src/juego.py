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

    @property
    def tablero(self) -> Tablero:
        return self.__tablero__
    
    @property
    def jugador1(self) -> Jugador:
        return self.__jugador1__
    
    @property
    def jugador2(self) -> Jugador:
        return self.__jugador2__
    
    @property
    def turno_actual(self) -> Jugador:
        return self.__turno_actual__
    
    @property
    def ganador(self):
        return self.__ganador__
    
    @property
    def dados_disponibles(self) -> list:
        return self.__dados_disponibles__

    def determinar_primer_turno(self) -> Jugador:
        print(f"\n{self.__jugador1__.nombre} vs {self.__jugador2__.nombre}")
        print("Tirando dados para determinar quién empieza...")
        
        while True:
            dado1_j1, dado2_j1 = self.__dados__.tirar_dado()
            suma_j1 = dado1_j1 + dado2_j1
            print(f"{self.__jugador1__.nombre} sacó: {dado1_j1} + {dado2_j1} = {suma_j1}")
            
            dado1_j2, dado2_j2 = self.__dados__.tirar_dado()
            suma_j2 = dado1_j2 + dado2_j2
            print(f"{self.__jugador2__.nombre} sacó: {dado1_j2} + {dado2_j2} = {suma_j2}")
            
            if suma_j1 > suma_j2:
                print(f"\n¡{self.__jugador1__.nombre} comienza!\n")
                return self.__jugador1__
            elif suma_j2 > suma_j1:
                print(f"\n¡{self.__jugador2__.nombre} comienza!\n")
                return self.__jugador2__
            else:
                print("¡Empate! Tirando de nuevo...\n")

    
    