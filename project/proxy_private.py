import core_transmit
import socket
import logging
import sys
import packet
import op_enum
from flask import Flask
from flask import request
from flask import json

PRIVATE_APP_PORT = 50001
PRIVATE_APP_ADDRESS = '192.168.56.101'
PUBLIC_SERVER_ADDRESS = 'ec2-13-231-5-245.ap-northeast-1.compute.amazonaws.com'   #NEED TO BE SET
PUBLIC_SERVER_PORT = 8000
BUFFER_SIZE = 2048

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.DEBUG)
app = Flask(__name__)

@app.route('/connect')
def connect():
    public_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    public_server_socket.connect((PUBLIC_SERVER_ADDRESS, PUBLIC_SERVER_PORT))
    while True:
        msg = core_transmit.get_operation(public_server_socket)
        logging.debug(msg)
        packet = json.loads(msg)
        if packet['op_code'] == op_enum.OP_BUILD_CONNECTION:
            tmp_public_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tmp_public_socket.connect((PUBLIC_SERVER_ADDRESS, PUBLIC_SERVER_PORT))
            tmp_private_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tmp_private_socket.connect((PRIVATE_APP_ADDRESS, PRIVATE_APP_PORT))
            core_transmit.transmit_data(tmp_public_socket, tmp_private_socket)

    '''
    private_app_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    public_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    public_server_socket.connect((PUBLIC_SERVER_ADDRESS, PUBLIC_SERVER_PORT))
    private_app_socket.connect((PRIVATE_APP_ADDRESS, PRIVATE_APP_PORT))
    core_transmit.transmit_data(public_server_socket, private_app_socket)
    '''
    return 'connect open'

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except Exception as err:
        logging.info('Please input the proxy app console port number')
        logging.debug(err)
    app.run(host='0.0.0.0', port=port, debug=True)



    