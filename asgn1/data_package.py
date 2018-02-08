import json

class data_package:
    data = ''

    def __init__(self):
        pass
    
    def __init__(self, data):
        self.data = data
    
    def __str__(self):
        return self.data
    
    def get_data(self):
        return self.data
    
    def set_data(self, data):
        self.data = data
    
    # def to_json(self):
    #     return json.dumps(self.__dict__)