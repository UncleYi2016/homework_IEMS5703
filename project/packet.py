import json

class packet(object):
    op_code = 0
    op_describe = ''
    msg = ''

    def packet(self, op_code, op_describe, msg):
        self.op_code = op_code
        self.op_describe = op_describe
        self.msg = msg
    
    def to_json():
        return json.dumps(self)
