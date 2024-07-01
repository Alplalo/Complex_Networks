import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys
import os

# Leer la red
filename = sys.argv[1] # Guardar el nombre del archivo de datos

G = nx.read_edgelist(filename)

filename = filename.split('/')[-1].split('.')[0]
os.makedirs(f'plots/kcore/{filename}', exist_ok=True)

# Calcular el core number de los nodos
core_number = nx.core_number(G)

# Obtener los diferentes niveles de k-core
k_levels = sorted(set(core_number.values()))

# Crear una posición para los nodos basada en capas concéntricas
pos = {}
layer_distance = 1.0  # Distancia entre capas
theta_offset = np.pi / 6  # Desplazamiento angular entre capas
for k in k_levels:
    nodes_in_k_core = [n for n, v in core_number.items() if v == k]
    angle_step = 2 * np.pi / len(nodes_in_k_core) if nodes_in_k_core else 2 * np.pi
    radius = layer_distance * (max(k_levels) - k + 1)
    for i, node in enumerate(nodes_in_k_core):
        theta = i * angle_step + theta_offset * k
        pos[node] = (radius * np.cos(theta), radius * np.sin(theta))

# Definir colores para cada capa de k-core
colors = plt.cm.rainbow(np.linspace(0, 1, len(k_levels)))

# Plot
plt.figure(figsize=(12, 12))

for i, k in enumerate(k_levels):
    nodes_in_k_core = [n for n, v in core_number.items() if v == k]
    nx.draw_networkx_nodes(G, pos, nodelist=nodes_in_k_core, node_size=20, label=f'k={k}', node_color=colors[i],edgecolors='black')

# nx.draw_networkx_edges(G, pos, alpha=0.5)
# nx.draw_networkx_labels(G, pos, font_size=8)

# plt.title('k-core de la red con capas')
# plt.legend()

plt.savefig(f'plots/kcore/{filename}/kcore.png')
