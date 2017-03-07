#-*- coding:utf-8 -*-
from levelconf.models import LevelConf, LevelUpReward

def update_level_cache():
    LevelConf.create_cache()
    LevelUpReward.create_cache()

def get_level(level):
    '''
    根据等级获取配置
    '''
    return LevelConf.get(level)

def get_levels():
    '''
    获取所有等级配置
    '''
    return LevelConf.get_all_list()
