# -*- encoding:utf8 -*-
from decorators import require_player, handle_common
from module.playeryuanbo.api import create_order, get_order, recharge_yuanbo
from module.yuanbo.api import get_yuanbo
from module.common.middleware import ErrorException
from django.conf import settings

@handle_common
@require_player
def paymentOrder(request, response):
    """
    生成订单
    """
    player = request.player
    yuanbo_id = getattr(request.logic_request, "diamondId", 0)
    osuser_id = getattr(request.logic_request, "channelUserId", "")
    channel = getattr(request.common_request, "channel", "")

    order = create_order(player, yuanbo_id, osuser_id, channel=channel)

    #debug 测试
    if settings.LOCAL_DEBUG:
        yuanbo = get_yuanbo(order.yuanbo_id)
        add_yuanbo, is_first = recharge_yuanbo(player, yuanbo, info="debug recharge")
        order.yuanbo = add_yuanbo
        order.price = yuanbo.price
        order.is_first = is_first
        order.serverid = order.serverid
        order.success()
        order.save()
    response.common_response.player.set("vip", player.vip)
    response.common_response.player.set("buyDiamondIds", player.yuanboshop.to_dict())
    #debug end

    response.logic_response.set("orderId", order.order_id)
    return response

@handle_common
@require_player
def paymentCheck(request, response):
    player = request.player
    order_id = getattr(request.logic_request, "orderId", 0)
    order = get_order(order_id)
    if not order:
        raise ErrorException(player, u"paymentCheck:order(%s) is not existed" % order_id)

    if settings.LOCAL_DEBUG and not order.is_success:
        yuanbo = get_yuanbo(order.yuanbo_id)
        add_yuanbo, is_first = recharge_yuanbo(player, yuanbo, info="debug recharge")
        order.yuanbo = add_yuanbo
        order.price = yuanbo.price
        order.is_first = is_first
        order.success()
        order.save()

    if order.is_success:
        result = True
        diamond = order.yuanbo
        is_first = order.is_first
    else:
        result = False
        diamond = 0
        is_first = False

    response.common_response.player.set("vip", player.vip)
    response.common_response.player.set("buyDiamondIds", player.yuanboshop.to_dict())
    response.logic_response.set("result", result)
    response.logic_response.set("diamond", diamond)
    response.logic_response.set("isFirst", is_first)
    return response
