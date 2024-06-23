INPUT = dolphins.txt
INPUT_FILE = networks/$(INPUT)
INPUT_FILE_NEW = $(INPUT_FILE:.txt=_new.txt)
DIR = $(INPUT:.txt=_new)
DIR_CM = CMs_analisis
FFLAGS = -Wall -Wextra -O2

$(INPUT_FILE_NEW): $(INPUT_FILE) retocar.py
	python3 retocar.py $(INPUT_FILE)

run:
	./ejecutable $(INPUT_FILE_NEW)

xfor: $(INPUT_FILE_NEW) xarxes_for.f90
	gfortran $(FFLAGS) -o ejecutable xarxes_for.f90
	./ejecutable $(INPUT_FILE_NEW)

xpy: $(INPUT_FILE_NEW) xarxes.py
	cmd /C if not exist plots\\$(DIR) md plots\\$(DIR)
	cmd /C if not exist outputs\\$(DIR) md outputs\\$(DIR)
	python3 xarxes.py $(INPUT_FILE_NEW)

a5: $(INPUT_FILE_NEW) crear_CMs.py
	cmd /C if exist CMs rmdir /S /Q CMs
	python3 crear_CMs.py $(INPUT_FILE_NEW)

aa5:
	cmd /C if not exist plots\\$(DIR_CM) md plots\\$(DIR_CM)
	cmd /C if not exist outputs\\$(DIR_CM) md outputs\\$(DIR_CM)
	python3 analizar_CMs.py



plot: script.gp
	gnuplot script.gp

clean5:
	cmd /C if exist CMs rmdir /S /Q CMs

cleanw:
	del /F /Q ejecutable.exe *.dat 

clean:
	rm -f ejecutable *.dat

help:
	@echo "xfor - Ejecuta 'python3 retocar.py' en $(INPUT_FILE), luego compila 'xarxes_for.f90' con gfortran y ejecuta el archivo resultante en $(INPUT_FILE_NEW)"
	@echo "xpy - Ejecuta 'python3 retocar.py' en $(INPUT_FILE) y luego 'python3 xarxes.py' en $(INPUT_FILE_NEW)"
	@echo "cleanw - Elimina el archivo ejecutable y $(INPUT_FILE_NEW) en Windows"
	@echo "clean - Elimina el archivo ejecutable y $(INPUT_FILE_NEW) en Linux"
