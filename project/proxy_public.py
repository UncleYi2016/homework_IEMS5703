import core_transmit
import socket
import logging

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
    (private_socket, private_address) = proxy_socket.accept()
    logging.debug('Accept private app %s', private_address)
    while True:
        (client_socket, client_address) = proxy_socket.accept()
        logging.debug('Accept client %s', client_address)
        core_transmit.transmit_data(client_socket, proxy_socket)
        