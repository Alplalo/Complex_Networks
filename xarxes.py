# ---------- XARXES COMPLEXES --------------
# ------------ ASSIGNMENTS -----------------
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

    # Añadir el ultimo k_i 
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
        P_K_cum[i] = sum(P_K[:i+1]) # Calcular la suma acumulada de P_K
        P_K_cum[i] = 1 - P_K_cum[i]
    return P_K_cum

# Calcular Average nearest neighbor degree, suma de vecinos de todos los nodos con k degrees
def average_nearest_neighbor_degree(vecinos, D):
    sumas = {}
    conteos = {}
    for i in range(len(D)): # Recorrer todos los nodos
        grado = D[i] # Grado del nodo i
        if grado not in sumas: # Si el grado no esta en el diccionario
            sumas[grado] = 0
            conteos[grado] = 0
        sumas[grado] += sum([D[j] for j in vecinos[i]])/grado # Sumar los grados de los vecinos de i
        conteos[grado] += 1
    k_nn = {grado: suma / conteos[grado] for grado, suma in sumas.items()} # Calcular el average nearest neighbor degree
    return k_nn

# Calcula el average clustering coefficient for each node
def clustering_coefficient(vecinos, D):
    C = {} # Diccionario para guardar el clustering coefficient de cada nodo
    triangles = [0]*len(D) # Lista para guardar el numero de triangulos de cada nodo
    for i in range(len(D)): # Recorrer todos los nodos
        vecinos_i = vecinos[i] # Vecinos del nodo i
        vecinos_i = [v for v in vecinos_i if v > i] # Solo vecinos con indice mayor que i para no contar dos veces el mismo triangulo
        if len(vecinos_i) < 2: # Si el nodo no tiene suficientes vecinos para formar un triangulo
            C[i] = 0
        else:
            triangles[i] = 0 # Contador de triangulos
            for j in vecinos_i:
                for k in vecinos_i:
                    if k in vecinos[j]: # Si j y k son vecinos
                        triangles[i] += 1 
            C[i] = 2*triangles[i]/(len(vecinos_i)*(len(vecinos_i)-1)) # Calcular el clustering coefficient
    return C, triangles

def clustering_coefficient_per_degree(C, D):
    C_k = {}
    for i in range(len(D)):
        if D[i] not in C_k:
            C_k[D[i]] = 0
        C_k[D[i]] += C[i]
    for k in C_k:
        C_k[k] /= D.count(k)
    return C_k

def average_clustering_coefficient(C):
    return sum(C.values())/(len(C))

def diferentes_k(D):
    k = set(D) # Quitar repetidos
    k = list(k)
    k.sort() # Ordenar k
    return k



############ Programa principal #############

V, D = contar(filename)
vecinos = crear_vecinos(V, D)
P_K = deggree_distribution(D)
P_K_cum = cumulative_degree_distribution(P_K)
k_nn = average_nearest_neighbor_degree(vecinos, D)
C,triangles = clustering_coefficient(vecinos, D)
C_k = clustering_coefficient_per_degree(C, D)
C_avg = average_clustering_coefficient(C)


# Print de los resultados
print('Triangulos: ',np.sum(triangles)/2)
print('Average clustering coefficient: {:.4f}'.format(C_avg/2))


# Nombre carpeta datos y plots

filename = filename.split(".")[0]
filename = filename.split("/")[1]


############ Outputs ################

open_file = open(f'outputs/{filename}/degree_distribution.dat', 'w')
for i in range(len(P_K)):
    open_file.write('{} {}\n'.format(i, P_K[i]))
open_file.close()

open_file = open(f'outputs/{filename}/cumulative_degree_distribution.dat', 'w')
for i in range(len(P_K_cum)-1):
    open_file.write('{} {}\n'.format(i, P_K_cum[i]))
open_file.close()

open_file = open(f'outputs/{filename}/average_nearest_neighbor_degree.dat', 'w')
for k, nn in k_nn.items():
    open_file.write('{} {}\n'.format(k, nn))
open_file.close()

open_file = open(f'outputs/{filename}/clustering_coefficient.dat', 'w')
for i, c in C.items():
    open_file.write('{} {}\n'.format(i, c))
open_file.close()



############# Plots ################

# Plot log P_K vs log k
plt.plot(range(len(P_K)-1), P_K[0:-1], 'o', color='black')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('k')
plt.ylabel('P(k)')
plt.title('Degree distribution')
plt.savefig(f'plots/{filename}/degree_distribution.png')
plt.close()

# Plot log P_K_cum vs log k
plt.plot(range(len(P_K_cum)-1), P_K_cum[0:-1], 'o', color='black')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('k')
plt.ylabel('P_cum(k)')
plt.title('Cumulative degree distribution')
plt.savefig(f'plots/{filename}/cumulative_degree_distribution.png')
plt.close()

# Plot k_nn vs k
plt.plot(k_nn.keys(), k_nn.values(), 'o', color='black')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('k')
plt.ylabel('k_nn')
plt.title('Average nearest neighbor degree')
plt.savefig(f'plots/{filename}/average_nearest_neighbor_degree.png')
plt.close()

# Plot C_k vs k
plt.plot(C_k.keys(), C_k.values(), 'o', color='black')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('k')
plt.ylabel('C(k)')
plt.title('Clustering coefficient per degree')
plt.savefig(f'plots/{filename}/clustering_coefficient.png')
plt.close()









    

