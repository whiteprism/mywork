# -*- encoding:utf8 -*-
class BaseMessage(object):
    def __init__(self, *args, **argvs):
        self.active_properties = [] 
        #pass

    def for_request(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def set(self, property_name, value):

        if hasattr(self, property_name):
            if property_name not in self.active_properties:
                self.active_properties.append(property_name)

        setattr(self, property_name, value)

    def for_response(self):
        _data = {} 
        for _property_name in self.active_properties:
        #for _property_name in self.__dict__:
            _property = getattr(self, _property_name)

            if isinstance(_property, BaseMessage):
                _data[_property_name] = _property.for_response()
            elif isinstance(_property, list):
                _list = []
                for _p in _property:
                    if isinstance(_p, BaseMessage):
                        _list.append(_p.for_response())
                    else:
                        _list.append(_p)
                _data[_property_name]  = _list
                
            else:
                _data[_property_name] = _property
                
        return _data
