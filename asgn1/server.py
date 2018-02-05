import socket
import json
from data_package import data_package

SERVER_PORT = 55703
BUFFER_SIZE = 2048
END_STRING = '--- THE END ---'

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
        data_package_json = client_socket.recv(BUFFER_SIZE)
        print(data_package_json)
        client_socket.sendall(data_package_json)
        dp_jobj = json.loads(data_package_json)
        dp = data_package(dp_jboj['data'])
        if(dp.get_data() == END_STRING):
            print('true')
            break
        else:
            print('false')
    client_socket.close()
