import socket
import logging
from threading import Thread
import traceback
import time

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.NOTSET)

MSG_LEN = 65536

def transmit_thread(s_sock, d_sock):
    try:
        while True:
            data = s_sock.recv(MSG_LEN)
            if(data == b''):
                break
            d_sock.sendall(data)
    except Exception as err:
        traceback.print_exc()
        logging.debug(err)

def transmit_data(c_sock, s_sock):
    logging.info('client socket: ' + str(c_sock.getpeername()))
    logging.info('server socket: ' + str(s_sock.getpeername()))
    c_to_s = Thread(target=transmit_thread, args=(c_sock,s_sock,), daemon=False)
    s_to_c = Thread(target=transmit_thread, args=(s_sock,c_sock,), daemon=False)
    c_to_s.start()
    s_to_c.start()

def send_operation(d_sock, msg):
    msg = msg + '[END]'
    logging.debug('send op: ' + msg)
    data = bytes(msg, encoding = 'ISO-8859-1')
    time.sleep(0.1)
    d_sock.sendall(data)

def get_operation(s_sock):
    time.sleep(0.1)
    msg = ''
    while True:
        data = s_sock.recv(MSG_LEN + 1024)
        data_str = data.decode('ISO-8859-1')
        msg = msg + data_str
        if msg.endswith('[END]'):
            msg = msg.strip('[END]')
            break
    #logging.debug('get: ' + data.decode('ISO-8859-1'))
    return msg

def send_data(d_sock, msg):
    logging.debug(str(d_sock.getsockname()) + 'send: ' + str(len(msg)))
    data = bytes(msg, encoding = 'ISO-8859-1')
    time.sleep(0.1)
    d_sock.sendall(data)

def get_data(s_sock):
    time.sleep(0.1)
    logging.debug(str(s_sock.getsockname()) + 'waiting for ++++++++++++ ' + str(s_sock.getpeername()))
    data = s_sock.recv(MSG_LEN)
    logging.debug('get + ' + str(len(data)) + ' bytes data from ------------ ' + str(s_sock.getpeername()))
    return data.decode('ISO-8859-1')
    

        