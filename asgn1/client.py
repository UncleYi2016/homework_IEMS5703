import socket
import json
from data_package import data_package

SERVER_PORT = 55703
BUFFER_SIZE = 2048
END_STRING = '--- THE END ---'.encode('utf-8')
END_PACKAGE = data_package(END_STRING.encode('utf-8'))

dp = data_package('test')
print(dp)
# Create and initialize client_socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', SERVER_PORT))
msg = input('Send message')
dp.set_data(msg)
data = dp.to_json()
print(data)
client_socket.sendall(bytes(data, encoding = 'utf-8'))
client_socket.send(bytes(END_PACKAGE.to_json(), encoding = 'utf-8'))
data2 = client_socket.recv(BUFFER_SIZE)
print(data2)
client_socket.close()
