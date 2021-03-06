import logging
import socket
import sys
from multiprocessing import Process, Queue
from threading import Thread
from threading import current_thread
from urllib import request
import time
import os
import traceback

import numpy as np
from keras_squeezenet import SqueezeNet
from keras.applications.imagenet_utils import preprocess_input
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing import image
import tensorflow as tf

SERVER_ADDRESS = '0.0.0.0'
NUM_WORKER = 4
BUFFER_SIZE = 2048
END_STRING = '[END]'

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.INFO)

'''
    define child process
'''

def child_process(request_queue):
    thread_pool = []
    logging.debug('Creation successed')
    graph = tf.get_default_graph()
    while True:
        '''
            Create thread
        '''
        if len(thread_pool) < NUM_WORKER:
            # TODO: Create a thread
            client_socket = request_queue.get()
            logging.info('Client %s connected', client_socket.getpeername())
            wt = Thread(target=worker_thread, args=(client_socket,graph,), daemon=True)
            wt.start()
            thread_pool.append(wt)
            logging.debug('Create thread %s', wt.name)
        else:
            for t in thread_pool:
                if not t.is_alive():
                    thread_pool.remove(t)

def worker_thread(client_socket, graph):
    data = b''
    data_str = ''
    index = -1
    try:
        continue_transmit = True
        while continue_transmit:
            logging.debug('Receive start')
            data = client_socket.recv(BUFFER_SIZE)
            logging.info('Received Client %s', client_socket.getpeername())
            if len(data) <= 0:
                break
            logging.debug('Receive end')
            data_str += data.decode('utf-8')
            index = data_str.find(END_STRING)   # index is the index of special string '[END]'
            logging.debug('index - %d', index)
            
            # Once detect the special string '[END]', process the data and send result back to client
            if(index > -1):
                data_str = data_str[0:index]
                continue_transmit = False
            # logging.info(data_str)
        logging.debug('Transmit exited')
        preds = get_image_result(data_str, graph)
        client_socket.sendall(bytes(str(preds), encoding = 'utf-8'))

    except Exception as err:
        # If connection broken, show it.
        # traceback.print_exc()
        logging.debug(err) 
    finally:
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()

def get_image_result(url, graph):
    logging.info('Client submitted URL %s', url)
    '''
        Download image
    '''
    filename = '%s-%s' % (time.time(), os.path.basename(url))
    request.urlretrieve(url, filename)

    '''
        Process image
    '''
    with graph.as_default():
        model = SqueezeNet()
        img = image.load_img(filename, target_size=(227, 227))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
    
    logging.debug(type(preds))

    preds = decode_predictions(preds)
    return preds[0][0]

if __name__ == '__main__':
    request_queue = Queue()
    process_pool = []
    try:
        port_number = int(sys.argv[1])
        num_process = int(sys.argv[2])
    except Exception as err:
        logging.info('Program should be started with <port> <number of process>')
        sys.exit()
    logging.info('Start listening for connections on port %d', port_number)
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
        logging.debug('Accept client %s', client_address)
        request_queue.put(client_socket)