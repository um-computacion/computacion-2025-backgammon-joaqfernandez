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



