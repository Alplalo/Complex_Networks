# ---------- XARXES COMPLEXES --------------
# --------------- S I S  -------------------
# ----------- ALBERT PLAZAS ----------------

############# Librerias ################

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from numba import jit
import sys
import os
import time

############# Funciones ################

def gillespie_SIS_stochastic(G, lam, sigma, initial_infected, max_time):
    nodes = list(G.nodes()) # Nodos de la red
    N = len(nodes) # Número de nodos
    infected = set(initial_infected) # Nodos infectados
    susceptible = set(nodes) - infected # Nodos susceptibles
    
    times = [0] 
    prevalence = [len(infected) / N] # Prevalencia inicial
    
    t = 0
    next_print_time = max_time * 0.1
    contador = 0
    while t < max_time and infected:
        Eact = sum(1 for i in infected for j in G.neighbors(i) if j in susceptible) # Número de enlaces activos
        nI = len(infected) # Número de infectados
        
        if nI + lam * Eact == 0:
            break
        
        p_recovery = nI / (nI + lam * Eact) # Probabilidad de recuperación
        p_infection = 1 - p_recovery # Probabilidad de infección
        
        rate = nI + lam * Eact # Tasa de eventos
        tau = np.random.exponential(1 / rate) # Tiempo hasta el próximo evento
        t += tau # Avanzar el tiempo

        if t >= next_print_time:
            contador += 1
            print(f"Tiempo: {t:.2f} ({contador}0% calculado)")
            next_print_time += max_time * 0.1
        
        if np.random.rand() < p_recovery:
            node_to_recover = np.random.choice(list(infected)) # Elegir un nodo para recuperar
            infected.remove(node_to_recover) # Remover de infectados
            susceptible.add(node_to_recover) # Agregar a susceptibles
        else:
            active_links = [(i, j) for i in infected for j in G.neighbors(i) if j in susceptible] # Enlaces activos
            if active_links:
                node_to_infect = active_links[np.random.randint(len(active_links))][1] # Elegir un nodo para infectar
                infected.add(node_to_infect) # Agregar a infectados
                susceptible.remove(node_to_infect) # Remover de susceptibles
        
        times.append(t) # Guardar el tiempo
        prevalence.append(len(infected) / N) # Guardar la prevalencia
    
    return times, prevalence


############# Inputs ################

# Crear una red aleatoria
G = nx.erdos_renyi_graph(200, 0.1)

filename = sys.argv[1] # Guardar el nombre del archivo de datos

# Leer una red real
G = nx.read_edgelist(filename, create_using=nx.Graph(), nodetype=int)
G = nx.convert_node_labels_to_integers(G, first_label=0)

print('Número de nodos:', G.number_of_nodes())
print('Número de enlaces:', G.number_of_edges())

# Parámetros del modelo
lambdas = [0.01, 0.1, 0.5, 1, 2, 3,4] # Tasa de infección
sigma = 1  # Tasa de recuperación
initial_infected = np.random.choice(G.nodes(), size=50, replace=False) # Nodos infectados iniciales
max_time = 15 # Tiempo máximo de simulación

# Ejecutar simulaciones para diferentes valores de beta
results = [] # Guardar los resultados de las simulaciones
lamb_prevalence = [] # Guardar la prevalencia final en función de lambda
print('\n')
print('###################################')
print('##### Inicio de simulaciones ######')
print('###################################')
print('\n')
tiempo_inicial = time.time()
############# Simulaciones ################

for lam in lambdas:
    times, prevalence = gillespie_SIS_stochastic(G, lam, sigma, initial_infected, max_time) # Simulación
    results.append((lam, times, prevalence)) # Guardar los resultados
    # print(len(prevalence))
    last_prevalence = prevalence[-20:] # Prevalencia final
    last_prevalence = sum(last_prevalence) / len(last_prevalence) # Promedio de la prevalencia final
    # Guardar en 2D vector lambda, prevalencia final
    lamb_prevalence.append([lam, last_prevalence]) # Guardar la prevalencia final en función de lambda
    print(f'Lambda= {lam:.4f} acabado')
    print('-----------------------------------')
    
tiempo_final = time.time()

print('tiempo de ejecución: ', tiempo_final - tiempo_inicial)

############# Plots ################

filename = filename.split('/')[-1].split('.')[0]
os.makedirs(f'plots/SIS/{filename}', exist_ok=True)

# Graficar los resultados
plt.figure(figsize=(10,6))
for lam, times, prevalence in results:
    plt.plot(times, prevalence, label=r'$\lambda= {:.2f}$'.format(lam))
plt.xlabel('t')
plt.ylabel(r'$\rho$')
plt.legend()
plt.savefig(f'plots/SIS/{filename}/dinamica_SIS.png')
# plt.show()

# Graficar la prevalencia final en función de lambda
lamb_prevalence = np.array(lamb_prevalence)
plt.figure(figsize=(10,6))
plt.plot(lamb_prevalence[:,0], lamb_prevalence[:,1], 'o-', color='black')
plt.xlabel(r'$\lambda$')
plt.ylabel(r'$\rho$')
plt.savefig(f'plots/SIS/{filename}/lambdas.png')
# plt.show()