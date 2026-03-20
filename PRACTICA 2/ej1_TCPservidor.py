import socket

HOST = 'localhost'
PORT = 1024

S_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S_tcp.bind((HOST, PORT))

#aquí necesitamos esperar a algo (almenos 1 vez)
print("A la espera de un cliente...")
S_tcp.listen(1)


s_cliente, addr = S_tcp.accept()
mensaje = s_cliente.recv(1024)

print("Recibo el mensaje: ["+mensaje.decode("utf-8")+"] del cliente con direccion" + str(addr))
s_cliente.send("Hola, cliente, soy el servidor".encode("utf-8"))
#una vez hecha la actividad cerramos la conexión
s_cliente.close()
S_tcp.close()