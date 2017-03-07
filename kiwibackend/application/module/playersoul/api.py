# -*- coding: utf-8 -*-
from soul.models import Soul
from module.utils import is_digits

def acquire_soul(player, soul_or_soul_id, number=1,  info="", **argvs):
    ''' 
    获取灵魂碎片
    '''
    if isinstance(soul_or_soul_id, Soul):
        soul_id = soul_or_soul_id.pk
    elif is_digits(int(soul_or_soul_id)):
        soul_id = int(soul_or_soul_id)

    _, playersoul = player.souls.get_or_create(soul_id, obj_id = soul_id, **argvs) 
    playersoul.add(number, info)

    player.update_soul(playersoul, True)

    return playersoul
