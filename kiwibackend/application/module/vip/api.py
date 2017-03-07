# -*- coding: utf-8 -*-
from vip.models import Vip, VipReward

def update_vip_cache():
    Vip.create_cache()
    VipReward.create_cache()

def get_vip(pk):
    return Vip.get(int(pk)+1)

def get_vips():
    return Vip.get_all_list()
