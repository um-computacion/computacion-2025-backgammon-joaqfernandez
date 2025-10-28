# Changelog
Todas las modificaciones importantes de este proyecto serán documentadas en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]

## [0.1.0] - 2025-09-09 19:25 (GMT-3)
### Added
- En src/jugador.py se implementó función para obtener los **movimientos permitidos** (sin incluir *bear-off*).
- 

## [0.2.0] - 2025-09-11 15:31
### Added
- Se agregó test unitario para verificar la dirección de **Jugador 1** y **Jugador 2**.

## [0.3.0] - 2025-09-12 14:39
### Added
- Hago un test para verificar que los movimientos sean validos y con sentidos. 

## [0.4.0] - 2025-09-15 13:28
### Added
- Hago un test para comprobar movimientos legales(cumplan las reglas).
  - Busca una ficha blanca y la mueve
  
## [0.5.0] - 2025-09-16 15:36
### Added
- Agrego una funcion(hecha por ia) para imprimir los movimientos legales, devolviendome una lista con una tupla adentro donde hay 3 enteros [int, int, int].
  [int, int, int] = 5, 3, 2 se mueve desde el punto 5 al 3, con el dado 2.

## [0.6.0] - 2025-09-16 15:41
### Added
- Funcion en ´src/jugador.py´ que returna True si existe un al menos un posible movimiento tras el resultado del tiraje de dados. 

## [0.7.0] - 2025-09-19 20:29
### Added
- Funcion en ´src/jugador.py´ para aplicar los movimentos que da el jugador

## [0.8.0] - 2025-09-20 19:38
### Added
- Funcion en src/tablero.pu que responde si ese jugador tiene fichas en la barra. En backgammon, si tenés fichas en la barra, estás obligado a reingresar antes de mover cualquier otra ficha 

## [0.9.0] - 2025-09-22 14:49
### Added
- Hago una funcion en jugador que devuelve el índice de punto de entrada al tablero desde la barra para un dado dado.

## [0.10.0] - 2025-09-22 14:53
### Added
- Hago una funcion en jugador que devuelve el índice de punto de entrada al tablero desde la barra para un dado dado.

## [0.11.0] - 2025-09-22 20:37
### Added
- Funcion para aplicar el reingreso y reingresar una ficha desde la barra al tablero usando 'dado'.
    Captura si hay 1 rival en el destino.
    Devuelve el índice 'destino' aplicado.

## [0.12.0] - 2025-09-25 16:56
### Added
- - Método `movimientos_legales` en `Jugador`:
  - Devuelve lista de jugadas válidas `(origen, destino, dado)`.
  - Soporta reingresos desde la barra (convención `origen = -1`).
  - Integra validaciones con `Tablero` (`hay_obligacion_reingresar`, `puede_reingresar`)

## [0.13.0] - 2025-09-26 21:54
### Added
- Test para verificar que el método movimientos_legales de la clase Jugador funciona correctamente cuando el jugador tiene fichas en la barra (es decir, fichas que fueron "comidas" y deben reingresar al tablero)

## [0.14.0] - 2025-09-27 17:32
### Added
- El jugador ahora puede obtener una lista de todos sus movimientos legales dados unos dados, ya sea desde el tablero o desde la barra

## [0.15.0] - 2025-09-29 09:35
### Added
- Tests para la clase `Tablero`, verificando el estado inicial del tablero según las reglas estándar.


## [0.16.0] - 2025-09-30 20:23
### Added
- Test para que ficha negra pueda o no entrar en 5, que tiene 5 BLANCAS → bloqueado

## [0.17.0] - 2025-10-2 12:17
### Added
- hago 3 test en jugador. 
  - creador de color correcto (que sea blanco o negro, no ROJO)
  - Mover con movimientos disponibles
  - Checkear que los colores sean los correctos (negro o blanco)

## [0.18.0] - 2025-10-2 12:23
### Added
- idento una funcion en clase jugador


## [0.19.0] - 2025-10-4 18:40
### Added
- Creo el constructor para el archivo juego.py 

## [0.20.0] - 2025-10-7 21:10
### Added
- Se agregaron propiedades (`@property`) en la clase `Juego` para acceder de forma segura a los atributos privados:
  - `tablero`
  - `jugador1`
  - `jugador2`
  - `turno_actual`
  - `ganador`
  - `dados_disponibles`

## [0.21.0] - 2025-10-9 10:25
### Added
- Creo una funcion que determina quién juega primero mediante tiradas de dados. Cada jugador tira hasta que uno obtenga un valor mayor. Retorna el jugador que comienza

## [0.22.0] - 2025-10-11 16:36
### Added
- Se agregó la función `iniciar_juego()` dentro de `src/juego.py` para determinar automáticamente el jugador que inicia la partida según las reglas de Backgammon.
- Se implementó la función `tirar_dados()` con soporte completo para tiradas dobles, generando correctamente los valores de los dados y configurando la lista `__dados_disponibles__`

