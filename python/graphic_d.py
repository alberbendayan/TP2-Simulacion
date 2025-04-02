import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np


def main():
    if len(sys.argv) < 3:
        print("Uso: python graphic_d.py <stationary_point> <results_folder1> [results_folder2] [results_folder3] ...")
        sys.exit(1)

    stationary_point = int(sys.argv[1])
    results_paths = sys.argv[2:]

    if len(results_paths) < 1:
        print("Se necesita al menos una carpeta de resultados")
        sys.exit(1)

    # Preparar los datos de cada carpeta de resultados
    all_data = {}
    grid_sizes = []

    # Colores para las diferentes curvas
    colors = ["blue", "red", "green", "yellow", "orange", "brown", "pink", "gray", "olive", "cyan"]

    for idx, results_path in enumerate(results_paths):
        config_file = os.path.join(results_path, "config.json")

        if not os.path.exists(config_file):
            print(f"No se encontró el archivo de configuración en: {results_path}")
            continue

        with open(config_file, "r") as f:
            config = json.load(f)

        grid_size = config.get("gridSize", None)
        probabilities = config.get("probabilities", [])

        if grid_size is None or not probabilities:
            print(f"El tamaño de la cuadrícula o las probabilidades no están definidos en: {results_path}")
            continue

        grid_sizes.append(grid_size)
        color = colors[idx % len(colors)]

        data = process_results(results_path, grid_size, probabilities, stationary_point)
        all_data[grid_size] = {"data": data, "color": color}

    if not all_data:
        print("No se pudieron procesar datos de ninguna carpeta de resultados")
        sys.exit(1)

    # Crear las figuras
    create_figures(all_data, grid_sizes)


def process_results(results_path, grid_size, probabilities, stationary_point):
    """Procesa los resultados de una carpeta específica."""
    graph_data = {}

    for p in probabilities:
        data_file = os.path.join(results_path, f"general_{p:.4f}.txt")

        if not os.path.exists(data_file):
            print(f"No se encontró el archivo de datos: {data_file}")
            continue

        data = np.loadtxt(data_file, dtype=float)

        if len(data) <= stationary_point:
            print(f"El punto estacionario ({stationary_point}) es mayor que la longitud de los datos en {data_file}")
            continue

        recent_data = data[stationary_point:]
        mean_consenso = np.mean(recent_data)
        mean_consenso_squared = np.mean(recent_data**2)
        susceptibility = grid_size**2 * (mean_consenso_squared - mean_consenso**2)
        std = np.std(recent_data)

        graph_data[f"{p:.4f}"] = {
            "mean_consenso": mean_consenso,
            "susceptibility": susceptibility,
            "std": std,
        }

    return graph_data


def create_figures(all_data, grid_sizes):
    # Figura 1: Susceptibilidad para cada tamaño de grilla
    fig_susceptibility = plt.figure(figsize=(10, 6))
    ax_susceptibility = fig_susceptibility.add_subplot(111)

    # Figura 2: consenso medio para cada tamaño de grilla
    fig_consenso = plt.figure(figsize=(10, 6))
    ax_consenso = fig_consenso.add_subplot(111)

    for grid_size in sorted(all_data.keys()):
        data = all_data[grid_size]["data"]
        color = all_data[grid_size]["color"]

        # Convertir las claves a valores numéricos para poder ordenarlos
        prob_values = [float(p) for p in data.keys()]
        sorted_indices = np.argsort(prob_values)
        sorted_probs = [prob_values[i] for i in sorted_indices]
        sorted_probs_str = [str(p) for p in sorted_probs]

        # Datos para graficar
        susceptibilities = [data[f"{p:.4f}"]["susceptibility"] for p in sorted_probs]
        mean_consensos = [data[f"{p:.4f}"]["mean_consenso"] for p in sorted_probs]
        std_devs = [data[f"{p:.4f}"]["std"] for p in sorted_probs]

        # Graficar susceptibilidad
        ax_susceptibility.plot(
            sorted_probs_str,
            susceptibilities,
            "o:",
            color=color,
            linewidth=1.5,
            label=f"Grid {grid_size}x{grid_size}",
        )

        # Graficar Consenso medio con barras de error
        ax_consenso.errorbar(
            sorted_probs_str,
            mean_consensos,
            yerr=std_devs,
            fmt="s:",
            color=color,
            linewidth=1.5,
            capsize=3,
            label=f"Grid {grid_size}x{grid_size}",
        )

    # Configurar gráfico de susceptibilidad
    ax_susceptibility.set_xlabel("Probabilidad")
    ax_susceptibility.set_ylabel("Susceptibilidad")
    ax_susceptibility.grid(True, alpha=0.3)
    ax_susceptibility.legend(loc="best")

    # Configurar gráfico de consenso medio
    ax_consenso.set_xlabel("Probabilidad")
    ax_consenso.set_ylabel("Consenso Medio")
    ax_consenso.grid(True, alpha=0.3)
    ax_consenso.legend(loc="best")

    # Guardar las figuras
    output_folder = "results/graphics"
    os.makedirs(output_folder, exist_ok=True)

    fig_susceptibility.tight_layout()
    fig_consenso.tight_layout()

    fig_susceptibility.savefig(os.path.join(output_folder, "comparison_susceptibility.png"), dpi=300)
    fig_consenso.savefig(os.path.join(output_folder, "comparison_consenso.png"), dpi=300)

    # Mostrar ambas figuras de forma no bloqueante
    plt.show(block=False)

    # Mantener las figuras abiertas hasta que el usuario cierre el programa
    input("Presione Enter para cerrar las figuras y finalizar...")


if __name__ == "__main__":
    main()
