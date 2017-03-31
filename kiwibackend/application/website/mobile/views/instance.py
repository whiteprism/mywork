# -*- encoding:utf-8 -*-
from decorators import require_player, handle_common
from module.playerinstance.api import get_player_view_instance_dict, get_all_player_star_by_instance_id, get_chest_rewards, get_star, get_player_open_raidinstance
from module.instance.api import get_smallGames, get_guildinstanceLevel,get_raidenemytoreward, get_instancelevel,get_eliteinstancelevel, get_raidinstance, get_raidlevel, get_elementtowerinstance
from module.common.static import Static, AlertID
from rewards.models import CommonReward
from module.rewards.api import reward_send
from module.common.middleware import ErrorException, AlertHandler
from module.vip.api import get_vip
from module.experiment.api import check_player_in_experiment_by_experimentname
from module.gashapon.api import get_gashapon
from module.guild.api import get_sysguildinstanceInfo, get_guild_by_id, create_guildauctionmaxinfo
from module.player.api import get_player
from module.playeritem.api import acquire_item
import datetime
import random, time

@handle_common
@require_player
def instanceStart(request, response):
    '''
    结算
    '''
    player = request.player
    level_id = getattr(request.logic_request, "instanceId", 0)
    heroLayoutData = getattr(request.logic_request, "heroLayoutData", [])
    isWin = getattr(request.logic_request, "isWin", False)
    summary = getattr(request.logic_request, "summary", {})

    deadCount = 0
    instancelevel = get_instancelevel(level_id)
    playerinstancelevel = player.instancelevels.get(instancelevel.pk)

    #副本没有开启
    if not playerinstancelevel:
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_NOT_OPEN, u"instanceStart:level_id(%s) is not open" % level_id)
        return response


    if instancelevel.minUserLevel > player.level:
        AlertHandler(player, response, AlertID.ALERT_LEVEL_SHORTAGE, u"instanceStart:level_id(%s) level is %s and playerLevel is %s" % (level_id, instancelevel.minUserLevel, player.level))
        return response

    if playerinstancelevel.succeedCount >= instancelevel.maxPlayCount:
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_FIGHT_COUNT_EXCEED_MAX, u"instanceStart:instance(%s) fight number(%s) exceed maxCount(%s)" % (level_id, playerinstancelevel.succeedCount, instancelevel.maxPlayCount))
        return response

    #[玩家卡id， 卡id， 站位行， 列]
    player.update_hero_layout(heroLayoutData)

    if summary:
        leftWarriorDead = summary["leftWarriorDead"] #英雄小兵全部存在
        for i in range(0, len(leftWarriorDead), 2):
            #检查英雄死亡数量
            if int(str(leftWarriorDead[i])[0:2]) == 11:
                # 根据这个判断副本的星级
                deadCount += leftWarriorDead[i+1]
        new_summary = []
        # 这部分操作暂时没有效果的
        if player.level >= Static.NEW_PLAYER_LEVEL:
            for index in range(0, len(leftWarriorDead)):
                if index % 2 == 0:
                    warrior_id = leftWarriorDead[index]
                    w_count = leftWarriorDead[index+1]
                    if int(str(warrior_id)[0:2]) == 11:
                        continue
                    new_summary.append(warrior_id)
                    new_summary.append(w_count)
                    player.armies.lost(warrior_id, w_count)
        summary["leftWarriorDead"] = new_summary

    star = get_star(deadCount)
    # 如果是以新手向导的方式进入，那么不去发奖励也不加经验。
    if not player.tutorial_id == Static.TUTORIAL_ID_GASHAPON_2:

        data = playerinstancelevel.fight(star, isWin)

        heroLevelUp = data["heroLevelUp"]
        rewards = data["rewards"]
        if isWin:
            player.sub_power(instancelevel.powerCost)
            player.dailytask_going(Static.DAILYTASK_CATEGORY_INSTANCE, number=1, is_incr=True, is_series=True)
            player.task_going(Static.TASK_CATEGORY_INSTANCE, number=1, c1=level_id, is_incr=False, is_series=False)
            player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_INSTANCE, number=1, c1=level_id, is_incr=True, is_series=False)

    else:
        rewards = []
        heroLevelUp = []

    playerinstancelevel.rewardBoxes = []

    player.update_instancelevel(playerinstancelevel, True)
    response.logic_response.set("rewards", rewards)
    response.logic_response.set("heroLevelUp",heroLevelUp)
    response.logic_response.set("summary",summary)
    response.logic_response.set("star", star)
    response.common_response.player.set("soldiers", player.armies.to_dict())
    response.common_response.player.set("tutorial", player.tutorial)
    response.common_response.player.set("populationCost", player.populationCost)
    return response

@handle_common
@require_player
def instanceSetUp(request, response):
    '''
    请求敌军信息
    '''
    player = request.player
    level_id = getattr(request.logic_request, "instanceId", 0)
    version = getattr(request.logic_request, "version", 0)
    data = {}

    instancelevel = get_instancelevel(level_id)
    playerinstancelevel = player.instancelevels.get(level_id)
    #副本
    if not playerinstancelevel:
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_NOT_OPEN, u"instanceSetUp:instance(%s) is not open" % level_id)
        return response

    if instancelevel.minUserLevel > player.level:
        AlertHandler(player, response, AlertID.ALERT_LEVEL_SHORTAGE, u"instanceSetUp:instance(%s) level is %s and playerLevel is %s" % (level_id, instancelevel.minUserLevel, player.level))
        return response

    if playerinstancelevel.succeedCount >= instancelevel.maxPlayCount:
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_FIGHT_COUNT_EXCEED_MAX, u"instanceSetUp:instance(%s) fight count(%s) exceed max count(%s)" % (level_id, playerinstancelevel.succeedCount, instancelevel.maxPlayCount))
        return response

    #体力不足
    if player.power < instancelevel.powerCost:
        AlertHandler(player, response, AlertID.ALERT_POWER_NOT_ENOUGH, u"instanceSetUp:power error (%s)" % player.power)
        return response

    enemies = instancelevel.enemies
    if not enemies:
        raise ErrorException(player, u"instanceSetUp: enemyData(%s) is not existed" % level_id)

    # 这个打完boss的剧情以后进行的赋值 状态为400，并且完成,200进400出
    if player.tutorial_id == Static.TUTORIAL_ID_INIT_1:
        player.tutorial_begin()

        # 这里的firstIn是选名字的新手引导。如果一进游戏提示你选名字是因为这个没有置成０
        player.set("firstIn", 0)

    if player.tutorial_id == Static.TUTORIAL_ID_INSTANCE_1ST_3:
            player.tutorial_complete()

    # 一请求副本就把新手引导的状态关闭掉。防止断线以后游戏会卡主

    elif player.tutorial_id == Static.TUTORIAL_ID_HEROCOMPOSE2_11:
        player.tutorial_complete()

    # 这里做的奖励提前展示，结算后会把展示的奖励发放出去

    rewards = playerinstancelevel.make_rewards_before_fight()
    player.update_instancelevel(playerinstancelevel, True)

    response.logic_response.set("rewards", rewards)
    response.logic_response.set("enemies", [enemy.to_dict() for enemy in enemies])
    response.logic_response.set("version", version)
    return response

