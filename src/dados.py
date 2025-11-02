import random

class Dados:
    def __init__(self):
        self.__dado1__ = random.randint(1, 6)
        self.__dado2__ = random.randint(1,6)

    @property
    def dado1(self):
        return self.__dado1__
    
    @property
    def dado2(self):
        return self.__dado2__
    
    def tirar_dado(self):
        self.__dado1__ = random.randint(1,6)
        self.__dado2__ = random.randint(1,6)
        return(self.__dado1__, self.__dado2__)