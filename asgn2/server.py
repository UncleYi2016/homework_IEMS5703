import logging
import socket
import sys

BIND_ADDRESS = '0.0.0.0'
NUM_WORKER = 4
REQUEST_LIST = []
logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.INFO)

'''
    define child process
'''

def child_process(self):
    pass

if __name__ == '__main__':
    try:
        port_number = int(sys.argv[1])
        num_process = int(sys.argv[2])
    except Exception as err:
        logging.info('Program should be started with <port> <number of process>')
        return
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_ADDRESS, port_number))