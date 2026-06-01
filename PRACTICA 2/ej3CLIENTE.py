import socket
import os

HOST ='localhost'
PORT = '1024'

def iniciar_cliente():
    # solicitamos por pantalla el archivo a invertir
    filename = "filein.txt"

    # verificamos primero que exista
    if not os.path.exists(filename):
        print(f"Error: El archivo '{filename}' no existe")
        return

    #guardamos el contenido del archivo, modo lectura normal
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            contenido = f.read()
            print(f"Archivo leído correctamente: {len(contenido)} caracteres")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return
    
    #hacemos la conexion de procesos entre clientes-servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((HOST, PORT))
        print(f"Conectado al servidor {HOST}:{PORT}")
        
        # 5. Enviar el nombre del archivo
        cliente.send(filename.encode('utf-8'))
        
        # Pequeña pausa para evitar mezcla de mensajes
        import time
        time.sleep(0.1)
        
        # 6. Enviar el tamaño del contenido
        tamano = len(contenido.encode('utf-8'))
        cliente.send(str(tamano).encode('utf-8'))

        # 7. Enviar el contenido del archivo
        cliente.send(contenido.encode('utf-8'))
        print("Archivo enviado")
        
        # 8. Recibir el tamaño del archivo invertido
        tamano_invertido = int(cliente.recv(1024).decode('utf-8'))
        print(f"Tamaño del archivo invertido: {tamano_invertido} bytes")
        
        # Confirmar que se recibió el tamaño
        cliente.send(b'OK')

        #guardamos el resultado en bytes y decodificamos
        invertido = b''
        while len(invertido) < tamano_invertido:
            parte = cliente.recv(1024)
            if not parte:
                break
            invertido += parte

        texto_invertido = invertido.decode('utf-8')

        # 10. Guardar el archivo invertido, y lo sacamos por salida
        nombre_salida = f"invertido_{filename}"
        with open(nombre_salida, 'w', encoding='utf-8') as f:
            f.write(texto_invertido)
        
        print("Recibido archivo invertido")
        print(f"Archivo guardado como: {nombre_salida}")
        
        # Mostrar resumen
        print("\n--- RESUMEN ---")
        print(f"Archivo original: {filename} ({tamano} bytes)")
        print(f"Archivo invertido: {nombre_salida} ({tamano_invertido} bytes)")
        print("\nPrimeros 100 caracteres del archivo invertido:")
        print(texto_invertido[:100])
        

if __name__ == "__main__":
    iniciar_cliente()