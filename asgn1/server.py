import socket
import json
import logging
from threading import Thread

SERVER_PORT = 55703
BUFFER_SIZE = 2048
END_STRING = '[END]'
logging.basicConfig(level=logging.DEBUG)

# Create and initialize server_socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', SERVER_PORT))
server_socket.listen(10)

threads = []

def comm_between_socket(client_socket):
    try:
        continue_transmit = True
        while continue_transmit:
            logging.debug('Receive start')
            data = client_socket.recv(BUFFER_SIZE)
            logging.debug('Receive end')
            data = str(data)
            logging.info(data)
            index = data.find(END_STRING)
            logging.debug('index - %d', index)
            if(index > -1):
                data = data[0:index]
                logging.debug('Cut : %s', data)
                continue_transmit = False
            logging.debug('Send start')
            client_socket.sendall(bytes(data, encoding = 'utf-8'))
            logging.debug('Send end')
        logging.info('Client disconnected')
        client_socket.close()
    except Exception as err:
        logging.info('Connection broken')
        logging.debug(err)

if __name__ == '__main__':
    while True:
        (client_socket, client_address) = server_socket.accept()
        (address, port) = client_socket.getsockname()
        print('Client %s:%d connected to server' % (address, port))
        comm_thread = Thread(target=comm_between_socket, args=(client_socket,), daemon=True)
        comm_thread.start()


