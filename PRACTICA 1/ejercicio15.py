import os 
import shutil

# creamos esta función para el caso que dos archivos tengan el mismo nombre en un directorio
def nuevo_nombre(directorio, nombre):
    base, extension = os.path.splitext(nombre) # obtenemos del archivo el nombre y su extension ejemplo prueba.cpp -> prueba y cpp
    nuevo_nombre = nombre
    contador = 1

    #miramos en todo el directorio si existe ya dicho nombre
    while os.path.exists(os.path.join(directorio, nuevo_nombre)):
        nuevo_nombre = f"{base}_{contador}{extension}"
        contador += 1

    return nuevo_nombre

def nuevo_dir(directorio_base ,directorio_actual): #vamos listando y recorriendo desde el actual
    for elemento in os.listdir(directorio_actual):

        ruta_origen = os.path.join(directorio_actual, elemento) #obtenemos del nombre del archivo la ruta

        # si en el directorio que estamos buscando ahora hay archivos vemos si son nuevos
        if os.path.isfile(ruta_origen): #ruta valida
                #solo movemos los que no estan el el directorio base
            if os.path.abspath(directorio_actual) != os.path.abspath(directorio_base):

                #actualizamos el archivo en nuestro directorio base, para que se guarde
                nuevo_nombre = nuevo_nombre(directorio_base, elemento)
                ruta_destino = os.path.join(directorio_base, nuevo_nombre)

                shutil.move(ruta_origen, ruta_destino) #solo movemos el fichero a otro directorio
                print(f"Movido: {ruta_origen} -> {ruta_destino}") # ya hemos movido el de la llamada al otro

        # si encontramos un directorio lo movemos y recorremos todo esos ficheros

        elif os.path.isdir(ruta_origen):
            nuevo_dir(directorio_base, ruta_origen)

if __name__ == "__main__":
    directorio_actual = os.getcwd() #obtenemos el directorio actual y lo actualizamos
    nuevo_dir(directorio_actual, directorio_actual)
