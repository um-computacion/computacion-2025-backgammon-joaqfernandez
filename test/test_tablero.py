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
        p = tablero.obtener_puntos() 
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


    def test_blanco_puede_mover_desde_12_con_dado4(self):
        tablero = Tablero()
        # Punto 12 tiene 5 fichas blancas, con dado 4 va a punto 8 (vacío)
        self.assertTrue(tablero.hay_ficha_o_no(ficha1, 12, 4))
    
    def test_negro_puede_mover_desde_0_con_dado3(self):
        tablero = Tablero()
        # Punto 0 tiene 2 fichas negras, con dado 3 va a punto 3 (vacío)
        self.assertTrue(tablero.hay_ficha_o_no(ficha2, 0, 3))
    
    def test_no_puede_mover_desde_punto_vacio(self):
        tablero = Tablero()
        # Punto 1 está vacío
        self.assertFalse(tablero.hay_ficha_o_no(ficha1, 1, 3))
    
    def test_no_puede_mover_ficha_enemiga(self):
        tablero = Tablero()
        # Punto 5 tiene fichas blancas, negro no puede moverlas
        self.assertFalse(tablero.hay_ficha_o_no(ficha2, 5, 3))
    
    def test_aplicar_movimiento_reduce_cantidad_origen(self):
        tablero = Tablero()
        cantidad_inicial = tablero._Tablero__puntos__[12]["cantidad"]
        
        tablero.aplicar_hay_ficha(ficha1, 12, 4)
        
        cantidad_final = tablero._Tablero__puntos__[12]["cantidad"]
        self.assertEqual(cantidad_final, cantidad_inicial - 1)
    
    def test_aplicar_movimiento_aumenta_cantidad_destino(self):
        tablero = Tablero()
        cantidad_inicial = tablero._Tablero__puntos__[8]["cantidad"]
        
        tablero.aplicar_hay_ficha(ficha1, 12, 4)  # 12 → 8
        
        cantidad_final = tablero._Tablero__puntos__[8]["cantidad"]
        self.assertEqual(cantidad_final, cantidad_inicial + 1)
    
    def test_aplicar_movimiento_cambia_color_destino(self):
        tablero = Tablero()
        
        tablero.aplicar_hay_ficha(ficha1, 12, 4)  # 12 → 8
        
        self.assertEqual(tablero._Tablero__puntos__[8]["color"], ficha1)

    def test_punto_origen_queda_sin_color_si_se_vacia(self):
        tablero = Tablero()
        
        # Punto 0 tiene solo 2 fichas negras
        tablero.aplicar_hay_ficha(ficha2, 0, 3)  # Primera
        tablero.aplicar_hay_ficha(ficha2, 0, 3)  # Segunda
        
        self.assertIsNone(tablero._Tablero__puntos__[0]["color"])
        self.assertEqual(tablero._Tablero__puntos__[0]["cantidad"], 0)
    
    def test_movimiento_invalido_lanza_error(self):
        tablero = Tablero()
        
        with self.assertRaises(ValueError):
            tablero.aplicar_hay_ficha(ficha1, 1, 3)  # Punto 1 está vacío
    
    def test_total_fichas_blanco_inicial_15(self):
        tablero = Tablero()
        p = tablero.obtener_puntos()
        
        total = sum(punto["cantidad"] for punto in p if punto["color"] == ficha1)
        self.assertEqual(total, 15)
    
    def test_total_fichas_negro_inicial_15(self):
        tablero = Tablero()
        p = tablero.obtener_puntos()
        
        total = sum(punto["cantidad"] for punto in p if punto["color"] == ficha2)
        self.assertEqual(total, 15)
    
    def test_barra_inicial_vacia_blanco(self):
        tablero = Tablero()
        self.assertEqual(tablero.fichas_en_barra(ficha1), 0)
    
    def test_barra_inicial_vacia_negro(self):
        tablero = Tablero()
        self.assertEqual(tablero.fichas_en_barra(ficha2), 0)

    def test_fichas_fuera_inicial_cero_blanco(self):
        tablero = Tablero()
        self.assertEqual(tablero.fichas_fuera(ficha1), 0)
    
    def test_fichas_fuera_inicial_cero_negro(self):
        tablero = Tablero()
        self.assertEqual(tablero.fichas_fuera(ficha2), 0)
    
    def test_no_hay_obligacion_reingresar_inicial_blanco(self):
        tablero = Tablero()
        self.assertFalse(tablero.hay_obligacion_reingresar(ficha1))
    
    def test_no_hay_obligacion_reingresar_inicial_negro(self):
        tablero = Tablero()
        self.assertFalse(tablero.hay_obligacion_reingresar(ficha2))
    
    def test_punto_entrada_blanco_dado1(self):
        tablero = Tablero()
        # Blanco entra en 24-1 = 23
        self.assertEqual(tablero.punto_entrada_desde_barra(ficha1, 1), 23)
    
    def test_punto_entrada_negro_dado1(self):
        tablero = Tablero()
        # Negro entra en 1-1 = 0
        self.assertEqual(tablero.punto_entrada_desde_barra(ficha2, 1), 0)
    
    def test_punto_entrada_dado_invalido_lanza_error(self):
        tablero = Tablero()
        
        with self.assertRaises(ValueError):
            tablero.punto_entrada_desde_barra(ficha1, 0)
        
        with self.assertRaises(ValueError):
            tablero.punto_entrada_desde_barra(ficha1, 7)
    
    def test_puede_reingresar_a_punto_vacio(self):
        tablero = Tablero()
        # Punto 22 está vacío, blanco puede entrar con dado 2 (24-2=22)
        self.assertTrue(tablero.puede_reingresar(ficha1, 2))


    def test_secuencia_movimientos_conserva_fichas(self):
        tablero = Tablero()
        p = tablero.obtener_puntos()
        
        inicial = sum(punto["cantidad"] for punto in p if punto["color"] == ficha1)
        
        # Hacer varios movimientos
        tablero.aplicar_hay_ficha(ficha1, 12, 3)
        tablero.aplicar_hay_ficha(ficha1, 12, 4)
        
        p = tablero.obtener_puntos()
        final = sum(punto["cantidad"] for punto in p if punto["color"] == ficha1)
        
        self.assertEqual(inicial, final)
    
    def test_iter_puntos_retorna_24_elementos(self):
        tablero = Tablero()
        puntos_iterados = list(tablero.iter_puntos())
        self.assertEqual(len(puntos_iterados), 24)
    
    def test_iter_puntos_formato_correcto(self):
        tablero = Tablero()
        
        for i, color, cantidad in tablero.iter_puntos():
            self.assertIsInstance(i, int)
            self.assertTrue(0 <= i < 24)
            self.assertTrue(color is None or color in [ficha1, ficha2])
            self.assertIsInstance(cantidad, int)


if __name__ == "__main__":
    unittest.main()
