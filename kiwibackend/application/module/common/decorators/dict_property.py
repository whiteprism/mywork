# -*- coding: utf-8 -*-

class dict_property(object):

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.__get = fget
        if fget is not None:
            self._attr_name = get_cache_name(fget.func_name)
            self._attr_name_touch_db = get_touch_db_name(fget.func_name)
    
    def __get__(self, inst, type=None):
        if inst is None:
            return self
        if self.__get is None:
            raise AttributeError, "unreadable attribute"
        
        if not hasattr(inst, self._attr_name_touch_db):
            result = self.__get(inst)
            inst._modify_datas[self._attr_name] = result
            #setattr(inst, self._attr_name, result)
            setattr(inst, self._attr_name_touch_db, True)
        return inst._modify_datas[self._attr_name]
    
    def __set__(self, inst, value):
        inst._modify_datas[self._attr_name] = value

def dict_property_get(func_name):
    def _func(inst, key, suffix="s"):
        if hasattr(func_name, 'func_name'):
            property_name = func_name.func_name
        else:
            raise
        property_dict_name = "%s%s" % (property_name[4:], suffix)
        _datas = {}
        if property_dict_name in inst._modify_datas:
            _datas= inst._modify_datas[property_dict_name]
            
        #_datas = getattr(inst, property_dict_name)
        if key not in _datas:
            _data = func_name(inst, key)
            if _data:
                _datas[key] = _data
                #setattr(inst, property_dict_name, _datas)
                inst._modify_datas[property_dict_name] = _datas

        return _datas.get(key, None)
    return _func


def get_cache_name(func_name):
    return "%s" % func_name

def get_touch_db_name(func_name):
    return "_%s_touch_db" % func_name
