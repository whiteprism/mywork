# -*- coding:utf8 -*-
from importlib import import_module

def url(method, action):
    return (action, method)

def patterns(prefix, *args):
    pattern_list = []
    for t in args:
        _url = []
        _url.append(t[0])
        _url.append({
            "view": getattr(import_module(prefix), t[1]),
            "name": t[1]
        })
        pattern_list.append(tuple(_url))
    return pattern_list