@handle_common
@require_player
def guildInstanceOpen(request, response):
    '''
    开启公会副本
    '''
    player = request.player
    # 前端从静态表里面取出来公会副本的id
    instanceLevelId = getattr(request.logic_request, "instanceId", 0)
    guildInfo = player.guild.guildInfo

    # if not player.guild.guildInfo.instanceIsOpen:
    #     AlertHandler(player, response, AlertID.ALERT_GUILD_INSTANCE_LEVEL_LIMIT, u"guildInstanceOpen your guild level %s is limit" % player.guild.guildInfo.level)
    #     guildInfo.self_release_lock()
    #     return response
    # 在公会达到十级的时候就已经把所有的副本全部加入备选的方案了，只不过状态还是设置为未开启的状态

    # 普通成员没有权限开启副本
    if player.guild.isMember:
        guildInfo.self_release_lock()
        AlertHandler(player, response, AlertID.ALERT_GUILD_LIMIT_CAN_NOT_OPEN_INSTANCE, u"guildInstanceOpen your position is %s open instance need 2 or 1" %(player.guild.position))
        return response
    # 去静态表里面取得公会副本的信息
    sysGuildInstance = get_sysguildinstanceInfo(instanceLevelId, player.guildId)
    guildinstancelevel = get_guildinstanceLevel(instanceLevelId)

    if player.yuanbo < guildinstancelevel.diamondCost:
        AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"guildInstanceOpen:instanceLevelId(%s)  melt costYuanbo(%s) playerYuanbo(%s)" % (instanceLevelId, guildinstancelevel.diamondCost, player.yuanbo))
        return response
    info = u"开启公会副本:%s:%s" % (player.guildId, instanceLevelId)
    player.sub_yuanbo(guildinstancelevel.diamondCost, info)


    if not sysGuildInstance or not  sysGuildInstance.isWaiting or player.guild.guildInfo.level < guildinstancelevel.guildLevelLimit:
        guildInfo.self_release_lock()
        if sysGuildInstance:
            sysGuildInstance.self_release_lock()
        response.logic_response.set("instanceInfo", sysGuildInstance.to_dict())
        return response
    sysGuildInstance.open()

    guildInfo.self_release_lock()
    response.logic_response.set("instanceInfo", sysGuildInstance.to_dict())

    return response

# todo 这个接口可能不会用到了。

# @handle_common
# @require_player
# def guildInstanceGetBossHp(request, response):
#     '''
#     请求公会副本boss血量
#     '''
#     player = request.player
#
#
#
#     guild = get_guild_by_id(player.guildId)
#
#     if not guild.instanceIds:
#         return response
#
#     totalEnemies = []
#
#     enemiesDatas = []
#
#     for instanceId in guild.instanceIds:
#         guildInstancelevel = get_guildinstanceLevel(instanceId)
#         enemies = guildInstancelevel.enemies
#         if not enemies:
#             raise ErrorException(player, u"instanceSetUp: enemyData(%s) is not existed" % instanceId)
#         totalEnemies.append(enemies)
#
#     for enemies in totalEnemies:
#         enemiesDatas.append([enemy.to_dict() for enemy in enemies])
#
#     response.logic_response.set("enemiesDatas", enemiesDatas)
#
#     return response

@handle_common
@require_player
def guildInstanceSetUp(request, response):
    '''
    请求敌军信息
    '''
    player = request.player
    level_id = getattr(request.logic_request, "instanceId", 0)


    guildInstancelevel = get_guildinstanceLevel(level_id)

    guildInstancelevelInfo = get_sysguildinstanceInfo(level_id,player.guildId)

    if not guildInstancelevelInfo or not guildInstancelevelInfo.isOpen:
        if guildInstancelevelInfo:
            guildInstancelevelInfo.self_release_lock()
        AlertHandler(player, response, AlertID.ALERT_GUILD_INSTANCE_HAS_ALREADY_EXPIRED, u"guildInstanceSetUp this instacelevel has already expired")
        return response



    #  副本有人正在打
    if guildInstancelevelInfo.isFighting > 0:
        guildInstancelevelInfo.self_release_lock()
        AlertHandler(player, response, AlertID.ALERT_GUILD_INSTANCE_IS_FIGHTING, u"guildInstanceSetUp somebody is in this instancelevel")
        return response

    # 已经打过这个副本一次了
    if player.id in guildInstancelevelInfo.memberList:
        guildInstancelevelInfo.self_release_lock()
        AlertHandler(player, response, AlertID.ALERT_GUILD_INSTANCE_HAS_ALREADY_FIGHTED, u"guildInstanceSetUp this instacelevel has already fighted")
        return response

    enemies = guildInstancelevel.enemies
    if not enemies:
        guildInstancelevelInfo.self_release_lock()
        raise ErrorException(player, u"instanceSetUp: enemyData(%s) is not existed" % level_id)

    guildInstancelevelInfo.fight(player)

    response.logic_response.set("bossHp", guildInstancelevelInfo.bossHp)
    response.logic_response.set("bossPercentage", guildInstancelevelInfo.bossPercentage)
    response.logic_response.set("enemies", [enemy.to_dict() for enemy in enemies])

    return response

