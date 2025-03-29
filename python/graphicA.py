import os
import sys
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import json

if len(sys.argv) != 3:
    print("Uso: python script.py <N>")
    sys.exit(1)


path = sys.argv[1]
p = sys.argv[2]
data_path = path+"/" + p + "/"
output_folder = "../graphics_result"

config_json = path + "/config.json"
if not os.path.exists(config_json):
    print("No se encontró el archivo de configuración:", config_json)
    sys.exit(1)

with open(config_json, "r") as config_file:
    config = json.load(config_file)

N = config.get("gridSize", None) 


os.makedirs(output_folder, exist_ok=True) # carpeta de salida

files = sorted([f for f in os.listdir(data_path) if f.endswith(".txt")])

if not files:
    print("No se encontraron archivos en", data_path)
    sys.exit(1)

matrices = []
for i, file in enumerate(files):
    if i % 10 == 0:
        filepath = os.path.join(data_path, file)
        matrix = np.loadtxt(filepath, dtype=int)
        matrices.append(matrix)

num_iteraciones = len(matrices)

fig, ax = plt.subplots()
im = ax.imshow(matrices[0], cmap="Blues", vmin=-1, vmax=1)

def update(frame):
    im.set_data(matrices[frame])
    ax.set_title(f"Iteración {(frame + 1) * 50}")
    return (im,)

ani = animation.FuncAnimation(
    fig, update, frames=num_iteraciones, interval=1, blit=False, repeat=False
)

file_path = os.path.join(output_folder, f"animacionA_{p}_N{N}.mp4")

ani.save(file_path, writer="ffmpeg", fps=100)


# si vamos a guardarlo, no lo mostremos xq perdemos tiempo y ram
# plt.show()
