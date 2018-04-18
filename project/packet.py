import json

def packet(op_code, op_describe, msg, app_name, client_port=0):
    packet_dict = {}
    packet_dict['op_code'] = op_code
    packet_dict['op_describe'] = op_describe
    packet_dict['msg'] = msg
    packet_dict['app_name'] = app_name
    packet_dict['client_port'] = client_port
    return packet_dict
