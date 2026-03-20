import socket

HOST = 'localhost' # El servidor al que deseas conectarte
PORT = 1025 # El puerto que utiliza el servidor
    # Creando el socket UDP dentro de un bloque with
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_udp:
    s_udp.sendto("Soy el cliente".encode("utf-8"), (HOST, PORT))
    
    # Imprimir la dirección y el puerto del socket del cliente
    print("Listening on:", s_udp.getsockname())