@handle_common
@require_player
def guildInstanceCancel(request, response):
    '''
    战斗中退出
    '''
    player = request.player
    instanceLevelId = getattr(request.logic_request, "instanceId", 0)

    # 取得动态的公会副本的信息
    guildInstancelevelInfo = get_sysguildinstanceInfo(instanceLevelId, player.guildId)
    if guildInstancelevelInfo.isFighting:
        guildInstancelevelInfo.cancel_fight()
    return response

@handle_common
@require_player
def guildInstanceReset(request, response):
    '''
    重置公会副本
    '''
    player = request.player
    instanceLevelId = getattr(request.logic_request, "instanceId", 0)

    # 普通成员没有权限开启副本
    if player.guild.isMember:
        AlertHandler(player, response, AlertID.ALERT_GUILD_LIMIT_CAN_NOT_OPEN_INSTANCE, u"guildInstanceReset your position is %s reset instance need 2 or 1" %(player.guild.position))
        return response

    # 取得动态的公会副本的信息
    guildInstancelevelInfo = get_guildinstanceInfo(instanceLevelId, player.guildId)
    new_guildinstance = reset_guildinstance(guildInstancelevelInfo)

    return response

@handle_common
@require_player
def guildInstanceStart(request, response):
    '''
    结算
    '''
    player = request.player
    level_id = getattr(request.logic_request, "instanceId", 0)
    isWin = getattr(request.logic_request, "isWin", False)
    bossHp = getattr(request.logic_request, "bossHp", 0)
    bossPercentage = getattr(request.logic_request, "bossPercentage", 0.0)

    guildInstancelevel = get_guildinstanceLevel(level_id)

    sysGuildInstance = get_sysguildinstanceInfo(level_id,player.guildId)

    #超时
    if not sysGuildInstance.isFighting or not sysGuildInstance.isOpen:
        sysGuildInstance.self_release_lock()
        return response
    subBossHPPercentage = float(sysGuildInstance.bossHp-bossHp)/guildInstancelevel.bossHp
    #打掉的boss 血量百分比
    #按照百分比获得此人应的公会币
    guildGold = int(subBossHPPercentage * guildInstancelevel.rewardGold)
    player.guild.add_gold(guildGold, info="get from attack guild boss. instanceId:%s. HP:%s " % (str(level_id), str(bossHp)))
    sysGuildInstance.end_fight(player, bossHp, bossPercentage, isWin)
    
    #reward
    # 完全通关（把boss打死以后发放公会副本的奖励）
    if isWin:
        rewardsCount = 0
        rewards_data = guildInstancelevel.rewardData
        for index, aucRewardId in enumerate(rewards_data["aucRewardIds"]):
            #修改副本掉落概率逻辑17-03-23
            #count = random.choice(range(0, rewards_data["aucRewardMaxCount"][index]+1))
            # for i in range(0, count):
            #     rewardsCount += 1
            #     create_guildauctionmaxinfo(player.guildId, aucRewardId, level_id)
            count = rewards_data["aucRewardMaxCount"][index]
            probability = rewards_data["probability"][index]
            for i in range(0,count):           
                if random.uniform(0,1) < probability:
                    rewardsCount += 1
                    create_guildauctionmaxinfo(player.guildId, aucRewardId, level_id)               
            
        #万一没有随机拿一个
        if rewardsCount == 0:
            aucRewardId = random.choice(rewards_data["aucRewardIds"])
            create_guildauctionmaxinfo(player.guildId, aucRewardId, level_id)


    #response.logic_response.set("aucRewardIds", rewardBoxes)
    response.logic_response.set("guild", player.guild.to_dict())

    return response

@handle_common
@require_player
def eliteInstanceStart(request, response):
    '''
    精英结算
    '''
    player = request.player
    eliteInstancelevel_id = getattr(request.logic_request, "instanceId", 0)
    heroLayoutData = getattr(request.logic_request, "heroLayoutData", [])
    deadCount = 0
    isWin = getattr(request.logic_request, "isWin", False)
    summary = getattr(request.logic_request, "summary", {})

    elite_instancelevel = get_eliteinstancelevel(eliteInstancelevel_id)
    playereliteinstancelevel = player.eliteinstancelevels.get(eliteInstancelevel_id)

    #副本没有开启
    if not playereliteinstancelevel:
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_NOT_OPEN, u"eliteInstanceStart:instance(%s) is not open" % eliteInstancelevel_id)
        return response


    if playereliteinstancelevel.succeedCount >= elite_instancelevel.eliteMaxPlayCount:
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_FIGHT_COUNT_EXCEED_MAX, u"eliteInstanceStart:instance(%s) fight number(%s) exceed maxCount(%s)" % (eliteInstancelevel_id, playereliteinstancelevel.succeedCount, elite_instancelevel.eliteMaxPlayCount))
        return response

    #[玩家卡id， 卡id， 站位行， 列]
    player.update_hero_layout(heroLayoutData)

    if summary:
        leftWarriorDead = summary["leftWarriorDead"] #英雄小兵全部存在
        for i in range(0, len(leftWarriorDead), 2):
            if int(str(leftWarriorDead[i])[0:2]) == 11:
                deadCount += leftWarriorDead[i+1]

    # 默認三星，死一個兩星，其餘一星
    star = get_star(deadCount)

    data = playereliteinstancelevel.fight(star, isWin)
    if isWin:
        player.sub_power(elite_instancelevel.elitePowerCost)

    rewards = data["rewards"]
    heroLevelUp = data["heroLevelUp"]


    if isWin:
        # 策划修改，完成精英副本的时候，计算每日任务，既算完成一次普通副本，也算完成一次精英副本
        player.dailytask_going(Static.DAILYTASK_CATEGORY_ELIT_INSTANCE, number=1, is_incr=True, is_series=True)
        # 完成一个副本以后，进行任务值的添加
        player.task_going(Static.TASK_CATEGORY_ELIT_INSTANCE, number=1, c1=eliteInstancelevel_id, is_incr=False, is_series=False)
        player.dailytask_going(Static.DAILYTASK_CATEGORY_INSTANCE, number=1, is_incr=True, is_series=True)
    player.update_eliteinstancelevel(playereliteinstancelevel, True)

    response.logic_response.set("rewards", rewards)
    response.logic_response.set("heroLevelUp",heroLevelUp)
    response.logic_response.set("summary",summary)
    response.common_response.player.set("soldiers", player.armies.to_dict())
    response.common_response.player.set("populationCost", player.populationCost)
    response.logic_response.set("star", star)

    return response


