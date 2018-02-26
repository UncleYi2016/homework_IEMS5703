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
    level=logging.DEBUG)


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
        logging.info('Connected to server.')
    except Exception as err:
        logging.info('Cannot connect to server at %s:%d', SERVER_ADDRESS, SERVER_PORT)
        logging.debug(err)
    
    try:
        msg = url
        msg += END_STRING
        client_socket.sendall(bytes(msg, encoding = 'utf-8'))
        result = ''
        # Receive result (Before receive all data, the program will not process the result)
        while True:
            try:
                data2 = client_socket.recv(BUFFER_SIZE)
                if(data2 == b''):
                    break
                logging.debug(data2.decode('utf-8'))
                result += data2.decode('utf-8')
            except Exception as err:
                logging.debug('Server disconnected')
        logging.debug(result)

        # # After decoded, process and devide the data by semicolon
        # length = len(result_list)
        # for r in range(length):
        #     word_content += result_list[r][0]
        #     word_type += result_list[r][1]
        #     if(r != length-1):
        #         word_content += ' ; '
        #         word_type += ' ; '
        # print(word_content)
        # print(word_type)
        # client_socket.close()
        # logging.info('Server disconnected')
    except Exception as err:
        logging.debug(err)
