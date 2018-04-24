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
import time
from threading import Thread
from flask import Flask
from flask import request
from flask import json
from flask import render_template

PRIVATE_APP_PORT = 50001
PRIVATE_APP_ADDRESS = '192.168.56.101'
PUBLIC_SERVER_ADDRESS = 'ec2-13-231-5-245.ap-northeast-1.compute.amazonaws.com'   #NEED TO BE SET
REGISTERED_APPS = []
PRIVATE_SOCKET_TABLE = []       # client_address -> private_socket
PUBLIC_SOCKET_TABLE = []        # app_name -> public_socket
REGISTER_IN_WAIT = []           # The app which are waiting for register success
OP_QUEUE = queue.Queue()
OP_PORT = 8001
PROXY_PORT = 8000

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.INFO)
app = Flask(__name__)


def check_hold_connection():
    while True:
        logging.debug(str(len(PRIVATE_SOCKET_TABLE)))
        time.sleep(10)

'''
    Get data from private app and send it to public server as operation
'''
def private_to_public(private_app_socket, client_address, app_name):
    try:
        public_socket = None
        for element in PUBLIC_SOCKET_TABLE:
            if app_name == element['app_name']:
                public_socket = element['public_socket']
        while True:
            msg = core_transmit.get_data(private_app_socket)
            if msg == '':
                logging.debug('DETECT \'\'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                logging.debug('DETECT \'\'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                logging.debug('DETECT \'\'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                logging.debug('DETECT \'\'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                logging.debug('DETECT \'\'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                logging.debug('DETECT \'\'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                logging.debug('DETECT \'\'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                logging.debug('DETECT \'\'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                break
            # After receive data
            data_packet = packet.packet(op_enum.OP_TRANSMIT_DATA, op_enum.DES_TRANSMIT_DATA, msg, app_name, client_address)
            data_packet_json = json.dumps(data_packet)
            logging.debug('generate: ' + str(data_packet_json))
            core_transmit.send_operation(public_socket, data_packet_json)
    except Exception as err:
        logging.debug(err)
    finally:
        private_app_socket.shutdown(socket.SHUT_RDWR)
        private_app_socket.close()
        disconn_packet = packet.packet(op_enum.OP_DISCONNECTED, op_enum.DES_DISCONNECTED, '', app_name, client_address)
        disconn_json = json.dumps(disconn_packet)
        logging.debug('generate: ' + str(disconn_json))
        core_transmit.send_operation(public_socket, disconn_json)
        for element in PRIVATE_SOCKET_TABLE:
            if client_address == element['client_address']:
                PRIVATE_SOCKET_TABLE.remove(element)

'''
    Get operation from private proxy and store into queue
'''
def get_operation(public_socket):
    try:
        while True:
            op = core_transmit.get_operation(public_socket)
            # op = op.strip('[END]')
            if op == '':
                logging.debug('DETECT \'\'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                logging.debug('DETECT \'\'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                logging.debug('DETECT \'\'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                logging.debug('DETECT \'\'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                logging.debug('DETECT \'\'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                logging.debug('DETECT \'\'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                logging.debug('DETECT \'\'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                logging.debug('DETECT \'\'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                break
            elif '[END]' in op:
                ops = op.split('[END]')
                # for i in range(len(ops)):
                #     if i == 0:
                #         ops[i] = ops[i] + '\"}'
                #     elif i != 0 and i < len(ops)-1:
                #         ops[i] = '{\"' + ops[i] + '\"}'
                #     else:
                #         ops[i] = ops[i] = '{\"' + ops[i]
                for each_op in ops:
                     OP_QUEUE.put(each_op)
            else:
                OP_QUEUE.put(op)
            logging.debug('get op(s)')
    except Exception as err:
        logging.debug(err)
        # public_socket.shutdown(socket.SHUT_RDWR)
        # public_socket.close()


def handle_operation():
    while True:
        operation = OP_QUEUE.get()
        omatted_json = json.dumps(json.loads(operation), indent=4)
        logging.debug(omatted_json)
        operation_packet = json.loads(operation)
        op_code = operation_packet['op_code']
        op_describe = operation_packet['op_describe']
        msg = operation_packet['msg']
        app_name = operation_packet['app_name']
        client_address = operation_packet['client_address']
        private_socket = None
        public_socket = None
        for public_socket_element in PUBLIC_SOCKET_TABLE:
            if app_name == public_socket_element['app_name']:
                public_socket = public_socket_element['public_socket']

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
                core_transmit.send_operation(public_socket, response)
            try:
                tmp_private_socket.connect((app_address, app_port))
            except Exception as err:
                failed_op = json.dumps(packet.packet(op_enum.OP_BUILD_CONNECTION_FAILED, op_enum.DES_BUILD_CONNECTION_FAILED, str(err), app_name, client_address))
                core_transmit.send_operation(public_socket, failed_op)
                unregister_app(app_name)
                continue
            private_socket_element = {'client_address': client_address, 'private_socket': tmp_private_socket}
            PRIVATE_SOCKET_TABLE.append(private_socket_element)
            private_to_public_thread = Thread(target=private_to_public, args=(tmp_private_socket, client_address, app_name ), daemon=False, name='private_to_public:'+str(client_address))
            private_to_public_thread.start()
        elif op_code == op_enum.OP_SUCCESS:
            logging.debug(packet.packet(op_code, op_describe, msg, app_name, client_address))
        elif op_code == op_enum.OP_TRANSMIT_DATA:
            for element in PRIVATE_SOCKET_TABLE:
                if client_address == element['client_address']:
                    private_socket = element['private_socket']
            if private_socket != None:
                core_transmit.send_data(private_socket, msg)
        # if client disconnected, close private socket of this client
        elif op_code == op_enum.OP_DISCONNECTED:
            logging.debug(str(op_describe) + ':' + str(client_address))
            for element in PRIVATE_SOCKET_TABLE:
                if client_address == element['client_address']:
                    private_socket = element['private_socket']
                    private_socket.shutdown(socket.SHUT_RDWR)
                    private_socket.close()
                    for element in PRIVATE_SOCKET_TABLE:
                        if client_address == element['client_address']:
                            PRIVATE_SOCKET_TABLE.remove(element)
        elif op_code == op_enum.OP_REGISTER_SUCCESS:
            for in_wait in REGISTER_IN_WAIT:
                if app_name == in_wait['register_app_name']:
                    in_wait['status'] = True
        elif op_code == op_enum.OP_REGISTER_FAILED:
            for in_wait in REGISTER_IN_WAIT:
                if app_name == in_wait['register_app_name']:
                    in_wait['status'] = False
                    in_wait['msg'] = msg


@app.route('/register_app/<app_name>/<app_address>/<int:app_port>/<int:public_server_port>')
def register_app(app_name=None, app_address=None, app_port=None, public_server_port=None):
    if app_name == None or app_address == None or app_port == None or public_server_port == None:
        return 'url must be \"/register_app/<app_name>/<app_address>/<app_port>/<public_server_port>\"'
    for app in REGISTERED_APPS:
        if app_name == app['app_name']:
            return 'This app name has been registered.'
        if app_address == app['app_address'] and app_port == app['app_port']:
            return 'This port has been registered.'
    register_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    register_socket.connect((PUBLIC_SERVER_ADDRESS, OP_PORT))
    register_operation = packet.packet(op_enum.OP_REGISTER_APP, op_enum.DES_REGISTER_APP, str(public_server_port), app_name, None)
    core_transmit.send_operation(register_socket, json.dumps(register_operation)) 
    public_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    public_socket.connect((PUBLIC_SERVER_ADDRESS, PROXY_PORT))
    public_socket_element = {'public_socket': public_socket, 'app_name': app_name}
    PUBLIC_SOCKET_TABLE.append(public_socket_element)
    app_get_op_thread = Thread(target=get_operation, args=(public_socket, ), daemon=False, name='get_operation:'+str(app_name))
    app_get_op_thread.start()
    register_app = {}
    register_app['app_name'] = app_name
    register_app['app_address'] = app_address
    register_app['app_port'] = app_port
    register_app['public_port'] = public_server_port
    register_app['public_socket'] = public_socket
    waiting_register_app = {'register_app_name': register_app['app_name'], 'status': None, 'msg': ''}
    REGISTER_IN_WAIT.append(waiting_register_app)
    waitcount = 200
    while waiting_register_app['status'] == None:
        time.sleep(0.1)
        waitcount -= 1
        if waitcount < 0:
            waiting_register_app['status'] = False
            waiting_register_app['msg'] = 'time out'
        # logging.debug('waiting for register')
    logging.debug(waiting_register_app)
    if waiting_register_app['status'] == True:
        REGISTER_IN_WAIT.remove(waiting_register_app)
    elif waiting_register_app['status'] == False:
        REGISTER_IN_WAIT.remove(waiting_register_app)
        return 'Register failed because of \"' + waiting_register_app['msg'] + '\"'
    REGISTERED_APPS.append(register_app)
    return 'Register success'

@app.route('/unregister_app/<app_name>')
def unregister_app(app_name=None):
    if app_name == None:
        return 'url must be \"unregister_app/<app_name>\"'
    for app in REGISTERED_APPS:
        if app_name == app['app_name']:
            public_socket = app['public_socket']
            public_socket_address = public_socket.getsockname()
            unregister_op = json.dumps(packet.packet(op_enum.OP_UNREGISTER_APP, op_enum.DES_UNREGISTER_APP, str(public_socket_address), app_name, None))
            core_transmit.send_operation(public_socket, unregister_op)
            REGISTERED_APPS.remove(app)
            return 'Unregister success'
    return 'There is no app named \"' + app_name + '\"'

@app.route('/list_app')
def list_app():
    return_list = []
    for element in REGISTERED_APPS:
        return_list.append(element.copy())
    for e in return_list:
        del e['public_socket']
    return str(return_list)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    handle_operation_thread = Thread(target=handle_operation, name='handle_operation_thread')
    handle_operation_thread.start()
    check_hold_connection_thread = Thread(target=check_hold_connection, name='check_hold_connection_thread')
    check_hold_connection_thread.start()
    try:
        port = int(sys.argv[1])
        OP_PORT = int(sys.argv[2])
        PROXY_PORT = int(sys.argv[3])
    except Exception as err:
        logging.debug('Please input the proxy app console port number')
        logging.debug(err)
    app.run(host='0.0.0.0', port=port, debug=True)



    