@handle_common
@require_player
def eliteInstanceSetUp(request, response):
    '''
    请求精英敌军信息
    '''

    player = request.player
    eliteInstanceId= getattr(request.logic_request, "instanceId", 0)

    eliteInstancelevel = get_eliteinstancelevel(eliteInstanceId)
    playereliteinstancelevel =  player.eliteinstancelevels.get(eliteInstanceId)

    if not playereliteinstancelevel:
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_NOT_OPEN, u"eliteInstanceSetUp:instance(%s) is not open" % eliteInstanceId)
        return response

    if playereliteinstancelevel.succeedCount >= eliteInstancelevel.eliteMaxPlayCount:
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_FIGHT_COUNT_EXCEED_MAX, u"eliteInstanceSetUp:instance(%s) fight count(%s) exceed max count(%s)" % (eliteInstanceId, playereliteinstancelevel.succeedCount, eliteInstancelevel.eliteMaxPlayCount))
        return response


    if player.power < eliteInstancelevel.elitePowerCost:
        AlertHandler(player, response, AlertID.ALERT_POWER_NOT_ENOUGH, u"eliteInstanceSetUp:power error (%s)" % player.power)
        return response
    # 敌人的信息表里面已经配置好了，不出意外可以直接拿来使用
    enemies = eliteInstancelevel.eliteEnemies
    if not enemies:
        raise ErrorException(player, u"eliteInstanceSetUp:levelid(%s) has not enemy" % eliteInstancelevel.id)

    #　做的是奖励的提前展示，具体这部分代码，以下会详细说明
    rewards = playereliteinstancelevel.make_elite_rewards_before_fight()

    player.update_eliteinstancelevel(playereliteinstancelevel, True)
    # 这里面添加了一个奖励的返回信息
    response.logic_response.set("rewards", rewards)
    response.logic_response.set("enemies", [enemy.to_dict() for enemy in enemies])
    return response


@handle_common
@require_player
def instanceSweep(request, response):
    '''
    扫荡
    '''
    level_id = getattr(request.logic_request, "instanceId", 0)
    count = getattr(request.logic_request, "count", 0)
    category = getattr(request.logic_request, "category", 0)


    player = request.player
    if category == 2:
        isElite = True
        instancelevel = get_eliteinstancelevel(level_id)
        playerinstancelevel = player.eliteinstancelevels.get(level_id)
    else:
        isElite = False
        instancelevel = get_instancelevel(level_id)
        playerinstancelevel = player.instancelevels.get(level_id)

    #副本没有开启
    if not playerinstancelevel:
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_NOT_OPEN, u"instanceSweep:instance(%s) is not open" % level_id)
        return response

    if not playerinstancelevel.can_sweep():
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_CAN_NOT_SWEEP, u"instanceSweep:instance(%s) can not sweep" % level_id)
        return response

    # todo １０级以前不可以扫荡

    if player.level < Static.SWEEP_OPEN_LEVEL:
        return response

    #扫荡卷判断
    #Static.ITEM_TYPE_SWEEP  扫荡卷id
    item_sweep = player.items.get(Static.ITEM_SWEEP_ID)
    if item_sweep and item_sweep.count > 0:
        use_diamond = False
    else:
        use_diamond = True

    if player.vip_level < Static.SWEEP_VIP_LEVEL and use_diamond:
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_SWEEP_VIP_ERROR, u"instanceSweep:vip(%s)  error" % player.vip_level)
        return response

    #次数判断
    if isElite:
        maxCount = instancelevel.eliteMaxPlayCount
        powerCost = instancelevel.elitePowerCost
    else:
        maxCount = instancelevel.maxPlayCount
        powerCost = instancelevel.powerCost

    if count > maxCount - playerinstancelevel.succeedCount:
        count = maxCount - playerinstancelevel.succeedCount

    if count == 0:
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_FIGHT_COUNT_EXCEED_MAX, u"instanceSweep:instance(%s) fight number(%s) exceed maxCount(%s)" % (level_id, count, maxCount))
        return response

    #体力判断
    if count > player.power/powerCost:
        count = player.power/powerCost

    if count == 0:
        AlertHandler(player, response, AlertID.ALERT_POWER_NOT_ENOUGH, u"instanceSweep:instance(%s) power is not enough" % level_id)
        return response

    if not use_diamond and not item_sweep.can_sub(count):
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_ITEM_SWEEP_NOT_ENOUGH, u"instanceSweep:item sweep number (%s) not enough" % (item_sweep.count))
        return response

    if use_diamond:
        if player.yuanbo < Static.SWEEP_INSTANCE_COST*count:
            AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"instanceSweep:playerDiamond(%s) costDiamond(%s)" % (player.yuanbo, Static.SWEEP_INSTANCE_COST*count))
            return response
        player.sub_yuanbo(Static.SWEEP_INSTANCE_COST*count, info=u"扫荡")
    else:
        item_sweep.sub(count , info=u"扫荡:%s:%s" % (level_id, isElite))


    rewards_list = playerinstancelevel.sweep(count)
    for rewards in rewards_list:
        for rewardDict in rewards:
            rewardTemp = CommonReward(rewardDict["type"], rewardDict["count"], 0)
            reward_send(player, rewardTemp, info=u"副本扫荡结算:%s" % level_id)


    if not isElite:
        player.sub_power(instancelevel.powerCost * count)
        player.task_going(Static.TASK_CATEGORY_INSTANCE, number=count, c1=instancelevel.id, is_incr=False, is_series=False)

    else:
        player.sub_power(instancelevel.elitePowerCost * count)
        player.task_going(Static.TASK_CATEGORY_ELIT_INSTANCE, number=count, c1=instancelevel.pk, is_incr=False, is_series=False)
        player.dailytask_going(Static.DAILYTASK_CATEGORY_ELIT_INSTANCE, number=count, is_incr=True, is_series=True)

    player.dailytask_going(Static.DAILYTASK_CATEGORY_INSTANCE, number=count, is_incr=True, is_series=True)


    if isElite:
        player.update_eliteinstancelevel(playerinstancelevel, True)
    else:
        player.update_instancelevel(playerinstancelevel, True)
    response.logic_response.set("rewards", rewards_list)
    return response


