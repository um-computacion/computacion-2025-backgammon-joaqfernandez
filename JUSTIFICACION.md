# Justificación Técnica del Proyecto: Backgammon

Este documento detalla las principales decisiones de diseño, arquitectura y calidad que guiaron el desarrollo del proyecto Backgammon. Su objetivo es servir como referencia académica y técnica para comprender por qué el código se estructuró de la forma actual y cómo se garantiza su mantenibilidad.

## 1. Resumen del Diseño General

La arquitectura sigue un esquema en capas inspirado en la separación de responsabilidades:

- **Capa de Dominio (`src/`)**: Contiene la lógica del juego y las reglas fundamentales. Aquí se encapsulan las entidades principales (tablero, jugadores, dados y coordinador de partida).
- **Capa de Interfaces**:
  - **CLI (`cli/`)**: Brinda interacción por consola para depurar y demostrar la lógica sin dependencias gráficas.
  - **UI Gráfica (`pygame_ui/`)**: Implementa la visualización y el flujo de interacción mediante Pygame.
- **Capa de Validación (`test/`)**: Aporta la suite de pruebas automatizadas que aseguran el cumplimiento de las reglas y previenen regresiones.
- **Capa de Documentación (`README.md`, `REPORTS.md`, etc.)**: Centraliza la evidencia del proceso de desarrollo y las métricas de calidad.

Este diseño modular busca que cada capa evolucione de manera independiente, permitiendo incorporar nuevas interfaces o reglas sin afectar el núcleo.

## 2. Justificación de Clases y Atributos

### 2.1 Clases Principales y Responsabilidades

- **`Juego` (`src/juego.py`)**: Orquesta la partida, administra turnos, delega validaciones y determina condiciones de victoria o finalización anticipada.
- **`Tablero` (`src/tablero.py`)**: Representa los 24 puntos, el bar y el borne-off. Expone operaciones para mover fichas, capturar y validar movimientos legales.
- **`Jugador` (`src/jugador.py`)**: Guarda el color, las fichas en la barra y la lógica para seleccionar jugadas posibles según la tirada actual.
- **`Dados` (`src/dados.py`)**: Modela los dos dados y contempla el caso de dobles otorgando cuatro movimientos.

### 2.2 Atributos Clave

- **`Tablero.puntos`**: Lista de enteros que refleja la cantidad de fichas por punto y su propietario (signo). Simplifica la detección de ocupaciones y capturas.
- **`Tablero.bar` / `Tablero.borne_off`**: Contadores separados para gestionar entradas y salidas de fichas sin recorrer toda la estructura principal.
- **`Jugador.color`**: Define la dirección de movimiento y permite que las reglas se expresen de forma genérica con operaciones aritméticas.
- **`Dados.valores_actuales`**: Registro de la tirada en curso para que el juego valide el consumo de movimientos, especialmente en dobles.

## 3. Decisiones de Diseño Relevantes

### 3.1 Alternativas Consideradas

1. **Integrar toda la lógica en la interfaz gráfica**: Rechazada porque dificultaba pruebas y reutilización.
2. **Modelar el tablero con objetos por punto**: Descartada por el costo de memoria y complejidad; una lista de enteros resultó más simple y eficiente.
3. **Gestionar estados con funciones globales**: Incompatible con los principios de encapsulamiento y dificultaba el mantenimiento.

### 3.2 Solución Adoptada

- **Separación dominio / interfaces**: Permite probar la lógica con la CLI sin depender de Pygame y facilita la incorporación de nuevas vistas (por ejemplo, una API web).
- **Uso de clases específicas**: Refuerza el principio de responsabilidad única y evita que un módulo concentre demasiadas funciones.
- **Validaciones estrictas**: Los métodos del tablero y del juego verifican precondiciones antes de modificar el estado, evitando inconsistencias.

## 4. Estrategia de Testing y Calidad

- **Framework**: Se utiliza `pytest` para estructurar y ejecutar las pruebas.
- **Cobertura**: El archivo `coverage_report.txt` evidencia la medición de líneas cubiertas; las pruebas se centran en reglas de movimiento, dobles, capturas y fin de partida.
- **Estilo y análisis estático**: `pylint_report.txt` documenta los resultados de análisis sobre convenciones y posibles errores.
- **Integración continua manual**: La suite de tests se ejecuta antes de integrar cambios importantes, asegurando que la lógica principal no se rompa.

## 5. Referencias a Principios SOLID

- **Responsabilidad Única (SRP)**: Cada clase del dominio tiene una preocupación concreta (coordinación, almacenamiento de estado, reglas de jugador, aleatoriedad).
- **Abierto/Cerrado (OCP)**: El motor acepta nuevas reglas o interfaces mediante extensión sin modificar código existente (por ejemplo, agregar un bot heredando de `Jugador`).
- **Sustitución de Liskov (LSP)**: Las estructuras permiten incorporar subclases (p. ej. `JugadorIA`) sin alterar la lógica de `Juego`.
- **Segregación de Interfaces (ISP)**: La división entre CLI y UI gráfica evita exponer métodos innecesarios a cada capa.
- **Inversión de Dependencias (DIP)**: Las interfaces dependen del núcleo y no al revés; cualquier componente de presentación consume la API del dominio.

## 6. Trabajo Futuro y Mejora Continua

- Ampliar la cobertura de reglas avanzadas (p. ej. gammon/backgammon y limitaciones de reingreso con bloqueo total).
- Incorporar animaciones y un flujo de turnos más guiado en la UI de Pygame.
- Añadir modos de juego automatizados (IA básica o soporte en red) reutilizando la capa de dominio.
- Integrar pipelines automáticos para ejecutar `pytest`, `pylint` y cobertura en cada commit.

## 7. Anexos

- **Diagrama de clases UML**: A deber.
- **Reportes de métricas**: `pylint_report.txt` y `coverage_report.txt` complementan esta justificación con datos cuantitativos.

