import socket
import json

SERVER_PORT = 55703
BUFFER_SIZE = 2048
END_STRING = '--- THE END ---'.encode('utf-8') 

# Create and initialize server_socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', SERVER_PORT))
server_socket.listen(10)

threads = []
while True:
    (client_socket, client_address) = server_socket.accept()
    (address, port) = client_socket.getsockname()
    print('Client %s:%d connected to server' % (address, port))
    while True:
        data = client_socket.recv(BUFFER_SIZE)
        print('data')

        client_socket.sendall(b'receive: ' + data)
        if(data == END_STRING):
            break
    client_socket.close()
