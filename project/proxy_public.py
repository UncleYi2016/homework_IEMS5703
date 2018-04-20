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
import sys
from threading import Thread
PROXY_ADDRESS = '0.0.0.0'
PROXY_PORT = 8000
PROXY_SOCKET = None
CLIENT_ADDRESS_TABLE = []       # client_address -> client_socket
PRIVATE_SOCKET_TABLE = []       # app_name -> private_socket
BIND_APP = {}
OP_QUEUE = queue.Queue()



logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.DEBUG)

'''
    Get operation from private proxy and store into queue
'''
def get_operation(private_sock):
    try:
        while True:
            op = core_transmit.get_operation(private_sock)
            # op = op.strip('[END]')
            if op == '':
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
    except Exception as err:
        logging.debug(err)
        private_sock.shutdown(socket.SHUT_RDWR)
        private_sock.close()

'''
    Handle operation which get from queue
'''
def handle_operation():
    while True:
        operation = OP_QUEUE.get()
        logging.info('handle op')
        omatted_json = json.dumps(json.loads(operation), indent=4)
        logging.debug(omatted_json)
        try:
            operation_packet = json.loads(operation)
        except Exception as err:
            logging.info(operation)
            logging.info(err)
        op_code = operation_packet['op_code']
        op_describe = operation_packet['op_describe']
        msg = operation_packet['msg']
        app_name = operation_packet['app_name']
        client_address = operation_packet['client_address']
        client_socket = None
        if op_code == op_enum.OP_REGISTER_APP:
            logging.debug('REGISTER')
            bind_port = int(msg)
            register_app(app_name, bind_port)
        elif op_code == op_enum.OP_TRANSMIT_DATA:
            logging.debug('CLIENT_ADDRESS_TABLE!!!!!!!!' + str(CLIENT_ADDRESS_TABLE))
            for element in CLIENT_ADDRESS_TABLE:
                if client_address == element['client_address']:
                    client_socket = element['client_socket']
            if client_socket != None:
                logging.debug('sent to client')
                core_transmit.send_data(client_socket, msg)
        # if private socket disconnected, close client of this private socket
        elif op_code == op_enum.OP_DISCONNECTED:
            logging.debug(str(op_describe) + ':' + str(client_address))
            for element in CLIENT_ADDRESS_TABLE:
                if client_address == element['client_address']:
                    client_socket = element['client_socket']
                    client_socket.shutdown(socket.SHUT_RDWR)
                    client_socket.close()
                    for element in CLIENT_ADDRESS_TABLE:
                        if client_address == element['client_address']:
                            CLIENT_ADDRESS_TABLE.remove(element)

'''
    Receive client data and transmit to private proxy
'''
def client_to_private(c_sock, c_address, pri_sock, app_name):
    try:
        while True:
            msg = core_transmit.get_data(c_sock)
            if msg == '':
                break
            # After receive data
            data_packet = packet.packet(op_enum.OP_TRANSMIT_DATA, op_enum.DES_TRANSMIT_DATA, msg, app_name, c_address)
            data_packet_json = json.dumps(data_packet)
            logging.debug('generate: ' + str(data_packet_json))
            core_transmit.send_operation(pri_sock, data_packet_json)
    except Exception as err:
        logging.debug(err)
    finally:
        logging.info('Client disconnected')
        c_sock.shutdown(socket.SHUT_RDWR)
        c_sock.close()
        disconn_packet = packet.packet(op_enum.OP_DISCONNECTED, op_enum.DES_DISCONNECTED, '', app_name, c_address)
        disconn_json = json.dumps(data_packet)
        logging.debug('generate: ' + str(disconn_json))
        core_transmit.send_operation(pri_sock, disconn_json)
        for element in CLIENT_ADDRESS_TABLE:
            if c_address == element['client_address']:
                CLIENT_ADDRESS_TABLE.remove(element)

'''
    Used to accept client connection
'''
def client_accept(client_handle_socket, app_name):
    while True:
        private_socket = None
        (client_socket, client_address) = client_handle_socket.accept()
        logging.info(str(client_address) + ' Connected')
        logging.debug('accept client: ' + str(client_address))
        c_address = json.loads(json.dumps(client_address))
        client_address_element = {'client_address': c_address, 'client_socket': client_socket}
        CLIENT_ADDRESS_TABLE.append(client_address_element)
        # private_socket_element = {'app_name': app_name, 'private_socket': private_socket}
        # PRIVATE_SOCKET_TABLE.append(private_socket_element)
        for element in PRIVATE_SOCKET_TABLE:
            logging.debug(element)
            if app_name == element['app_name']:
                private_socket = element['private_socket']
        build_connect_packet = json.dumps(packet.packet(op_enum.OP_BUILD_CONNECTION, op_enum.DES_BUILD_CONNECTION, '', app_name, client_address))
        if private_socket != None:
            core_transmit.send_operation(private_socket, build_connect_packet)
            client_to_private_thread = Thread(target=client_to_private, args=(client_socket, client_address, private_socket, app_name), daemon=False, name=app_name + str(client_address))
            client_to_private_thread.start()

'''
    Register APP
'''
def register_app(app_name=None, bind_port=None):
    if app_name in BIND_APP:
        return json.dumps(packet.packet(op_enum.OP_FAILED, op_enum.DES_FAILED, 'APP \"' + app_name + '\" has already exist', app_name, None))
    BIND_APP[app_name] = bind_port
    try:
        (private_socket, private_address) = PROXY_SOCKET.accept()
        logging.debug('accept address: ' + str(private_address))
        private_socket_element = {'app_name': app_name, 'private_socket': private_socket}
        PRIVATE_SOCKET_TABLE.append(private_socket_element)
        get_op_thread = Thread(target=get_operation, args=(private_socket,), daemon=False, name='get_operation: ' + app_name)
        get_op_thread.start()
        client_handle_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_handle_socket.bind((PROXY_ADDRESS, bind_port))
        client_handle_socket.listen(20)
        logging.debug(BIND_APP)
        logging.debug(PRIVATE_SOCKET_TABLE)
        client_accept_thread = Thread(target=client_accept, args=(client_handle_socket, app_name, ), daemon=False, name='client_accept_thread: ' + app_name)
        client_accept_thread.start()
        return json.dumps(packet.packet(op_enum.OP_SUCCESS, op_enum.DES_SUCCESS, 'APP \"' + app_name + '\" created', app_name, None))
    except Exception as err:
        return json.dumps(packet.packet(op_enum.OP_FAILED, op_enum.DES_FAILED, str(err), app_name, None))



if __name__ == '__main__':
    get_op_port = int(sys.argv[1])
    proxy_port = int(sys.argv[2])
    handle_operation_thread = Thread(target=handle_operation, name='handle_operation_thread')
    handle_operation_thread.start()
    get_op_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    get_op_socket.bind(('0.0.0.0', get_op_port))
    get_op_socket.listen(20)
    PROXY_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PROXY_SOCKET.bind(('0.0.0.0', proxy_port))
    PROXY_SOCKET.listen(20)
    while True:
        (register_socket, register_address) = get_op_socket.accept()
        get_register_thread = Thread(target=get_operation, args=(register_socket,), daemon=False, name='get_register_thread')
        get_register_thread.start()
    
    


