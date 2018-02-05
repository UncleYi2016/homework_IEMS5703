import json

class data_package:
    __data = ''

    def __init__(self):
        pass
    
    def __init__(self, data):
        self.__data = data
    
    def __str__(self):
        return self.__data
    
    def get_data(self):
        return self.__data
    
    def set_data(self, data):
        self.__data = data
    
    def to_json(self):
        return json.dumps(self.__dict__)