@handle_common
@require_player
def instanceBoxOpen(request, response):
    '''
    打开章节宝箱
    '''
    rewards = []
    player = request.player
    instance_id = getattr(request.logic_request, "instanceId", 0)
    chestLevel = getattr(request.logic_request, "level", 0)
    category = getattr(request.logic_request, "category", 0)

    if category == 2:
        isElite = True
        star_data = Static.ELITE_STAR_CHEST_OPEN_COUNTS
    else:
        isElite = False
        star_data = Static.STAR_CHEST_OPEN_COUNTS

    playerinstance_star = get_all_player_star_by_instance_id(player, instance_id, isElite)
    if playerinstance_star < star_data[chestLevel]:
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_CHEST_CAN_NOT_OPEN, u"instanceBoxOpen:instatnce(%s) playerinstance_star(%s) chestlevel(%s)" % (instance_id, playerinstance_star, star_data[chestLevel]))
        return response

    if not player.chestWithDrawn(instance_id, chestLevel, isElite):
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_CHEST_ALREADY_OPEN, u"instanceBoxOpen:instatnce(%s) chest is opened" % (instance_id))
        return response

    rewards = get_chest_rewards(player, instance_id, chestLevel, isElite)
    for reward in rewards:
        rewardTemp = CommonReward(reward["type"], reward["count"], 0)
        reward_send(player, rewardTemp, info=u"打开章节宝箱:%s" % instance_id)

    response.common_response.player.set("starBox", {"history" : player.starChest})
    response.common_response.player.set("eliteStarBox", {"history" : player.eliteStarChest})
    response.logic_response.set("rewards", rewards)
    return response

@handle_common
@require_player
def instanceReset(request, response):
    '''
    刷新副本次数
    '''
    #type = 1 普通 2 精英
    player = request.player
    level_id = getattr(request.logic_request, "instanceId", 0)
    category = getattr(request.logic_request, "category", 0)


    if category == 1:
        isElite = False
        instancelevel = get_instancelevel(level_id)
    elif category == 2:
        isElite = True
        instancelevel = get_eliteinstancelevel(level_id)
    else:
        raise ErrorException(player, u"instance reset category error (%s)" % level_id)

    if isElite:
        playerinstancelevel = player.eliteinstancelevels.get(instancelevel.pk)
    else:
        playerinstancelevel = player.instancelevels.get(instancelevel.pk)

    if not playerinstancelevel:
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_NOT_OPEN, u"instanceReset:instance(%s) is not open" % level_id)
        return response


    vip = get_vip(player.vip_level)
    if playerinstancelevel.refreshCount >= vip.resetElitInstanceCount:
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_REFRESH_COUNT_EXCEED_MAX, u"instanceReset:instance(%s) refresh count(%s) exceed max(%s)" % (level_id, playerinstancelevel.refreshCount , vip.resetElitInstanceCount))
        return response

    cost_diamond = Static.REFRESH_INSTANCE_COST * (playerinstancelevel.refreshCount + 1)

    if player.yuanbo < cost_diamond:
        AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"instanceReset:instance(%s) refresh costDiamond(%s) playerDiamond(%s)" % (level_id, cost_diamond,  player.yuanbo ))
        return response

    player.sub_yuanbo(cost_diamond, info=u"重置副本次数")
    playerinstancelevel.refresh_count()

    if isElite:
        player.update_eliteinstancelevel(playerinstancelevel, True)
    else:
        player.update_instancelevel(playerinstancelevel, True)

    return response

@handle_common
@require_player
def raceInstanceSetUp(request, response):
    """
    活动副本阵容
    """
    player = request.player
    data = {}
    # 活动副本的id，通过活动副本里面配置的字段去找对应的活动副本关卡的信息
    raidinstancelevel_id = getattr(request.logic_request, "raidId", 0)



    # 活动副本关卡id
    level_id = getattr(request.logic_request, "instanceId", 0)
    raidinstance = get_raidinstance(raidinstancelevel_id)


    # 验证没有这个章节
    if not raidinstance:
        raise ErrorException(player, u"raid instance id error (%s)" % raidinstancelevel_id)

    # 验证关卡是否包含在章节中
    if level_id not in raidinstance.raidLevel_ids:
        raise ErrorException(player, u"raid instance level id error (%s)" % level_id)

    # 活动副本关卡对象
    raidlevel = get_raidlevel(level_id)

    if raidlevel.minUserLevel > player.level:
        AlertHandler(player, response, AlertID.ALERT_PLAYER_LEVEL_NOT_ENOUGH, u"raceInstanceSetUp:instance(%s) openlevel(%s) playerlevel(%s)" % (level_id, raidlevel.minUserLevel, player.level))
        return response

    # 检查活动副本是否开启，黑名单，白名单，时间之类的检查。
    if raidinstance.experiment1 and not check_player_in_experiment_by_experimentname(player.id, raidinstance.experiment1):
        AlertHandler(player, response, AlertID.ALERT_RAID_INSTANCE_IS_NOT_OPEN, u"raceInstanceSetUp:instance(%s) is not open" % (level_id))
        return response

    _, playerraidinstance = player.raidinstances.get_or_create(raidinstance.id)
    vip = get_vip(player.vip_level)
    if playerraidinstance.succeedCount >= vip.titanCount and not raidinstance.category == 6:
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_FIGHT_COUNT_EXCEED_MAX, u"raceInstanceStart:instance(%s) level_id(%s) fight number(%s) exceed maxCount(%s)" % (raidinstance.id, level_id, playerraidinstance.succeedCount, vip.titanCount))
        return response
    #if raidinstance.category == 6:
    #    enemyId = raidlevel.enemyIds[(player.dailyWaveCount/3 * 3 + 2)] * 10
    #    Towerrewards = get_raidenemytoreward(enemyId)
    #    if Towerrewards:
    #        rewards = Towerrewards.get_towerrewards()
    #        towerrewards = [reward.to_dict() for reward in rewards]

    #    else:
    #        towerrewards = []

    #    # 记录当前的奖励
    #    player.towerRewardsId = enemyId
    #    player.set_update("towerRewardsId")

    # 检查通过以后返回活动副本关卡的敌方阵容
    enemies = raidlevel.enemies
    #difficulties = []
    #monsterId = []

    #if not enemies:
    #    response.logic_response.set("enemies", [])
    #else:
        # 如果是爬塔模式，历史波数定制
        #if raidinstance.category == 6:
        #    response.logic_response.set("rewards", towerrewards)
        #    # -1 代表未完成完整的一层，一层三波。
        #    if player.towerStatus == -1:
        #        enemies = enemies[player.dailyWaveCount/3*3:player.dailyWaveCount/3*3+3]
        #        enemyDiffIds = raidlevel.enemyIds[player.dailyWaveCount/3*3:player.dailyWaveCount/3*3+3]
        #        for enemyid in enemyDiffIds:
        #            difficulties.extend(get_raidenemytoreward(enemyid).get_difficulties())
        #            Towerrewards = get_raidenemytoreward(enemyid)
        #            monsterId.append(Towerrewards.monsterId)

        #    else:
        #        enemies = enemies[player.dailyWaveCount/3*3 - 3:player.dailyWaveCount/3*3]
        #        for enemy in enemies:
        #            monsterId.append(get_raidenemytoreward(enemy.pk).monsterId)


        # 这个塔一共有多少层
        #response.logic_response.set("towerLevel", len(raidlevel.enemyIds) / 3)
        #response.logic_response.set("difficulties", difficulties)
    response.logic_response.set("enemies", [enemy.to_dict() for enemy in enemies])
    response.logic_response.set("experiment2", raidinstance.experiment2)

        #response.logic_response.set("monsterIds", monsterId)

    return response

