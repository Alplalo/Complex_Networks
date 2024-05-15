INPUT_FILE = networks/Gowalla_edges.txt
INPUT_FILE_NEW = $(INPUT_FILE:.txt=_new.txt)
FFLAGS = -Wall -Wextra -O2

$(INPUT_FILE_NEW): $(INPUT_FILE) retocar.py
	python3 retocar.py $(INPUT_FILE)

run:
	./ejecutable $(INPUT_FILE_NEW)

xfor: $(INPUT_FILE_NEW) xarxes_for.f90
	gfortran $(FFLAGS) -o ejecutable xarxes_for.f90
	./ejecutable $(INPUT_FILE_NEW)

xpy: $(INPUT_FILE_NEW) xarxes.py
	python3 xarxes.py $(INPUT_FILE_NEW)

plot: script.gp
	gnuplot script.gp

cleanw:
	del /F /Q ejecutable.exe *.dat 

clean:
	rm -f ejecutable *.dat

help:
	@echo "xfor - Ejecuta 'python3 retocar.py' en $(INPUT_FILE), luego compila 'xarxes_for.f90' con gfortran y ejecuta el archivo resultante en $(INPUT_FILE_NEW)"
	@echo "xpy - Ejecuta 'python3 retocar.py' en $(INPUT_FILE) y luego 'python3 xarxes.py' en $(INPUT_FILE_NEW)"
	@echo "cleanw - Elimina el archivo ejecutable y $(INPUT_FILE_NEW) en Windows"
	@echo "clean - Elimina el archivo ejecutable y $(INPUT_FILE_NEW) en Linux"
