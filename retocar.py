############## Xarxes Complexes ################
###### Programa para generalizar el input ######
############### Albert Plazas ##################

import sys

filename = sys.argv[1] # Guardar el nombre del archivo de datos

openfile = open(filename, 'r')
lines = openfile.readlines()
openfile.close()

# Quitar lineas sin datos
lines = [line for line in lines if line.strip() != ''] # Quitar lineas vacias, si la linea no esta vacia, añadirla a la lista

# Quitar lineas donde no hay columna 2
lines = [line for line in lines if len(line.split()) > 1] # Si la linea tiene mas de una columna, añadirla a la lista

# Quitar enlaces a si mismo
lines = [line for line in lines if line.split()[0] != line.split()[1]] # Si la columna 1 es diferente a la columna 2, añadirla a la lista

# Quitar enlaces repetidos
lines = list(set(lines)) # Convertir la lista en un set para quitar duplicados y volver a convertir en lista

# Ordenar enlaces por columna 1 con su respectiva columna 2
lines = sorted(lines, key=lambda x: (int(x.split()[0]), int(x.split()[1]))) # Ordenar la lista por la columna 1 y luego por la columna 2

# Guardo lo que hay delante del . en el nombre del archivo para el nuevo archivo
filename = filename.split('.')[0] # Guardar el nombre del archivo sin la extension

# Escritura de archivo
openfile = open(f'{filename}_new.txt', 'w')
openfile.writelines(lines)
openfile.close()