@handle_common
@require_player
def raceInstanceStart(request, response):
    """
    活动副本结算
    """
    player = request.player
    raidinstance_id = getattr(request.logic_request, "raidId", 0)
    level_id = getattr(request.logic_request, "instanceId", 0)
    waveCount = getattr(request.logic_request, "waveCount", 0)
    star = getattr(request.logic_request, "star", 0)
    isWin = getattr(request.logic_request, "isWin", False)
    heroLayoutData = getattr(request.logic_request, "heroLayoutData", [])
    percentage = getattr(request.logic_request, "percentage", 0.0)
    summary = getattr(request.logic_request, "summary", {})

    if percentage > 1:
        percentage = 0

    # 活动副本章节
    raidinstance = get_raidinstance(raidinstance_id)

    if not raidinstance:
        raise ErrorException(player, u"raceInstanceStart:raid instance id error (%s)" % raidinstance_id)
    if level_id not in raidinstance.raidLevel_ids:
        raise ErrorException(player, u"raceInstanceStart:raid instance level id error (%s)" % level_id)

    raidlevel = get_raidlevel(level_id)
    if raidlevel.minUserLevel > player.level:
        AlertHandler(player, response, AlertID.ALERT_LEVEL_SHORTAGE, u"raceInstanceStart:instance(%s) openlevel(%s) playerlevel(%s)" % (level_id, raidlevel.minUserLevel, player.level))
        return response

    #次数check
    _, playerraidinstance = player.raidinstances.get_or_create(raidinstance_id)
    vip = get_vip(player.vip_level)
    # 爬塔没有次数限制
    if playerraidinstance.succeedCount >= vip.titanCount and not raidinstance.category == 6:
        AlertHandler(player, response, AlertID.ALERT_INSTANCE_FIGHT_COUNT_EXCEED_MAX, u"raceInstanceStart:instance(%s) level_id(%s) fight number(%s) exceed maxCount(%s)" % (raidinstance.id, level_id, playerraidinstance.succeedCount, vip.titanCount))
        return response
    player.update_hero_layout(heroLayoutData)


    data = playerraidinstance.fight(raidlevel, isWin, percentage)
    player.update_raidinstance(playerraidinstance, True)
    if isWin:
        # raidinstance.powerCost 消耗的体力 现改为消耗耐力
        player.sub_stamina(raidinstance.powerCost)

        #if raidinstance.category == 6:
        #    if level_id > player.lastRaidId:
        #        # 记录最新的塔id
        #        player.lastRaidId = level_id
        #        player.set_update("lastRaidId")

        #    # 记录当前的波数
        #    player.dailyWaveCount = waveCount
        #    player.set_update("dailyWaveCount")
        #    # 副本完成状态

        #    # 记录当前一共有的星星的数
        #    player.towerStar += star
        #    player.set_update("towerStar")
        #    # 顺序记录副本的通关星星状态
        #    # todo 这里没想好怎么做。暂时先屏蔽了
        #    # player.towerSweep.append(level_id)
        #    # player.towerSweep.append(star)

        #    player.set_update("towerSweep")
        #    # -1 继续进副本战斗 0去开箱领奖　1-5领了几层箱子
        #    if waveCount % 3 == 0:
        #        # 记录当前一层完成状态更改
        #        player.towerStatus = 0
        #        player.set_update("towerStatus")
        #        player.choiceBuffs()
        #        response.logic_response.set("buffs", player.buyBuffsList)

        #    player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_RACE_INSTANCE, number=player.dailyWaveCount, is_incr=False, with_top=True, is_series=True)

        #else:
        player.dailytask_going(Static.DAILYTASK_CATEGORY_RACE_INSTANCE, number=1, is_incr=True, is_series=True)

    #if raidinstance.category == 6:
    #    player.dailytask_going(Static.DAILYTASK_CATEGORY_EXPEDITION_SUCCESS, number=1, is_incr=True, is_series=True)



    rewards = data["rewards"]
    heroLevelUp  = []
    heroLevelUp = data["heroLevelUp"]
    number = data["number"]
    for rewardDict in rewards:
        rewardTemp = CommonReward(rewardDict["type"], rewardDict["count"], 0)
        rewardDict["count"] *= number
        reward_send(player, rewardTemp, info=u"活动副本结算:%s:%s" % (raidinstance_id,level_id), number=number)

    response.logic_response.set("rewards", rewards)
    response.logic_response.set("heroLeveleUp",heroLevelUp)
    response.logic_response.set("summary",summary)
    #response.common_response.player.set("towerStar", player.towerStar)
    #response.common_response.player.set("towerStatus", player.towerStatus)
    #response.common_response.player.set("buyBuffsList", player.buyBuffsList)
    response.common_response.player.set("soldiers", player.armies.to_dict())
    response.common_response.player.set("populationCost", player.populationCost)
    response.common_response.player.set("raidInstance", {"instances":get_player_open_raidinstance(player)})

    return response


