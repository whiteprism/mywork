# -*- encoding:utf8 -*-

from decorators import require_player, handle_common
from module.common.static import Static, AlertID
from module.item.api import get_item, get_storeitem,get_towerstore, get_couragepointstore, get_itemcomposes_by_item_id
from module.playeritem.api import acquire_item, acquire_buyrecord
from module.utils import step_count
from module.gashapon.api import get_gashapon
from module.common.middleware import ErrorException, AlertHandler
from module.vip.api import get_vip
from module.common.actionlog import ActionLogWriter
from module.playerhero.api import acquire_hero
from module.playerequip.api import acquire_equip, acquire_equipfragment
from module.playerartifact.api import acquire_artifact
from module.playersoul.api import acquire_soul
from module.rewards.api import reward_send


@handle_common
@require_player
def itemUse(request, response):
    
    """
    物品使用
    
    """
    count = getattr(request.logic_request, "count", 0)
    playerhero_id = getattr(request.logic_request, "playerHeroId", 0)
    playeritem_id = getattr(request.logic_request, "playerItemId", 0)

    player = request.player
    rewards = []

    playeritem = player.items.get(playeritem_id)
    if not playeritem:
        raise ErrorException(player, u"itemUse:playeritem(%s) no existed" % (playeritem_id))

    if not playeritem.can_sub(count):
        #更新数据
        player.update_item(playeritem)
        AlertHandler(player, response, AlertID.ALERT_ITEM_NOT_ENOUGH,  u"itemUse:item(%s) playeritem(%s) useCount(%s) count(%s)" % (playeritem.item_id,playeritem_id, count, playeritem.count))
        return response

    if playeritem.item.is_gold:
        player.add_gold(playeritem.item.number*count, info=u"道具使用")
    elif playeritem.item.is_power:
        player.add_power(playeritem.item.number*count)
    elif playeritem.item.is_stamina:
        player.add_stamina(playeritem.item.number*count)
    elif playeritem.item.is_xp:
        playerhero = player.heroes.get(playerhero_id)
        playerhero.add_xp(playeritem.item.number*count, player)
        player.update_hero(playerhero, True)
    elif playeritem.item.is_key:
        playerbox = player.items.get(playeritem.item.boxId)

        if not playerbox:
            raise ErrorException(player, u"itemUse:item(%s) playeritem(%s) box(%s) no existed" % (playeritem.item_id, playeritem_id , playeritem.item.boxId))

        if not playerbox.can_sub(count):
            raise ErrorException(player, u"itemUse:item(%s) playeritem(%s) box(%s) count(%s) useCount(%)" % (playeritem.item_id, playeritem_id , playeritem.item.boxId, playerbox.count, count))

        playerbox.sub(count, info=u"物品使用")

        gashapon= get_gashapon(playerbox.item.gashapon_id)
        is_new, playergashapon = player.gashapons.get_or_create(gashapon.pk)
        units = playergashapon.acquire(player, gashapon, count=count)
        player.gashapons.update(playergashapon)

        for unit in units:
            reward = {"count": unit.gashapon_number, "type": unit.obj_id}
            rewards.append(reward)

    elif playeritem.item.is_box:
        #if playeritem.item.boxKeyId and player.vip_level < 5:
        if playeritem.item.boxKeyId:
            playerboxkey = player.items.get(playeritem.item.boxKeyId)
            if not playerboxkey:
                raise ErrorException(player, u"itemUse:item(%s) playeritem(%s) key(%s) no existed" % (playeritem.item_id, playeritem_id , playeritem.item.boxKeyId))
            if not playerboxkey.can_sub(count):
                raise ErrorException(player, u"itemUse:item(%s) playeritem(%s) box(%s) count(%s) useCount(%)" % (playeritem.item_id, playeritem_id , playeritem.item.boxKeyId, playerboxkey.count, count))

            playerboxkey.sub(count, info=u"物品使用")

        gashapon= get_gashapon(playeritem.item.gashapon_id)
        is_new, playergashapon = player.gashapons.get_or_create(gashapon.pk)
        units = playergashapon.acquire(player, gashapon, count=count)
        player.gashapons.update(playergashapon)

        for unit in units:
            reward = {"count": unit.gashapon_number, "type": unit.obj_id}
            rewards.append(reward)
    # elif playeritem.item.is_waravoid:
    #     player.waravoid_add(playeritem.item.number*count)
    #     response.common_response.player.set("waravoidCDTime", player.waravoidCDTime)
    elif playeritem.item.is_package_all:
        for tmpreward in playeritem.item.rewards:
            _rewards = reward_send(player, tmpreward, info=u"物品使用", number=count)
            for _, v in _rewards.items():
                rewards.append(v)
    elif playeritem.item.is_package_single:
        count = 1            
        selectIndex = getattr(request.logic_request, "selectIndex", 1)
        selectReward = playeritem.item.rewards[selectIndex - 1]
        _rewards = reward_send(player, selectReward, info=u"物品使用", number=count)
        for _, v in _rewards.items():
            rewards.append(v)
    elif playeritem.item.is_fruit_flower or playeritem.item.is_fruit_tree:
        selectRewards = playeritem.item.rewards
        for selectReward in selectRewards:
            _rewards = reward_send(player, selectReward, info=u"物品使用", number=count)
            for _, v in _rewards.items():
                rewards.append(v)
    else:
        raise ErrorException(player, u"itemUse:item(%s) playeritem(%s) no used" % (playeritem.item_id,playeritem_id))

    playeritem.sub(count, u"物品使用")
    response.logic_response.set("rewards", rewards)
    return response

