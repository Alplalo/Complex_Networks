########### Variables ###########

INPUT = powergrid.txt
INPUT_FILE = networks/$(INPUT)
INPUT_FILE_NEW = $(INPUT_FILE:.txt=_new.txt)
DIR = $(INPUT:.txt=_new)
DIR_CM = CMs_analisis
FFLAGS = -Wall -Wextra -O2


########### Reglas ###########

# Regla para retocar el archivo de entrada usando retocar.py
$(INPUT_FILE_NEW): $(INPUT_FILE) retocar.py
	python3 retocar.py $(INPUT_FILE)


# Ejecución con Python y preparación de directorios
xpy: $(INPUT_FILE_NEW) xarxes.py
	cmd /C if not exist plots\\$(DIR) md plots\\$(DIR)
	cmd /C if not exist outputs\\$(DIR) md outputs\\$(DIR)
	python3 xarxes.py $(INPUT_FILE_NEW)

# Preparación CMs
p5: $(INPUT_FILE_NEW) crear_CMs.py
	cmd /C if exist CMs rmdir /S /Q CMs
	python3 crear_CMs.py $(INPUT_FILE_NEW)

# Análisis CMs
a5:
	cmd /C if not exist plots\\$(DIR_CM) md plots\\$(DIR_CM)
	cmd /C if not exist outputs\\$(DIR_CM) md outputs\\$(DIR_CM)
	python3 analizar_CMs.py

# Ejecución del modelo SIS
sis: $(INPUT_FILE_NEW) SIS.py
	cmd /C if not exist plots\\SIS md plots\\SIS
	python3 SIS.py $(INPUT_FILE_NEW)

# Limpiar directorios CMs
clean5:
	cmd /C if exist CMs rmdir /S /Q CMs

# Explica que hace cada regla
help:
	@echo "xpy - Ejecuta 'xarxes.py' con el archivo de entrada procesado."
	@echo "p5 - Prepara el entorno eliminando el directorio CMs si existe y luego ejecuta 'crear_CMs.py' para preparar los CMs."
	@echo "a5 - Verifica y crea los directorios necesarios para los plots y outputs de los CMs, luego ejecuta 'analizar_CMs.py' para el análisis."
	@echo "sis - Verifica y crea el directorio necesario para los plots del modelo SIS, luego ejecuta 'SIS.py' con el archivo de entrada procesado."
	@echo "clean5 - Elimina el directorio CMs si existe, limpiando el entorno de trabajo."
