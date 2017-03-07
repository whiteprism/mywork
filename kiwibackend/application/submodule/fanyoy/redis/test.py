# -*- coding: utf-8 -*- 
from dynamic import PlayerDynamicRedisHandler, PlayerDynamicObjectsRedisHandler, PlayerDynamicSetRedisHandler
from static import StaticSetDataRedisHandler, StaticSortedSetDataRedisHandler, StaticDataRedisHandler 
import threading

class TestPlayer(PlayerDynamicRedisHandler):
    """
    测试用例 用户
    """

    def __str__(self):
        return "player:%s---->card(%s,%s,%s)" %(self.player_id, self.card_1,self.card_2,self.card_3)
    
    all_params = {
        "card_1": {"default":0, "type":int},
        "card_2": {"default":0, "type":int},
        "card_3": {"default":0, "type":str},
    }

class TestPlayerObjects(PlayerDynamicObjectsRedisHandler):
    """
    测试用例 用户对象
    """

    def __str__(self):
        return "test"

    all_params = {
        "card_1": {"default":0, "type":int},
        "card_2": {"default":0, "type":int},
        "card_3": {"default":0, "type":str},
    }
    
class TestPlayerSetObjects(PlayerDynamicSetRedisHandler):
    """
    测试用例 用户列表
    """

    def __init__(self, player_id): 
        player_id = int(player_id)
        super(self.__class__, self).__init__(player_id)
