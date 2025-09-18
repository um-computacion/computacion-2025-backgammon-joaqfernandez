# 📜 Prompts de Desarrollo – Backgammon Computación 2025  

En este archivo se registran todos los prompts utilizados con herramientas de IA durante el **desarrollo** del proyecto.  
Cada entrada incluye el modelo usado, el prompt original, la respuesta obtenida y cómo se aplicó (si se usó o mse dificó).  

---

## 🔹 Prompt #1 – Funcion para movimientos legales de `Jugador`

**🛠️ Herramienta / Modelo:** ChatGPT (GPT-5)  
**📅 Fecha:** 16/09/2025 – 15:03  
**📂 Archivo relacionado:** `src/jugador.py`  

---

### 📝 Prompt enviado  
```markdown 
Necesito una funcion que me devuela los posibles movimientos legales
que puede hacer un jugador
```
---
### 📝 Respuesta de la IA
```markdown 
def movimientos_legales(self, tablero, dados: List[int]) -> List[Tuple[int, int, int]]:
        """
        Calcula movimientos (origen, destino, dado) legales con el estado actual del tablero.
        Por ahora considera SOLO movimientos regulares (sin barra ni bearing-off).

        Args:
            tablero (Tablero): instancia del tablero actual.
            dados (List[int]): valores disponibles del turno (ej: [3, 5] o [4,4,4,4]).

        Return:
            List[Tuple[int, int, int]]: lista de (origen, destino, dado).
        """
        legales: List[Tuple[int, int, int]] = []

        # Recorremos los 24 puntos y probamos cada dado.
        for origen in range(24):
            punto = tablero._Tablero__puntos__[origen]  # usamos lo que ya tenés
            if punto["color"] != self.__color__ or punto["cantidad"] == 0:
                continue

            for dado in dados:
                destino = tablero.lugar_destino(self.__color__, origen, dado)
                if tablero.hay_ficha_o_no(self.__color__, origen, dado):
                    legales.append((origen, destino, dado))

        return legales
```
