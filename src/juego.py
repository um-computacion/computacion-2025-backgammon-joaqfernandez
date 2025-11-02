from dados import Dados
from tablero import Tablero
from jugador import Jugador

ficha1 = "BLANCO"
ficha2 = "NEGRO"


class BackgammonGame:
    def __setattr__(self, name, value):
        if name in ("_BackgammonGame__turno_actual__", "__turno_actual__"):
            super().__setattr__("__turno_actual__", value)
            super().__setattr__("_BackgammonGame__turno_actual__", value)
            return

        if name in ("_BackgammonGame__dados_disponibles__", "__dados_disponibles__"):
            super().__setattr__("__dados_disponibles__", value)
            super().__setattr__("_BackgammonGame__dados_disponibles__", value)
            return

        super().__setattr__(name, value)

    
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

    def verificar_victoria(self) -> bool:
        color = self.__turno_actual__.color
        fichas_fuera = self.__tablero__.fichas_fuera(color)
        
        # Si tiene 15 fichas fuera, ganó
        if fichas_fuera == 15:
            self.__ganador__ = self.__turno_actual__
            return True
        
        return False

    def obtener_movimientos_legales(self) -> list:
        if not self.tiene_dados_disponibles():
            return []
        
        return self.__turno_actual__.movimientos_legales(
            self.__tablero__, 
            self.__dados_disponibles__
        )
    
    def jugar_turno(self) -> bool:
        # Tirar dados
        dado1, dado2 = self.tirar_dados()
        print(f"\n{self.__turno_actual__.nombre} tiró: {dado1} y {dado2}")
        
        if dado1 == dado2:
            print(f"¡Dobles! Puedes usar {dado1} cuatro veces")
        
        # Verificar si puede mover
        if not self.puede_realizar_movimiento():
            print(f"{self.__turno_actual__.nombre} no puede mover. Pierde el turno.")
            self.cambiar_turno()
            return False
        
        return True

    def esta_terminado(self) -> bool:
        return self.__ganador__ is not None

    def obtener_estado_juego(self) -> dict:
        return {
            "turno": self.__turno_actual__.nombre if self.__turno_actual__ else None,
            "color_turno": self.__turno_actual__.color if self.__turno_actual__ else None,
            "dados_disponibles": self.__dados_disponibles__.copy(),
            "ganador": self.__ganador__.nombre if self.__ganador__ else None,
            "fichas_blanco_barra": self.__tablero__.fichas_en_barra(ficha1),
            "fichas_negro_barra": self.__tablero__.fichas_en_barra(ficha2),
            "fichas_blanco_fuera": self.__tablero__.fichas_fuera(ficha1),
            "fichas_negro_fuera": self.__tablero__.fichas_fuera(ficha2),
        }

    def reiniciar_juego(self):
        self.__tablero__ = Tablero()
        self.__turno_actual__ = None
        self.__ganador__ = None
        self.__dados_disponibles__ = []
        print("\n¡Juego reiniciado!")