import logging
import socket
import sys
from multiprocessing import Pool

SERVER_ADDRESS = '0.0.0.0'
NUM_WORKER = 4
REQUEST_QUEUE = []
logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.INFO)

'''
    define child process
'''

def child_process():
    pass

def worker_thread(client_socket):
    pass

if __name__ == '__main__':
    try:
        port_number = int(sys.argv[1])
        num_process = int(sys.argv[2])
    except Exception as err:
        logging.info('Program should be started with <port> <number of process>')
        sys.exit()
    with Pool(num_process) as cp:
        cp.map(child_process)
        logging.info('Create process %s', cp.name)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_ADDRESS, port_number))
    server_socket.listen(20)
    while True:
        (client_socket, client_address) = server_socket.accept()
        REQUEST_QUEUE.append(client_socket)