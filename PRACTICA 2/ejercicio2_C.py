import socket 
import os

def enviarArchivo (servidor, puerto, path):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # una vez el servidor acepta la conexión, nos conenctamos
    try:
        cliente.connect((servidor, puerto))

        filename = os.path.basename(path)
        cliente.send(filename.encode('utf-8'))
        # esperamos la respuesta del servidor
        respuesta = cliente.recv(1024).decode('utf-8').strip()
        
        if respuesta == "EXISTE":
            accion = input(f"El archivo {filename} ya existe en el servidor. ¿Quieres sobreescribirlo? (S/N)").strip().upper()
        #usamos strip para eliminar todos los espacios en blanco que el usuario introduzca para que no falle y upper para que no importe si es mayus/minus
        cliente.send(accion.encode('utf-8'))
        if respuesta != "S":
            print("Transferencia cancelada")
            cliente.close()
            return

        # Obtener tamaño del archivo y enviarlo en
        # formato fijo de 10 caracteres
        # zfill(10) -> 10 caracteres, rellenando con ceros
        tamano_file = str(os.path.getsize(path).zfill(10))
        cliente.send(filename.encode('utf-8'))

        with open(path, 'rb') as f:
            bytes_enviados = 0
            while bytes_enviados < int(tamano_file):
                datos = f.read(1024)
                cliente.send(datos)
                bytes_enviados += len(datos)

        #segunda opcion. Alternativamente, en TCP, podemos enviar todo
        # el fichero de una vez con sendall()
        # with open(ruta_archivo, 'rb') as archivo:
        # cliente.sendall(archivo.read())

        notificacion = cliente.recv(1024).decode('utf-8')
        if notificacion == "Recibido":
            print("Servidor ha recibido el archivo. Eliminando archivo local...")
            os.remove(path)

    except Exception as e:
        print(f"Error en el cliente: {e}")
    finally:
        #cerramos la conexión con el cliente
        cliente.close()
        

#ejecutamos la respuesta del cliente
if __name__ == "__main__":
    enviarArchivo('localhost', 65432, '/home/alfonso/Escritorio/Python-SD-practicas/PRACTICA 2/file.pdf')