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


    def test_tablero_inicial_tiene_fichas_correctas(self):
        tablero = Tablero()
        puntos = tablero.obtener_puntos()
        #Todas las fichas
        self.assertEqual(len(p), 24)

        #-------Fichas en sus posiciones----- 
        
        self.assertEqual(p[0]["color"], "NEGRO")
        self.assertEqual(p[0]["cantidad"], 2)
        
        self.assertEqual(p[5]["color"], "BLANCO")
        self.assertEqual(p[5]["cantidad"], 5)
        
        self.assertEqual(p[7]["color"], "BLANCO")
        self.assertEqual(p[7]["cantidad"], 3)
        
        self.assertEqual(p[11]["color"], "NEGRO")
        self.assertEqual(p[11]["cantidad"], 5)
        
        self.assertEqual(p[12]["color"], "BLANCO")
        self.assertEqual(p[12]["cantidad"], 5)
        
        self.assertEqual(p[16]["color"], "NEGRO")
        self.assertEqual(p[16]["cantidad"], 3)
        

        self.assertEqual(p[18]["color"], "NEGRO")
        self.assertEqual(p[18]["cantidad"], 5)
        
        self.assertEqual(p[23]["color"], "BLANCO")
        self.assertEqual(p[23]["cantidad"], 2)
        #---Posiciones que no llevan ficha----
        for i in range(24):
            if i not in [0, 5, 7, 11, 12, 16, 18, 23]:
                self.assertIsNone(p[i]["color"])
                self.assertEqual(p[i]["cantidad"], 0)

    def test_no_puede_reingresar_negro_dado6(self):
        tablero = Tablero()
        self.assertFalse(tablero.puede_reingresar("NEGRO", 6))

    def test_direccion_blanco_negativa(self):
        tablero = Tablero()
        self.assertEqual(tablero.definir_direccion(ficha1), -1)
    
    def test_direccion_negro_positiva(self):
        tablero = Tablero()
        self.assertEqual(tablero.definir_direccion(ficha2), +1)
    
    def test_lugar_destino_blanco_dado3(self):
        tablero = Tablero()
        # Blanco en 23, dado 3 → 20
        self.assertEqual(tablero.lugar_destino(ficha1, 23, 3), 20)
    
    def test_lugar_destino_negro_dado4(self):
        tablero = Tablero()
        # Negro en 0, dado 4 → 4
        self.assertEqual(tablero.lugar_destino(ficha2, 0, 4), 4)
    
    def test_movimiento_a_punto_vacio_es_valido(self):
        tablero = Tablero()
        # Punto 1 está vacío
        self.assertTrue(tablero.movimiento_regular(ficha1, 1))
    
    def test_movimiento_a_punto_propio_es_valido(self):
        tablero = Tablero()
        # Punto 5 tiene fichas blancas
        self.assertTrue(tablero.movimiento_regular(ficha1, 5))
    
    def test_movimiento_fuera_de_rango_no_valido(self):
        tablero = Tablero()
        self.assertFalse(tablero.movimiento_regular(ficha1, -1))
        self.assertFalse(tablero.movimiento_regular(ficha1, 24)) 














if __name__ == "__main__":
    unittest.main()
