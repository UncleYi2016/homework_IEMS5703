import socket
import json
import logging
import sys

SERVER_PORT = 50001
SERVER_ADDRESS = 'localhost'
BUFFER_SIZE = 2048
END_STRING = '[END]'

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.INFO)


# Create and initialize client_socket
if __name__ == '__main__':
    # Initialize msg: The data needed to be send
    # And continue_send: If the client send [END], continue_send will be set as False the sending while loop will be terminated and client start receive data
    msg = ''
    continue_send = True
    # Set arguments for connecting server
    try:
        SERVER_ADDRESS = sys.argv[1]
        SERVER_PORT = int(sys.argv[2])
        url = sys.argv[3]
    except Exception as err:
        logging.info('Input arguements should be <address> <port> <url>')
    # Try to connect server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
        logging.info('Connected to server at %s', client_socket.getsocksname())
    except Exception as err:
        logging.info('Cannot connect to server at %s:%d', SERVER_ADDRESS, SERVER_PORT)
        logging.debug(err)
    
    try:
        msg = url
        msg += END_STRING
        client_socket.sendall(bytes(msg, encoding = 'utf-8'))
        logging.info('URL sent to the server')
        result = ''
        # Receive result (Before receive all data, the program will not process the result)
        while True:
            try:
                data2 = client_socket.recv(BUFFER_SIZE)
                if(data2 == b''):
                    break
                result += data2.decode('utf-8')
            except Exception as err:
                logging.debug('Server disconnected')
        logging.info('Server response: %s', result)
    except Exception as err:
        logging.debug(err)