@handle_common
@require_player
def itemBuy(request, response):
    """
    物品购买
    """
    player = request.player
    count = getattr(request.logic_request, "count", 0)
    storeitem_id = getattr(request.logic_request, "storeItemId", 0)
    level = getattr(request.logic_request, "level", 0)
    targetId = getattr(request.logic_request, "targetId", 0)

    storeitem = get_storeitem(storeitem_id)

    #条件检查
    if not storeitem or not storeitem.display:
        raise ErrorException(player, u"itemBuy:storeitem(%s) no buy" % (storeitem_id))
    
    playerbuyrecord = player.buyrecords.get(storeitem.item_id)

    today_buy_number = playerbuyrecord.today_buy_number if playerbuyrecord else 0

    rewards = []
    critCount = 0 #点金手暴击倍数

    if  storeitem.is_limitbuy:
        dailyCount = storeitem.dailyCount
        #体力 耐力  点金手次数根据vip等级判断
        if storeitem.item.is_power  or storeitem.item.is_stamina or storeitem.item.is_goldhand or storeitem.item.is_gold_box :
            vip = get_vip(player.vip_level)
            if storeitem.item.is_power:
                dailyCount = vip.buyPowerCount
            elif storeitem.item.is_stamina:
                dailyCount = vip.buyStaminaCount
            elif storeitem.item.is_gold_box:
                dailyCount = vip.buyGoldBoxCount
            else:
                dailyCount = vip.goldHandCount
        if count + today_buy_number > dailyCount:
            if playerbuyrecord:
                player.update_buyrecord(playerbuyrecord)
            AlertHandler(player, response, AlertID.ALERT_ITEM_LIMITBUY, u"itemBuy:storeitem(%s) exceed limitbuy(%s) todayBuy(%s) nowBuy(%s)" % (storeitem_id, dailyCount, today_buy_number, count))
            return response

    _price = storeitem.baseDiamond
    _price,_  = step_count(_price, storeitem.incrDiamond, today_buy_number) 

    _,total_price = step_count(_price, storeitem.incrDiamond, count) 

    #价格检查
    if total_price > player.yuanbo:
        AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"itemBuy:storeitem(%s) startPrice(%s) stepPrice(%s) totalPrice(%s) playerYuanbo(%s)" % (storeitem_id, _price, total_price, player.yuanbo))
        return response

    #点金手
    if storeitem.item.is_goldhand:
        info = u"点金手"
        critCount, gold = storeitem.item.goldhand_gold(player, today_buy_number, total_price)

        before_gold = player.gold
        player.add_gold(gold, info=info)
        after_gold = player.gold

        ActionLogWriter.item_goldhand(player, gold, before_gold, after_gold, info)
        player.dailytask_going(Static.DAILYTASK_CATEGORY_GOLDHAND, number=count, is_incr=True, is_series=True)#点金手
        reward = {"count": gold, "type": Static.GOLD_ID}
        rewards.append(reward)

        response.logic_response.set("rewards", rewards)
        response.logic_response.set("critCount", critCount)
    
    elif storeitem.item.is_woodhand:
        info = u""
        total_price = (today_buy_number + 2) * 5
        critCount, wood = storeitem.item.woodhand_wood(today_buy_number) # wood是float型
        wood = int(wood * total_price)
        before_wood = player.wood
        player.add_wood(wood, info=info)
        after_wood = player.wood

        ActionLogWriter.item_woodhand(player, wood, before_wood, after_wood, info)
        player.dailytask_going(Static.DAILYTASK_CATEGORY_WOOD, number=count, is_incr=True, is_series=True)#点金手
        reward = {"count": wood, "type": Static.WOOD_ID}
        rewards.append(reward)

        response.logic_response.set("rewards", rewards)
        response.logic_response.set("critCount", critCount)
        
    else:
        acquire_item(player, storeitem.item, number=count, info=u"购买")

    acquire_buyrecord(player, storeitem.item, number=count, info=u"购买")

    if storeitem.item.is_power:
        player.dailytask_going(Static.DAILYTASK_CATEGORY_BUY_POWER, number=count, is_incr=True, is_series=True)#双人套餐
    
    player.sub_yuanbo(total_price, info=u"购买道具")

    return response



