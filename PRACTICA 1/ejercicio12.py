#IMPORTANTE LECTURA/ESCRITURA FICHEROS

import os

def copiar(origen, destino):

    if origen is None or destino is None:
        raise ValueError("Algún nombre es None")

    if not isinstance(origen, str) or not isinstance(destino, str):
        raise TypeError("Los nombres deben ser string")

    if not os.path.exists(origen):
        raise FileNotFoundError("El fichero origen no existe")
    
    #leemos primero el contenido del origen
    with open(origen, "r") as f1:
        texto = f1.read()

    #escribimos ahora el contenido en el destino
    with open(destino, "w") as f2:
        f2.write(texto)
    
