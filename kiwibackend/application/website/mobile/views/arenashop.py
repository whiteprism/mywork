# -*- encoding:utf8 -*-
from decorators import require_player, handle_common
from module.common.static import Static, AlertID
from module.arenashop.api import get_arenashop
from module.playeritem.api import acquire_item
from module.playerartifact.api import acquire_artifactfragment
from module.common.middleware import ErrorException, AlertHandler
from module.playersoul.api import acquire_soul
from module.playerequip.api import acquire_equipfragment

@handle_common
@require_player
def honorShopBuy(request, response):
    """
    荣誉商店兑换
    """
    arenashop_id  = getattr(request.logic_request, "honorShopId", 0)

    player = request.player

    #检查竞技场开放状态
    if not player.isOpenArena:
        return response

    arenashop = get_arenashop(arenashop_id)
    if not arenashop:
        raise ErrorException(player, u"honorShopBuy:arenashop(%s) no existed" % arenashop_id)

    info = u"荣誉商店兑换:%s" % arenashop_id

    if not player.arenashop.can_exchange(arenashop_id):
        response.common_response.player.set("honorShop", player.arenashop.to_dict())
        AlertHandler(player, response, AlertID.ALERT_ARENASHOP_CAN_NO_EXCHANGE, u"honorShopBuy:arenashop(%s) can not buyed buyItem(%s) shopItem(%s)" % (arenashop_id, str(player.arenashop.buyItem), str(player.arenashop.shopItem)))
        return response

    if player.PVP.honor < arenashop.score:
        response.common_response.player.set("arena", player.PVP.to_dict())
        AlertHandler(player, response, AlertID.ALERT_HONOR_NOT_ENOUGH, u"honorShopBuy:arenashop(%s) can not buyed honor(%s) playerhonor(%s)" % (arenashop_id, arenashop.score, player.PVP.honor))
        return response

    player.PVP.sub_honor(arenashop.score, info=info)
    player.arenashop.exchange(arenashop.pk)

    if arenashop.is_item:
        acquire_item(player, arenashop.itemId, number=arenashop.count, info=info)
    elif arenashop.is_equipfragment:
        acquire_equipfragment(player, arenashop.itemId, arenashop.count, info=info)
    elif arenashop.is_artifactfragment:
        acquire_artifactfragment(player, arenashop.itemId, number=arenashop.count, info=info)
    elif arenashop.is_soul:
        acquire_soul(player, arenashop.itemId, number=arenashop.count, info=info)
    else:
        raise ErrorException(player, u"honorShopBuy:arenashop(%s) is error" % (arenashop_id))


    response.common_response.player.set("honorShop", player.arenashop.to_dict())
    # 这里只是为了更新荣誉点数，因为买东西消耗了这个
    response.common_response.player.set("arena", player.PVP.to_dict())
    return response

'''
@handle_common
@require_player
def honorShopInit(request, response):
    """
    荣誉商店刷新
    """
    player = request.player
    #onlyDia = getattr(request.logic_request, "onlyUseDia", 0)
    autoRefresh = getattr(request.logic_request, "autoRefresh", 1)

    if autoRefresh:
        player.arenashop.refresh_auto()
    else:

        if not player.arenashop.can_refresh_manual():
            return response

        #if onlyDia:
        if player.yuanbo < Static.HONORSHOP_REFRESH_YUANBO:
            return response

        player.sub_yuanbo(Static.HONORSHOP_REFRESH_YUANBO, info=u"荣誉商店刷新钻石刷新")
        #else:
        #    if player.PVP.honor < Static.HONORSHOP_REFRESH_HONOR:
        #        return response
        #    else:
        #        player.PVP.sub_honor(Static.HONORSHOP_REFRESH_HONOR, info=u"荣誉商店荣誉刷新")
        player.arenashop.refresh_manual()
    response.common_response.player.set("arena", player.PVP.to_dict())
    response.common_response.player.set("honorShop", player.arenashop.to_dict())

    return response
'''
