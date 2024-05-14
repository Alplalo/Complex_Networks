# ---------- XARXES COMPLEXES --------------
# ------------ ASSIGNMENT 1 ----------------
# ----------- ALBERT PLAZAS ----------------

############# Librerias ################

import sys
import numpy as np
import matplotlib.pyplot as plt

############# Argumentos ################

filename = sys.argv[1] # Guardar el nombre del archivo de datos


############# Funciones ################

# Contar el numero de nodos, aristas y grado medio
def contar(filename):

    # Leer archivo de datos
    open_file = open(filename, "r")
    lines = open_file.readlines()
    open_file.close()

    print('Numero de lineas:', len(lines)) # Numero de lineas en el archivo

    # Dividir cada linea en columnas y guardar la primera columna
    first_column = [line.split()[0] for line in lines] # Guardar la primera columna de cada linea en una lista
    vecinos = [int(line.split()[1]) for line in lines]
    # Inicializar k's
    k_i = [] # Lista para guardar la suma de k de cada nodo
    k_n = 1

    # Bucle crear vector k_i
    for i in range(len(first_column) - 1): # Recorrer todas las columnas menos la ultima, añadir su k_i a la lista si es diferente al siguiente
        if first_column[i] == first_column[i+1]:
            k_n = k_n + 1
        else:
            k_i.append(k_n)
            k_n = 1

    # Verificar el ultimo elemento
    if first_column[-1] != first_column[-2]: # Si el ultimo elemento es diferente al penultimo, añadir su k_i a la lista 
        k_i.append(k_n)

    # Print de los resultados
    print('Nodes: ',len(k_i)) # Numero de nodos
    print('E :', 0.5*sum(k_i)) # Numero de aristas
    print('<k> : {:.4f}'.format(sum(k_i)/len(k_i))) # Grado medio

    return vecinos, k_i

# Dicción de vecinos, donde la clave es el nodo y el valor es una lista con los vecinos
def crear_vecinos(V, D):
    vecinos = {}
    start = 0
    for i in range(len(D)):
        vecinos[i] = V[start:start+D[i]]
        start += D[i]
        # print(i)
    return vecinos

# Calcular degree distribution
def deggree_distribution(D):
    P_K = np.zeros(max(D)+1)
    for i in D:
        P_K[i] += 1

    P_K = P_K/sum(P_K)
    return P_K

# Calcular Cumulative degree distribution
def cumulative_degree_distribution(P_K):
    P_K_cum = np.zeros(len(P_K))
    for i in range(len(P_K)):
        P_K_cum[i] = sum(P_K[:i+1])
        P_K_cum[i] = 1 - P_K_cum[i]
    return P_K_cum

# Calcular Average nearest neighbor degree
def average_nearest_neighbor_degree(V, D):
    k_nn = np.zeros(len(D))
    for i in range(len(D)):
        k_nn[i] = np.mean([D[j] for j in V[i]])
    return k_nn



############ Programa principal #############

V, D = contar(filename)
vecinos = crear_vecinos(V, D)
P_K = deggree_distribution(D)
P_K_cum = cumulative_degree_distribution(P_K)
k_nn = average_nearest_neighbor_degree(vecinos, D)

############ Outputs ################

open_file = open('degree_distribution.dat', 'w')
for i in range(len(P_K)):
    open_file.write('{} {}\n'.format(i, P_K[i]))
open_file.close()

open_file = open('cumulative_degree_distribution.dat', 'w')
for i in range(len(P_K_cum)-1):
    open_file.write('{} {}\n'.format(i, P_K_cum[i]))
open_file.close()





############# Plots ################

# Plot log P_K vs log k
plt.plot(range(len(P_K)), P_K, '-', color='black')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('k')
plt.ylabel('P(k)')
plt.title('Degree distribution')
plt.savefig('degree_distribution.png')
plt.close()

# Plot log P_K_cum vs log k
plt.plot(range(len(P_K_cum)), P_K_cum, '-', color='black')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('k')
plt.ylabel('P_cum(k)')
plt.title('Cumulative degree distribution')
plt.savefig('cumulative_degree_distribution.png')
plt.close()

# Plot k_nn vs k
plt.plot(D, k_nn, '.', color='black')
plt.xlabel('k')
plt.ylabel('k_nn')
plt.title('Average nearest neighbor degree')
plt.savefig('average_nearest_neighbor_degree.png')
plt.close()






    

