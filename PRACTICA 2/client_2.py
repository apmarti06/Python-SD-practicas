import socket

clientSocket = socket.socket()
host = '127.0.0.1'
port = 1254

print('Waiting for connection')
try:
    clientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

response = clientSocket.recv(1024)
while True:
    inputMessage = input('Say Something: ')
    clientSocket.send(str.encode(inputMessage))
    response = clientSocket.recv(1024)
    print(response.decode('utf-8'))

clientSocket.close()