# Proyecto TP2-Simulacion

Este proyecto incluye scripts en Python para la generación de gráficos basados en resultados de simulaciones.

## Requisitos

- Python (compatible con `uv`)
- [`uv`](https://github.com/astral-sh/uv) instalado para la ejecución eficiente de los scripts

## Instalación

Si aún no tienes `uv` instalado, puedes instalarlo con:

```sh
pip install uv
```
Para sincronizar los paquetes
```sh
uv sync
```

## Ejecución
Para guardar un grafico, hay que correr este comando donde X puede ser A o B
```
uv run graphicX.py <ruta_de_resultados> <p>
```
A es la animacion paso a paso y B es el grafico que muestra la evolucion.
Los resultados se van a encontrar en el directorio graphics_results
