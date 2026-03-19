import socket
import os
from _thread import *

serverSocket = socket.socket()
host = '127.0.0.1'
port = 1254
threadCount = 0
try:
    serverSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
serverSocket.listen(5)


def threaded_client(connection):
    connection.send(str.encode('Welcome to the Server'))
    while True:
        data = connection.recv(2048)
        reply = 'Server Says - Hola: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()

while True:
    client, address = serverSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (client, ))
    threadCount += 1
    print('Thread Number: ' + str(threadCount))
serverSocket.close()