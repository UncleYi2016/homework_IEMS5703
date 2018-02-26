import logging
import socket
import sys
from multiprocessing import Process, Queue
from threading import Thread

SERVER_ADDRESS = '0.0.0.0'
NUM_WORKER = 4
BUFFER_SIZE = 2048
END_STRING = '[END]'

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.DEBUG)

'''
    define child process
'''

def child_process(request_queue):
    thread_pool = []
    logging.debug('Creation successed')
    while True:
        '''
            Create thread
        '''
        if len(thread_pool) < NUM_WORKER:
            # TODO: Create a thread
            client_socket = request_queue.get()
            logging.info('Client %s connected', client_socket.getsockname())
            wt = Thread(target=worker_thread, args=(client_socket,), daemon=True)
            wt.start()
            thread_pool.append(wt)
            logging.debug('Create thread %s', wt.name)

def worker_thread(client_socket):
    data = b''
    data_str = ''
    index = -1
    try:
        continue_transmit = True
        while continue_transmit:
            logging.debug('Receive start')
            data = client_socket.recv(BUFFER_SIZE)
            logging.debug('Receive end')
            data_str += data.decode('utf-8')
            logging.info(data_str)
            index = data_str.find(END_STRING)   # index is the index of special string '[END]'
            # logging.debug('index - %d', index)
            
            # Once detect the special string '[END]', process the data and send result back to client
            if(index > -1):
                data_str = data_str[0:index]
                continue_transmit = False
    except Exception as err:
        # If connection broken, show it.
        logging.info('Connection broken')
        logging.debug(err)

if __name__ == '__main__':
    request_queue = Queue()
    process_pool = []
    try:
        port_number = int(sys.argv[1])
        num_process = int(sys.argv[2])
    except Exception as err:
        logging.info('Program should be started with <port> <number of process>')
        sys.exit()
    for i in range(num_process):
        cp = Process(target=child_process, args=(request_queue,))
        cp.start()
        process_pool.append(cp)
        logging.info('Create process %s', cp.name)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_ADDRESS, port_number))
    server_socket.listen(20)
    while True:
        (client_socket, client_address) = server_socket.accept()
        logging.debug('Accept client %s', client_socket.getsockname())
        request_queue.put(client_socket)