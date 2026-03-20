import socket

HOST = 'localhost'
PORT = 1025
#identificamos que es un socket udp

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_udp:
    s_udp.bind((HOST, PORT))

    #Identificamos que a la hora de esperar la llamada del cliente, no hace falta solicitarla lo hace internamente la func
    #sin embargo espera cualquier dato de cualquier máquina, lo cual no asegura que se capte el dato correctamente
    print("Me quedo a la espera")
    mensaje, addr = s_udp.recvfrom(1024)

    print("Recibido el mensaje --->" + mensaje.decode("utf-8"))
    print("IP cliente: " + str(addr[0]))
    print("Puerto cliente: " + str(addr[1]))

    



