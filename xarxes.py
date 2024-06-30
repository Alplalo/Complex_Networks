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
    max_val = max(k_nn.values())
    k_nn_normalizado = {grado: valor / max_val for grado, valor in k_nn.items()}

    return k_nn_normalizado


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
    
    # Encontrar el valor máximo
    max_value = max(C_k.values())
    
    # Normalizar los valores por el valor máximo
    for k in C_k:
        if C_k[k] != 0:
            C_k[k] /= max_value
        else:
            C_k[k] = 0
    return C_k


if __name__ == "__main__":
############ Programa principal #############

    V, D = contar(filename)
    vecinos = crear_vecinos(V, D)
    P_K_norm, P_K = deggree_distribution(D)
    P_K_cum = cumulative_degree_distribution(P_K)
    k_nn = average_nearest_neighbor_degree(vecinos, D)
    k_nn = dict(sorted(k_nn.items())) # Ordenar claves de k_nn de menor a mayor
    C,avg_C = clustering_coefficient(vecinos, D)
    C_k = clustering_coefficient_per_degree(C, D)
    C_k = dict(sorted(C_k.items())) # Ordenar claves de C_k de menor a mayor
    # Eliminar los de C_k igual a 0
    C_k = {k: v for k, v in C_k.items() if v != 0}


    # Print de los resultados
    print('Degree max: ',max(D))
    print('Degree min: ',min(D))
    print('Average clustering coefficient: {:.6f}'.format(avg_C))
    print('Clustering coefficient max: ',max(C.values()))
    print('Clustering coefficient min: ',min(C.values()))


    # Nombre carpeta datos y plots

    filename = filename.split(".")[0]
    filename = filename.split("/")[1]


    ############ Outputs ################

    # open_file = open(f'outputs/{filename}/degree_distribution.dat', 'w')
    # for i in range(len(P_K)):
    #     open_file.write('{} {}\n'.format(i, P_K[i]))
    # open_file.close()

    # open_file = open(f'outputs/{filename}/cumulative_degree_distribution.dat', 'w')
    # for i in range(len(P_K_cum)-1):
    #     open_file.write('{} {}\n'.format(i, P_K_cum[i]))
    # open_file.close()

    # open_file = open(f'outputs/{filename}/average_nearest_neighbor_degree.dat', 'w')
    # for k, nn in k_nn.items():
    #     open_file.write('{} {}\n'.format(k, nn))
    # open_file.close()

    # open_file = open(f'outputs/{filename}/clustering_coefficient.dat', 'w')
    # for i, c in C.items():
    #     open_file.write('{} {}\n'.format(i, c))
    # open_file.close()



    ############# Plots ################

    # Plot log P_K vs log k
    plt.plot(range(len(P_K_norm)-1), P_K_norm[0:-1], 'o', color='black')
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
    plt.plot(k_nn.keys(), k_nn.values(), '-', color='black')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('k')
    plt.ylabel('k_nn')
    plt.title('Average nearest neighbor degree')
    plt.savefig(f'plots/{filename}/average_nearest_neighbor_degree.png')
    plt.close()

    # Plot C_k vs k
    plt.plot(C_k.keys(), C_k.values(), '-', color='black')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('k')
    plt.ylabel('C(k)')
    plt.title('Clustering coefficient per degree')
    plt.savefig(f'plots/{filename}/clustering_coefficient.png')
    plt.close()









    

