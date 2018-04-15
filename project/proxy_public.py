import core_transmit
import socket
import logging

PROXY_ADDRESS = '0.0.0.0'
PROXY_PORT = 8000
CLIENT_HANDLE_PORT = 60003
BUFFER_SIZE = 2048

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.DEBUG)

if __name__ == '__main__':
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((PROXY_ADDRESS, PROXY_PORT))
    proxy_socket.listen(20)
    (private_socket, private_address) = proxy_socket.accept()
    logging.debug('Accept private app %s', private_address)
    client_handle_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_handle_socket.bind((PROXY_ADDRESS, CLIENT_HANDLE_PORT))
    client_handle_socket.listen(20)
    while True:
        (client_socket, client_address) = client_handle_socket.accept()
        logging.debug('Accept client %s', client_address)
        core_transmit.transmit_data(client_socket, proxy_socket)
        