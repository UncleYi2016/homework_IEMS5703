import socket
import logging
from threading import Thread
import traceback

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.DEBUG)

MSG_LEN = 1024

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

#@staticmethod
def transmit_data(c_sock, s_sock):
    logging.info('client socket: ' + str(c_sock.getpeername()))
    logging.info('server socket: ' + str(s_sock.getpeername()))
    c_to_s = Thread(target=transmit_thread, args=(c_sock,s_sock,), daemon=True)
    s_to_c = Thread(target=transmit_thread, args=(s_sock,c_sock,), daemon=True)
    c_to_s.start()
    s_to_c.start()

    

        