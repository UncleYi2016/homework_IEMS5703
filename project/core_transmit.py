import socket
import logging
from threading import Thread
import traceback
import time

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.DEBUG)

MSG_LEN = 20480

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
    data = bytes(msg, encoding = 'utf-8')
    d_sock.sendall(data)

def get_operation(s_sock):
    msg = ''
    while True:
        data = s_sock.recv(MSG_LEN + 1024)
        data_str = data.decode('utf-8')
        msg = msg + data_str
        if msg.endwith('[END]'):
            msg = msg.strip('[END]')
            break
    #logging.debug('get: ' + data.decode('utf-8'))
    return msg

def send_data(d_sock, msg):
    logging.debug('send: ' + msg)
    data = bytes(msg, encoding = 'utf-8')
    d_sock.sendall(data)

def get_data(s_sock):
    data = s_sock.recv(MSG_LEN)
    return data.decode('utf-8')
    

        