@handle_common
@require_player
def itemTowerBuy(request, response):
    """
    爬塔物品购买
    """
    player = request.player
    count = getattr(request.logic_request, "count", 0)
    towerItemId = getattr(request.logic_request, "towerItemId", 0)

    toweritem = get_towerstore(towerItemId)

    # 仿照商店的信息，做了一个爬塔的商店，里面出售灵魂碎片以及装备碎片，大致逻辑和物品购买一致。

    #条件检查
    if not toweritem or not toweritem.display:
        raise ErrorException(player, u"itemBuy:storeitem(%s) no buy" % (towerItemId))

    playerbuytowerrecord = player.buytowerrecords.get(toweritem.item_id)

    today_buy_number = playerbuytowerrecord.today_buy_number if playerbuytowerrecord else 0

    if toweritem.is_limitbuy:
        dailyCount = toweritem.dailyCount

        if count + today_buy_number > dailyCount:
            #if playerbuytowerrecord:
            #    player.update_buytowerrecord(playerbuytowerrecord)
            AlertHandler(player, response, AlertID.ALERT_ITEM_LIMIT_BUY, u"itemBuy:itemTowerBuy(%s) exceed limitbuy(%s) todayBuy(%s) nowBuy(%s)" % (towerItemId, dailyCount, today_buy_number, count))
            return response

    _price = toweritem.basePrice

    # 这里购买东西是消耗爬塔币这样的东西
    #价格检查
    if _price > player.towerGold:
        AlertHandler(player, response, AlertID.ALERT_TOWER_GOLD_NOT_ENOUGH, u"itemBuy:itemTowerBuy(%s)  totalPrice(%s) playertowerGold(%s)" % (towerItemId, _price, player.towerGold))
        return response


    if str(toweritem.item_id).startswith("20"):
        acquire_soul(player, toweritem.item_id, number=count, info=u"购买爬塔物品")
    elif str(toweritem.item_id).startswith("23"):
        acquire_equipfragment(player, toweritem.item_id, number=count, info=u"购买爬塔物品")

    #acquire_buytowerrecord(player, toweritem.item_id, number=count, info=u"购买爬塔物品")

    player.sub_towerGold(_price, info=u"购买爬塔物品")

    reward = {"count": count, "type": toweritem.item_id}

    response.logic_response.set("rewards", [reward])

    return response



