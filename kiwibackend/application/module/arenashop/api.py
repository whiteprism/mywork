# -*- coding: utf-8 -*-
from arenashop.models import ArenaShop

def update_arenashop_cache():
    ArenaShop.create_cache()

def get_arenashop(pk):
    return ArenaShop.get(int(pk))

def get_arenashops():
    return ArenaShop.get_all_list()
