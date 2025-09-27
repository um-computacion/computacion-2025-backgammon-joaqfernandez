from src.tablero import Tablero, ficha1, ficha2
import unittest

class testTablero(unittest.TestCase):
    def test_blanco_mueve_a_casilla_vacia(self):
        tablero = Tablero()
       
        tablero.__puntos__[22] = {"color": None, "cantidad": 0}
        self.assertTrue(tablero.hay_ficha_o_no(ficha1, 23, 1))
        tablero.aplicar_hay_ficha(ficha1, 23, 1)
        self.assertEqual(tablero.__puntos__[23]["cantidad"], 1)  # antes había 2
        self.assertEqual(tablero.__puntos__[22]["cantidad"], 1)
        self.assertEqual(tablero.__puntos__[22]["color"], ficha1)


    def test_negro_no_puede_mover_a_casilla_bloqueada_por_blanco(self):
        tablero = Tablero()
        tablero.__puntos__[6] = {"color": ficha1, "cantidad": 3}
        self.assertFalse(tablero.hay_ficha_o_no(ficha2, 0, 6))



if __name__ == "__main__":
    unittest.main()
