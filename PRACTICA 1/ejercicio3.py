import shutil
import filecmp

origen = "archivo.txt"
copia = "archivo_copia.txt"

# Crear copia del fichero
shutil.copy(origen, copia)

# Comprobar si son iguales
if filecmp.cmp(origen, copia, shallow=False):
    print("Los archivos son iguales")
else:
    print("Los archivos son diferentes")
