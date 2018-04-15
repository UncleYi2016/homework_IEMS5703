OP_SUCCESS = 10000
OP_BUILD_CONNECTION = 10001
OP_FAILED = 10010
OP_CONNECTION_BROKEN = 10011
OP_NO_PORT = 10020
OP_NO_ADDRESS = 10021
OP_PRIVATE_OPEN = 10030
OP_PRIVATE_CLOSE = 10031


DES_SUCCESS = 'success'
DES_BUILD_CONNECTION = 'build_connection'
DES_FAILED = 'failed'
DES_CONNECTION_BROKEN = 'connection_broken'
DES_NO_PORT = 'no_port'
DES_NO_ADDRESS = 'no_address'
DES_PRIVATE_OPEN = 'private_open'
DES_PRIVATE_CLOSE = 'private_close'



class packet(object):
    op_code = 0
    op_describe = ''
    msg = ''

    packet(self, op_code, op_describe, msg):
        self.op_code = op_code
        self.op_describe = op_describe
        self.msg = msg
