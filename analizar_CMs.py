import sys
import os
import numpy as np
import matplotlib.pyplot as plt



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

    P_K = P_K/sum(P_K)  # Normalización inicial por la suma total para obtener probabilidades
    
    # Encontrar el valor máximo
    max_value = max(P_K)
    
    # Normalizar los valores por el valor máximo
    if max_value > 0:
        P_K_norm = P_K / max_value
    
    return P_K_norm, P_K

# Calcular Cumulative degree distribution
def cumulative_degree_distribution(P_K):
    P_K_cum = np.zeros(len(P_K))
    for i in range(len(P_K)):
        P_K_cum[i] = sum(P_K[:i+1])  # Calcular la suma acumulada de P_K
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


def clustering_coefficient(vecinos, D):

    # Inicializar diccionario de clustering y variables para contar triangulos
    C = {}
    total_tri = 0
    cerrados_tri = 0
    
    # Calcular el clustering coefficient de cada nodo
    for i in range(len(D)):
        vecinos_i = vecinos[i] # Vecinos del nodo i
        if len(vecinos_i) < 2: # Si el nodo i no tiene vecinos para formar triangulos
            C[i] = 0
            continue
        
        contar_pos_tri = 0 # Contar posibles triangulos de un nodo
        contar_triangulos = 0 # Contar triangulos cerrados de un nodo
        
        for j in range(len(vecinos_i)): # Recorrer nodos vecinos
            for k in range(j + 1, len(vecinos_i)):
                contar_pos_tri += 1 # Contar posibles triangulos
                if vecinos_i[k] in vecinos[vecinos_i[j]]: # Si hay un nodo k en los vecinos de j
                    contar_triangulos += 1 # Contar triangulos cerrados
        
        C[i] = contar_triangulos / contar_pos_tri if contar_pos_tri > 0 else 0
        total_tri += contar_pos_tri # Sumar de posibles triangulos de todos los nodos
        cerrados_tri += contar_triangulos # Sumar triangulos cerrados de todos los nodos
    
    # Calcular el clustering coefficient medio, triángulos cerrados entre todos los triángulos abiertos y cerrados
    avg_C = cerrados_tri / total_tri if total_tri > 0 else 0
    print('Triangulos: ',cerrados_tri/3)
    return C, avg_C


def clustering_coefficient_per_degree(C, D):
    C_k = {}
    for i in range(len(D)):
        if D[i] not in C_k:
            C_k[D[i]] = 0
        C_k[D[i]] += C[i]
    for k in C_k:
        C_k[k] /= D.count(k)
    
    return C_k



############# Inputs ################

# Entrar al directorio CMs
os.chdir('CMs')

# Listar los archivos en el directorio
files = os.listdir()
os.chdir('..')
# Calcular el numero de redes a analizar
num_net = len(files)

k_nn_sum = {}
C_k_sum = {}

for filename in files:

    if __name__ == "__main__":
    ############ Programa principal #############
        os.chdir('CMs')
        V, D = contar(filename)
        os.chdir('..')
        vecinos = crear_vecinos(V, D)
        P_K_norm, P_K = deggree_distribution(D)
        P_K_cum = cumulative_degree_distribution(P_K)
        k_nn = average_nearest_neighbor_degree(vecinos, D)

        C,avg_C = clustering_coefficient(vecinos, D)
        C_k = clustering_coefficient_per_degree(C, D)
        
        # Sumar k_nn de cada red para calcular el promedio
        for k, nn in k_nn.items():
            if k in k_nn_sum:
                k_nn_sum[k] += nn
            else:
                k_nn_sum[k] = nn
        
        # Sumar C_k de cada red para calcular el promedio
        for k, c in C_k.items():
            if k in C_k_sum:
                C_k_sum[k] += c
            else:
                C_k_sum[k] = c

        
    
        # Print de los resultados
        print('Average clustering coefficient: {:.4f}'.format(avg_C))


        # Nombre carpeta datos y plots

        filename = filename.split(".")[0]
        filename = filename.split("_")[1]

        print('-------------------------------------------------------------------------------------------------')
        print('-------------------------------------------------------------------------------------------------')


# Calcular el promedio de k_nn y C_k
# Los valores de k_nn y C_K se dividen entre el numero de redes
k_nn = {k: v / num_net for k, v in k_nn_sum.items()}
C_k = {k: v / num_net for k, v in C_k_sum.items()}

