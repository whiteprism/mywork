# -*- coding: utf-8 -*-
from module.player.api import *

def get_player_by_id_or_str(playerId, severId):
    if len(playerId) >= 8:
        player = Player.objects.get(id=int(short_data.decompress(str.upper(str(playerId)))))
    else:
        player = get_player_by_userid(int(playerId), severId)
    return player

def get_datetime(time_str):
    t = str(time_str)
    try:
        return datetime.datetime.strptime(t, '%Y-%m-%d %H:%M')
    except:
        return False

def get_playerId(playerId, severId):
    if len(playerId) < 8:
        print 'severId:', severId
        player_id = int(severId) * 1000000000 + int(playerId)
    else:
        player_id = int(playerId)
    return player_id
