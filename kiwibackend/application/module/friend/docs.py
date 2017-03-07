# -*- coding: utf-8 -*-
from mongoengine import *
from common.docs import PlayerRelationBase
from common.decorators.memoized_property import memoized_property
from common.static import Static

class FriendBase(PlayerRelationBase):
    ids = ListField(default=[])
    meta = {
        'abstract': True,
    }

    def check(self, target_player_id):
        target_player_id = int(target_player_id)
        return target_player_id in self.ids

    def add(self, target_player_id):
        target_player_id = int(target_player_id)
        self.ids.append(target_player_id)

    def del(self, target_player_id):
        target_player_id = int(target_player_id)
        self.ids.remove(target_player_id)
    
class FriendRequests(FriendBase):
    """
    请求好友列表
    """
    pass

class FriendRequesteds(FriendBase)
    """
    被请求好友列表
    """
    pass

class Friends(FriendBase)
    """
    好友列表
    """
    pass
    
