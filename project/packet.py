import json

def packet(op_code, op_describe, msg):
    packet_dict = {}
    packet_dict.op_code = op_code
    packet_dict.op_describe = op_describe
    packet_dict.msg = msg
    return packet_dict
