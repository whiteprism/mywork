# -*- encoding:utf8 -*-
from decorators import require_player, handle_common
from module.common.static import Static, AlertID
from module.common.middleware import ErrorException, AlertHandler
from module.mysteryshop.api import get_mysteryshop
from module.rewards.api import reward_send

@handle_common
@require_player
def mysteryShopBuy(request, response):
    """
    神秘商店兑换
    """
    player = request.player
    info = u"神秘商店兑换"
    shop_id  = getattr(request.logic_request, "mysteryShopId", 0)
    #shop_id = int(shop_id)
    shop_item = get_mysteryshop(shop_id)
    if not shop_item:
        raise ErrorException(player, u"mysteryShopBuy:shopitem(%s) no existed" % shop_id)

    if not player.mysteryshop.can_exchange(shop_id):
        response.common_response.player.set("mysteryShop", player.mysteryshop.to_dict())
        AlertHandler(player, response, AlertID.ALERT_MYSTERYSHOP_CAN_NOT_EXCHANGE, u"mysteryShopBuy:shopitem(%s) can not buyed buyItem(%s) shopItem(%s)" % (shop_id, str(player.mysteryshop.buyItem), str(player.mysteryshop.shopItem)))
        return response

    if shop_item.diamond > 0:
        if player.yuanbo < shop_item.diamond:
            AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"mysteryShopBuy:shopitem(%s) can not buyed diamond(%s) playerYuanbo(%s)" % (shop_id, shop_item.diamond, player.yuanbo))
            return response
    else:
        if player.gold < shop_item.gold:
            AlertHandler(player, response, AlertID.ALERT_GOLD_NOT_ENOUGH, u"mysteryShopBuy:shopitem(%s) can not buyed gold(%s) playerCouragePoint(%s)" % (shop_id, shop_item.gold, player.couragepoint))
            return response


    if shop_item.diamond > 0:
        player.sub_yuanbo(shop_item.diamond, info=info)
    else:
        player.sub_gold(shop_item.gold, info=info)

    player.mysteryshop.exchange(shop_item.pk)
    reward_send(player, shop_item.reward, info=u"神秘商店购买")
    response.common_response.player.set("mysteryShop", player.mysteryshop.to_dict())
    return response


@handle_common
@require_player
def mysteryShopInit(request, response):
    """
    神秘商店刷新
    """
    player = request.player
    info = u"神秘商店刷新"

    if player.mysteryshop.refresh_auto():
        pass
    #elif player.mysteryshop.refresh_free():
    #    pass
    else:
        playeritem = player.items.get(Static.ITEM_REFRESH_TICKET_ID)
        if playeritem and playeritem.can_sub(1):
            player.mysteryshop.refresh_ticket()
            playeritem.sub(1, info=info)
        else:

            costYuanbo = player.mysteryshop.refreshCostYuanbo
            if player.yuanbo < costYuanbo:
                AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"mysteryShopInit:needYuanbo(%s) playerYuanbo(%s)" % (costYuanbo, player.yuanbo))
                return response

            #if not player.mysteryshop.refresh_yuanbo():
            #    response.common_response.player.set("mysteryShop", player.mysteryshop.to_dict())
            #    AlertHandler(player, response, AlertID.ALERT_MYSTERYSHOP_DIAMOND_REFRESH_OVER_TIME, u"mysteryShopInit:yuanboRefreshCount(%s) yuanbo_number(%s)" % (player.mysteryshop.yuanboRefreshCount, player.mysteryshop.yuanbo_number))
            #    return response
            player.sub_yuanbo(costYuanbo, info=info)
            player.mysteryshop.refresh()

    response.common_response.player.set("mysteryShop", player.mysteryshop.to_dict())

    return response
