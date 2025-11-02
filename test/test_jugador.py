import unittest
from src.jugador import Jugador, ficha1, ficha2
from src.tablero import Tablero

class TestJugador(unittest.TestCase):
    def setUp(self):
        self.tablero = Tablero()
        self.blanco = Jugador("Joaquin", ficha1)
        self.negro = Jugador("Profe Walter", ficha2)

# ============================================================
                # TESTS DEL CONSTRUCTOR
# ============================================================

    def test_constructor_color_invalido(self):
        with self.assertRaises(ValueError) as context:
            Jugador("Test", "ROJO")
        self.assertIn("Color inválido", str(context.exception))

    def test_constructor_color_blanco_valido(self):
        jugador = Jugador("TestBlanco", "BLANCO")
        self.assertEqual(jugador.color, "BLANCO")
        self.assertEqual(jugador.nombre, "TestBlanco") 

    def test_constructor_color_negro_valido(self):
        jugador = Jugador("TestNegro", "NEGRO")
        self.assertEqual(jugador.color, "NEGRO")
        self.assertEqual(jugador.nombre, "TestNegro")
    
    def test_constructor_nombre_con_espacios(self):
        jugador = Jugador("Profe Walter", "NEGRO")
        self.assertEqual(jugador.nombre, "Profe Walter")
    
    def test_constructor_nombre_vacio(self):
        jugador = Jugador("", "BLANCO")
        self.assertEqual(jugador.nombre, "")

# ============================================================
                # TESTS DE PROPERTIES
# ============================================================
       

    def test_property_color(self):
        self.assertEqual(self.blanco.color, ficha1)
        self.assertEqual(self.blanco.color, "BLANCO")
        self.assertEqual(self.negro.color, ficha2)
        self.assertEqual(self.negro.color, "NEGRO")

    def test_property_nombre(self):
        self.assertEqual(self.blanco.nombre, "Joaquin")
        self.assertEqual(self.negro.nombre, "Profe Walter")
    
    def test_properties_inmutables(self):
        with self.assertRaises(AttributeError):
            self.blanco.color = "NEGRO" 
        with self.assertRaises(AttributeError):
            self.blanco.nombre = "Otro nombre"


# ============================================================
                # TESTS DE DIRECCIÓN
# ============================================================
    
    def test_direccion(self):
        self.assertEqual(self.blanco.direccion(self.tablero), -1)
        self.assertEqual(self.negro.direccion(self.tablero), +1)


    def test_direccion_es_consistente(self):
        dir1 = self.blanco.direccion(self.tablero)
        dir2 = self.blanco.direccion(self.tablero)
        self.assertEqual(dir1, dir2)
        self.assertEqual(dir1, -1)

 # ============================================================
                 # TESTS DE PUEDE_MOVER
# =============================================================

    def test_puede_mover_con_movimientos_disponibles(self):
        dados = [1, 2]
        resultado = self.blanco.puede_mover(self.tablero, dados)
        self.assertTrue(resultado)

    def test_puede_mover_sin_movimientos(self):
        # Crear un tablero donde BLANCO no pueda mover
        tablero_bloqueado = Tablero()
        # Vaciar posiciones de BLANCO
        for i in range(24):
            if tablero_bloqueado.__puntos__[i]["color"] == "BLANCO":
                tablero_bloqueado.__puntos__[i] = {"color": None, "cantidad": 0}
        
        # BLANCO no debería poder mover porque no tiene fichas
        dados = [1, 2]
        resultado = self.blanco.puede_mover(tablero_bloqueado, dados)
        self.assertFalse(resultado)

# ========================================================================
        # TESTS DE MOVIMIENTOS_LEGALES - FORMATO Y ESTRUCTURA
# ========================================================================

    def test_movimientos_legales_funcione(self):
        dados = [1, 2]
        movim_jug1 = self.blanco.movimientos_legales(self.tablero, dados)
        movim_jug2 = self.negro.movimientos_legales(self.tablero, dados)
        self.assertIsInstance(movim_jug1, list)
        self.assertIsInstance(movim_jug2, list)

    def test_movimientos_legales_formato_tupla(self):
        dados = [3, 5]
        movs = self.blanco.movimientos_legales(self.tablero, dados)
        
        # Debe haber al menos un movimiento en tablero inicial
        self.assertGreater(len(movs), 0)
        
        for mov in movs:
            self.assertIsInstance(mov, tuple)
            self.assertEqual(len(mov), 3)
            origen, destino, dado_usado = mov
            self.assertIsInstance(origen, int)
            self.assertIsInstance(destino, int)
            self.assertIsInstance(dado_usado, int)
            self.assertIn(dado_usado, dados)