@handle_common
@require_player
def itemBuyAndUse(request, response):
    """
    物品购买并且使用
    仅限体力和耐力
    """
    count = getattr(request.logic_request, "count", 0)
    storeitem_id = getattr(request.logic_request, "storeItemId", 0)
    player = request.player
    storeitem = get_storeitem(storeitem_id)
    
    #条件检查
    if not storeitem or not storeitem.display and (not storeitem.item.is_power or not storeitem.item.is_stamina):
        raise ErrorException(player, u"itemBuyAndUse:storeitem(%s) no buy" % (storeitem_id))
    
    playerbuyrecord = player.buyrecords.get(storeitem.item_id)
    today_buy_number = playerbuyrecord.today_buy_number if playerbuyrecord else 0

    if  storeitem.is_limitbuy:
        dailyCount = storeitem.dailyCount
        vip = get_vip(player.vip_level)
        if storeitem.item.is_power:
            dailyCount = vip.buyPowerCount
        elif storeitem.item.is_stamina:
            dailyCount = vip.buyStaminaCount
        
        if count + today_buy_number > dailyCount:
            if playerbuyrecord:
                player.update_buyrecord(playerbuyrecord)
            AlertHandler(player, response, AlertID.ALERT_ITEM_LIMIT_BUY, u"itemBuyAndUse:storeitem(%s) exceed limitbuy(%s) todayBuy(%s) nowBuy(%s)" % (storeitem_id, dailyCount, today_buy_number, count))
            return response

    _price = storeitem.baseDiamond
    _price,_  = step_count(_price, storeitem.incrDiamond, today_buy_number) 

    _,total_price = step_count(_price, storeitem.incrDiamond, count) 

    #价格检查
    if total_price > player.yuanbo:
        AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"itemBuyAndUse:storeitem(%s) startPrice(%s) stepPrice(%s) totalPrice(%s) playerYuanbo(%s)" % (storeitem_id, _price, total_price, player.yuanbo))
        return response

    playeritem = acquire_item(player, storeitem.item, number=count, info=u"购买并使用")
    acquire_buyrecord(player, storeitem.item, number=count, info=u"购买并使用")

    if storeitem.item.is_power:
        player.dailytask_going(Static.DAILYTASK_CATEGORY_BUY_POWER, number=count, is_incr=True, is_series=True)#双人套餐
    
    player.sub_yuanbo(total_price, info=u"购买道具")

    if playeritem.item.is_power:
        player.add_power(playeritem.item.number*count)
    elif playeritem.item.is_stamina:
        player.add_stamina(playeritem.item.number*count)

    playeritem.sub(count, info=u"物品购买并使用")

    return response


@handle_common
@require_player
def itemCompose(request, response):
    """
    物品合成
    """
    item_id = getattr(request.logic_request, "itemId", 0)

    player = request.player

    item = get_item(item_id)
    if not item:
        raise ErrorException(player, u"itemCompose:item(%s) is not existed" % item_id)

    info = u"物品合成:%s" % item_id
    itemfragments = get_itemcomposes_by_item_id(item_id)

    playeritemfragments = []
    
    playeritemfragment_costs = []

    for itemfragment in itemfragments:
        _playeritem = player.items.get(itemfragment.fragmentId)
        if _playeritem:
            playeritemfragments.append(_playeritem)
            playeritemfragment_costs.append(itemfragment.num)
        else:
            raise ErrorException(player, u"itemCompose:player itemfragment(%s) not existed" % (itemfragment.fragmentId))

        if not _playeritem.can_sub(itemfragment.num):
            player.update_item(_playeritem)
            AlertHandler(player, response, AlertID.ALERT_ITEM_NOT_ENOUGH, u"itemCompose: item(%s) playeritemfragment(%s) costNumber(%s) playerNumber(%s)" % (item_id, itemfragment.fragmentId, itemfragment.num, _playeritem.count))
            return response

    for index, playeritemfragment in enumerate(playeritemfragments):
        playeritemfragment.sub(playeritemfragment_costs[index], info)
         
    playerItem = acquire_item(player, item, number=1, info=info)
    response.logic_response.set("itemId", playerItem.item_id)

    return response

