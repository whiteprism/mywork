# -*- coding: utf-8 -*-
from attr.models import *

def update_attr_cache():
    Attr.create_cache()

def get_attr(pk):
    return Attr.get(int(pk))

def get_attrs():
    return Attr.get_all_list()
