# XARXES COMPLEXES

Este proyecto se centra en el procesamiento y análisis de redes utilizando diferentes herramientas y lenguajes de programación. El flujo de trabajo está automatizado con un `Makefile` que permite realizar tareas comunes de compilación y ejecución de scripts.

## Estructura del Proyecto

- `xarxes.txt`: Archivo de entrada con datos de redes de delfines.
- `networks/`: Directorio que contiene el archivo de entrada.
- `retocar.py`: Script de Python para procesar el archivo de entrada.
- `xarxes_for.f90`: Código Fortran para análisis de redes.
- `xarxes.py`: Script de Python para análisis de redes.
- `assignment_5.py`: Script adicional de Python para análisis de redes.
- `script.gp`: Script de Gnuplot para visualización de datos.
- `plots/`: Directorio donde se guardan las gráficas generadas.
- `outputs/`: Directorio donde se guardan los resultados de salida.

## Uso del Makefile

El `Makefile` contiene varias reglas para automatizar tareas. A continuación se describen las principales reglas disponibles:

### Regla Principal

#### `$(INPUT_FILE_NEW)`

Esta regla ejecuta el script `retocar.py` para procesar el archivo de entrada `dolphins.txt` y generar un nuevo archivo con sufijo `_new.txt`.

```sh
make $(INPUT_FILE_NEW)
```

### Reglas de Ejecución

#### `run`

Ejecuta el archivo binario `ejecutable` con el archivo procesado `$(INPUT_FILE_NEW)`.

```sh
make run
```

#### `xfor`

Compila `xarxes_for.f90` usando `gfortran` con las banderas `$(FFLAGS)` y luego ejecuta el archivo resultante con `$(INPUT_FILE_NEW)`.

```sh
make xfor
```

#### `xpy`

Ejecuta los scripts de Python para crear directorios necesarios y procesar el archivo `$(INPUT_FILE_NEW)`.

```sh
make xpy
```

#### `a5`

Ejecuta el script `assignment_5.py` con el archivo procesado `$(INPUT_FILE_NEW)`.

```sh
make a5
```

### Regla de Visualización

#### `plot`

Genera gráficos usando `gnuplot` y el script `script.gp`.

```sh
make plot
```

### Reglas de Limpieza

#### `cleanw`

Elimina el archivo ejecutable y los archivos `.dat` en sistemas Windows.

```sh
make cleanw
```

#### `clean`

Elimina el archivo ejecutable y los archivos `.dat` en sistemas Linux.

```sh
make clean
```

### Ayuda

#### `help`

Muestra una descripción de las reglas disponibles en el `Makefile`.

```sh
make help
```

## Instrucciones Adicionales

- Asegúrate de tener instaladas todas las dependencias necesarias (Python, gfortran, gnuplot).
- Los directorios `plots/` y `outputs/` se crean automáticamente si no existen al ejecutar `xpy`.