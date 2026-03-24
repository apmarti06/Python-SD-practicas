#Servidor TCP

import os
import socket

# vemos si el nombre del fichero existe
def archivo_existe(filename):
    return os.path.isfile(filename)

#recordar que escribimos/sobrescribimos en un pdf (binario) y que en caso de que se sobreescriba tendra que ser evaluado por precondiciones
def recibir_archivo(sockeT, filename, tamano_archivo):
    with open(filename, 'wb') as pdf:
        bytes_recibidos = 0
        while bytes_recibidos < tamano_archivo:
            #ajustamos el tamano restante
            datos = sockeT.recv(min(1024, tamano_archivo - bytes_recibidos))
            # si no hay ningun datos se ha terminado leer antes de lo deseado
            if not datos:
                break
            #guardamos los datos mientras sigamos leyendo del
            pdf.write(datos)
            bytes_recibidos += len(datos)


def Iniciar_server(direccion, puerto):
    #preparamos el servidor a que espere al cliente
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((direccion, puerto))
    servidor.listen(1)
    print(f"Servidor escuchando en {direccion}:{puerto}")

    while True:
        try:
            sockeT, addr = servidor.accept()
            print(f"Conexión establecida desde {addr}")

            #Recibimos el nombre del archivo
            filename = sockeT.recv(1024).decode('utf-8').strip()
            print(F"El cliente desea enviar: {filename}")

            # vemos el archivo introducido por el usuario si existe, para ver si sobreescribimos o no
            if archivo_existe(filename):
                sockeT.send(b"Existe")
                respuesta = sockeT.recv(1024).decode('utf-8').strip()
                if respuesta != "SI":
                    print("El cliente ")
                    sockeT.close()
                    continue

            else:
                sockeT.send(b"Ok")
            
            tamano_archivo = int(sockeT.recv(10).decode('utf-8').strip()) #convertimos la info del proceso del socket a entero, para leer bytes (32 bit int)
            print(f"Tamaño del archivo: {tamano_archivo}")

            # una vez con el tamaño recibimos el archivo del cliente
            recibir_archivo(sockeT, filename, tamano_archivo)
            print(f"Archivo {filename} recibido correctamente.")

            sockeT.send(b"Recibido")


        except Exception as error:
            print(f"Error en el servidor: {error} ")
        
        finally:
            sockeT.close()


if __name__ == "__main__":
    Iniciar_server('localhost', 65432)