k_nn = dict(sorted(k_nn.items())) # Ordenar claves de k_nn de menor a mayor
C_k = dict(sorted(C_k.items())) # Ordenar claves de C_k de menor a mayor


# Analizar red de referencia
print('Red de referencia')
os.chdir('networks')
filename = 'astro_new.txt'
V, D = contar(filename)
os.chdir('..')
vecinos = crear_vecinos(V, D)
P_K_norm, P_K = deggree_distribution(D)
P_K_cum = cumulative_degree_distribution(P_K)
k_nn_origen = average_nearest_neighbor_degree(vecinos, D)
C_origen,avg_C_origen = clustering_coefficient(vecinos, D)
C_k_origen = clustering_coefficient_per_degree(C_origen, D)
print('-------------------------------------------------------------------------------------------------')
print('-------------------------------------------------------------------------------------------------')
# Analizar 1 CM
print('1 CM')
os.chdir('CMs')
filename = 'CMnet_0001.txt'
V, D = contar(filename)
os.chdir('..')
vecinos = crear_vecinos(V, D)
P_K_norm, P_K = deggree_distribution(D)
P_K_cum = cumulative_degree_distribution(P_K)
k_nn_1CM = average_nearest_neighbor_degree(vecinos, D)
C_1CM,avg_C_1CM = clustering_coefficient(vecinos, D)
C_k_1CM = clustering_coefficient_per_degree(C_1CM, D)

# Ordenar diccionarios
k_nn = dict(sorted(k_nn.items())) # Ordenar claves de k_nn de menor a mayor
C_k = dict(sorted(C_k.items())) # Ordenar claves de C_k de menor a mayor

k_nn_origen = dict(sorted(k_nn_origen.items())) # Ordenar claves de k_nn de menor a mayor
C_k_origen = dict(sorted(C_k_origen.items())) # Ordenar claves de C_k de menor a mayor

k_nn_1CM = dict(sorted(k_nn_1CM.items())) # Ordenar claves de k_nn de menor a mayor
C_k_1CM = dict(sorted(C_k_1CM.items())) # Ordenar claves de C_k de menor a mayor

# Normalizar los valores de k_nn y C_k por el valor máximo de los 3 diccionarios
max_val = max(max(k_nn.values()), max(k_nn_origen.values()), max(k_nn_1CM.values()))
k_nn = {k: v / max_val for k, v in k_nn.items()}
k_nn_origen = {k: v / max_val for k, v in k_nn_origen.items()}
k_nn_1CM = {k: v / max_val for k, v in k_nn_1CM.items()}

max_val = max(max(C_k.values()), max(C_k_origen.values()), max(C_k_1CM.values()))
C_k = {k: v / max_val for k, v in C_k.items()}
C_k_origen = {k: v / max_val for k, v in C_k_origen.items()}
C_k_1CM = {k: v / max_val for k, v in C_k_1CM.items()}

# Eliminar los de C_k igual a 0
C_k = {k: v for k, v in C_k.items() if v != 0}
C_k_origen = {k: v for k, v in C_k_origen.items() if v != 0}
C_k_1CM = {k: v for k, v in C_k_1CM.items() if v != 0}

# Plot k_nn vs k
plt.plot(k_nn_origen.keys(), k_nn_origen.values(), '-', color='gray', label='Red de referencia')
plt.plot(k_nn_1CM.keys(), k_nn_1CM.values(), '+', color='lightgray', label='1 CM')
plt.plot(k_nn.keys(), k_nn.values(), '-', color='black', label='100 CMs')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('k')
plt.ylabel('k_nn')
plt.title('Average nearest neighbor degree')
plt.legend()
plt.savefig(f'plots/CMs_analisis/average_nearest_neighbor_degree.png')
plt.close()

# Plot C_k vs k
plt.plot(C_k_origen.keys(), C_k_origen.values(), '-', color='gray', label='Red de referencia')
plt.plot(C_k_1CM.keys(), C_k_1CM.values(), '+', color='lightgray', label='1 CM')
plt.plot(C_k.keys(), C_k.values(), '-', color='black', label='100 CMs')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('k')
plt.ylabel('C(k)')
plt.title('Clustering coefficient per degree')
plt.legend()
plt.savefig(f'plots/CMs_analisis/clustering_coefficient.png')
plt.close()