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
            if tablero_bloqueado._Tablero__puntos__[i]["color"] == "BLANCO":
                tablero_bloqueado._Tablero__puntos__[i] = {"color": None, "cantidad": 0}
        
        # BLANCO no debería poder mover porque no tiene fichas
        dados = [1, 2]
        resultado = self.blanco.puede_mover(tablero_bloqueado, dados)
        self.assertFalse(resultado)


    def test_movimientos_legales_funcione(self):
        dados = [1, 2]
        movim_jug1 = self.blanco.movimientos_legales(self.tablero, dados)
        movim_jug2 = self.negro.movimientos_legales(self.tablero, dados)
        self.assertIsInstance(movim_jug1, list)
        self.assertIsInstance(movim_jug2, list)
    
    def test_mover_valido(self):
        dados = [1, 2]
        movim = self.blanco.movimientos_legales(self.tablero, dados)
        if movim:
            origen, destino, dado = movim[0]
            d_aplicado = self.blanco.mover(self.tablero, origen, dado)
            self.assertEqual(destino, d_aplicado)

    def test_movimientos_legales_con_barra(self):
        tablero = Tablero()
        tablero._Tablero__barra__["BLANCO"] = 1
        jugador = Jugador("Blanco", "BLANCO")
        dados = [1, 6]

        movs = jugador.movimientos_legales(tablero, dados)
        self.assertIn((-1, 23, 1), movs)
        self.assertNotIn((-1, 18, 6), movs)

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


    
if __name__ == "__main__":
    unittest.main()
