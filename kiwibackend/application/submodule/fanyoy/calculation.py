# -*- coding: utf-8 -*-
#計算関係

import random


def choice_index_ratio(ratio_list):
    """ 
    ratio_listの割合を考慮し、どれか一つを選ぶ。
    ratio_listは整数のリスト。
    10,10,80 のリストの場合、80%の確率で 2 が返される。
    """
        
    total = 0 
    total_list = []
    for ratio in ratio_list:
        total += int(ratio)
        total_list.append(total)
    r = random.randint(1,total)
        
    for i in xrange(len(total_list)):
        if total_list[i] >= r:
            return i
    return None #返らない
