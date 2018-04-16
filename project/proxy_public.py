import core_transmit
import socket
import logging
import packet
import op_enum
import json
from threading import Thread
PROXY_ADDRESS = '0.0.0.0'
PROXY_PORT = 8000
CLIENT_HANDLE_PORT = 60003
CLIENT_SOCKETS = []
CLIENT_SOCKETS_PRIVATE_PORT = {}



logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
    level=logging.DEBUG)

def client_to_private(c_sock, c_port, p_sock):
    try:
        while True:
            msg = core_transmit.get_data(c_sock)
            # After receive data
            data_packet = packet.packet(op_enum.OP_SUCCESS, op_enum.DES_SUCCESS, msg, c_port)
            data_packet_json = json.dumps(data_packet)
            core_transmit.send_data(p_sock, data_packet_json)
    except Exception as err:
        logging.debug(err)
        c_sock.shutdown(socket.SHUT_RDWR)
        c_sock.close()

def get_op_from_private(pri_sock):
    try:
        while True:
            data = core_transmit.get_operation(pri_sock)
            data_packet = json.loads(data)
            if data_packet['op_code'] == op_enum.OP_SUCCESS:
                msg_to_client = data_packet['msg']
                port_to_client = data_packet['port']
                socket_to_client = CLIENT_SOCKETS_PRIVATE_PORT[port_to_client]
                core_transmit.send_data(socket_to_client, msg_to_client)
            elif data_packet['op_code'] == op_enum.OP_BUILD_OK:
                client_port = data_packet['port']
                private_port = data_packet['msg']
                for c in CLIENT_SOCKETS:
                    logging.debug('.getsockname()[1]: ' + str(c.getsockname()[1]))
                    if c.getsockname()[1] == client_port:
                        CLIENT_SOCKETS_PRIVATE_PORT[client_port] = c
    except Exception as err:
        pri_sock.shutdown(socket.SHUT_RDWR)
        pri_sock.close()

if __name__ == '__main__':
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((PROXY_ADDRESS, PROXY_PORT))
    proxy_socket.listen(20)
    (private_socket, private_address) = proxy_socket.accept()
    logging.debug('Accept private app %s', private_address)
    get_op_from_private_thread = Thread(target=get_op_from_private, args=(private_socket,), daemon=False)
    get_op_from_private_thread.start()
    client_handle_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_handle_socket.bind((PROXY_ADDRESS, CLIENT_HANDLE_PORT))
    client_handle_socket.listen(20)
    while True:
        (client_socket, client_address) = client_handle_socket.accept()
        logging.debug('Accept client %s', client_address)
        client_port = client_address[1]
        msg = packet.packet(op_enum.OP_BUILD_CONNECTION, op_enum.DES_BUILD_CONNECTION, '', client_port)
        logging.debug(json.dumps(msg))
        core_transmit.send_operation(private_socket, json.dumps(msg))
        logging.debug('client : ' + str(client_address))
        logging.debug('private : ' + str(tmp_proxy_address))
        CLIENT_SOCKETS.append(client_socket)
        