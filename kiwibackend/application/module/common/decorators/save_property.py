# -*- coding: utf-8 -*-

class save_property(object):
    def __init__(self, fget=None):
        self.__get = fget
        if fget is not None:
            self._attr_name = get_cache_name(fget.func_name)
    
    def __get__(self, inst, type=None):
        if inst is None:
            return self
        if self.__get is None:
            raise AttributeError, "unreadable attribute"
        
        if not hasattr(inst, self._attr_name):
            result = self.__get(inst)
            setattr(inst, self._attr_name, result)
        return getattr(inst, self._attr_name)
    
    def __set__(self, inst, value):
        setattr(inst, self._attr_name, value)

def get_cache_name(func_name):
    return "_%s" % func_name
