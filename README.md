# Redes Complejas

Este repositorio contiene herramientas y scripts para analizar cualquier tipo de red utilizando diferentes modelos y técnicas. A continuación, se describen los diferentes componentes del proyecto y cómo utilizarlos.

> [!WARNING]  
> Las redes que contienen nodos desconectados pueden dar lugar a problemas en el cálculo de las propiedades de la red.

## Introducción

El objetivo de este proyecto es proporcionar una serie de herramientas para la manipulación, análisis y simulación de redes. Utilizando scripts en Python y un Makefile para automatizar tareas, se puede procesar un archivo de red, preparar las redes con método Configurational Model (CMs), analizarlas y ejecutar un modelo SIS (Susceptible-Infected-Susceptible) sobre la red.

## Estructura del Proyecto

- **Makefile**: Archivo de automatización de tareas que facilita la ejecución de diferentes procesos.
- **Scripts en Python**: Varios scripts encargados de realizar tareas específicas sobre la red.
- **Directorios de Trabajo**:
  - `plots/`: Almacena los gráficos generados.
  - `outputs/`: Almacena las salidas generadas.
  - `networks/`: Contiene los archivos de red de entrada.

## Modelos y Scripts

### Variables en el Makefile

- **INPUT**: Nombre del archivo de red de entrada (por defecto `powergrid.txt`).
- **INPUT_FILE**: Ruta completa al archivo de entrada dentro del directorio `networks`.
- **INPUT_FILE_NEW**: Ruta al archivo de entrada procesado.
- **DIR**: Nombre del directorio basado en el archivo de entrada.
- **DIR_CM**: Directorio específico para el análisis de CMs.
- **FFLAGS**: Flags para el compilador (en caso de uso).

### Reglas en el Makefile

#### Retoque del Archivo de Entrada

```makefile
$(INPUT_FILE_NEW): $(INPUT_FILE) retocar.py
	python3 retocar.py $(INPUT_FILE)
```

Esta regla procesa el archivo de entrada utilizando `retocar.py` y genera un nuevo archivo procesado.

#### Ejecución con Python y Preparación de Directorios

```makefile
xpy: $(INPUT_FILE_NEW) xarxes.py
	cmd /C if not exist plots\\$(DIR) md plots\\$(DIR)
	cmd /C if not exist outputs\\$(DIR) md outputs\\$(DIR)
	python3 xarxes.py $(INPUT_FILE_NEW)
```

Ejecuta `xarxes.py` con el archivo de entrada procesado y crea los directorios necesarios para almacenar los gráficos y salidas.

#### Preparación de CMs

```makefile
p5: $(INPUT_FILE_NEW) crear_CMs.py
	cmd /C if exist CMs rmdir /S /Q CMs
	python3 crear_CMs.py $(INPUT_FILE_NEW)
```

Elimina el directorio `CMs` si existe y ejecuta `crear_CMs.py` para preparar las redes CM.

#### Análisis de CMs

```makefile
a5:
	cmd /C if not exist plots\\$(DIR_CM) md plots\\$(DIR_CM)
	cmd /C if not exist outputs\\$(DIR_CM) md outputs\\$(DIR_CM)
	python3 analizar_CMs.py
```

Verifica y crea los directorios necesarios para los gráficos y salidas de los CMs, luego ejecuta `analizar_CMs.py` para el análisis.

#### Ejecución del Modelo SIS

```makefile
sis: $(INPUT_FILE_NEW) SIS.py
	cmd /C if not exist plots\\SIS md plots\\SIS
	python3 SIS.py $(INPUT_FILE_NEW)
```

Verifica y crea el directorio necesario para los gráficos del modelo SIS y ejecuta `SIS.py` con el archivo de entrada procesado.

#### Limpieza de Directorios CMs

```makefile
clean5:
	cmd /C if exist CMs rmdir /S /Q CMs
```

Elimina el directorio `CMs` si existe, limpiando el entorno de trabajo.

#### Ayuda

```makefile
help:
	@echo "xpy - Ejecuta 'xarxes.py' con el archivo de entrada procesado."
	@echo "p5 - Prepara el entorno eliminando el directorio CMs si existe y luego ejecuta 'crear_CMs.py' para preparar los CMs."
	@echo "a5 - Verifica y crea los directorios necesarios para los plots y outputs de los CMs, luego ejecuta 'analizar_CMs.py' para el análisis."
	@echo "sis - Verifica y crea el directorio necesario para los plots del modelo SIS, luego ejecuta 'SIS.py' con el archivo de entrada procesado."
	@echo "clean5 - Elimina el directorio CMs si existe, limpiando el entorno de trabajo."
```

## Uso

Para ejecutar las diferentes tareas, utiliza las siguientes reglas del Makefile:

- **Procesar archivo de entrada**: `make $(INPUT_FILE_NEW)`
- **Ejecutar análisis con xarxes.py**: `make xpy`
- **Preparar redes CM**: `make p5`
- **Analizar redes CM**: `make a5`
- **Ejecutar modelo SIS**: `make sis`
- **Limpiar entorno**: `make clean5`
- **Mostrar ayuda**: `make help`

## Contribuciones

[Albert Plazas](https://github.com/Alplalo)