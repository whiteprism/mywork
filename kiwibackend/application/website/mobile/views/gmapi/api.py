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

def get_item(rewardIdStr):
    pattern = re.compile(r"t(\d+)v?(\d*)c?(\d*)")
    match = pattern.match(rewardIdStr)
    category = 0
    level = 0
    count = 0
    if match:
        category, level, count = match.groups()
        category = int(category) if category else 0
        level = int(level) if level else 0
        count = int(count) if count else 1

    item = (category, count, level)

    return item
