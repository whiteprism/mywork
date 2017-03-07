# -*- coding: utf-8 -*-
from soul.models import Soul

def update_soul_cache():
    Soul.create_cache()

def get_soul(pk):
    return Soul.get(int(pk))

def get_souls():
    return Soul.get_all_list()
