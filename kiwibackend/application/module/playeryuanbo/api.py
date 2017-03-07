# -*- coding: utf-8 -*-
import time
from module.playeryuanbo.docs import PlayerYuanboLog, PurchaseOrder, PlayerYuanboShop
from module.common.static import Static
from django.conf import settings

def add_player_yuanbo(player, amount, type=1, info=""):
    """
    用户元宝增加
    """
    before_yuanbo= player.yuanbo
    player.add_yuanbo(amount, info=info)
    #元宝添加记录
    PlayerYuanboLog.objects.create(player_id=player.pk, amount=amount, type=type, info=info, serverid=settings.SERVERID)
    return True

def sub_player_yuanbo(player, amount, info=''):
    """
    用户元宝使用
    """
    if player.yuanbo >= amount:
        before_yuanbo = player.yuanbo
        player.sub_yuanbo(amount, info=info)
        PlayerYuanboLog.objects.create(player_id=player.pk, amount=-amount, type=3, info=info, serverid=settings.SERVERID)
        return True
    else:
        return False

def get_order(order_id):
    """
    获得订单
    """
    try:
        order = PurchaseOrder.objects.get(pk=str(order_id))
    except:
        order = None
    return order

def create_order(player, yuanbo_id, pid="", channel=""):
    """
    创建订单
    """
    order_id = "%s%s" % (player.userid, int(time.time()*1000))
    order = PurchaseOrder(order_id=order_id, yuanbo_id=yuanbo_id, osuser_id=pid, player_id=player.id, channel=channel, serverid=settings.SERVERID)
    order.save()
    return order 

def recharge_yuanbo(player, yuanbo ,info = u''):
    '''
    充值元宝统一方法
    '''
    is_first = False
    #首冲 单项计算
    if player.yuanboshop.is_first_buy(yuanbo.id):
        add_yuanbo = yuanbo.amount + yuanbo.first_amount
        is_first = True
    else:
        add_yuanbo = yuanbo.amount + yuanbo.reward_amount

    player.yuanboshop.buy(yuanbo.pk)
    add_player_yuanbo(player, add_yuanbo, type = 2, info = info)
    player.add_charge_yuanbo(yuanbo.amount)
    # if player.vip_levelup:
    #     if player.mysteryshop.refresh_with_vip():
    #         if hasattr(player, "response"):
    #             player.response.common_response.player.set("mysteryShop", player.mysteryshop.to_dict())

    if yuanbo.price >= 10:
        player.open_week_card()
    
    if yuanbo.price >= 30:
        player.open_month_card()

    if yuanbo.price >= 100:
        player.open_permanent_card()
    
    player.task_going(Static.TASK_CATEGORY_RECHARGE, number=yuanbo.amount, is_incr=True, is_series=True)
    if player.daysFromcreated == 1:
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_RECHARGE1, number=yuanbo.price, is_incr=True, is_series=True)
    elif player.daysFromcreated == 4:
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_RECHARGE4, number=yuanbo.price, is_incr=True, is_series=True)

    # 单笔充值恰好为这个数字的时候才能完成任务
    elif player.daysFromcreated == 3:
        if yuanbo.price == 6:
            player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_SINGLE_RECHARGE3_6, number=yuanbo.price, is_incr=False, with_top=True, is_series=False)
        elif yuanbo.price == 12:
            player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_SINGLE_RECHARGE3_12, number=yuanbo.price, is_incr=False, with_top=True, is_series=False)
        elif yuanbo.price == 30:
            player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_SINGLE_RECHARGE3_30, number=yuanbo.price, is_incr=False, with_top=True, is_series=False)
        elif yuanbo.price == 50:
            player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_SINGLE_RECHARGE3_50, number=yuanbo.price, is_incr=False, with_top=True, is_series=False)

    elif player.daysFromcreated == 6:
        if yuanbo.price == 6:
            player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_SINGLE_RECHARGE6_6, number= yuanbo.price, is_incr=False, with_top=True, is_series=False)
        elif yuanbo.price == 12:
            player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_SINGLE_RECHARGE6_12, number=yuanbo.price, is_incr=False, with_top=True, is_series=False)
        elif yuanbo.price == 30:
            player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_SINGLE_RECHARGE6_30, number=yuanbo.price, is_incr=False, with_top=True, is_series=False)
        elif yuanbo.price == 50:
            player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_SINGLE_RECHARGE6_50, number=yuanbo.price, is_incr=False, with_top=True, is_series=False)

    return add_yuanbo, is_first
