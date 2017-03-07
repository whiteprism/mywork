# -*- coding: utf-8 -*-
from module.utils import is_digits
from module.common.actionlog import ActionLogWriter
from module.equip.api import get_equip
from equip.models import Equip, EquipFragment

def acquire_equip(player, equip_or_equip_id, info="", **argvs):
    ''' 
    获取装备
    '''
    if isinstance(equip_or_equip_id, Equip):
        equip = equip_or_equip_id
    elif is_digits(equip_or_equip_id):
        equip = get_equip(equip_or_equip_id)
        if not equip:
            return None

    playerequip = player.equips.create(equip_id = equip.id, **argvs) 
    ActionLogWriter.equip_acquire(player, playerequip.pk, equip.id, info)
    player.update_equip(playerequip, True)
    return playerequip

def get_playerhero_equips(player, playerhero):
    return get_playerheroes_equips(player, [playerhero])

def get_playerheroes_equips(player, playerheroes):
    """
    获取playerheroies的装备
    """

    playerequips = []
    for playerhero in playerheroes:
        #获取1-4位的装备
        for i in range(1, 5):
            playerequip_id = playerhero.get_equip(i) 
            if playerequip_id:
                playerequips.append(player.equips.get(playerequip_id))
    return playerequips


def acquire_equipfragment(player, fragment_or_fragment_id, number=1, info="", **argvs):
    """
    获取装备碎片
    """
    if isinstance(fragment_or_fragment_id, EquipFragment):
        equipfragment_id = fragment_or_fragment_id.pk
    elif is_digits(int(fragment_or_fragment_id)):
        equipfragment_id = int(fragment_or_fragment_id)

    _, playerequipfragment = player.equipfragments.get_or_create(equipfragment_id, obj_id=equipfragment_id, **argvs)
    playerequipfragment.add(number, info)
    player.update_equipfragment(playerequipfragment, True)
    
    return playerequipfragment
