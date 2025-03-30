import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np


def main():
    if len(sys.argv) < 3:
        print("Uso: python graphic_b.py <results_folder> <probability> [show_figure]")
        sys.exit(1)

    results_path = sys.argv[1]
    p = float(sys.argv[2])
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

    if grid_size is None or p not in probabilities:
        print("El tamaño de la cuadrícula o la probabilidad seleccionada no están definidos en el archivo de configuración.")
        sys.exit(1)

    data_file = os.path.join(results_path, f"general_{p:.4f}.txt")
    data = np.loadtxt(data_file, dtype=float)

    steps = np.arange(1, len(data) + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(steps, data, "b-", linewidth=1)

    plt.xlabel("Pasos de Monte Carlo")
    plt.ylabel("Media de opiniones")
    plt.title("Opiniones en la simulación de Monte Carlo")

    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1)
    plt.tight_layout()

    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"opiniones_{p:.4f}.png")
    plt.savefig(output_file)

    if show_figure:
        plt.show()


if __name__ == "__main__":
    main()
