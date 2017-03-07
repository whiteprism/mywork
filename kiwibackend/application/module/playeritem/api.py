# -*- coding: utf-8 -*-
from module.utils import is_digits
from item.models import Item

def acquire_item(player, item_or_item_id, number=1, info="", **argvs):
    ''' 
    获取物品
    '''
    if isinstance(item_or_item_id, Item):
        item_id = item_or_item_id.pk
    elif is_digits(int(item_or_item_id)):
        item_id = int(item_or_item_id)

    _, playeritem = player.items.get_or_create(item_id, obj_id=item_id)
    playeritem.add(number, info)
    player.update_item(playeritem, True)

    return playeritem

def acquire_buyrecord(player, item_or_item_id, number=1, info="", **argvs):
    ''' 
    添加购买记录
    '''
    if isinstance(item_or_item_id, Item):
        item_id = item_or_item_id.pk
    elif is_digits(int(item_or_item_id)):
        item_id = int(item_or_item_id)

    _, playerbuyrecord= player.buyrecords.get_or_create(item_id, item_id = item_id, **argvs)
    playerbuyrecord.buy(player, number, info)
    player.update_buyrecord(playerbuyrecord, True)
    return playerbuyrecord


#def acquire_buytowerrecord(player, item_or_item_id, number=1, info="", **argvs):
#    '''
#    添加购买记录
#    '''
#    if isinstance(item_or_item_id, Item):
#        item_id = item_or_item_id.pk
#    elif is_digits(int(item_or_item_id)):
#        item_id = int(item_or_item_id)
#
#    _, playerbuytowerrecord= player.buytowerrecords.get_or_create(item_id, item_id = item_id,**argvs)
#    playerbuytowerrecord.buy(player, number, info)
#    player.update_buytowerrecord(playerbuytowerrecord, True)
#    return playerbuytowerrecord

