# 📜 Prompts de Documentacion – Backgammon Computación 2025

En este archivo se registran todos los prompts utilizados con herramientas de IA durante el **documentacion** del proyecto.  
Cada entrada incluye el modelo usado, el prompt original, la respuesta obtenida y cómo se aplicó (si se usó o mse dificó).  
---

## 🔹 Prompt #1 – Generar el Readme.md

**🛠️ Herramienta / Modelo:** ChatGPT (GPT-5)  
**📅 Fecha:** 1/11/2025 – 19:31  
**📂 Archivo relacionado:** `README.md`  

---

### 📝 Prompt enviado  
```markdown 
Realiza un Readme completo de este proyecto. Explicandolo, mostrando su estructura, y sus formas de ejecutarlo
```
---
### 📝 Respuesta de la IA
```markdown 
# Backgammon

Proyecto académico que implementa la lógica completa de un juego de Backgammon, junto con
interfaces para jugarlo desde la terminal o mediante una interfaz gráfica construida con
[Pygame](https://www.pygame.org/). La solución está escrita en Python y está organizada en
módulos independientes que modelan el tablero, los jugadores, los dados y el flujo general
del juego.

## Características principales

- **Motor de juego** con clases dedicadas para tablero, dados y jugadores (`src/`).
- **Interfaz de línea de comandos (CLI)** interactiva para jugar desde la terminal (`cli/`).
- **Interfaz gráfica** con Pygame que representa el tablero, los movimientos posibles y el
  estado de la partida en tiempo real (`pygame_ui/`).
- **Conjunto de pruebas unitarias** basadas en `unittest` y ejecutables con `pytest`
  (`test/`).
- Scripts auxiliares y reportes generados durante el desarrollo (`generate_reports.py`,
  `coverage_report.txt`, `pylint_report.txt`, etc.).

## Estructura del proyecto

```
.
├── cli/                    # CLI interactiva del juego
│   └── cli.py
├── pygame_ui/              # Interfaz gráfica desarrollada con Pygame
│   └── pygame_ui.py
├── src/                    # Lógica principal del juego
│   ├── dados.py            # Clase "Dados" y tiradas
│   ├── juego.py            # Clase "BackgammonGame" que orquesta la partida
│   ├── jugador.py          # Clase "Jugador" y movimientos legales
│   └── tablero.py          # Clase "Tablero" y reglas de movimiento
├── test/                   # Suite de pruebas unitarias
│   ├── test_dados.py
│   ├── test_juego.py
│   ├── test_jugador.py
│   └── test_tablero.py
├── requirements.txt        # Dependencias del proyecto
├── generate_reports.py     # Script auxiliar para informes de cobertura/pylint
├── *.md / *.txt            # Documentos del proyecto y reportes generados
└── README.md               # Este archivo
```

## Requisitos previos

- Python 3.11 o superior.
- Se recomienda trabajar dentro de un entorno virtual (`venv`, `conda`, etc.).
- Para la interfaz gráfica es necesario instalar `pygame`.

### Instalación de dependencias

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install pygame         # Sólo si utilizarás la interfaz gráfica
```

> `requirements.txt` contiene únicamente las dependencias usadas en el curso. Puedes añadir
> `pytest`, `pygame` u otras herramientas según las necesites.

## Formas de ejecución

### 1. Ejecutar el juego desde la terminal (CLI)

La CLI guía la partida turno a turno, mostrando el tablero textual, los dados disponibles y
los comandos admitidos (`mover`, `barra`, `pasar`, `ayuda`, `salir`).

```bash
python -m cli.cli
```

### 2. Ejecutar la interfaz gráfica con Pygame

La interfaz gráfica ofrece un tablero visual, resaltando movimientos posibles, fichas en la
barra, fichas fuera y mensajes contextualizados.

```bash
python -m pygame_ui.pygame_ui
```

### 3. Ejecutar las pruebas automatizadas

El repositorio incluye una extensa batería de pruebas unitarias. Puedes ejecutarlas con
`pytest` (recomendado) o con el runner estándar de `unittest`.

```bash
# Usando pytest
python -m pytest

# Usando unittest
python -m unittest discover -s test

# Midiendo cobertura con coverage + unittest
coverage run -m unittest discover -s test
coverage report -m              # Muestra el resumen en la terminal
coverage html                   # (Opcional) Genera un reporte navegable en htmlcov/
```

> Nota: al momento de escribir este README algunos casos de prueba fallan debido a cambios
> recientes en la encapsulación del tablero y a validaciones estrictas al mover fichas. Se
> recomienda revisar las aserciones fallidas para alinear la implementación con las reglas
> esperadas o actualizar las pruebas según corresponda.

### 4. Generar reportes de calidad (opcional)

El script `generate_reports.py` automatiza la ejecución de herramientas como `coverage` y
`pylint`, dejando los resultados en archivos `.txt` dentro del repositorio.

```bash
python generate_reports.py
```

## Módulos principales

- **`src/tablero.py`**: gestiona el estado del tablero, el conteo de fichas, la barra y las
  reglas para validar y aplicar movimientos o reingresos.
- **`src/jugador.py`**: encapsula la información de cada jugador y calcula los movimientos
  legales disponibles según la tirada de dados y la situación del tablero.
- **`src/dados.py`**: modela la tirada de dos dados de seis caras, manejando el caso especial
  de los dobles (uso de cuatro movimientos).
- **`src/juego.py`**: coordina turnos, tiradas, validaciones y la detección de victoria.

## Documentación y recursos adicionales

Además del código fuente, el repositorio incluye varios documentos (`prompts_*.md`,
`REPORTS.md`, `JUSTIFICACION.md`, `CHANGELOG.md`) que registran decisiones de diseño,
actividades de testing y entregables del curso.

## Contribuciones y mantenimiento

1. Crea una rama a partir de `main` para cada mejora o corrección.
2. Ejecuta las pruebas antes de enviar cambios.
3. Abre un *pull request* describiendo el impacto de la modificación.

¡Disfruta jugando y experimentando con Backgammon en Python!
```
