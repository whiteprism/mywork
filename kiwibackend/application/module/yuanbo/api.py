# -*- coding: utf-8 -*-

from yuanbo.models import Yuanbo

def update_yuanbo_cache():
    Yuanbo.create_cache()

def get_yuanbos():
    yuanbo_list = Yuanbo.get_all_list()
    yuanbo_list = sorted(yuanbo_list,lambda x,y: cmp(x.id, y.id), reverse=True)
    return yuanbo_list

def get_yuanbo(pk):
    """
    获取元宝
    """
    return Yuanbo.get(int(pk))
