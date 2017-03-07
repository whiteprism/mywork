# -*- coding: utf-8 -*-
from decorators import *
from api import *
from opensocial.http import HttpResponseJson
from module.common.static import ErrorCode
from module.playeryuanbo.docs import PurchaseOrder
from module.utils import delta_time

@handle_verification
def query_orders_by_time(request):
    '''
        按时间查询订单
    '''
    channel = request.REQUEST.get("channel", "").strip()
    startTimeStr = request.REQUEST.get("startTime", "").strip() # 格式：xxxx-xx-xx xx:xx:xx
    endTimeStr = request.REQUEST.get("endTime", "").strip()
    status = int(request.REQUEST.get("status", 2)) # 0 失败(未完成) 1 成功 2 全部
    startTime = get_datetime(startTimeStr)
    endTime = get_datetime(endTimeStr)

    resdata = {}
    if (not startTime) or (not endTime) or (status not in range(3)) or (startTime > endTime):
        resdata["success"] = False
        resdata["message"] = u"输入的参数有误!"
        resdata["data"] = []
        return HttpResponseJson(resdata)
    orders = []
    if status == 2:
        if not channel:
            orders = PurchaseOrder.objects.filter(
                updated_at__gte = startTime,
                updated_at__lte = endTime
                )
        else:
            orders = PurchaseOrder.objects.filter(
                channel = channel,
                updated_at__gte = startTime,
                updated_at__lte = endTime
                )

    else:
        if not channel:
            orders = PurchaseOrder.objects.filter(
                status = status,
                updated_at__gte = startTime,
                updated_at__lte = endTime
                )
        else:
            orders = PurchaseOrder.objects.filter(
                channel = channel,
                status = status,
                updated_at__gte = startTime,
                updated_at__lte = endTime
                )

    data = []
    for order in orders:
        meta = {}
        meta = order.to_dict()
        data.append(meta)
    resdata["success"] = True
    resdata["message"] = ""
    resdata["data"] = data
    return HttpResponseJson(resdata)

@handle_verification
def query_orders_by_playerid(request):
    '''
        按玩家ID查询订单
    '''
    playerId = request.REQUEST.get("playerId", "").strip()
    serverId = request.REQUEST.get("serverId", str(settings.SERVERID)).strip()
    startTimeStr = request.REQUEST.get("startTime", "").strip() # 格式：xxxx-xx-xx xx:xx:xx
    endTimeStr = request.REQUEST.get("endTime", "").strip()
    status = int(request.REQUEST.get("status", 2)) # 0 失败(未完成) 1 成功 2 全部
    startTime = get_datetime(startTimeStr)
    endTime = get_datetime(endTimeStr)

    player = get_player_by_id_or_str(playerId, int(serverId))

    resdata = {}
    # if (playerId == "") or (not startTime) or (not endTime) or (status not in range(3)) or (startTime > endTime):
    if not player:
        resdata["success"] = False
        #resdata["message"] = "The user is not exist!"
        resdata["message"] = u"该玩家不存在!"
        resdata["data"] = []
        return HttpResponseJson(resdata)

    orders = []
    if status == 2:
        if startTime and endTime:
            orders = PurchaseOrder.objects.filter(
                player_id = get_playerId(playerId, serverId),
                updated_at__gte = startTime,
                updated_at__lte = endTime
                )
        elif startTime:
            orders = PurchaseOrder.objects.filter(
                player_id = get_playerId(playerId, serverId),
                updated_at__gte = startTime
                )
        elif endTime:
            orders = PurchaseOrder.objects.filter(
                player_id = get_playerId(playerId, serverId),
                updated_at__lte = endTime
                )
        else:
            orders = PurchaseOrder.objects.filter(
                player_id = get_playerId(playerId, serverId),
                )
    else:
        if startTime and endTime:
            orders = PurchaseOrder.objects.filter(
                player_id = get_playerId(playerId, serverId),
                status = status,
                updated_at__gte = startTime,
                updated_at__lte = endTime
                )
        elif startTime:
            orders = PurchaseOrder.objects.filter(
                player_id = get_playerId(playerId, serverId),
                status = status,
                updated_at__gte = startTime
                )
        elif endTime:
            orders = PurchaseOrder.objects.filter(
                player_id = get_playerId(playerId, serverId),
                status = status,
                updated_at__lte = endTime
                )
        else:
            orders = PurchaseOrder.objects.filter(
                player_id = get_playerId(playerId, serverId),
                status = status
                )
    data = []
    for order in orders:
        meta = {}
        meta = order.to_dict()
        data.append(meta)
    resdata["success"] = True
    resdata["message"] = ""
    resdata["data"] = data
    return HttpResponseJson(resdata)

