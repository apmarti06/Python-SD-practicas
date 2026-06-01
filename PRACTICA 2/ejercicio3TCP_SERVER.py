import socket 
import os 

#definimos el puerto y direccion IP
HOST = 'localhost'
PORT = 1024

# vemos si el nombre del fichero existe
def archivo_existe(filename):
    return os.path.isfile(filename)

# invertimos la cadena
def Invertir_string(texto):
    return texto[::-1]

def conexion_servidor():
    # creamos socket y lo asociamos esperando conexion
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_server:
        sock_server.bind((HOST, PORT))
        sock_server.listen(1)
        print(f"Servidor escuchando en {HOST}:{PORT}")
        print("Esperando conexión del cliente...")

        conn, addr = sock_server.accept()
        print(f"Cliente conectado desde {addr}")

        with conn:
            # 1. Recibimos el nombre del archivo a cambiar
            file_name = conn.recv(1024).decode('utf-8')
            print(f"Recibiendo archivo: {file_name}")

            # 2. Recibir el tamaño del contenido, lo pasamos a bytes (int 32 bits)
            tamano_contenido = int(conn.recv(1024).decode('utf-8'))
            print(f"Tamaño del contenido: {tamano_contenido} bytes")

            # 3. Recibimos el contenido en si (string) del fichero
            if (archivo_existe(file_name)):
                contenido = b''
                while len(contenido) < tamano_contenido:
                    parte = conn.recv(1024)
                    if not parte:
                        break
                    contenido += parte
                
                texto = contenido.decode('utf-8')
                print(f"Contenido recibido: {len(texto)} caracteres")

                # 4. Invertimos el texto
                texto_invertido = Invertir_string(texto)
                tamano = len(texto_invertido)

                print(f"Texto invertido: {tamano} caracteres")
                print(f"Contenido invertido (primeros 50 chars): {texto_invertido[:50]}...")

                 #5. Enviar el tamaño al cliente
                conn.send(str(tamano).encode('utf-8'))
                
                # Esperar confirmación del cliente (opcional, pero buena práctica)
                conn.recv(1024)
                
                # 6. Enviar el contenido invertido
                conn.send(texto_invertido.encode('utf-8'))
                
                print("Archivo invertido enviado al cliente")
                print("Conexión cerrada")

if __name__ == "__main__":
    conexion_servidor()