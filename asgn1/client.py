import socket
import json

SERVER_PORT = 55703
BUFFER_SIZE = 2048
END_STRING = '--- THE END ---'

# Create and initialize client_socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', SERVER_PORT))
msg = 'hello'.encode('utf-8')
client_socket.send(msg)
client_socket.send(END_STRING)
client_socket.close()
