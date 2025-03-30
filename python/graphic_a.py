import json
import os
import sys

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def main():
    if len(sys.argv) < 3:
        print("Uso: python graphic_a.py <results_folder> <probability> [frame_skip] [show_animation]")
        sys.exit(1)

    results_path = sys.argv[1]
    p = float(sys.argv[2])
    frame_skip = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    show_animation = sys.argv[4] == "True" if len(sys.argv) > 4 else False

    data_path = os.path.join(results_path, f"{p:.4f}")
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

    files = sorted([f for f in os.listdir(data_path) if f.endswith(".txt")])
    if not files:
        print("No se encontraron archivos en", data_path)
        sys.exit(1)

    matrices = []
    for i, file in enumerate(files):
        if i % frame_skip == 0:
            filepath = os.path.join(data_path, file)
            matrix = np.loadtxt(filepath, dtype=int)
            matrices.append(matrix)

    total_iterations = len(matrices)

    fig, ax = plt.subplots()
    im = ax.imshow(matrices[0], cmap="Blues", vmin=-1, vmax=1)

    def update(frame):
        im.set_data(matrices[frame])
        ax.set_title(f"Iteración {(frame + 1) * frame_skip}")
        return (im,)

    ani = animation.FuncAnimation(fig, update, frames=total_iterations, interval=1, blit=False, repeat=False)

    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, f"animation_{p:.4f}_N{grid_size}.mp4")

    ani.save(file_path, writer="ffmpeg", fps=100)

    if show_animation:
        plt.show()


if __name__ == "__main__":
    main()
