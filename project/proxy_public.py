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
from threading import Thread
from flask import Flask
from flask import request
from flask import json
PROXY_ADDRESS = '0.0.0.0'
PROXY_PORT = 8000
CLIENT_HANDLE_PORT = 60003
CLIENT_SOCKETS = []
CLIENT_SOCKETS_PRIVATE_PORT = {}
CLIENT_PRIVATE_PORT = {}
BIND_APP = {}



logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.DEBUG)
app = Flask(__name__)

def client_to_private(c_sock, c_port, pri_sock):
    try:
        while True:
            msg = core_transmit.get_data(c_sock)
            # After receive data
            data_packet = packet.packet(op_enum.OP_SUCCESS, op_enum.DES_SUCCESS, msg, c_port)
            data_packet_json = json.dumps(data_packet)
            logging.debug('generate: ' + str(data_packet_json))
            core_transmit.send_operation(pri_sock, data_packet_json)
    except Exception as err:
        logging.debug(err)
        c_sock.shutdown(socket.SHUT_RDWR)
        c_sock.close()

def client_accept(client_handle_socket):
    while True:
        (client_socket, client_address) = client_handle_socket.accept()

@app.route('/get_operation', method=['POST'])
def get_operation():
    if request.method == 'POST':
        op_code = request.form['op_code']
        op_describe = request.form['op_describe']
        msg = request.form['msg']
        app_name = request.form['app_name']
        client_port = request.form['client_port']
        '''
        procedure operation
        '''

    else:
        return ''

@app.route('/register_app/<app_name>/<int:bind_port>')
def register_app(app_name=None, bind_port=None):
    if BIND_APP.has_key(app_name):
        return json.dumps(packet.packet(op_enum.OP_FAILED, op_enum.DES_FAILED, 'APP \"' + app_name + '\" has already exist', app_name, None))
    try:
        client_handle_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_handle_socket.bind((PROXY_ADDRESS, CLIENT_HANDLE_PORT))
        client_handle_socket.listen(20)
        client_accept_thread = Thread(target=client_accept, args=(client_handle_socket,), daemon=False, name='client_accept_thread: ' + app_name)
        return json.dumps(packet.packet(op_enum.OP_SUCCESS, op_enum.DES_SUCCESS, 'APP \"' + app_name + '\" created', app_name, None))
    except Exception as err:
        return json.dumps(packet.packet(op_enum.OP_FAILED, op_enum.DES_FAILED, str(err), app_name, None))
def get_op_from_private(pri_sock):
    try:
        while True:
            logging.debug('start get_op')
            data = core_transmit.get_operation(pri_sock)
            logging.debug('end get_op')
            data = data.decode('utf-8')
            if data == '':
                break
            data_packet = json.loads(data)
            logging.debug('get: ' + str(data))
            if data_packet['op_code'] == op_enum.OP_SUCCESS:
                msg_to_client = data_packet['msg']
                port_to_client = data_packet['port']
                socket_to_client = CLIENT_SOCKETS_PRIVATE_PORT[port_to_client]
                core_transmit.send_data(socket_to_client, msg_to_client)
            elif data_packet['op_code'] == op_enum.OP_BUILD_OK:
                client_port = data_packet['port']
                private_port = data_packet['msg']
                for c in CLIENT_SOCKETS:
                    logging.debug('getpeername()[1]: ' + str(c.getpeername()[1]))
                    if c.getpeername()[1] == client_port:
                        CLIENT_SOCKETS_PRIVATE_PORT[private_port] = c
                        CLIENT_PRIVATE_PORT[client_port] = private_port
    except Exception as err:
        pri_sock.shutdown(socket.SHUT_RDWR)
        pri_sock.close()

if __name__ == '__main__':
    tmp_client_private_port = CLIENT_PRIVATE_PORT.copy()
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((PROXY_ADDRESS, PROXY_PORT))
    proxy_socket.listen(20)
    (private_socket, private_address) = proxy_socket.accept()
    logging.debug('Accept private app %s', private_address)
    get_op_from_private_thread = Thread(target=get_op_from_private, args=(private_socket,), daemon=False, name='get_op_from_private')
    get_op_from_private_thread.start()
    
    
        CLIENT_SOCKETS.append(client_socket)
        logging.debug('Accept client %s', client_address)
        client_port = client_address[1]
        msg = packet.packet(op_enum.OP_BUILD_CONNECTION, op_enum.DES_BUILD_CONNECTION, '', client_port)
        logging.debug(json.dumps(msg))
        core_transmit.send_operation(private_socket, json.dumps(msg))
        logging.debug('client : ' + str(client_address))
        while tmp_client_private_port == CLIENT_PRIVATE_PORT:
            logging.debug('same')
            logging.debug(tmp_client_private_port)
            logging.debug(CLIENT_PRIVATE_PORT)
            time.sleep(1)
            pass
        logging.debug('not same')
        tmp_client_private_port = CLIENT_PRIVATE_PORT.copy()
        logging.debug('CLIENT_PRIVATE_PORT[client_port]: ' + str(CLIENT_PRIVATE_PORT[client_port]))
        client_to_private_thread = Thread(target=client_to_private, args=(client_socket, CLIENT_PRIVATE_PORT[client_port], private_socket, ), daemon=False, name='client_to_private')
        client_to_private_thread.start()