@handle_common
@require_player
def smallGameFinish(request, response):
    '''
    小游戏
    '''
    player = request.player
    score = getattr(request.logic_request, "score", 0) #得分
    #次数不足
    if player.smallGameLeftTimes <= 0:
        return response

    rewards = []
    # 获取小游戏的奖励
    gameRules = get_smallGames()
    #　按照积分顺序从大到小排
    gameRules = sorted(gameRules,key=lambda x: x.score)

    info = u'小游戏奖励'

    for gameRule in gameRules:
        if score < gameRule.score:
            rewards = gameRule.rewards
            break

    # 奖励分为三个类别，金币，钻石，和物品
    for reward in rewards:
        reward_send(player, reward, info)

    player.smallGameBattle()

    player.dailytask_going(Static.DAILYTASK_CATEGORY_SMALLGAME, number=1, is_incr=True, is_series=True)

    response.logic_response.set("rewards", [reward.to_dict() for reward in rewards])
    response.common_response.player.set("smallGameLeftTimes", player.smallGameLeftTimes)

    return response

@handle_common
@require_player
def elementTowerOpen(request, response):
    '''
    元素之塔开启
    '''
    towerId = getattr(request.logic_request, "towerId", -1)
    player = request.player

    towerInstance = get_elementtowerinstance(towerId)

    if not towerInstance:
        raise ErrorException(player, u"elementTowerOpen towerId(%s) is error" % towerId)

    if player.level < towerInstance.minUserLevel:
        raise ErrorException(player, u"elementTowerOpen towerId(%s) level(%s) is error" % (towerId, player.level))

    if player.elementTower.towerId > 0:
        raise ErrorException(player, u"elementTowerOpen towerId(%s) is opened" % (player.elementTower.towerId))

    player.elementTower.open(towerId)
    response.common_response.player.set("elementTower", player.elementTower.to_dict())
    return response


@handle_common
@require_player
def elementTowerReset(request, response):
    '''
    元素之塔重置
    '''
    player = request.player

    if player.elementTower.towerId <= 0:
        raise ErrorException(player, u"elementTowerReset tower is not opened")

    if player.elementTower.refreshLeftCount > 0:
        player.elementTower.reset(1)
    elif player.elementTower.rewardCount > 0:
        player.elementTower.reset(2)
    elif player.elementTower.diamondLeftCount > 0:
        cost = player.elementTower.diamondResetCost
        if player.yuanbo < cost:
            AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"elementTowerReset:playerDiamond(%s) costDiamond(%s) is not enough" % (player.yuanbo, cost))
            return response
        player.sub_yuanbo(cost, info=u"元素之塔重置")
        player.elementTower.reset(3)

    response.common_response.player.set("elementTower", player.elementTower.to_dict())
    return response

@handle_common
@require_player
def elementTowerInstanceSetUp(request, response):
    """
    活动副本阵容
    """
    player = request.player

    instance = get_elementtowerinstance(player.elementTower.towerId)
    instanceLevel = instance.levels[player.elementTower.levelId - 1]
    response.logic_response.set("enemies", [enemy.to_dict() for enemy in instanceLevel.enemies])
    return response


@handle_common
@require_player
def elementTowerInstanceStart(request, response):
    """
    活动副本结算
    """
    player = request.player
    isWin = getattr(request.logic_request, "isWin", False)
    star = getattr(request.logic_request, "star", 0)
    levelId = getattr(request.logic_request, "levelId", 0)
    towerId = getattr(request.logic_request, "towerId", 0)

    if player.elementTower.towerId != towerId:
        raise ErrorException(player, u"elementTowerInstanceStart towerId(%s) is error" % towerId)

    if player.elementTower.levelId != levelId:
        raise ErrorException(player, u"elementTowerInstanceStart levelId(%s) is error" % levelId)

    if not player.elementTower.levelIsOpen:
        raise ErrorException(player, u"elementTowerInstanceStart levelStatus(%s) is error" % player.elementTower.levelStatus)

    data = player.elementTower.fight(isWin, star)
    #七日任务 日常任务
    if isWin:
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_ELEMENTTOWER_SUCCESS, number=levelId/3, is_incr=False, with_top=True, is_series=True)
    player.dailytask_going(Static.DAILYTASK_CATEGORY_ELEMENTTOWER_FIGHT, number=1, is_incr=True, is_series=True)


    rewards = data["rewards"]
    for reward in rewards:
        reward_send(player, reward, info=u"爬塔结算:%s:%s" % (towerId,levelId))

    response.logic_response.set("rewards", [reward.to_dict() for reward in rewards])
    response.common_response.player.set("elementTower", player.elementTower.to_dict())

    return response

@handle_common
@require_player
def elementTowerBoxOpen(request, response):
    """
    元素之塔宝箱开启状态
    """

    player = request.player
    status = getattr(request.logic_request, "status", 0) #0 放弃 1 开启
    category = getattr(request.logic_request, "category", 0)
    levelId = getattr(request.logic_request, "levelId", 0)

    #正常逻辑开箱子
    if not player.elementTower.isInSweep:
        if not player.elementTower.boxCanOpen:
            raise ErrorException(player, u"elementTowerBoxOpen levelStatus(%s) is error" % player.elementTower.levelStatus)

        cost = player.elementTower.tower.levels[player.elementTower.levelId - 1].diamondCosts[player.elementTower.diamondBoxIndex]

        if status and player.yuanbo < cost:
            AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"elementTowerBoxOpen:playerDiamond(%s) costDiamond(%s)" % (player.yuanbo,  cost))
            return response

        if status and cost:
            player.sub_yuanbo(cost, info=u"元素之塔%s, level(%s)开启宝箱, %s" % (player.elementTower.towerId, player.elementTower.levelId, player.elementTower.diamondBoxIndex))

        rewards = player.elementTower.openDiamondBox(status)
    #扫荡开箱子
    else:
        if "boxLevelIds" not in player.elementTower.sweepInfo or len(player.elementTower.sweepInfo["boxLevelIds"]) == 0:
            raise ErrorException(player, u"elementTowerBoxOpen sweep not box can open")

        # levelId = player.elementTower.sweepInfo["boxLevelIds"][0][0]
        # boxIndex = player.elementTower.sweepInfo["boxLevelIds"][0][1]
        cost = 0
        if status:
            cost = player.elementTower.openSweepDiamondBoxCost(category, levelId)
        if status and player.yuanbo < cost:
            AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"elementTowerBoxOpen:sweep:playerDiamond(%s) costDiamond(%s)" % (player.yuanbo,  cost))
            return response

        if status and cost:
            player.sub_yuanbo(cost, info=u"元素之塔%s, sweep level(%s)开启宝箱, %s" % (player.elementTower.towerId, levelId, status))

        rewards = player.elementTower.openSweepDiamondBox(status, category, levelId)

    for reward in rewards:
        reward_send(player, reward, info=u"开宝箱奖励:%s:%s" % (player.elementTower.towerId,player.elementTower.levelId))

    response.logic_response.set("rewards", [reward.to_dict() for reward in rewards])
    response.logic_response.set("category", category)
    response.common_response.player.set("elementTower", player.elementTower.to_dict())
    return response

