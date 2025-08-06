# 🛰️ DroneCore - Juego de drones basado en Costa Rica

Este es un videojuego educativo y estratégico, desarrollado como proyecto de programación, que simula la operación de un dron con recursos energéticos limitados en un entorno hostil y dinámico. El jugador debe tomar decisiones rápidas para entregar paquetes, esquivar amenazas y administrar eficientemente la batería disponible. El juego fue desarrollado en Python usando la librería **Pygame**, con enfoque modular y educativo.

## 🧠 Resumen

El sistema representa una simulación caótica que combina logística, sostenibilidad y gestión autónoma de recursos. En este entorno, el jugador pilota un dron que debe esquivar aves, vacas enemigas, árboles que caen y otros obstáculos. A lo largo del camino, podrá encontrar puntos de recarga (vidas flotantes) que permiten recuperar batería. La misión final es alcanzar la **Meta**, representada como una diana flotante, antes de perder todas las vidas.

---

## 📁 Estructura del Proyecto

```
📦JuegoProgra/
┣ 📁assets/                  # Archivos gráficos y sonidos (sprites, fondos, música)
┣ 📜main.py                 # Punto de entrada principal del juego
┣ 📜escenario.py            # Lógica principal del juego (scroll, enemigos, eventos)
┣ 📜npc_indio.py            # Clase del NPC enemigo: Indio (dispara flechas)
┣ 📜npc_tucan.py            # Clase del NPC enemigo: Tucán (dispara proyectiles)
┣ 📜npc_vaca.py             # Clase del NPC enemigo: Vaca (lanza leche)
┣ 📜sistema_vidas.py        # Gestión de vidas y baterías flotantes
┣ 📜pantalla_gano.py        # Pantalla que aparece al ganar el juego
┣ 📜game_over_screen.py     # Pantalla que aparece al perder el juego
┣ 📜meta.py                 # Elemento de victoria (Meta final flotante)
┣ 📜lluvia.py               # Evento aleatorio: Tormenta Tropical
┣ 📜disparo.py              # Lógica del disparo del dron (huevos congelantes)
┣ 📜arbol.py                # Árbol que cae al detectar proximidad
┗ 📜README.md               # Este archivo
```

---

## 🛠️ Dependencias

Este proyecto fue desarrollado con:

- **Python 3.10+**
- **Pygame 2.5.2**

Para instalar las dependencias necesarias:

```bash
pip install pygame
```

> [!WARNING]
> Asegúrate de estar en el directorio `/JuegoProgra` antes de ejecutar `main.py`, ya que las rutas relativas a los assets están configuradas para esta ubicación.

---

## 🎮 Cómo jugar

1. Ejecutá el archivo `main.py`:
   ```bash
   python main.py
   ```
2. Usá las teclas de dirección para mover el dron.
3. Usá `ESPACIO` para lanzar disparos (huevos).
4. Podés usar `ALT` para apuntar automáticamente al enemigo más cercano.
5. El objetivo es llegar a la **Meta Final** antes de quedarte sin vidas.

Para una guía completa y visual del juego, podés seguir este tutorial:

📘 [https://code2tutorial.com/tutorial/aa1604b7-54a6-4042-99b2-450b24a1783d/index.md](https://code2tutorial.com/tutorial/aa1604b7-54a6-4042-99b2-450b24a1783d/index.md)

---

## 👥 Desarrolladores

- **Byron Bolaños Zamora** - [bolanoscontacto@gmail.com](mailto:bolanoscontacto@gmail.com)
- **Javier Mendoza Gonzalez** - [ag7000107@gmail.com](mailto:ag7000107@gmail.com)

---

## 📌 Observaciones

- Todo el código fue modularizado para facilitar su comprensión, depuración y futura expansión.
- Se utilizaron sprites con máscaras para mejorar la precisión de las colisiones.
- El juego incluye eventos aleatorios como tormentas o árboles cayendo, para simular un entorno más realista.
- El sistema de disparo permite congelar temporalmente enemigos y destruir obstáculos.

---

¡Esperamos que este proyecto sea de tu agrado!
¡Te deseamos un buen código hermano!
