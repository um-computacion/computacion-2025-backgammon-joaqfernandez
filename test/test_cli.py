import os
import sys
import unittest
from unittest.mock import MagicMock, patch


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


from cli.cli import CLI


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.cli = CLI()
        self.cli.__juego__ = MagicMock()

    def test_limpiar_pantalla(self):
        with patch('cli.cli.os.system') as mock_system:
            self.cli.limpiar_pantalla()

        esperado = 'cls' if os.name == 'nt' else 'clear'
        mock_system.assert_called_once_with(esperado)

    def test_mostrar_bienvenida(self):
        with patch('builtins.print') as mock_print:
            self.cli.mostrar_bienvenida()

        mock_print.assert_any_call("=" * 60)
        mock_print.assert_any_call(" " * 20 + "BACKGAMMON")

    def test_solicitar_nombres_por_defecto(self):
        with patch('builtins.input', side_effect=['', '']):
            nombres = self.cli.solicitar_nombres()

        self.assertEqual(nombres, ("Jugador 1", "Jugador 2"))

    def test_solicitar_nombres_personalizados(self):
        with patch('builtins.input', side_effect=['Ana', 'Luis']):
            nombres = self.cli.solicitar_nombres()

        self.assertEqual(nombres, ("Ana", "Luis"))

    def test_mostrar_tablero(self):
        puntos = [{"cantidad": 0, "color": None} for _ in range(24)]
        puntos[12] = {"cantidad": 2, "color": "BLANCO"}
        puntos[5] = {"cantidad": 3, "color": "NEGRO"}

        tablero = MagicMock()
        tablero.obtener_puntos.return_value = puntos
        tablero.fichas_en_barra.side_effect = lambda color: 1 if color == "BLANCO" else 0
        tablero.fichas_fuera.side_effect = lambda color: 2 if color == "NEGRO" else 0

        self.cli.__juego__.tablero = tablero

        with patch('builtins.print') as mock_print:
            self.cli.mostrar_tablero()

        llamado_superior = any("TABLERO" in args[0] for args, _ in mock_print.call_args_list)
        self.assertTrue(llamado_superior)

    def test_mostrar_estado_turno(self):
        estado = {
            'turno': 'Ana',
            'color_turno': 'BLANCO',
            'dados_disponibles': [3, 5]
        }

        self.cli.__juego__.obtener_estado_juego.return_value = estado
        self.cli.__juego__.obtener_movimientos_legales.return_value = [1, 2, 3]

        with patch('builtins.print') as mock_print:
            self.cli.mostrar_estado_turno()

        mock_print.assert_any_call("Turno de: Ana (BLANCO)")
        mock_print.assert_any_call("Dados disponibles: [3, 5]")

    def test_mostrar_comandos(self):
        with patch('builtins.print') as mock_print:
            self.cli.mostrar_comandos()

        comandos = [call.args[0] for call in mock_print.call_args_list if call.args]
        self.assertTrue(any("mover" in linea for linea in comandos))

    def test_procesar_comando_mover_exitoso(self):
        self.cli.__juego__.realizar_movimiento.return_value = True

        with patch('builtins.print'):
            resultado = self.cli.procesar_comando('mover 5 3')

        self.assertTrue(resultado)
        self.cli.__juego__.realizar_movimiento.assert_called_once_with(5, 3)

    def test_procesar_comando_mover_error_valor(self):
        with patch('builtins.print') as mock_print:
            resultado = self.cli.procesar_comando('mover a b')

        self.assertFalse(resultado)
        self.assertTrue(any('✗ Error' in args[0] for args, _ in mock_print.call_args_list))

    def test_procesar_comando_barra_exitoso(self):
        self.cli.__juego__.realizar_movimiento.return_value = True

        with patch('builtins.print'):
            resultado = self.cli.procesar_comando('barra 4')

        self.assertTrue(resultado)
        self.cli.__juego__.realizar_movimiento.assert_called_once_with(-1, 4)

    def test_procesar_comando_pasar_sin_movimientos(self):
        self.cli.__juego__.puede_realizar_movimiento.return_value = False

        with patch('builtins.print'):
            resultado = self.cli.procesar_comando('pasar')

        self.assertTrue(resultado)
        self.cli.__juego__.cambiar_turno.assert_called_once()

    def test_procesar_comando_pasar_con_movimientos(self):
        self.cli.__juego__.puede_realizar_movimiento.return_value = True

        with patch('builtins.print'):
            resultado = self.cli.procesar_comando('pasar')

        self.assertFalse(resultado)

    def test_procesar_comando_ayuda(self):
        with patch.object(self.cli, 'mostrar_comandos') as mock_ayuda:
            resultado = self.cli.procesar_comando('ayuda')

        self.assertTrue(resultado)
        mock_ayuda.assert_called_once()

    def test_procesar_comando_salir(self):
        self.cli.__ejecutando__ = True

        resultado = self.cli.procesar_comando('salir')

        self.assertTrue(resultado)
        self.assertFalse(self.cli.__ejecutando__)

    def test_procesar_comando_desconocido(self):
        with patch('builtins.print') as mock_print:
            resultado = self.cli.procesar_comando('desconocido')

        self.assertFalse(resultado)
        self.assertTrue(any('Comando no reconocido' in args[0] for args, _ in mock_print.call_args_list))

    def test_procesar_comando_error_inesperado(self):
        self.cli.__juego__.realizar_movimiento.side_effect = RuntimeError('falló')

        with patch('builtins.print') as mock_print:
            resultado = self.cli.procesar_comando('barra 4')

        self.assertFalse(resultado)
        self.assertTrue(any('Error inesperado' in args[0] for args, _ in mock_print.call_args_list))

    def test_jugar_turno_no_inicia(self):
        self.cli.__juego__.jugar_turno.return_value = False

        self.cli.jugar_turno()

        self.cli.__juego__.tiene_dados_disponibles.assert_not_called()

    def test_jugar_turno_sin_movimientos_disponibles(self):
        self.cli.__juego__.jugar_turno.return_value = True
        self.cli.__juego__.tiene_dados_disponibles.side_effect = [True, True]
        self.cli.__juego__.puede_realizar_movimiento.return_value = False

        with patch.object(self.cli, 'mostrar_tablero'), patch.object(self.cli, 'mostrar_estado_turno'), \
                patch('builtins.print'):
            self.cli.jugar_turno()

        self.cli.__juego__.cambiar_turno.assert_called_once()

    def test_jugar_turno_victoria(self):
        self.cli.__juego__.jugar_turno.return_value = True
        self.cli.__juego__.tiene_dados_disponibles.side_effect = [True]
        self.cli.__juego__.puede_realizar_movimiento.return_value = True
        self.cli.__juego__.verificar_victoria.return_value = True

        with patch.object(self.cli, 'mostrar_tablero'), patch.object(self.cli, 'mostrar_estado_turno'), \
                patch.object(self.cli, 'procesar_comando'), patch.object(self.cli, 'mostrar_victoria') as mock_victoria, \
                patch('builtins.input', return_value='mover 1 1'):
            self.cli.jugar_turno()

        mock_victoria.assert_called_once()
        self.cli.__juego__.cambiar_turno.assert_not_called()

    def test_jugar_turno_salida_usuario(self):
        self.cli.__juego__.jugar_turno.return_value = True
        self.cli.__juego__.tiene_dados_disponibles.side_effect = [True, False]
        self.cli.__juego__.puede_realizar_movimiento.return_value = True
        self.cli.__juego__.verificar_victoria.return_value = False

        with patch.object(self.cli, 'mostrar_tablero'), patch.object(self.cli, 'mostrar_estado_turno'), \
                patch.object(self.cli, 'procesar_comando') as mock_procesar, \
                patch('builtins.input', return_value='salir'), patch('builtins.print'):
            self.cli.jugar_turno()

        self.assertFalse(self.cli.__ejecutando__)
        mock_procesar.assert_not_called()
        self.cli.__juego__.cambiar_turno.assert_called_once()

    def test_mostrar_victoria(self):
        ganador = MagicMock()
        ganador.nombre = 'Ana'
        ganador.color = 'BLANCO'
        self.cli.__juego__.ganador = ganador

        with patch.object(self.cli, 'mostrar_tablero'), patch('builtins.print') as mock_print:
            self.cli.mostrar_victoria()

        self.assertTrue(any('¡VICTORIA' in args[0] for args, _ in mock_print.call_args_list))

    def test_jugar_de_nuevo(self):
        with patch('builtins.input', return_value='s'):
            self.assertTrue(self.cli.jugar_de_nuevo())

        with patch('builtins.input', return_value='n'):
            self.assertFalse(self.cli.jugar_de_nuevo())

    def test_iniciar_flujo_completo(self):
        self.cli.__ejecutando__ = False

        juego_simulado = MagicMock()
        juego_simulado.esta_terminado.side_effect = [False, True, True]

        with patch('cli.cli.BackgammonGame', return_value=juego_simulado) as mock_game, \
                patch.object(self.cli, 'limpiar_pantalla') as mock_limpiar, \
                patch.object(self.cli, 'mostrar_bienvenida') as mock_bienvenida, \
                patch.object(self.cli, 'solicitar_nombres', return_value=('Ana', 'Luis')), \
                patch.object(self.cli, 'mostrar_comandos') as mock_comandos, \
                patch.object(self.cli, 'jugar_turno') as mock_jugar_turno, \
                patch.object(self.cli, 'jugar_de_nuevo', return_value=False) as mock_repetir, \
                patch('builtins.print') as mock_print:
            self.cli.iniciar()

        mock_limpiar.assert_called()
        mock_bienvenida.assert_called()
        mock_comandos.assert_called()
        mock_jugar_turno.assert_called()
        mock_repetir.assert_called_once()
        mock_game.assert_called_once_with('Ana', 'Luis')
        juego_simulado.iniciar_juego.assert_called_once()
        self.assertTrue(any('Gracias por jugar' in args[0] for args, _ in mock_print.call_args_list))


if __name__ == '__main__':
    unittest.main()