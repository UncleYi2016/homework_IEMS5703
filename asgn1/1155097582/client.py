import socket
import json
import logging
import sys

SERVER_PORT = 55703
SERVER_ADDRESS = 'localhost'
BUFFER_SIZE = 2048
FILEPATH = 'sentence.txt'
END_STRING = '[END]'

logging.basicConfig(level = logging.INFO)

def read_sentences(path):
    result = ''
    data_file = open(path, 'r')
    for line in data_file:
        line = line.strip()
        result += line
    return result

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
        FILEPATH = sys.argv[3]
    except Exception as err:
        logging.info('Input arguements should be <address> <port> <filepath>\nProgram started with default configuration: %s:%d, filepath:%s', SERVER_ADDRESS, SERVER_PORT, FILEPATH)
        logging.debug(err)
    # Try to connect server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
        logging.info('Connected to server.')
    except Exception as err:
        logging.info('Cannot connect to server at %s:%d', SERVER_ADDRESS, SERVER_PORT)
        logging.debug(err)
    
    try:
        # Read sentences and send to server
        msg = read_sentences(FILEPATH)
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
        result_list = json.loads(result)
        word_content = ''
        word_type = ''

        # After decoded, process and devide the data by semicolon
        length = len(result_list)
        for r in range(length):
            word_content += result_list[r][0]
            word_type += result_list[r][1]
            if(r != length-1):
                word_content += ' ; '
                word_type += ' ; '
        print(word_content)
        print(word_type)
        client_socket.close()
        logging.info('Server disconnected')
    except Exception as err:
        logging.debug(err)