# ============================================================
        # TESTS DE MOVIMIENTOS_LEGALES - SIN BARRA
# ============================================================
    
    def test_movimientos_legales_sin_barra(self):
        tablero = Tablero()
        jugador_blanco = Jugador("Blanco", "BLANCO")
        dados = [1, 2]

        movs = jugador_blanco.movimientos_legales(tablero, dados)
        self.assertGreater(len(movs), 0)
        for origen, destino, dado_usado in movs:
            self.assertIsInstance(origen, int)
            self.assertIsInstance(destino, int)
            self.assertIn(dado_usado, dados)

    def test_movimientos_legales_dados_diferentes(self):
        dados = [2, 5]
        movs = self.blanco.movimientos_legales(self.tablero, dados)
        
        # Debe haber movimientos con dado 2 y con dado 5
        dados_usados = set(dado for _, _, dado in movs)
        self.assertTrue(2 in dados_usados or 5 in dados_usados)
    
    def test_movimientos_legales_dados_dobles(self):
        dados = [4, 4, 4, 4]
        movs = self.blanco.movimientos_legales(self.tablero, dados)
        
        # Debe haber movimientos disponibles
        self.assertGreater(len(movs), 0)
        
        # Todos deben usar el dado 4
        for origen, destino, dado in movs:
            self.assertEqual(dado, 4)

    def test_movimientos_legales_excluye_bloqueados(self):

        tablero = Tablero()
        
        # Bloquear punto 22 con 2+ fichas NEGRAS
        tablero.__puntos__[22] = {"color": "NEGRO", "cantidad": 2}
        
        jugador_blanco = Jugador("Blanco", "BLANCO")
        dados = [1]  # Desde punto 23, dado 1 llevaría a punto 22 (bloqueado)
        
        movs = jugador_blanco.movimientos_legales(tablero, dados)
        
        # Verificar que NO exista movimiento desde 23 hacia 22
        movimientos_desde_23 = [m for m in movs if m[0] == 23]
        
        # Si hay un movimiento desde 23, NO debe ir al punto 22
        for origen, destino, dado in movimientos_desde_23:
            self.assertNotEqual(destino, 22, 
                "No debería poder mover a un punto bloqueado")


    def test_movimientos_legales_todos_validos(self):
        dados = [3, 4]
        movs = self.blanco.movimientos_legales(self.tablero, dados)
        
        # Verificar que cada movimiento es realmente válido
        for origen, destino, dado in movs:
            # El dado usado debe estar en la lista
            self.assertIn(dado, dados)
            
            # Si no es desde la barra, debe haber una ficha del color correcto
            if origen != -1:
                punto_origen = self.tablero.__puntos__[origen]
                self.assertEqual(punto_origen["color"], "BLANCO")
                self.assertGreater(punto_origen["cantidad"], 0)

    def test_movimientos_legales_incluye_bearing_off_blanco(self):
        tablero = Tablero()

        for i in range(24):
            tablero._Tablero__puntos__[i] = {"color": None, "cantidad": 0}

        tablero._Tablero__puntos__[0] = {"color": ficha1, "cantidad": 10}
        tablero._Tablero__puntos__[1] = {"color": ficha1, "cantidad": 4}
        tablero._Tablero__puntos__[2] = {"color": ficha1, "cantidad": 1}
        tablero._Tablero__barra__[ficha1] = 0

        jugador_blanco = Jugador("Blanco", ficha1)
        dados = [3, 6]

        movimientos = jugador_blanco.movimientos_legales(tablero, dados)

        self.assertIn((2, -1, 3), movimientos)


    def test_movimientos_legales_sin_obligacion_reingresar(self):

        tablero = Tablero()
        
        # Asegurar que NO hay fichas en la barra
        tablero.__barra__["BLANCO"] = 0
        tablero.__barra__["NEGRO"] = 0
        
        jugador_blanco = Jugador("Blanco", "BLANCO")
        dados = [2, 3]
        
        movs = jugador_blanco.movimientos_legales(tablero, dados)
        
        # Debe haber movimientos regulares (no desde la barra)
        self.assertGreater(len(movs), 0)
        
        # NINGUNO debe ser desde la barra
        for origen, destino, dado in movs:
            self.assertNotEqual(origen, -1, 
                "No debería haber movimientos desde la barra si no hay fichas allí")

    def test_movimientos_legales_ignora_puntos_vacios(self):
        tablero = Tablero()
        
        # Vaciar punto 23 (que normalmente tiene fichas BLANCAS)
        tablero.__puntos__[23] = {"color": None, "cantidad": 0}
        
        jugador_blanco = Jugador("Blanco", "BLANCO")
        dados = [1, 2]
        
        movs = jugador_blanco.movimientos_legales(tablero, dados)
        
        # NO debe haber movimientos desde el punto 23
        movimientos_desde_23 = [m for m in movs if m[0] == 23]
        self.assertEqual(len(movimientos_desde_23), 0,
            "No debería haber movimientos desde un punto vacío")




    
