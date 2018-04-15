import core_transmit
import socket
import logging

PRIVATE_APP_PORT = 50001
PRIVATE_APP_ADDRESS = '192.168.56.101'
PUBLIC_SERVER_ADDRESS = 'ec2-13-231-5-245.ap-northeast-1.compute.amazonaws.com'   #NEED TO BE SET
PUBLIC_SERVER_PORT = 60002
BUFFER_SIZE = 2048

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.DEBUG)

if __name__ == '__main__':
    private_app_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    public_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    public_server_socket.connect((PUBLIC_SERVER_ADDRESS, PUBLIC_SERVER_PORT))
    private_app_socket.connect((PRIVATE_APP_ADDRESS, PRIVATE_APP_PORT))
    core_transmit.transmit_data(public_server_socket, private_app_socket)


    