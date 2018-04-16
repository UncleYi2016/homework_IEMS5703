import json

def packet(op_code, op_describe, msg, port=0):
    packet_dict = {}
    packet_dict['op_code'] = op_code
    packet_dict['op_describe'] = op_describe
    packet_dict['msg'] = msg
    packet_dict['port'] = port
    return packet_dict
