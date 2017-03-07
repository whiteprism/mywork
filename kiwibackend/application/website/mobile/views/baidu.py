# -*- coding: utf-8 -*-
import hashlib
from django.conf import settings
import simplejson
import base64
from opensocial.http import HttpResponseJson
from module.playeryuanbo.api import get_order, recharge_yuanbo
from module.yuanbo.api import get_yuanbo
from module.player.api import get_player


def purchase_callback(request):
    """
    支付回调
    """

    AppID = request.POST.get("AppID", "")
    OrderSerial = request.POST.get("OrderSerial", "")
    CooperatorOrderSerial = request.POST.get("CooperatorOrderSerial", "")
    Sign = request.POST.get("Sign", "")
    Content = request.POST.get("Content", "")
    secret_key = settings.CHANNELS["baidu"]["secret_key"]

    sign = hashlib.md5("%s%s%s%s%s" % (AppID, OrderSerial, CooperatorOrderSerial, Content, secret_key)).hexdigest()

    result = {"AppID": AppID, "ResultCode": 0, "resultMsg": "", "Sign":"", "Content":""}
    if sign != Sign:
        result["resultMsg"] = u"Sign Error"
    
    else:
        contentStr=base64.b64decode(Content)
        #json解析
        content=simplejson.loads(contentStr)

        order = get_order(CooperatorOrderSerial)

        if not order:
            result["ResultMsg"] = "No order"
        else:
            if not order.is_success:
                order.notify_data = simplejson.dumps(content)
                order.plat_order_id = OrderSerial
                yuanbo = get_yuanbo(order.yuanbo_id)

                #if yuanbo.price <= content["OrderMoney"] and content["OrderStatus"] == 1:
                if content["OrderStatus"] == 1:
                    player = get_player(order.player_id)
                    add_yuanbo, is_first = recharge_yuanbo(player, yuanbo, info="baidu recharge") 
                    order.yuanbo = add_yuanbo
                    order.is_first = is_first
                    order.success()
                    player.update()
                else:
                    order.failure()

                order.save()
            result["ResultCode"] = 1

    result["Sign"] = hashlib.md5("%s%s%s" %(result["AppID"], result["ResultCode"], secret_key)).hexdigest()

    return HttpResponseJson(result)
