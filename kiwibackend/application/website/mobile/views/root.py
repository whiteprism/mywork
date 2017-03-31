# -*- encoding:utf8 -*-
import time
from decorators import require_player, handle_common, deco_root
from module.common.static import Static, AlertID, ErrorID
from module.vip.api import get_vip
from module.common.middleware import AlertHandler
from django.conf import settings
from module.playeractivity.api import update_playeractivities
from module.playerinstance.api import get_player_view_instance_dict, get_player_open_raidinstance
from module.instance.api import get_instancelevel
from module.activity.api import get_activities
from module.playerhero.api import get_tutorial_heroes
from module.rewards.api import reward_send
import datetime
from module.utils import _check_name, datetime_to_unixtime
from module.hero.api import get_heroskill
from module.playerPVP.api import get_lastweek_rank, get_yesterday_rank
import random
from module.utils import delta_time
import time

@handle_common
@deco_root
def init(request, response):
    player = request.player

    player.init_md5Keys()#初始化md5 seed
    #封号检查
    now = datetime.datetime.now()
    if delta_time(now, player.banAt) > 1:
        #时间差大于1秒
        response.common_response.set("success", False)
        response.common_response.set("errorCode", ErrorID.ERROR_BANNED)
        return response
    activities = get_activities()
    #更新所有奖励
    update_playeractivities(player)
    player.mysteryshop.refresh_auto()

    # player.guildshop.refresh_auto()

    playeritems = player.items.all().values()
    for playeritem in playeritems:
        player.update_item(playeritem)

    playerbuyrecords = player.buyrecords.all().values()
    for playerbuyrecord in playerbuyrecords:
        player.update_buyrecord(playerbuyrecord)

    #playerbuytowerrecords = player.buytowerrecords.all().values()
    #for playerbuytowerrecord in playerbuytowerrecords:
    #    player.update_buytowerrecord(playerbuytowerrecord)

    playerequips = player.equips.all().values()
    for playerequip in playerequips:
        player.update_equip(playerequip)

    playerequipfragments = player.equipfragments.all().values()
    for playerequipfragment in playerequipfragments:
        player.update_equipfragment(playerequipfragment)

    playerartifacts = player.artifacts.all().values()
    for playerartifact in playerartifacts:
        player.update_artifact(playerartifact)

    playerheroes = player.heroes.all().values()
    for playerhero in playerheroes:

        skillhero = get_heroskill(playerhero.warrior.cardId)
        for i in range(0, len(skillhero.skillinfo)/3):
            skillGild, _, upgrade = skillhero.skillinfo[i*3:(i+1)*3]
            if upgrade > playerhero.upgrade:
                setattr(playerhero, "skill%sLevel" % (i+1), 0)
            else:
                if not getattr(playerhero, "skill%sLevel" % (i+1), 0):
                    setattr(playerhero, "skill%sLevel" % (i+1), 1)

        player.update_hero(playerhero, True)

    playerheroteams = player.heroteams.all().values()
    for playerheroteam in playerheroteams:
        playerheroteam.update_score()
        player.update_heroteam(playerheroteam, True)

    playersouls = player.souls.all().values()
    for playersoul in playersouls:
        player.update_soul(playersoul)

    playerbuildings = player.buildings.all().values()
    for playerbuilding in playerbuildings:
        playerbuilding.check_upgrade()
        player.update_building(playerbuilding)

    playerbuildingplants = player.buildingplants.all().values()
    for playerplant in playerbuildingplants:
        playerplant.check_status()
        player.update_buildingplant(playerplant)

    playerartifacts = player.artifacts.all().values()
    for playerartifact in playerartifacts:
        player.update_artifact(playerartifact)

    playerartifactfragments = player.artifactfragments.all().values()
    for playerartifactfragment in playerartifactfragments:
        player.update_artifactfragment(playerartifactfragment)
        
    playerbuildingfragments = player.buildingfragments.all().values()
    for playerbuildingfragment in playerbuildingfragments:
        player.update_buildingfragment(playerbuildingfragment)

    playeractivities = player.activities.all().values()
    for playeractivity in playeractivities:
        if playeractivity.activity.isOpen(player.userid):
            player.update_activity(playeractivity)

    for category, _ in player.dailyTasks.items():
        player.update_dailytask(category)

    for category, _ in player.tasks.items():
        player.update_task(category)


    for category, _ in player.dailyTasks.items():
        player.update_dailytask(category)

    for category, _ in player.sevenDaystasks.items():
        player.update_seven_days_task(category)


    if player.tutorial["guideGid"] == Static.TUTORIAL_ID_ELITE_INSTANCE and player.tutorial["status"] == 1:
        player.tutorial_complete()

    # 提前先更新，不然一会返回倒计时的时候会刷新时间
    #player.PVP.update_oppIds()

    #response.common_response.player.set("opps", sumOpps)
    response.common_response.player.set("dailyOppdata", get_yesterday_rank())
    response.common_response.player.set("weekOppdata", get_lastweek_rank())

    response.common_response.player.set("activityValue", player.activityValue)
    response.common_response.player.set("towerGold", player.towerGold)
    response.common_response.player.set("tavern", player.tavern)
    response.common_response.player.set("gold",player.gold)
    response.common_response.player.set("wood",player.wood)
    response.common_response.player.set("diamond", player.yuanbo)
    response.common_response.player.set("xp", player.xp)
    response.common_response.player.set("couragePoint", player.couragepoint)
    response.common_response.player.set("level", player.level)
    response.common_response.player.set("power", player.power)
    response.common_response.player.set("stamina", player.stamina)
    response.common_response.player.set("vip", player.vip)
    response.common_response.player.set("daysFromcreated", player.daysFromcreated)
    response.common_response.player.set("activityBoxIds", player.activityBoxIds)
    response.common_response.player.set("completeTaskList", [(int(taskId), status) for taskId, status in player.completeSevenTasks.items()])
    response.common_response.player.set("dailyTaskActivity", player.dailyTaskActivity)
    response.common_response.player.set("halfBuyIds", player.halfBuyIds)
    #response.common_response.player.set("speedCount", player.speedCount)
    #response.common_response.player.set("beSpeededCount", player.beSpeededCount)
    response.common_response.player.set("powerCDTime",  player.next_power_time)
    response.common_response.player.set("staminaCDTime",  player.next_stamina_time)
    response.common_response.player.set("weekCardLeftDay", player.week_card_left_day)
    response.common_response.player.set("monthCardLeftDay", player.month_card_left_day)
    response.common_response.player.set("permanentCardActivity", player.permanent_card_is_activity)
    response.common_response.player.set("wallHp", player.wall_level)
    response.common_response.player.set("tutorial", player.tutorial)
    response.common_response.player.set("buyDiamondIds", player.yuanboshop.to_dict())
    response.common_response.player.set("hasUnReadMails", player.has_unread_mails)
    response.common_response.player.set("openDiamondShop", settings.OPEN_PAYMENT)
    response.common_response.player.set("mysteryShop", player.mysteryshop.to_dict())
    response.common_response.player.set("guildShop", player.guildshop.to_dict())
    response.common_response.player.set("guild", player.guild.to_dict(True, True))

    response.common_response.player.set("playerWarriorIds", player.playerWarriorIds)
    response.common_response.player.set("lastRaidId", player.lastRaidId)
    response.common_response.player.set("smallGameLeftTimes", player.smallGameLeftTimes)
    response.common_response.player.set("elementTower", player.elementTower.to_dict())
    response.common_response.player.set("offlinebonus",player.offlinebonus)
    response.common_response.player.set("wallWarriorIds", player.wallWarriorIds)
    response.common_response.player.set("safedTime", player.safedTime)

    #PVP
    if player.isOpenArena:
        player.arenashop.refresh_auto()
        response.common_response.player.set("honorShop", player.arenashop.to_dict())
        response.common_response.player.set("arena", player.PVP.to_dict())
    #攻城战
    if player.isOpenSiege:
        # TODO: 攻城战刷新
        # player.SiegeBattle.refresh_auto()
        response.common_response.player.set("siegeBattle", player.SiegeBattle.to_dict())

    # fire = get_fireinfo_by_guildId(player.guildId)
    # if fire:
    #     fire = fire[0]
    #     make_fireInfo(fire)

    # response.common_response.player.set("fireBuff", player.fireBuff)

    response.common_response.player.set("userInfo", player.userSimple_dict())
    response.common_response.player.set("soldiers", player.armies.to_dict())


    if player.tutorial_id == Static.TUTORIAL_ID_INIT_1:
        player_tutorial_heroes = get_tutorial_heroes(player)


        response.common_response.player.set("tutorialHeroes",  [hero.to_dict() for hero in player_tutorial_heroes])
        enemies = get_instancelevel(1).enemies
        response.common_response.player.set("enemies", [enemy.to_dict() for enemy in enemies])

    response.common_response.player.set("instance", get_player_view_instance_dict(player))
    response.common_response.player.set("starBox", {"history": player.starChest})
    response.common_response.player.set("eliteStarBox", {"history": player.eliteStarChest})
    response.common_response.player.set("raidInstance", {"instances":get_player_open_raidinstance(player)})
    # response.common_response.player.set("waravoidCDTime", player.waravoidCDTime)
    response.common_response.player.set("seeds", player.md5Seeds)
    response.common_response.player.set("firstIn", player.firstIn)
    #整点请求
    now = datetime.datetime.now()
    next_hour = now + datetime.timedelta(seconds=3600)
    next_int_hour = datetime.datetime(next_hour.year, next_hour.month, next_hour.day, next_hour.hour)
    serverIntCDTime = (next_int_hour - now).total_seconds() + 1
    response.common_response.set("serverIntCDTime", int(serverIntCDTime))
    response.common_response.player.set("defenseHeroIds", player.defenseHeroIds)
    response.common_response.player.set("defenseSiegeIds", player.defenseSiegeIds)
    response.common_response.player.set("defenseSiegeSoldierIds", player.defenseSiegeSoldierIds)
    #zrd
    response.common_response.set("activities",  [activity.to_dict() for activity in activities])
    response.common_response.set("serverTime", int(time.time()))
    return response

