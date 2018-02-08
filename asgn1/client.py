import socket
import json
import logging

SERVER_PORT = 55703
SERVER_ADDRESS = 'localhost'
BUFFER_SIZE = 2048
END_STRING = '[END]'

logging.basicConfig(level = logging.DEBUG)
# Create and initialize client_socket
if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
        logging.info('Connected to server.')
    except Exception as err:
        logging.info('Cannot connect to server at %s:%d', SERVER_ADDRESS, SERVER_PORT)
        logging.debug(err)
    msg = ''
    continue_send = True
    try:
        while continue_send:
            msg = input('Send message: ')
            client_socket.sendall(bytes(msg, encoding = 'utf-8'))
            if(msg.find(END_STRING) > -1):
                continue_send = False
            data2 = client_socket.recv(BUFFER_SIZE)
            logging.info(data2)
        # print(data)
        client_socket.close()
        logging.info('Disconnected to server')
    except Exception as err:
        login.debug(err)
