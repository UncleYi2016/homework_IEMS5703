import logging
import socket
import sys
from multiprocessing import Process, Queue
from threading import Thread
import time

SERVER_ADDRESS = '0.0.0.0'
NUM_WORKER = 4

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.INFO)

'''
    define child process
'''

def child_process(request_queue):
    logging.debug('Creation successed')
    time.sleep(2)
    # while True:
    #     handle = request_queue.get()
    #     client_socket = multiprocessing.reduction.rebuild_socket(handle)
    #     logging.info('Client %s connected', client_socket)
    # thread_pool = []
    # for i in range(4):
    #     wt = Thread(target=worker_thread, args=(None,), daemon=True)
    #     logging.debug('Create thread %s', wt.name)

def worker_thread(client_socket):
    pass

if __name__ == '__main__':
    request_queue = Queue()
    try:
        port_number = int(sys.argv[1])
        num_process = int(sys.argv[2])
    except Exception as err:
        logging.info('Program should be started with <port> <number of process>')
        sys.exit()
    for i in range(5):
        cp = Process(target=child_process, args=(request_queue,))
        cp.start()
        cp.join()
        logging.info('Create process %s', cp.name)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_ADDRESS, port_number))
    server_socket.listen(20)
    while True:
        (client_socket, client_address) = server_socket.accept()
        handle = multiprocessing.reduction.reduce_socket(client_socket)
        request_queue.put(handle)