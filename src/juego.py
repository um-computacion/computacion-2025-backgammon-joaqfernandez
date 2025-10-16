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

    
    def iniciar_juego(self):
        self.__turno_actual__ = self.determinar_primer_turno()

    def tirar_dados(self) -> tuple:
        dado1, dado2 = self.__dados__.tirar_dado()
        
        if dado1 == dado2:
            # Dobles: se pueden usar 4 veces
            self.__dados_disponibles__ = [dado1, dado1, dado1, dado1]
        else:
            self.__dados_disponibles__ = [dado1, dado2]
        
        return dado1, dado2

    def usar_dado(self, valor: int):

        if valor not in self.__dados_disponibles__:
            raise ValueError(f"El dado {valor} no está disponible")
        self.__dados_disponibles__.remove(valor)

    def tiene_dados_disponibles(self) -> bool:
        return len(self.__dados_disponibles__) > 0

    def puede_realizar_movimiento(self) -> bool:
        if not self.tiene_dados_disponibles():
            return False
        
        return self.__turno_actual__.puede_mover(
            self.__tablero__, 
            self.__dados_disponibles__
        )
    
    def realizar_movimiento(self, origen: int, dado: int) -> bool:
        if dado not in self.__dados_disponibles__:
            raise ValueError(f"El dado {dado} no está disponible")
        
        color = self.__turno_actual__.color
        
        # Movimiento desde la barra
        if origen == -1:
            if not self.__tablero__.hay_obligacion_reingresar(color):
                raise ValueError("No hay fichas en la barra para reingresar")
            if not self.__tablero__.puede_reingresar(color, dado):
                raise ValueError("No se puede reingresar con ese dado")
            
            self.__tablero__.aplicar_reingreso(color, dado)
            self.usar_dado(dado)
            return True
        
        # Movimiento regular
        if not self.__tablero__.hay_ficha_o_no(color, origen, dado):
            raise ValueError("Movimiento inválido")
        
        self.__tablero__.aplicar_hay_ficha(color, origen, dado)
        self.usar_dado(dado)
        return True
    
    def cambiar_turno(self):
        if self.__turno_actual__ == self.__jugador1__:
            self.__turno_actual__ = self.__jugador2__
        else:
            self.__turno_actual__ = self.__jugador1__
        
        self.__dados_disponibles__ = []