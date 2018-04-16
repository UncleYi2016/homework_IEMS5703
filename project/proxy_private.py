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
TMP_PRIVATE_SOCKETS = {}

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.DEBUG)
app = Flask(__name__)

def private_to_public(s_sock, s_port, pub_sock):
    try:
        while True:
            msg = core_transmit.get_data(s_sock)
            # After receive data
            data_packet = packet.packet(op_enum.OP_SUCCESS, op_enum.DES_SUCCESS, msg, s_port)
            data_packet_json = json.dumps(data_packet)
            core_transmit.send_data(pub_sock, data_packet_json)
    except Exception as err:
        logging.debug(err)
        s_sock.shutdown(socket.SHUT_RDWR)
        s_sock.close()
        


@app.route('/listen')
def listen():
    public_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    public_server_socket.connect((PUBLIC_SERVER_ADDRESS, PUBLIC_SERVER_PORT))
    while True:
        msg = core_transmit.get_operation(public_server_socket)
        logging.debug(msg)
        data_packet = json.loads(msg)
        if data_packet['op_code'] == op_enum.OP_BUILD_CONNECTION:
            # tmp_public_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # tmp_public_socket.connect((PUBLIC_SERVER_ADDRESS, PUBLIC_SERVER_PORT))
            client_port = data_packet['port']
            tmp_private_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tmp_private_socket.connect((PRIVATE_APP_ADDRESS, PRIVATE_APP_PORT))
            tmp_private_port = tmp_private_socket.getsockename()[1]
            TMP_PRIVATE_SOCKETS[tmp_private_port] = tmp_private_socket
            get_data_thread = Thread(target=private_to_public, args=(tmp_private_socket, tmp_private_port, public_server_socket, ), daemon=False)
            get_data_thread.start()
            # Tell public server that private connection is build
            response_packet = packet.packet(op_enum.OP_BUILD_OK, op_enum.DES_BUILD_OK, tmp_private_port, client_port)
            core_transmit.send_operation(public_server_socket, json.dumps(response_packet))
        elif data_packet['op_code'] == op_enum.OP_SUCCESS:
            msg_to_private = data_packet['msg']
            port_to_private = data_packet['port']
            socket_to_private = TMP_PRIVATE_SOCKETS[port_to_private]
            core_transmit.send_data(socket_to_private, msg_to_private)
    return 'connect open'

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except Exception as err:
        logging.info('Please input the proxy app console port number')
        logging.debug(err)
    app.run(host='0.0.0.0', port=port, debug=True)



    