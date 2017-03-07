# -*- coding: utf-8 -*-

class memoized_property(object):

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        if doc is None and fget is not None and hasattr(fget, "__doc__"):
            doc = fget.__doc__
        self.__get = fget
        self.__set = fset
        self.__del = fdel
        self.__doc__ = doc
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
        if self.__set is None:
            raise AttributeError, "can't set attribute"
        delattr(inst, self._attr_name)
        return self.__set(inst, value)

    def __delete__(self, inst):
        if self.__del is None:
            raise AttributeError, "can't delete attribute"
        delattr(inst, self._attr_name)
        return self.__del(inst)


def memoized_property_set(inst, func_name, value):
    if isinstance(func_name, basestring):
        property_name = get_cache_name(func_name)
    elif hasattr(func_name, 'func_name'):
        property_name = get_cache_name(func_name.func_name)
    else:
        raise
    setattr(inst, property_name, value)

def memoized_property_delete(inst, func_name):
    if isinstance(func_name, basestring):
        property_name = get_cache_name(func_name)
    elif hasattr(func_name, 'func_name'):
        property_name = get_cache_name(func_name.func_name)
    else:
        raise
    try:
        delattr(inst, property_name)
    except AttributeError:
        pass

def get_cache_name(func_name):
    return "_%s_cache" % func_name
