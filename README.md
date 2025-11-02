# K.E.K.O SPACE


**K.E.K.O SPACE** es un videojuego 2D tipo *arcade espacial*, desarrollado en **Python** con la librería **Pygame**, como proyecto final de grado (TFG).  
El jugador controla a **K.E.K.O**, un navegante cibermercenario que viaja de planeta en planeta en busca de recursos, enfrentándose a meteoritos y cometas.

## Historia

> Hace mucho tiempo, en una galaxia perdida...
>
> K.E.K.O, un navegante cibermercenario, viaja a través del espacio en busca de tecnología prohibida, recursos y reliquias olvidadas.  
> Pero una antigua señal resuena desde un mundo perdido, y K.E.K.O se prepara para su mayor desafío...


## Jugabilidad

- Controla la nave de K.E.K.O con las **flechas del teclado**.
- Evita los **meteoritos** y demás obstáculos.
- Supera cada planeta hasta completar la misión.
- Si logras sobrevivir los cinco niveles, habrás terminado la **DEMO de K.E.K.O SPACE**.

### OBJETIVO 

Suma la mayor cantidad de puntos posibles antes de perder todas las vidas.  
Al finalizar, podrás introducir tus **iniciales** si consigues un **nuevo récord**.

##  Características principales

-  Motor hecho con **Pygame** desde cero.
-  Sistema modular con carpetas `core/`, `models/`, `views/`.
-  Música de fondo y efectos de sonido (colisiones, motor, ambiente).
-  Animaciones de **aterrizaje y despegue** con partículas.
-  Guardado de puntuaciones en base de datos local (SQLite).
-  Pantalla de introducción tipo **máquina de escribir**.
-  Transiciones entre niveles con planetas distintos.
-  Código comentado y limpio, orientado a objetos.

## Estructura del proyecto

KEKO-SPACE/

── main.py # Punto de entrada principal



── core/
── game.py # Lógica central del juego
── settings.py # Configuración general
── levels.json # Datos de niveles




── models/
── player.py # Lógica del jugador
── obstacle.py # Obstáculos y colisiones
── particle.py # Efectos visuales de partículas
── transition.py # Aterrizajes, despegues y animaciones




── views/
── ui.py # Menús, introducción y pantallas finales



── assets/
── music/ # Música de fondo (cosmicchase.mp3)
── sounds/ # Efectos de sonido (engine_fire.ogg, hit.wav, etc.)
── player/ # Sprites del jugador
── obstacles/ # Meteoritos, cometas, etc.
── planets/ # Imágenes de planetas


── README.md
── requeriments.txt


## Requisitos: 

- **Python 3.9+**
- **Pygame 2.5+**

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/BalderBG/KEKO-SPACE.git
cd KEKO-SPACE

# (Opcional) Crear entorno virtual
python -m venv env
source env/bin/activate   # En Linux/Mac
env\Scripts\activate      # En Windows

# Instalar dependencias
pip install pygame

# Ejecutar el juego
python main.py
```
## Créditos

Desarrollado por: Balder-bg
Lenguaje: Python
Framework: Pygame
Música: Creada con SunoAI libre de derechos "16bit" y "Cosmic Chase"
Sonidos: mezclados y editador para ambientacion de motor, impactos y entorno espacial.
Creditos de assets y sonidos: https://kenney.nl/games


## Reflexión final:

El desarrollo de **K.E.K.O SPACE** ha sido una experiencia completa:
combina programación, diseño visual y narrativa interactiva, demostrando el potencial de Python como herramienta para crear videojuegos sencillos pero inmersivos.
El objetivo del proyecto no solo fue construir un juego funcional, sino aprender a estructurar un motor modular y escalable, con un enfoque claro en la jugabilidad y la experiencia del jugador.