@handle_verification
def query_orders_by_orderid(request):
    '''
        按订单号查询
    '''
    orderId = request.REQUEST.get("orderId", "").strip()

    order = PurchaseOrder.objects.get(order_id=str(orderId))

    resdata = {}
    if not order:
        resdata["success"] = False
        resdata["message"] = u"该玩家不存在!"
        resdata["data"] = []
        return HttpResponseJson(resdata)

    data = []
    data.append(order.to_dict())
    resdata["success"] = True
    resdata["message"] = ""
    resdata["data"] = data
    return HttpResponseJson(resdata)
    # if not order:
    #     data = {}
    #     data["success"] = False
    #     data["message"] = "The parameter is incorrect!"
    #     data["errorcode"] = ErrorCode.ERROR_PARAMETER_FORMAT
    #     return HttpResponseJson(data)
    # return HttpResponseJson(order.to_dict())

@handle_verification
def query_orders_by_plat_orderid(request):
    '''
        按订平台单号查询
    '''
    platOrderId = request.REQUEST.get("platOrderId", "").strip()

    order = PurchaseOrder.objects.get(plat_order_id=str(platOrderId))
    if not order:
        data = {}
        data["success"] = False
        data["message"] = u"该订单不存在!"
        data["errorcode"] = ErrorCode.ERROR_PARAMETER_FORMAT
        return HttpResponseJson(data)
    return HttpResponseJson(order.to_dict())

@handle_verification
def query_rank_by_price(request):
    '''
        充值排行
    '''
    channel = request.REQUEST.get("channel", "").strip()
    startTimeStr = request.REQUEST.get("startTime", "").strip()
    endTimeStr = request.REQUEST.get("endTime", "").strip()
    startTime = get_datetime(startTimeStr)
    endTime = get_datetime(endTimeStr)

    resdata = {}
    if startTime > endTime:
        meta = {}
        resdata["success"] = False
        resdata["message"] = u"输入的参数有误!"
        resdata["data"] = []
        return HttpResponseJson(resdata)
    if not channel:
        orders = PurchaseOrder.objects.filter(
            status = 1,
            updated_at__gte = startTime,
            updated_at__lte = endTime
            )
    else:
        orders = PurchaseOrder.objects.filter(
            channel = channel,
            status = 1,
            updated_at__gte = startTime,
            updated_at__lte = endTime
            )
    rank_dic = {}
    for order in orders:
        if order.player_id in rank_dic:
            rank_dic[order.player_id] += order.price
        else:
            rank_dic[order.player_id] = order.price
    #data.items().sort(lambda x,y:cmp(y[1],x[1]))
    rank_list = sorted(rank_dic.items(),key=lambda item:item[1],reverse=True)
    data = []
    i = 1
    for rank in rank_list:
        meta = {}
        meta["rank"] = i
        meta["player_id"] = rank[0]
        meta["price"] = rank[1]
        data.append(meta)
        i += 1
    resdata["success"] = True
    resdata["message"] = ""
    resdata["data"] = data
    return HttpResponseJson(resdata)
