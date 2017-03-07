# -*- coding: utf-8 -*-
from friend.docs import FriendRequests, FriendRequesteds, Friends

def get_player_friendrequests(player):
    """
    获取玩家发出邀请
    """
    _, friendrequests = FriendRequests.objects.get_or_create(player_id=player.pk)
    return friendrequests

def get_player_friendrequesteds(player):
    """
    获取玩家被邀请邀请
    """
    _, friendrequesteds = FriendRequesteds.objects.get_or_create(player_id=player.pk)
    return friendrequesteds

def get_player_friends(player):
    """
    获取玩家好友
    """
    _, friends = Friends.objects.get_or_create(player_id=player.pk)
    return friends


