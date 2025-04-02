<h1 align="center">Simulación de Sistemas</h1>
<h3 align="center">TP2: Autómatas Celulares</h3>
<h4 align="center">Primer cuatrimestre 2025</h4>

# Requisitos

* Java versión 21: Para correr el simulador
* Maven: Para compilar el proyecto de Java
* Python ([versión 3.12.9](https://www.python.org/downloads/release/python-3129/)): Para los gráficos
* [UV](https://github.com/astral-sh/uv): Administrador de dependencias para
Python

# Instalando las dependencias

Para instalar las dependencias, ubicarse en la carpeta `python` haciendo `cd ./python/` y luego correr:

```sh
# Si python 3.12.9 no esta instalado se puede instalar haciendo
uv python install 3.12.9

# Para crear y activar el entorno virtual
uv venv
source .venv/bin/activate  # En Unix
.venv\Scripts\activate     # En Windows

# Para instalar las dependencias
uv sync
```

# Compilando el proyecto

Desde la consola, para compilar el proyecto de **Java**, desde la raíz del
proyecto, correr:

```bash
mvn clean package
```

# Ejecución de la simulación

Para correr la simulación, en Java, se le pueden pasar dos parámetros
opcionales, especificando el tamaño de la grilla de simulación (`N`) y la
cantidad de pasos de Monte Carlo (`M`).

Cada fotograma de la simulación estará dada cada `N x N` pasos de Monte Carlo.
Por lo que para `M`, pasos, habrá un total de `M / (N x N)` fotogramas.

Para correr la simulación simplemente correr desde la raíz del proyecto:

```bash
java -classpath target/classes ar.edu.itba.ss.VoterModel <grid_size> <monte_carlo_steps> <probabilities> <save_states>
```

Estos parámetros son opcionales, si no se ingresan, el simulador tomará valores
por defecto.

El parámetro `<save_states>` representa si se guarda cada uno de los estados de
la grilla. Puede ponerse en `false` si no se quiere guardar para ahorrar
almacenamiento y solo guardará los valores de **consenso** calculados en cada
estado.

Los resultados de la simulación, estarán guardados en la carpeta `results/`, con
los estados por cada probabilidad para cada fotograma, junto de los valores de
consenso en cada estado.

# Ejecución de la animación y los gráficos

Hay cuatro archivos dentro de la carpeta `python` que generan los videos y las
imágenes de los gráficos dentro de una carpeta `graphics/` en la carpeta de
resultados de la simulación que se seleccione:

1. Uno genera una animación con los estados de cada fotograma.
2. El otro muestra una línea temporal de la media de las opiniones pudiéndose
observar un eventual estado estacionario.

## Animación

Para visualizar la animación se puede correr:

```bash
uv run graphic_a.py <results_path> <probability> [frame_skip] [show_animation]
```

La variable opcional `frame_skip` permite configurar cada cuantos fotogramas
muestra un fotograma en la animación. Esto permite acelerar el proceso ya que a
veces el estado estacionario se alcanza a los 7000 fotogramas.

La variable opcional `show_animation` permite, mostrar la animación en una
ventana aparte para no tener que ir a abrirlo desde el explorador de archivos.

## Gráficos

### Evolución temporal

Para visualizar el gráfico de evolución se puede correr:

```bash
uv run graphic_b.py <results_path> <probability> [show_figure]
```

La variable opcional `show_figure` permite, mostrar la figura en una ventana
aparte para no tener que ir a abrirlo desde el explorador de archivos.

### Susceptibilidad y consenso

Para visualizar el gráfico de susceptibilidad y consenso por cada probabilidad
utilizada se puede correr:

```bash
uv run graphic_c.py <results_folder> <stationary_point> [show_figure]
```

La variable `stationary_point` es la cantidad de pasos de Monte Carlo a partir
del cuál se alcanza el estado estacionario. Para obtener dicho valor es
recomendable correr el [gráfico de evolución temporal](#evolución-temporal) y
visualizar a partir de que punto se alcanza dicho estado.

### Comparativa de susceptibilidad y consenso para diferentes grillas

Para visualizar esta comparativa de susceptibilidad y consenso para varios
tamaños de grilla (o varios **sets** de resultados) diferentes se puede correr:

```bash
uv run graphic_d.py <stationary_point> <results_folder1> [results_folder2] [results_folder3] ...
```

Donde, al igual que en el [gráfico de susceptibilidad y consenso](#susceptibilidad-y-consenso)
hay que especificar el punto donde se alcanza el estado estacionario.
