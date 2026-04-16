import os 

def union_archivos(directorio_actual):

    nombre_archivo_end = os.path.join(directorio_actual, "union.txt")

    with open(nombre_archivo_end, "w", encoding="utf-8") as f:
        for archivo in os.listdir(directorio_actual):
            ruta = os.path.join(directorio_actual, archivo)

            if os.path.isfile(ruta) and archivo.endswith(".txt") and archivo != "union.txt":
                with open(ruta, "r", encoding="utf-8") as f_copiar:
                    f.write(f_copiar.read())
                    f.write("\n")

    print("Se han combinado todos los archivos .txt en union.txt")


if __name__ == "__main__":
    directorio_actual = os.getcwd()
    print("Directorio actual:", directorio_actual)
    union_archivos(directorio_actual)