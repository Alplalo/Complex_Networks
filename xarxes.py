# ---------- XARXES COMPLEXES --------------
# ------------ ASSIGNMENT 1 ----------------
# ----------- ALBERT PLAZAS ----------------

import sys

filename = sys.argv[1] # Guardar el nombre del archivo de datos

def contar(filename):

    # Leer archivo de datos
    open_file = open(filename, "r")
    lines = open_file.readlines()
    open_file.close()

    print('Numero de lineas:', len(lines)) # Numero de lineas en el archivo

    # Dividir cada linea en columnas y guardar la primera columna
    first_column = [line.split()[0] for line in lines] # Guardar la primera columna de cada linea en una lista
    vecinos = [line.split()[1] for line in lines]
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


# Programa principal
V, D = contar(filename)
    

