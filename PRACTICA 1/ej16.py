import os 

def renombrar_archivo(directorio_actual):

    #listamos los archivos para ver cual usario quiere modificar

    for archivo in os.listdir(directorio_actual):
        if os.path.isfile(archivo):
            print(archivo)

    
    # si entra aquí es porque el usuario quiere cambiar el nombre de un fichero
    nombre_antiguo = input("Introduce el nombre del fichero que quieres renombrar: ")
    nombre_nuevo = input("Introduce el nuevo nombre del fichero: ")

    # dos casos, que ya haya sido guardado el deseado, o que no exista el que se quiera renombrar
    try:
        if not os.path.exists(nombre_antiguo):
            print("Error: el fichero que quieres renombrar no existe.")
        elif os.path.exists(nombre_nuevo):
            print("Error: ya existe un fichero con el nuevo nombre.")
        else:
            os.rename(nombre_antiguo, nombre_nuevo)
            print("Fichero renombrado correctamente.")

    except OSError as e: #Para manejar excepciones no controladas (memoria...)
        print("Error del sistema operativo:", e)


if __name__ == "__main__":
    directorio_actual = os.getcwd()
    si = input("Si quieres cambiar algún fichero indica S")
    if si == 'S':
        renombrar_archivo(directorio_actual)
    

    
