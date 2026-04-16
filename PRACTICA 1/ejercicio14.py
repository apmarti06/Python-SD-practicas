#ejercicio 14, listamos todos los ficheros del directorio actual   
import os

total = 0

for ruta, directorios, ficheros in os.walk("."):
    for fichero in ficheros:
        path = os.path.join(ruta, fichero)
        tamano = os.path.getsize(path)

        print(path, tamano, "bytes")

        total += tamano

print("Tamaño total:", total, "bytes")

