import sys
import os
import numpy as np
import time

# ------------------ Argumentos ------------------
filename = sys.argv[1]

# ------------------ Funciones ------------------

def assignment_5(intentos,filename=sys.argv[1]):
    filename = sys.argv[1] # Guardar el nombre del archivo de datos

    k_i = contar(filename)


    # Create a list of nodes
    nodes = []
    for i in range(len(k_i)):
        for j in range(k_i[i]):
            nodes.append(i)

    # print(len(nodes))

    back_nodes = nodes.copy()
    edges = set()

    while len(nodes) > 1:
        i = np.random.randint(0, len(nodes))
        j = np.random.randint(0, len(nodes))
        
        if i != j:
            edge = frozenset([nodes[i], nodes[j]])
            if ((len(nodes) in {2, 4} and nodes[i] == nodes[j]) or 
                (len(nodes) in {2, 4} and edge in edges)):
                nodes = back_nodes.copy()
                edges.clear()
                continue
            
            if edge not in edges and nodes[i] != nodes[j]:
                edges.add(edge)
                nodes.pop(max(i, j))
                nodes.pop(min(i, j))
                # print(len(nodes))

    edges = [list(edge) for edge in edges]

    # Comprobar si hay nodos repetidos
    print('enlaces antes',len(edges))
    # set_edges = set(edges)
    # edges = list(set_edges)
    # print(type(edges))
    
    # Escribir archivo
    write_file = open("assignment_5.txt", "w")
    for edge in edges:
        write_file.write(str(edge[0]) + "\t" + str(edge[1]) + "\n")
    write_file.close()

    ####### Copia de programa RETOCAR #######
    # ------------------ Argumentos ------------------

    filename = 'assignment_5.txt'

    # ------------------ Input ------------------
    openfile = open(filename, 'r')
    lines = openfile.readlines()
    openfile.close()

    # ------------------ Retocar ------------------

    # Quitar lineas sin datos
    lines = [line for line in lines if line.strip() != ''] # Quitar lineas vacias, si la linea no esta vacia, añadirla a la lista

    # Quitar lineas donde no hay columna 2
    lines = [line for line in lines if len(line.split()) > 1] # Si la linea tiene mas de una columna, añadirla a la lista

    # Quitar enlaces a si mismo
    lines = [line for line in lines if line.split()[0] != line.split()[1]] # Si la columna 1 es diferente a la columna 2, añadirla a la lista

    # Quitar enlaces repetidos
    lines = list(set(lines)) # Convertir la lista en un set para quitar duplicados y volver a convertir en lista

    # Verificar que para cada enlace en la lista, su enlace inverso también está presente, y que no hay duplicados.
    lines_set = set(lines)
    new_lines = []
    for line in lines:
        split_line = line.split()
        link = f'{split_line[0]}\t{split_line[1]}\n'
        reverse_link = f'{split_line[1]}\t{split_line[0]}\n'
        if link in lines_set:
            new_lines.append(link)
            if reverse_link not in lines_set:
                new_lines.append(reverse_link)
                lines_set.add(reverse_link)
        elif link not in lines_set:
            new_lines.append(link)
            lines_set.add(link)
    lines = new_lines

    # Ordenar enlaces por columna 1 con su respectiva columna 2
    lines = sorted(lines, key=lambda x: (int(x.split()[0]), int(x.split()[1]))) # Ordenar la lista por la columna 1 y luego por la columna 2

    # Restar a cada nodo el primer calor de la columna 1 para que empiecen en 0, en las columnas 1 y 2
    lines = [f'{int(line.split()[0])-int(lines[0].split()[0])}\t{int(line.split()[1])-int(lines[0].split()[0])}\n' for line in lines]

    # ------------------ Output ------------------

    # Guardo lo que hay delante del . en el nombre del archivo para el nuevo archivo
    filename = filename.split('.')[0] # Guardar el nombre del archivo sin la extension
    print('enlaces despues',len(lines))
    # Escritura de archivo
    openfile = open(f'{filename}_new_{str(intentos).zfill(4)}.txt', 'w')
    openfile.writelines(lines)
    openfile.close()

    # Si no existe la carpeta assignment_5, la crea
    if not os.path.exists('CMs'):
        os.makedirs('CMs')

    # Mover archivo a carpeta assignment_5
    os.rename(f'{filename}_new_{str(intentos).zfill(4)}.txt', f'CMs/CMnet_{str(intentos).zfill(4)}.txt')
    os.remove('assignment_5.txt')

def contar(filename):

    # Leer archivo de datos
    open_file = open(filename, "r")
    lines = open_file.readlines()
    open_file.close()

    # print('Numero de lineas:', len(lines)) # Numero de lineas en el archivo

    # Dividir cada linea en columnas y guardar la primera columna
    first_column = [line.split()[0] for line in lines] # Guardar la primera columna de cada linea en una lista

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

    # # Print de los resultados
    # print('Nodes: ',len(k_i)) # Numero de nodos
    # print('E :', 0.5*sum(k_i)) # Numero de aristas
    # print('<k> : {:.4f}'.format(sum(k_i)/len(k_i))) # Grado medio

    return k_i



## Ejecutar el programa


inicio = time.time()

intentos = 5 # Numero de CM a realizar

for i in range(intentos):
    assignment_5(i+1)
    print(f'CM {i+1}/{intentos} completada.')
    
final = time.time()

print('Tiempo de ejecucion:',final-inicio)