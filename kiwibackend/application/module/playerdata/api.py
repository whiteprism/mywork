# -*- coding: utf-8 -*-
from playerdata.docs import PlayerData

def get_playerdata(player, keys=[], save=True):
    _keys = []
    for key in keys:
        _keys.append("%s_bin" % key)

    playerdata = PlayerData.get(player.pk, _keys)
    if not playerdata:
        # 这里必须指明 id = XXX 如果没有说明就会报错,这是一个字典形式那种参数。
        playerdata = PlayerData.create(id=player.pk)
    playerdata.player = player
    return playerdata
