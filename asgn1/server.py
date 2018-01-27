import socket
import json

SERVER_PORT = 55703
BUFFER_SIZE = 2048
END_STRING = '--- THE END ---'

# Create and initialize server_socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', SERVER_PORT))

threads = []
while True:
    (client_socket, client_address) = server_socket.accept()
    print(client_socket)
    client_socket.close()