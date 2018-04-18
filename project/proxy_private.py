import core_transmit
import socket
import logging
import sys
import packet
import op_enum
import queue
import urllib
import urllib.request
import urllib.parse
from threading import Thread
from flask import Flask
from flask import request
from flask import json

PRIVATE_APP_PORT = 50001
PRIVATE_APP_ADDRESS = '192.168.56.101'
PUBLIC_SERVER_ADDRESS = 'ec2-13-231-5-245.ap-northeast-1.compute.amazonaws.com'   #NEED TO BE SET
PUBLIC_SERVER_PORT = 8000
REGISTERED_APPS = []
PRIVATE_SOCKET_TABLE = {}
OP_QUEUE = queue.Queue()

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.DEBUG)
app = Flask(__name__)

'''
    Get data from private app and send it to public server as operation
'''
def private_to_public(private_app_socket, client_address):
    try:
        while True:
            msg = core_transmit.get_data(private_app_socket)
            if msg == '':
                continue
            # After receive data
            data_packet = packet.packet(op_enum.OP_TRANSMIT_DATA, op_enum.DES_TRANSMIT_DATA, msg, app_name, client_address)
            data_packet_json = json.dumps(data_packet)
            logging.debug('generate: ' + str(data_packet_json))
            core_transmit.send_operation(pri_sock, data_packet_json)
    except Exception as err:
        logging.debug(err)
        s_sock.shutdown(socket.SHUT_RDWR)
        s_sock.close()
        

'''
    Get operation from private proxy and store into queue
'''
def get_operation(public_socket):
    try:
        while True:
            op = core_transmit.get_operation(pri_sock)
            if op == '':
                continue
            OP_QUEUE.put(op)
    except Exception as err:
        logging.debug(err)
        pri_sock.shutdown(socket.SHUT_RDWR)
        pri_sock.close()


def handle_operation():
    while True:
        operation = OP_QUEUE.get()
        logging.debug('operation get: ' + operation)
        operation_packet = json.loads(operation)
        op_code = operation_packet['op_code']
        op_describe = operation_packet['op_describe']
        msg = operation_packet['msg']
        app_name = operation_packet['app_name']
        client_address = operation_packet['client_address']
        '''
        proceduce operation
        '''
        if op_code == op_enum.OP_BUILD_CONNECTION:
            tmp_private_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            for app in REGISTERED_APPS:
                if app_name == app['app_name']:
                    app_address = app['app_address']
                    app_port = app['app_port']
            if app_name == None or app_port == None:
                response = json.dumps(packet.packet(op_enum.OP_FAILED, op_enum.DES_FAILED, 'No such app', app_name, client_address))
                logging.debug(response)
                core_transmit.send_operation(response)
            tmp_private_socket.connect((app_address, app_port))
            PRIVATE_SOCKET_TABLE[client_address] = tmp_private_socket
            private_to_public_thread = Thread(target=private_to_public, args=(client_element['private_socket'], client_element['client_address'], ), daemon=False, name='private_to_public:'+str(client_address))
            get_data_thread.start()
            # Tell public server that private connection is build
            response_packet = packet.packet(op_enum.OP_SUCCESS, op_enum.DES_SUCCESS, 'App socket build success', app_name, client_address)
            response_json = json.dumps(response_packet)
            core_transmit.send_operation(public_socket, response_json)
        elif op_code == op_enum.OP_SUCCESS:
            logging.debug(packet.packet(op_code, op_describe, msg, app_name, client_address))
        elif op_code == op_enum.OP_TRANSMIT_DATA:
            private_socket = PRIVATE_SOCKET_TABLE[client_address]
            core_transmit.send_data(private_socket, msg)

@app.route('/register_app/<app_name>/<app_address>/<int:app_port>/<int:public_server_port>/<int:op_port>')
def register_app(app_name=None, app_address=None, app_port=None, public_server_port=None, op_port=None):
    if app_name == None or app_address == None or app_port == None or public_server_port == None:
        return 'url must be \"/register_app/<app_name>/<app_address>/<app_port>/<public_server_port>\"'
    for app in REGISTERED_APPS:
        if app_name == app['app_name']:
            return 'This app name has been registered.'
        if app_port == app['app_port']:
            return 'This port has been registered.'
    register_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    register_socket.connect((PUBLIC_SERVER_ADDRESS, op_port))
    register_operation = packet.packet(op_enum.OP_REGISTER_APP, op_enum.DES_REGISTER_APP, str(public_server_port), app_name, None)
    core_transmit.send_operation(register_socket, json.dumps(register_operation)) 
    public_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    public_socket.connect((PUBLIC_SERVER_ADDRESS, PUBLIC_SERVER_PORT))
    app_get_op_thread = Thread(target=get_operation, args=(public_socket, ), daemon=False, name='get_operation:'+str(app_name))
    app_get_op_thread.start()
    registered_app = {}
    registered_app['app_name'] = app_name
    registered_app['app_address'] = app_address
    registered_app['app_port'] = app_port
    registered_app['public_socket'] = public_socket
    REGISTERED_APPS.append(registered_app)
    return 'Register success'

@app.route('/unregister_app/<app_name>')
def unregister_app(app_name=None):
    if app_name == None:
        return 'url must be \"unregister_app/<app_name>\"'
    for app in REGISTERED_APPS:
        if app_name == app['app_name']:
            REGISTERED_APPS.remove(app)
            return 'Unregister success'
    
    return 'There is no app named \"' + app_name + '\"'

@app.route('/list_app')
def list_app():
    return str(REGISTERED_APPS)

if __name__ == '__main__':
    handle_operation_thread = Thread(target=handle_operation, name='handle_operation_thread')
    handle_operation_thread.start()
    try:
        port = int(sys.argv[1])
    except Exception as err:
        logging.info('Please input the proxy app console port number')
        logging.debug(err)
    app.run(host='0.0.0.0', port=port, debug=True)



    