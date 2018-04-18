import core_transmit
import socket
import logging
import packet
import op_enum
import json
import time
import urllib
import urllib.request
import urllib.parse
import queue
from threading import Thread
from flask import Flask
from flask import request
from flask import json
PROXY_ADDRESS = '0.0.0.0'
PROXY_PORT = 8000
CLIENT_ADDRESS_TABLE = {}
PRIVATE_SOCKET_TABLE = {}
BIND_APP = {}
OP_QUEUE = queue.Queue()



logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.DEBUG)
app = Flask(__name__)

'''
    Get operation from private proxy and store into queue
'''
def get_operation(pri_sock):
    try:
        while True:
            op = core_transmit.get_operation(pri_sock)
            logging.debug('Got op!')
            op = op.decode('utf-8')
            if data == '':
                continue
            OP_QUEUE.put(op)
    except Exception as err:
        logging.debug(err)
        pri_sock.shutdown(socket.SHUT_RDWR)
        pri_sock.close()

'''
    Handle operation which get from queue
'''
def handle_operation():
    operation = OP_QUEUE.get()
    operation_packet = json.loads(data)
    op_code = operation['op_code']
    op_describe = operation['op_describe']
    msg = operation['msg']
    app_name = operation['app_name']
    client_address = operation['client_address']
    logging.debug('get: ' + str(operation))
    if op_code == op_enum.OP_TRANSMIT_DATA:
        client_socket = CLIENT_ADDRESS_TABLE[client_address]
        core_transmit.send_data(client_socket, msg)

'''
    Receive client data and transmit to private proxy
'''
def client_to_private(c_sock, c_address, pri_sock, app_name):
    try:
        while True:
            msg = core_transmit.get_data(c_sock)
            # After receive data
            data_packet = packet.packet(op_enum.OP_TRANSMIT_DATA, op_enum.DES_TRANSMIT_DATA, msg, app_name, c_address)
            data_packet_json = json.dumps(data_packet)
            logging.debug('generate: ' + str(data_packet_json))
            core_transmit.send_operation(pri_sock, data_packet_json)
    except Exception as err:
        logging.debug(err)
        c_sock.shutdown(socket.SHUT_RDWR)
        c_sock.close()

'''
    Used to accept client connection
'''
def client_accept(client_handle_socket, app_name):
    while True:
        (client_socket, client_address) = client_handle_socket.accept()
        CLIENT_ADDRESS_TABLE[client_address] = client_socket
        private_socket = PRIVATE_SOCKET_TABLE[app_name]
        build_connect_packet = json.dumps(packet.packet(op_enum.OP_BUILD_CONNECTION, op_enum.DES_BUILD_CONNECTION, '', app_name, client_address))
        core_transmit.send_operation(private_socket, build_connect_packet)
        client_to_private_thread(target=client_to_private, args=(client_socket, client_address, private_socket, app_name), daemon=False, name=app_name + str(client_address))
        client_to_private_thread.start()

'''
    Register APP
'''
@app.route('/register_app/<app_name>/<int:bind_port>')
def register_app(app_name=None, bind_port=None):
    if app_name in BIND_APP:
        return json.dumps(packet.packet(op_enum.OP_FAILED, op_enum.DES_FAILED, 'APP \"' + app_name + '\" has already exist', app_name, None))
    BIND_APP[app_name] = bind_port
    try:
        (private_socket, private_address) = proxy_socket.accept()
        PRIVATE_SOCKET_TABLE[app_name] = private_socket
        get_op_thread = Thread(target=get_operation, args=(private_socket,), daemon=False, name='get_operation: ' + app_name)
        get_op_thread.start()
        client_handle_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_handle_socket.bind((PROXY_ADDRESS, bind_port))
        client_handle_socket.listen(20)
        client_accept_thread = Thread(target=client_accept, args=(client_handle_socket, app_name, ), daemon=False, name='client_accept_thread: ' + app_name)
        return json.dumps(packet.packet(op_enum.OP_SUCCESS, op_enum.DES_SUCCESS, 'APP \"' + app_name + '\" created', app_name, None))
    except Exception as err:
        return json.dumps(packet.packet(op_enum.OP_FAILED, op_enum.DES_FAILED, str(err), app_name, None))



if __name__ == '__main__':
    try:
        flask_port = int(sys.argv[1])
    except Exception as err:
        logging.info('Please input the proxy app console port number')
        logging.debug(err)
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((PROXY_ADDRESS, PROXY_PORT))
    proxy_socket.listen(20)
    app.run(host='0.0.0.0', port=flask_port, debug=True)

