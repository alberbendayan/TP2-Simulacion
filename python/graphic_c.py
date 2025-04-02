import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np


def main():
    if len(sys.argv) < 3:
        print("Uso: python graphic_c.py <results_folder> <stationary_point> [show_figure]")
        sys.exit(1)

    results_path = sys.argv[1]
    stationary_point = int(sys.argv[2])
    show_figure = bool(sys.argv[3]) if len(sys.argv) > 3 else False

    output_folder = os.path.join(results_path, "graphics")
    config = os.path.join(results_path, "config.json")

    if not os.path.exists(config):
        print("No se encontró el archivo de configuración:", config)
        sys.exit(1)

    with open(config, "r") as config_file:
        config = json.load(config_file)

    grid_size = config.get("gridSize", None)
    probabilities = config.get("probabilities", [])

    if grid_size is None or not probabilities:
        print("El tamaño de la cuadrícula o las probabilidades no están definidos en el archivo de configuración.")
        sys.exit(1)

    graph_data = {}

    for p in probabilities:
        # vamos a calcular la media de opiniones y la susceptibilidad a partir del estado estacionario
        data_file = os.path.join(results_path, f"general_{p:.4f}.txt")
        data = np.loadtxt(data_file, dtype=float)

        recent_data = data[stationary_point:]
        mean_consenso = np.mean(recent_data)
        mean_consenso_squared = np.mean(recent_data**2)
        succeptibility = grid_size**2 * (mean_consenso_squared - mean_consenso**2)
        std = np.std(recent_data)

        graph_data[f"{p:.4f}"] = {
            "mean_consenso": mean_consenso,
            "succeptibility": succeptibility,
            "std": std,
        }

    # Graficar la susceptibilidad y la consenso medio en el mismo gráfico con diferentes escalas
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Convertir las claves a valores numéricos para poder ordenarlos
    prob_values = [float(p) for p in graph_data.keys()]
    sorted_indices = np.argsort(prob_values)
    sorted_probs = [prob_values[i] for i in sorted_indices]
    sorted_probs_str = [str(p) for p in sorted_probs]

    # Datos para graficar
    susceptibilities = [graph_data[f"{p:.4f}"]["succeptibility"] for p in sorted_probs]
    mean_consensos = [graph_data[f"{p:.4f}"]["mean_consenso"] for p in sorted_probs]
    std_devs = [graph_data[f"{p:.4f}"]["std"] for p in sorted_probs]

    # Gráfico de susceptibilidad (eje izquierdo)
    color1 = "blue"
    ax1.set_xlabel("Probabilidad")
    ax1.set_ylabel("Susceptibilidad", color=color1)
    ax1.plot(sorted_probs_str, susceptibilities, "o:", color=color1, linewidth=1, label="Susceptibilidad")
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    # Gráfico de consenso medio (eje derecho)
    ax2 = ax1.twinx()
    color2 = "red"
    ax2.set_ylabel("Consenso Medio", color=color2)
    ax2.errorbar(sorted_probs_str, mean_consensos, yerr=std_devs, fmt="s:", color=color2, linewidth=1, capsize=3, label="Consenso Medio ± σ")
    ax2.tick_params(axis="y", labelcolor=color2)

    # Añadir leyendas para ambos ejes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    plt.tight_layout()

    # Si se encuentra en output_folder, guarda la figura
    os.makedirs(output_folder, exist_ok=True)
    plt.savefig(os.path.join(output_folder, "susceptibility_and_concensus.png"), dpi=300)

    if show_figure:
        plt.show()


if __name__ == "__main__":
    main()
