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