import os
import sys

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

# Leer N desde los argumentos de la terminal
if len(sys.argv) != 2:
    print("Uso: python script.py <N>")
    sys.exit(1)

N = int(sys.argv[1])
data_path = "../result/p_0.01/"

# Obtener la lista de archivos ordenada
files = sorted([f for f in os.listdir(data_path) if f.endswith(".txt")])

# for i in range(len(files)):
#     print("Archivo de nombre: ")
#     print(files[i])

if not files:
    print("No se encontraron archivos en", data_path)
    sys.exit(1)

# Cargar los datos de los archivos
matrices = []
for i, file in enumerate(files):
    if i % 10 == 0:
        filepath = os.path.join(data_path, file)
        matrix = np.loadtxt(filepath, dtype=int)
        matrices.append(matrix)

num_iteraciones = len(matrices)

# Configurar la figura
fig, ax = plt.subplots()
im = ax.imshow(matrices[0], cmap="Blues", vmin=-1, vmax=1)


# Función para actualizar la animación
def update(frame):
    im.set_data(matrices[frame])
    ax.set_title(f"Iteración {(frame + 1) * 10}")
    return (im,)


# Crear animación
ani = animation.FuncAnimation(
    fig, update, frames=num_iteraciones, interval=1, blit=False, repeat=False
)

plt.show()