# ============================================================
    # TESTS DE MOVIMIENTOS_LEGALES - CON BARRA
# ============================================================

    def test_movimientos_legales_con_barra(self):
        tablero = Tablero()
        tablero.__barra__["BLANCO"] = 1
        jugador = Jugador("Blanco", "BLANCO")
        dados = [1, 6]

        movs = jugador.movimientos_legales(tablero, dados)
        # Debe incluir reingreso válido
        self.assertIn((-1, 23, 1), movs)
        
        # NO debe incluir reingreso bloqueado
        # (punto 18 tiene 5 fichas NEGRAS en tablero inicial)
        self.assertNotIn((-1, 18, 6), movs)
        
        # TODOS los movimientos deben ser desde la barra
        for origen, _, _ in movs:
            self.assertEqual(origen, -1)


    def test_movimientos_legales_obligacion_reingresar(self):
        tablero = Tablero()
        tablero.__barra__["NEGRO"] = 2
        jugador_negro = Jugador("Negro", "NEGRO")
        dados = [3, 4]
        
        movs = jugador_negro.movimientos_legales(tablero, dados)
        
        # Todos deben ser desde la barra
        for origen, destino, dado in movs:
            self.assertEqual(origen, -1)

    def test_movimientos_legales_sin_reingreso_posible(self):
        tablero = Tablero()
        
        # Bloquear todos los puntos de entrada para NEGRO
        # (puntos 0-5 bloqueados con 2+ fichas BLANCAS)
        for i in range(6):
            tablero.__puntos__[i] = {"color": "BLANCO", "cantidad": 2}
        
        tablero.__barra__["NEGRO"] = 1
        jugador_negro = Jugador("Negro", "NEGRO")
        dados = [1, 2, 3, 4, 5, 6]  # Todos los dados posibles
        
        movs = jugador_negro.movimientos_legales(tablero, dados)
        
        # No debería haber movimientos posibles
        self.assertEqual(len(movs), 0)

 # ============================================================
                    # TESTS DE MOVER
# ============================================================

    def test_mover_valido(self):
        dados = [1, 2]
        movim = self.blanco.movimientos_legales(self.tablero, dados)
        
        if movim:
            origen, destino, dado = movim[0]
            d_aplicado = self.blanco.mover(self.tablero, origen, dado)
            self.assertEqual(destino, d_aplicado)
    
    
    def test_mover_actualiza_tablero(self):
        # Guardar estado inicial
        origen = 23  # Punto inicial de BLANCO con 2 fichas
        dado = 1
        
        cantidad_origen_antes = self.tablero.__puntos__[origen]["cantidad"]
        destino = self.tablero.lugar_destino("BLANCO", origen, dado)
        cantidad_destino_antes = self.tablero.__puntos__[destino]["cantidad"]
        
        # Ejecutar movimiento
        self.blanco.mover(self.tablero, origen, dado)
        
        # Verificar cambios
        cantidad_origen_despues = self.tablero.__puntos__[origen]["cantidad"]
        cantidad_destino_despues = self.tablero.__puntos__[destino]["cantidad"]
        
        self.assertEqual(cantidad_origen_despues, cantidad_origen_antes - 1)
        self.assertEqual(cantidad_destino_despues, cantidad_destino_antes + 1)

    def test_mover_retorna_destino_correcto(self):
        origen = 23
        dado = 2
        
        destino_esperado = self.tablero.lugar_destino("BLANCO", origen, dado)
        destino_retornado = self.blanco.mover(self.tablero, origen, dado)
        
        self.assertEqual(destino_retornado, destino_esperado)

# ============================================================
                # TESTS DE MOVER - CASOS ADICIONALES
