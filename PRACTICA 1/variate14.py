import os 

def listar(ruta):
    total = 0
    # Aquí solo lista todos los ficheros del directorio actual
    for f in os.listdir(ruta):
        path = os.path.join(ruta, f)

        if os.path.isfile(path):
            tamaño = os.path.getsize(path)
            print(path, tamaño, "bytes")
            total += tamaño

        elif os.path.isdir(path):
            total += listar(path)   

    return total

total = listar(".")
print("EL tamaño obtenido es de:", total, bytes)

