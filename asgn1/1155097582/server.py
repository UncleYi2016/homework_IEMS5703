import socket
import json
import logging
import nltk
import sys


SERVER_PORT = 55703
SERVER_ADDRESS = 'localhost'
BUFFER_SIZE = 2048
END_STRING = '[END]'
logging.basicConfig(level=logging.INFO)

# Create and initialize server_socket

def comm_between_socket(client_socket):
    data_str = ''
    try:
        continue_transmit = True
        while continue_transmit:
            logging.debug('Receive start')
            data = client_socket.recv(BUFFER_SIZE)
            logging.debug('Receive end')
            data_str += data.decode('utf-8')
            # logging.info(data_str)
            index = data_str.find(END_STRING)   # index is the index of special string '[END]'
            logging.debug('index - %d', index)
            
            # Once detect the special string '[END]', process the data and send result back to client
            if(index > -1):
                data_str = data_str[0:index]
                logging.info(data_str)
                logging.debug('Cut : %s', data_str)
                continue_transmit = False
                data_token = nltk.word_tokenize(data_str)
                data_tagged = nltk.pos_tag(data_token)
                logging.debug(data_tagged)
                data_json = json.dumps(data_tagged)
                logging.debug(len(data_json))
                logging.debug('Send start')
                client_socket.sendall(bytes(data_json, encoding = 'utf-8'))
                logging.debug('Send end')
        logging.info('Client disconnected')
        client_socket.close()
    except Exception as err:
        # If connection broken, show it.
        logging.info('Connection broken')
        logging.debug(err)

if __name__ == '__main__':
    # Initialize arguement of server port
    try:
        SERVER_PORT = int(sys.argv[1])
    except Exception as err:
        logging.info('Started with default port %d', SERVER_PORT)
        logging.debug(err)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
    server_socket.listen(10)

    # Start accept, once accept, it will go to communicate with client
    while True:
        (client_socket, client_address) = server_socket.accept()
        c_address = client_address[0]
        c_port = client_address[1]
        logging.info('Client %s:%d connected to server', c_address, c_port)
        comm_between_socket(client_socket)


