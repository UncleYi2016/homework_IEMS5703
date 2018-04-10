import socket
import logging
import Thread

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.DEBUG)

MSG_LEN = 1024

def transmit_thread(s_sock, d_sock):
    try:
        while True:
            data = s_sock.recv(MSG_LEN)
            d_sock.sendall(data)
    except Exception as err:
        logging.debug(err)

#@staticmethod
def transmit_data(c_sock, p_sock, s_sock):
    p_to_s = Thread(target=transmit_thread, args=(p_sock,s_sock,), daemon=True)
    s_to_p = Thread(target=transmit_thread, args=(s_sock,p_sock,), daemon=True)
    c_to_p = Thread(target=transmit_thread, args=(c_sock,p_sock,), daemon=True)
    p_to_c = Thread(target=transmit_thread, args=(p_sock,c_sock,), daemon=True)
    wt.start()
        