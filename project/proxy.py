import core_transmit
import socket
import logging

SERVER_PORT = 50001
SERVER_ADDRESS = 'localhost'
PROXY_ADDRESS = '0.0.0.0'
PROXY_PORT = 60001
BUFFER_SIZE = 2048

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.DEBUG)

if __name__ == '__main__':
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((PROXY_ADDRESS, PROXY_PORT))
    proxy_socket.listen(20)
    while True:
        (client_socket, client_address) = proxy_socket.accept()
        logging.debug('Accept client %s', client_address)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((SERVER_ADDRESS, SERVER_PORT))
        logging.info('Connected to server at %s', client_socket.getsocksname())
        core_transmit.transmit_data(client_socket, proxy_socket, server_socket)