# ============================================================

    def test_mover_desde_punto_con_ficha_solitaria_rival(self):

        tablero = Tablero()
        
        # Colocar una ficha NEGRA solitaria en un punto
        tablero.__puntos__[22] = {"color": "NEGRO", "cantidad": 1}
        
        # Colocar ficha BLANCA en posición para capturar
        tablero.__puntos__[23] = {"color": "BLANCO", "cantidad": 1}
        
        jugador_blanco = Jugador("Blanco", "BLANCO")
        dado = 1  # Moverá de 23 a 22
        
        # Verificar que es un movimiento válido (puede capturar)
        self.assertTrue(tablero.hay_ficha_o_no("BLANCO", 23, 1))
        
        # Aplicar el movimiento
        destino = jugador_blanco.mover(tablero, 23, dado)
        
        # Verificar que el movimiento se aplicó correctamente
        self.assertEqual(destino, 22)
        
        # Verificar que la ficha blanca llegó al destino
        self.assertEqual(tablero.__puntos__[22]["color"], "BLANCO")
        self.assertEqual(tablero.__puntos__[22]["cantidad"], 1)
        
        # Verificar que el origen quedó vacío
        self.assertEqual(tablero.__puntos__[23]["cantidad"], 0)
        
    def test_movimientos_legales_multiples_fichas_barra(self):
        tablero = Tablero()
        tablero.__barra__["NEGRO"] = 3  # Varias fichas en barra
        
        jugador_negro = Jugador("Negro", "NEGRO")
        dados = [2, 5]
        
        movs = jugador_negro.movimientos_legales(tablero, dados)
        
        # Debe haber movimientos de reingreso
        self.assertGreater(len(movs), 0)
        
        # Todos deben ser desde la barra
        for origen, destino, dado in movs:
            self.assertEqual(origen, -1)
            self.assertIn(dado, dados)

    def test_direccion_afecta_movimientos(self):
        dados = [2]
        
        # Movimientos de BLANCO (dirección -1)
        movs_blanco = self.blanco.movimientos_legales(self.tablero, dados)
        
        # Movimientos de NEGRO (dirección +1)
        movs_negro = self.negro.movimientos_legales(self.tablero, dados)
        
        # Ambos deben tener movimientos
        self.assertGreater(len(movs_blanco), 0)
        self.assertGreater(len(movs_negro), 0)
        
        # Verificar que las direcciones son opuestas
        if movs_blanco and movs_negro:
            # Para BLANCO, destino < origen (se mueve hacia 0)
            origen_b, destino_b, _ = movs_blanco[0]
            if origen_b != -1:  # Si no es desde la barra
                self.assertLess(destino_b, origen_b, 
                    "BLANCO debe moverse en dirección decreciente")
            
            # Para NEGRO, destino > origen (se mueve hacia 23)
            origen_n, destino_n, _ = movs_negro[0]
            if origen_n != -1:  # Si no es desde la barra
                self.assertGreater(destino_n, origen_n, 
                    "NEGRO debe moverse en dirección creciente")

    def test_movimientos_con_dados_repetidos_no_dobles(self):
        dados = [3, 3]  # Simulando que se pasaron dos veces el mismo valor
        
        movs = self.blanco.movimientos_legales(self.tablero, dados)
        
        # Debe poder usar ambos 3s
        self.assertGreater(len(movs), 0)
        
        # Verificar que se pueden usar múltiples veces
        dados_usados = [dado for _, _, dado in movs]
        cuenta_tres = dados_usados.count(3)
        
        # Debería haber al menos un movimiento con el dado 3
        self.assertGreaterEqual(cuenta_tres, 1)

# ============================================================
            # TESTS DE CASOS LÍMITE Y EDGE CASES
# ============================================================
    
    def test_movimientos_con_lista_dados_vacia(self):
        dados = []
        movs = self.blanco.movimientos_legales(self.tablero, dados)
        self.assertEqual(len(movs), 0)
    
    def test_movimientos_con_un_solo_dado(self):
        dados = [3]
        movs = self.blanco.movimientos_legales(self.tablero, dados)
        
        # Debe haber movimientos
        self.assertGreater(len(movs), 0)
        
        # Todos deben usar el dado 3
        for _, _, dado in movs:
            self.assertEqual(dado, 3)
    
    def test_diferentes_jugadores_mismos_dados(self):
        dados = [2, 3]
        movs_blanco = self.blanco.movimientos_legales(self.tablero, dados)
        movs_negro = self.negro.movimientos_legales(self.tablero, dados)
        
        # Ambos deben tener movimientos
        self.assertGreater(len(movs_blanco), 0)
        self.assertGreater(len(movs_negro), 0)
        
        # Los movimientos deben ser diferentes (diferentes direcciones)
        # Comparamos los conjuntos de movimientos
        set_blanco = set(movs_blanco)
        set_negro = set(movs_negro)
        
        # No deberían ser idénticos
        self.assertNotEqual(set_blanco, set_negro)
    
    def test_consistencia_puede_mover_y_movimientos_legales(self):
        dados = [4, 5]
        
        puede_mover = self.blanco.puede_mover(self.tablero, dados)
        movimientos = self.blanco.movimientos_legales(self.tablero, dados)
        
        if puede_mover:
            self.assertGreater(len(movimientos), 0)
        else:
            self.assertEqual(len(movimientos), 0)



if __name__ == "__main__":
    unittest.main()
