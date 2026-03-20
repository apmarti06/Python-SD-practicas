import socket

HOST = 'localhost'
PORT = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send("Hola, servidor".encode("utf-8"))
mensaje = s.recv(1024)

print("Recibido:["+mensaje.decode("utf-8")+"] del servidor ")

s.close()