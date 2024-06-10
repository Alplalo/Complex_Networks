import sys
import os
import numpy as np
from xarxes import contar


intentos = 100


def assignment_5(intentos):
    filename = sys.argv[1] # Guardar el nombre del archivo de datos

    vecinos, k_i = contar(filename)


    # Create a list of nodes
    nodes = []
    for i in range(len(k_i)):
        for j in range(k_i[i]):
            nodes.append(i)

    print(len(nodes))

    # Create a list of edges
    edges = []
    while len(nodes) > 1:
        # Choose two nodes randomly
        i = np.random.randint(0, len(nodes))
        j = np.random.randint(0, len(nodes))
        # If the nodes are different and the edge does not exist
        if i != j and i < len(nodes) and j < len(nodes) and (nodes[i], nodes[j]) not in edges and (nodes[j], nodes[i]) not in edges and nodes[i] != nodes[j]:
            # Add the edge
            edges.append((nodes[i], nodes[j]))
            # Remove the nodes from the list
            nodes.pop(max(i, j))
            nodes.pop(min(i, j))

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

    # Eliminar el archivo de datos
    os.remove(filename)

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

    # Escritura de archivo
    openfile = open(f'{filename}_new_{str(intentos).zfill(4)}.txt', 'w')
    openfile.writelines(lines)
    openfile.close()

    # Si no existe la carpeta assignment_5, la crea
    if not os.path.exists('assignment_5'):
        os.makedirs('assignment_5')

    # Mover archivo a carpeta assignment_5
    os.rename(f'{filename}_new_{str(intentos).zfill(4)}.txt', f'assignment_5/{filename}_new_{str(intentos).zfill(4)}.txt')


for i in range(intentos):
    assignment_5(i+1)
    