## [0.23.0] - 2025-10-16 20:43
### Added
- `usar_dado(valor: int)` en `src/juego.py`: consume un valor de dado disponible y valida su existencia.
- `tiene_dados_disponibles() -> bool` en `src/juego.py`: expone si aún quedan dados por jugar en el turno actual.
- `puede_realizar_movimiento() -> bool` en `src/juego.py`: consulta a `__turno_actual__` y `__tablero__` para determinar si hay movimientos válidos con los dados restantes.
- `realizar_movimiento(origen: int, dado: int) -> bool` en `src/juego.py`:
  - Soporte para **reingreso desde la barra** (`origen == -1`) con validaciones: obligación de reingreso y posibilidad con el dado específico.
  - Soporte para **movimiento regular** con verificación previa y aplicación de captura/avance.
  - Consumo automático del dado utilizado.
- `cambiar_turno()` en `src/juego.py`: alterna entre `__jugador1__` y `__jugador2__` y resetea `__dados_disponibles__`.

## [0.24.0] - 2025-10-23 15:41
### Added
- `verificar_victoria() -> bool` en `src/juego.py`: determina si el jugador actual ganó (15 fichas fuera) y setea `__ganador__`.
- `obtener_movimientos_legales() -> list` en `src/juego.py`: expone desde `Jugador` los movimientos válidos dados el estado de `Tablero` y `__dados_disponibles__`.
- `jugar_turno() -> bool` en `src/juego.py`: orquesta un turno completo (tirada de dados, detección de dobles, chequeo de posibilidad de mover y manejo de pérdida de turno).
- `esta_terminado() -> bool` en `src/juego.py`: consulta rápida para saber si hay ganador.
- `obtener_estado_juego() -> dict` en `src/juego.py`: snapshot del estado (turno, color, dados disponibles, ganador, fichas en barra y fuera por color).
- `reiniciar_juego()` en `src/juego.py`: reestablece `Tablero`, limpia `__turno_actual__`, `__ganador__` y `__dados_disponibles__`.

## [0.25.0] - 2025-10-27 18:59
### Added
- Implementación inicial de la **interfaz de línea de comandos (CLI)** para el juego de **Backgammon**.
- Integración con la clase `BackgammonGame` ubicada en el módulo `src/juego.py`.
- Función `limpiar_pantalla()` para limpiar la consola según el sistema operativo.
- Mensaje de **bienvenida** y **pantalla de victoria** con formato visual.
- Solicitud de nombres de jugadores, con valores por defecto ("Jugador 1", "Jugador 2").
- Renderizado textual del **tablero de Backgammon**, mostrando:
  - Los 24 puntos numerados.
  - Fichas representadas por símbolos (`B` para blancas, `N` para negras).
  - Fichas en la barra y fuera del tablero.
- Comandos disponibles para interacción en consola:
  - `mover <origen> <dado>` → Mover ficha.
  - `barra <dado>` → Reingresar ficha desde la barra.
  - `pasar` → Pasar turno si no hay movimientos válidos.
  - `ayuda` → Mostrar lista de comandos.
  - `salir` → Finalizar la partida.
- Sistema de turnos alternado automáticamente entre jugadores.
- Validación y ejecución de movimientos mediante `obtener_movimientos_legales()` y `realizar_movimiento()`.
- Verificación de victoria al finalizar cada movimiento.
- Gestión de errores y validaciones de entrada:
  - Control de valores numéricos incorrectos.
  - Manejo de excepciones con mensajes descriptivos.
- Documentación en docstrings estilo PEP 257 para todas las funciones y clases.

## [0.26.0] - 2025-10-28 12:48
### Added
- Método `iniciar()` que implementa el **bucle principal del juego**, permitiendo:
  - Iniciar una nueva partida de Backgammon.
  - Configurar los nombres de los jugadores antes de comenzar.
  - Ejecutar el flujo completo de juego hasta que haya un ganador o el jugador decida salir.
- Método `jugar_de_nuevo()` que permite **reiniciar el juego** tras finalizar una partida.
  - Acepta respuestas afirmativas (`s`, `si`, `sí`, `yes`, `y`)
- Mensaje de despedida al salir del programa.

## [0.27.0] - 2025-10-28 13:20
### Added
- **Interfaz gráfica (GUI) con Pygame**: Proporciona una experiencia visual e interactiva del Backgammon.
- **Inicialización de ventana y contexto gráfico**:
  - Tamaño por defecto `1200x800`, título de ventana “Backgammon”.
  - Reloj (`pygame.Clock`) para control de FPS.
- **Sistema de estados de la UI**:
  - Atributo `__estado__` con valores `menu`, `juego`, `victoria`.
  - Variables de apoyo: `__mensaje__` y `__tiempo_mensaje__` para mostrar feedback temporal.
- **Tipografía y estilos**:
  - Fuentes preconfiguradas para título, texto y texto pequeño.
- **Paleta y constantes visuales**:
  - Colores para fondo, tablero, puntos claros/oscursos, barra, fichas (blancas/negras), bordes, selección y movimientos posibles.
  - Colores para mensajes de error/éxito y botones (normal/hover).
  - Dimensiones: márgenes y radio de ficha configurables.
- **Selección y asistencia al movimiento**:
  - `__punto_seleccionado__` y `__movimientos_posibles__` para interacción guiada del usuario.
- **Integración con lógica de juego**:
  - Importación de `BackgammonGame` desde `src/juego.py`.
  - Preparativos para cálculo de layout del tablero vía `__calcular_dimensiones_tablero__()`.