@handle_common
@require_player
def setting(request, response):
    """
    用户设置
    """
    player = request.player
    category = getattr(request.logic_request, "category", 0)

    if category == 1:
        iconId = getattr(request.logic_request, "iconId", 0)
        player.set("iconId", iconId)
        status = 1
    elif category == 2:
        # status = 1 #成功   2  重名   3  名字长短在2-6位   4  含有特殊字符    5 禁词
        name = getattr(request.logic_request, "name", '')
        if type(name) == str:
            name = unicode(name, "utf8")
        status = _check_name(name)
        if status == 1:
            player.set("name", name)
            if not player.tutorial_id == Static.TUTORIAL_ID_INIT_1:
                player.set("firstIn", 0)

    response.common_response.player.set("userInfo", player.userSimple_dict())
    response.logic_response.set("status", status)
    return response


@handle_common
@require_player
def vipRewardsGet(request, response):
    player = request.player
    vip_level = getattr(request.logic_request, "vipLevel", 0)
    vip_level = int(vip_level)

    if not player.can_buy_vip_bag(vip_level) and vip_level > 0:

        AlertHandler(player, response, AlertID.ALERT_VIP_CAN_NOT_BUY, u"vipRewardsGet:vipLevel(%s) playerVipLevel(%s) can_buy_vip_bag" % (vip_level, player.vip_level))
        return response

    vip = get_vip(vip_level)
    if player.yuanbo < vip.giftBagDiamond:
        AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"vipRewardsGet:vipLevel(%s) playerVipLevel(%s) price(%s) playerYuanbo(%s)" % (vip_level, player.vip_level, vip.giftBagDiamond, player.yuanbo))
        return response


    player.buy_vip_bag(vip_level)
    rewards = vip.giftRewards
    info = u"VIP礼包:%s" % vip_level
    for reward in rewards:
        reward_send(player, reward, info)
    player.sub_yuanbo(vip.giftBagDiamond, info)
    response.common_response.player.set("vip", player.vip)
    return response