@handle_common
@require_player
def elementTowerChoiceBuff(request, response):
    """
    元素之塔选择BUFF
    """

    player = request.player
    index = list(set(getattr(request.logic_request, "index", [0]))) #0 放弃 1-3 3个buff

    if not player.elementTower.isInSweep:
        if not player.elementTower.buffCanChoice:
            raise ErrorException(player, u"elementTowerChoiceBuff levelStatus(%s) is error" % player.elementTower.levelStatus)

        if 0 not in index:
            costStar = 0
            for i in index:
                costStar += Static.ELEMENTTOWER_CHOCIE_BUFF_COSTS[i - 1]
            #星星数量不足
            if player.elementTower.star < costStar:
                response.common_response.player.set("elementTower", player.elementTower.to_dict())
                return response
            player.elementTower.sub_star(costStar)
        player.elementTower.choiceBuff(index)
    else:
        if "buffLevelIds" not in player.elementTower.sweepInfo or len(player.elementTower.sweepInfo["buffLevelIds"]) == 0:
            raise ErrorException(player, u"elementTowerChoiceBuff sweep not box can choice")

        if 0 not in index:
            costStar = 0
            for i in index:
                costStar += Static.ELEMENTTOWER_CHOCIE_BUFF_COSTS[i - 1]

            #星星数量不足
            if player.elementTower.star < costStar:
                response.common_response.player.set("elementTower", player.elementTower.to_dict())
                return response

            player.elementTower.sub_star(costStar)
        player.elementTower.choiceSweepBuff(index)

    response.common_response.player.set("elementTower", player.elementTower.to_dict())
    return response

@handle_common
@require_player
def elementTowerInstanceSweep(request, response):
    """
    扫荡
    """

    player = request.player

    if player.elementTower.isSweep:
        return response
    data = player.elementTower.sweep()
    _t1Rewards = []
    for rewards in data["rewards"]:
        _t2Rewards = []
        for reward in rewards:
            reward_send(player, reward, info=u"元素之塔扫荡结算")
            _t2Rewards.append(reward.to_dict())
        _t1Rewards.append(_t2Rewards)

    _t3Rewards = []
    for rewards in data["freeBoxRewards"]:
        reward_send(player, rewards, info=u"元素之塔扫荡开启免费宝箱")
        _t3Rewards.append(rewards.to_dict())

    player.dailytask_going(Static.DAILYTASK_CATEGORY_ELEMENTTOWER_FIGHT, number=1, is_incr=True, is_series=True)
    response.common_response.player.set("elementTower", player.elementTower.to_dict())
    response.logic_response.set("rewards", _t1Rewards)
    response.logic_response.set("freeBoxRewards", _t3Rewards)

    return response


@handle_common
@require_player
def guildInstanceBook(request, response):
    """
    公会副本飞鸽传书  & bookType 0 为一键提醒  其他为关闭此副本的提醒
    """
    player = request.player
    instanceId = getattr(request.logic_request, "instanceId", 0)
    bookType = getattr(request.logic_request, "bookType", 0)

    if bookType == 1:
        if str(player.id) in player.guild.guildInfo.feiBookDict:
            if str(instanceId) in player.guild.guildInfo.feiBookDict[str(player.id)]:
                del player.guild.guildInfo.feiBookDict[str(player.id)][str(instanceId)]
                player.guild.guildInfo.save()
        return response
    #会长
    if not player.guild.isChairman:
        # TODO：更换 AlertID
        AlertHandler(player, response, AlertID.ALERT_GUILD_LIMIT_NOT_ENOUGH, u"guildInstanceBook:only chairman or vice-chairman can send feiBook")
        return response

    # if not instanceId or (bookType and not to_player_id):

    # 取得公会副本的信息
    sysGuildInstanceInfo = get_sysguildinstanceInfo(instanceId, player.guildId)
    if not sysGuildInstanceInfo or not sysGuildInstanceInfo.canFeiBook:
        if sysGuildInstanceInfo:
            sysGuildInstanceInfo.self_release_lock()
        AlertHandler(player, response, AlertID.ALERT_GUILD_INSTANCE_HAS_ALREADY_EXPIRED, u"guildInstanceBook this instacelevel has already expired")
        return response


    if not sysGuildInstanceInfo or not sysGuildInstanceInfo.isOpen:
        if sysGuildInstanceInfo:
            sysGuildInstanceInfo.self_release_lock()
        AlertHandler(player, response, AlertID.ALERT_GUILD_INSTANCE_HAS_ALREADY_EXPIRED, u"guildInstanceBook this instacelevel has already expired")
        return response

    pid_list = sysGuildInstanceInfo.get_unFighting_member_list()
    for player_id in pid_list:
        if str(player_id) not in player.guild.guildInfo.feiBookDict:
            player.guild.guildInfo.feiBookDict[str(player_id)] = {str(instanceId): int(time.time())}
        elif instanceId not in player.guild.guildInfo.feiBookDict[str(player_id)].keys():
            player.guild.guildInfo.feiBookDict[str(player_id)][str(instanceId)] = int(time.time())
    # response.logic_response.set("configinfo", configinfo.to_dict())
    return response