@handle_common
@require_player
def couragePointStoreBuy(request, response):
    """
    勇气商店购买
    """
    player = request.player
    count = getattr(request.logic_request, "count", 0)
    store_id = getattr(request.logic_request, "storeId", 0)

    couragepoint_store = get_couragepointstore(store_id)
    if not couragepoint_store:
        raise ErrorException(player, u"couragePointStoreBuy:storeitem(%s) no buy" % (store_id))

    if player.couragepoint < couragepoint_store.couragepoint * count :
        AlertHandler(player, response, AlertID.ALERT_COURAGEPOINT_NOT_ENOUGH, u"couragePointStoreBuy: couragepoint(%s) and playerCouragepoint(%s)" % (player.couragepoint, couragepoint_store.couragepoint * count))
        return response

    info = u"勇气商店购买"
    acquire_item(player, couragepoint_store.item_id, number=couragepoint_store.count*count, info=info)
    player.sub_couragepoint(couragepoint_store.couragepoint * count, info)
    return response

# @handle_common
# @require_player
# def sevenDaysHalfOpen(request, response):
#     """
#     七天乐半价打开
#     """
#     player = request.player
#     # 拿到套装id
#     suitId = getattr(request.logic_request, "suitId", 0)
#     # 如果是英雄需要发送一个选中的英雄
#     heroId = getattr(request.logic_request, "heroId", 0)
#     #使用数量
#     count = abs(getattr(request.logic_request, "count", 0))

#     # 获取套装的数据
#     itemsuit = get_itemsuit(suitId)
#     playeritem = player.items.get(itemsuit.suitToItemId)

#     #数量检查
#     if not playeritem.can_sub(count):
#         player.update_item(playeritem)
#         AlertHandler(player, response, AlertID.ALERT_ITEM_NOT_ENOUGH,  u"sevenDaysHalfOpen:item(%s) playeritem(%s) useCount(%s) count(%s)" % (playeritem.item_id,playeritem.item_id, count, playeritem.count))


#     rewards = []

#     if heroId:
#         # 判断传入的英雄是否在套装里面
#         if heroId in itemsuit.itemIds:

#             star = int(str(heroId)[-2:])
#             new_id = heroId / 100 * 100
#             # 按照给定的id适配相应的星级
#             playerunit = acquire_hero(player, new_id, info=u"英雄套装打开", star=star)
#             if playerunit.is_hero:
#                 # 返回给前端展示
#                 rewards.append({"type": new_id, "count": 1})
#             else:
#                 rewards.append({"type": playerunit.soul_id, "count": playerunit.soul.breakCost})
#     else:
#         # 如果是除了英雄的其他套装
#         for id, _count in zip(itemsuit.itemIds, itemsuit.itemCounts):
#             # 装备套装
#             if str(id).startswith('12'):
#                 for i in range(0, count*_count):
#                     acquire_equip(player, id)
#             # 圣物套装
#             elif str(id).startswith('14'):
#                 for i in range(0, count*_count):
#                     acquire_artifact(player, id)
#             # 物品套装
#             rewards.append({"type": id, "count": count*_count})

#     playeritem = player.items.get(itemsuit.suitToItemId)
#     playeritem.sub(count, info=u"打开套装宝箱")

#     response.logic_response.set("rewards", rewards)


#     return response

