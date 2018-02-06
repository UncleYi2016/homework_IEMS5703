import socket
import json
from data_package import data_package

SERVER_PORT = 55703
BUFFER_SIZE = 2048
END_STRING = '[END]'
END_PACKAGE = data_package(END_STRING)

dp = data_package('test')
print(dp)
# Create and initialize client_socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', SERVER_PORT))
msg = ''
while True:
    msg = input('Send message: ')
    client_socket.sendall(bytes(msg, encoding = 'utf-8'))
    if(msg.find(END_STRING) <= -1):
        break
# print(data)
data2 = client_socket.recv(BUFFER_SIZE)
print(data2)
client_socket.close()
