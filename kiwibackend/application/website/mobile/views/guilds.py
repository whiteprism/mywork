# -*- encoding:utf-8 -*-
from decorators import require_player, handle_common
from module.common.static import Static, AlertID
from module.player.api import get_player, filter_robots_by_level, get_pvp_players
from module.common.middleware import ErrorException, AlertHandler
from module.playerequip.api import  acquire_equipfragment
from module.playerartifact.api import acquire_artifactfragment
import random, datetime
from module.mail.api import send_system_mail
from module.guild.api import get_guildmaxinfo, get_guildauctionmaxinfos, get_sysguildinstanceInfo, get_guildinfos,get_all_guilds, get_guild_by_id, get_guild_by_name
from module.guild.api import get_guild, get_guildfirebuff, get_guildshop, get_sysguild_instances, create_sysguildinstance, get_guildfirelevel, get_guildsiegeconfiginfo_by_playerid, create_guildsiegeconfiginfo
from module.vip.api import get_vip
from module.instance.api import get_all_guildinstancelevels, get_all_instancelevels, get_instancelevel
from module.guild.api import make_logInfo, get_loginfo_by_guildId, create_loginfo
from module.guild.api import get_sysguildsiege
from module.playersoul.api import acquire_soul
from module.playeritem.api import acquire_item
from submodule.fanyoy import short_data
import math
import time
import copy

@handle_common
@require_player
def guildIndex(request, response):
    player = request.player
    if player.guildId:
        player.guild.guildInfo.fires_checkstatus()
    response.common_response.player.set("guild", player.guild.to_dict(True))
    return response

@handle_common
@require_player
def createGuild(request, response):
    """
    创建社团
    """
    player = request.player
    # 如果玩家在社团内部那么他不可以再创建社团
    if player.guildId:
        AlertHandler(player, response, AlertID.ALERT_IS_IN_GUILD,u"already in guild")
        return response
    # 钻石不足不可以创建社团
    if player.yuanbo < Static.CREATE_GUILD:
        AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"createGuild:need diamond(%s) player has %s" %(Static.CREATE_GUILD, player.yuanbo))
        return response
    # 等级不足不可以创建社团
    if player.level < Static.CREATE_GUILD_LEVEL:
        AlertHandler(player, response, AlertID.ALERT_LEVEL_SHORTAGE, u"createGuild:need level(%s) player level is  %s" %(Static.CREATE_GUILD_LEVEL, player.level))
    if player.guild.canJoinGuildAt > time.time():
        return response

    # 社团名字
    guildName = getattr(request.logic_request, "name", "")
    # 图标
    iconId = getattr(request.logic_request, "icon", 0)
    # 限制的等级
    limitLevel = getattr(request.logic_request, "limitLevel", 0)
    #　加入的类型，随意加，需审核，不允许
    category = getattr(request.logic_request, "category", 0)

    # 判断是否名字重复
    if get_guild_by_name(guildName):
        AlertHandler(player, response, AlertID.ALERT_GUILD_ALREADY_EXITS, u"name already exits")
        return response

    # 创建社团
    player.guild.create_guild(guildName, iconId, limitLevel, category)
    player.sub_yuanbo(Static.CREATE_GUILD, info=u"创建公会")
    # 创建一级公会的副本
    allGuildInstanceLevels = get_all_guildinstancelevels()
    for guildInstanceLevel in allGuildInstanceLevels:
        if guildInstanceLevel.guildLevelLimit == 1:
            sysGuildInstance = create_sysguildinstance(player, guildInstanceLevel.pk)
    #player.joinGuild(guild.id, Static.GUILD_CHAIRMAN_POSITION)
    # 返回公会的信息
   # info = make_guildInfo(guild)
    # 更新信息，告诉前端
    response.common_response.player.set("guild", player.guild.to_dict(True))
    return response



@handle_common
@require_player
def searchGuild(request, response):
    """
    搜索社团
    """
    player = request.player
    guildParam = getattr(request.logic_request, "guildParam", None)
    category = getattr(request.logic_request, "category", 0)

    res = []
    guilds = []

    # # 类型1按照名字模糊查询,按照id精确查询
    # if category == 1:
    #     if len(guildParam) > 6:
    #         id = long(guildParam)
    #         try:
    #             guilds = [get_guild_by_id(id)]
    #         except:
    #             guilds =[]
    #     else:
    #         guildName = unicode(guildParam)
    #         guilds = get_guildinfos(guildName)
    # # 所有所有的社团
    # elif category == 2:

    # # 也是搜索所有，但是返回一个有顺序的列表，但是前端说分开写，不知道做什么用
    # elif category == 5:
    #     guilds = get_all_guilds()
    #     guilds = sorted(guilds, key=lambda x: x.guildPowerRank, reverse=True)

    guildInfos = []
    if category == 1:
         if len(guildParam) == 10:
            try:
                guildId = short_data.decompress(guildParam.upper())
                guildInfo = get_guild_by_id(guildId, False)
                if guildInfo:
                    guildInfos.append(guildInfo)
            except:
                pass

    elif category == 2:
        guildInfos = get_all_guilds()
    elif category == 3:
        guildInfos = get_all_guilds()
        guildInfos = sorted(guildInfos, key=lambda x: x.powerRank, reverse=True)
    #add by ljdong, 公会名称模糊查询
    elif category == 5:
        guildName = unicode(guildParam)
        guildInfos = get_guildinfos(guildName)
        if len(guildInfos) > 5 :
            guildInfos = sorted(guildInfos, key=lambda x: x.guildName, reverse=True)
            guildInfos = guildInfos[0:5]
    for i in guildInfos:
        res.append(i.to_SimpleDict())

    response.logic_response.set("category", category)
    response.logic_response.set("result", res)
    return response


@handle_common
@require_player
def modifyGuildAttention(request, response):
    """
    修改公告
    """
    player = request.player
    context = getattr(request.logic_request, "context", "")
    category = getattr(request.logic_request, "category", 0) # 1修改内部公告,2修改外部公告

    # 前端这里应该加入验证。只有管理员才可以更改
    if not player.guildId or player.guild.position > Static.GUILD_VI_CHAIRMAN_POSITION:
        # todo　权限不够
        return response

    guildInfo = player.guild.guildInfo
    # 如果是修改内部公告，那么会刷新已经阅读的列表
    if category == 2:
        guildInfo.attention = context
        guildInfo.attentionV += 1
        guildInfo.hasReadMembers = []
    elif category == 1:
        guildInfo.outerAttention = context
    guildInfo.save()
    response.common_response.player.set("guild", player.guild.to_dict())
    return response

@handle_common
@require_player
def confirmGuildAttention(request, response):
    """
    确认信息
    """

    # 将阅读过公告的玩家加入到公会阅读列表中，下次再进入就不会弹出提示小窗了
    player = request.player

    guildInfo = player.guild.guildInfo

    player.guild.readAttV = guildInfo.attentionV
    player.guild.update()

    response.common_response.player.set("guild", player.guild.to_dict())

    return response

@handle_common
@require_player
def joinGuild(request, response):
    """
    加入社团
    """
    player = request.player
    # 加入社团需要一定的等级。针对所有人，不包括公会自己设定的等级
    if player.level < Static.JOIN_GUILD_LEVEL:
        AlertHandler(player, response, AlertID.ALERT_LEVEL_SHORTAGE, u"joinGuild:need level(%s) player level is  %s" %(Static.JOIN_GUILD_LEVEL, player.level))
        return response

    #已经加入公会
    if player.guildId > 0:
        return response

    #离开公会24小时禁止再次加入
    if player.guild.canJoinGuildAt > time.time():
        return response

    guildId = getattr(request.logic_request, "id", 0)
    if not guildId:
        return response

    guildInfo = get_guild_by_id(guildId)

    if player.level < guildInfo.limitLevel:
        guildInfo.self_release_lock()
        AlertHandler(player, response, AlertID.ALERT_LEVEL_SHORTAGE, u"joinGuild:this guild limit level need level(%s) player level is  %s" %(guildInfo.limitLevel, player.level))
        return response

    guildLevel = get_guild(guildInfo.level)
    # 每个公会在一定级别会有人员上限的限制
    if guildLevel.memberCount < guildInfo.membersCount + 1:
        guildInfo.self_release_lock()
        AlertHandler(player, response, AlertID.ALERT_GUILD_MEMBERS_HAS_FULL, u"joinGuild:this guild has full")
        return response

    #  如果是随意加入的公会
    if guildInfo.category == 1:
        player.guild.join_guild(guildInfo)

        # 为公会创建一条日志
        create_loginfo(str(guildId), 1, player.name)
        response.common_response.player.set("guild", player.guild.to_dict(True))

    # 如果是需要审核的。先加入到审核列表
    elif guildInfo.category == 2:
        if player.id not in guildInfo.requestMemberIds:
            player.guild.request_guild(guildInfo)
            response.logic_response.set("info", guildInfo.to_SimpleDict())
        else:
            guildInfo.self_release_lock()
            AlertHandler(player, response, AlertID.ALERT_GUILD_HAD_APPLIED_ALREADY, u"joinGuild has already applied")
            response.logic_response.set("info", guildInfo.to_SimpleDict())
            return response
    # 不允许加入
    elif guild.category == 3:
        guildInfo.self_release_lock()
        AlertHandler(player, response, AlertID.ALERT_GUILD_NOT_ALLOWED_JOIN, u"joinGuild not allowed join in ")
        return response

    return response


@handle_common
@require_player
def displayAppMember(request, response):
    """
    展示申请加入的人员信息
    """
    player = request.player
    guildInfo = player.guild.guildInfo

    membersInfo = []

    # 如果在等待审核期间，发出申请的人已经加入别的社团那么就不展示他的信息。直接删掉
    for _playerId in guildInfo.requestMemberIds:
        _player = get_player(_playerId, False)
        if _player.guildId:
            player.guild.disallow_join_guild(_playerId)#已经加入其它公会
            #guildInfo.requestMemberIds.remove(_playerId)
        else:
            membersInfo.append(_player.guild.userGuild_dict(guildInfo))

    guildInfo.save()

    response.logic_response.set("members", membersInfo)
    return response

@handle_common
@require_player
def allowedMemberJoinGuild(request, response):
    """
    加入或者拒绝社团
    """
    player = request.player

    category = getattr(request.logic_request, "category", 0) # 1允许　２　拒绝
    targetPlayerId = getattr(request.logic_request, "targetPlayerId", 0)

    if player.guild.position not in [Static.GUILD_CHAIRMAN_POSITION, Static.GUILD_VI_CHAIRMAN_POSITION]:
        # 不是会长不可以审核
        return response

    guildInfo = player.guild.guildInfo

    if targetPlayerId and targetPlayerId not in guildInfo.requestMemberIds:  #检查是否在请求列表中
        guildInfo.self_release_lock()
        return response


    # 如果是拒绝的话，分为单个拒绝和拒绝所有
    if category == 2:
        if targetPlayerId:
            targetPlayer = get_player(targetPlayerId, False)
            # 从列表里面删除
            player.guild.disallow_join_guild(targetPlayerId)
            contents = []
            contents.append({
                "content": "fytext_300760",
                "paramList": [guildInfo.name],
            })

            # 发送邮件通知对方，没有加入成功
            send_system_mail(targetPlayer, None, "fytext_300762", contents=contents)
        else:
            # 所有
            for targetPlayerId in guildInfo.requestMemberIds:
                targetPlayer = get_player(targetPlayerId, False)
                # 再进行一次验证
                if not targetPlayer.guildId:
                    contents = []
                    contents.append({
                        "content": "fytext_300760",
                        "paramList": [guildInfo.name],
                    })

                    send_system_mail(targetPlayer, None, "fytext_300762", contents=contents)

                player.guild.disallow_join_guild(targetPlayerId)

    # 如果同意操作基本类似
    elif category == 1:
        targetPlayers = []
        if targetPlayerId:
            targetPlayer = get_player(targetPlayerId)
            targetPlayers.append(targetPlayer)
        else:
            for id in guildInfo.requestMemberIds:
                targetPlayer = get_player(id)
                targetPlayers.append(targetPlayer)

        for targetPlayer in targetPlayers:
            contents = []
            contents.append({
                "content": "fytext_300759",
                "paramList": [guildInfo.name],
            })

            send_system_mail(targetPlayer, None, "fytext_300761", contents=contents)
            player.guild.allow_join_guild(targetPlayer)

    guildInfo.save()
    response.common_response.player.set("guild", player.guild.to_dict())

    return response




@handle_common
@require_player
def quitGuild(request, response):
    """
    退出社团
    """
    player = request.player
    guildId = player.guildId

    if player.guildId <= 0:
        # 会长不能退出公会
        return response

    if not player.guild.isChairman:
        player.guild.quit_guild()
        create_loginfo(str(guildId), 2, player.name)
        response.common_response.player.set("guild", player.guild.to_dict())
    else:
        #解散公会
        if len(player.guild.guildInfo.membersIds) == 1:
            player.guild.guildInfo.self_release_lock()
            player.guild.dissolve_guild()
            response.common_response.player.set("guild", player.guild.to_dict(True))
        else:
            player.guild.guildInfo.self_release_lock()
            return response

    response.logic_response.set("result", True)
    return response


@handle_common
@require_player
def guildKickMembers(request, response):
    """
    社团踢人
    """
    player = request.player

    targetPlayerId = getattr(request.logic_request, "targetPlayerId", 0)
    targetPlayer = get_player(targetPlayerId)

    # 不能踢出所选的人因为权限不够
    if player.guild.position >= targetPlayer.guild.position:
        targetPlayer.self_release_lock()
        AlertHandler(player, response, AlertID.ALERT_GUILD_LIMIT_CAN_NOT_KICK_MEMBERS, u"guildKickMembers your position is %s targert position is %s "%(player.guild.position, targetPlayer.guild.position))
        return response

    if player.guildId != targetPlayer.guildId:
        targetPlayer.self_release_lock()
        return response

    player.guild.kick_from_guild(targetPlayer)

    # # 把训练所里的英雄信息更新
    # if targetPlayer.trainingHeroIds:
    #     for hero_id in targetPlayer.trainingHeroIds:
    #         hero = targetPlayer.heroes.get(hero_id)
    #         hero.quiteHeroFromGuild()
    #         targetPlayer.heroes.update(hero, True)

    # #　把自己有关公会的信息更新
    # targetPlayer.quiteGuild()

    # 创建一条日志
    create_loginfo(player.guildId, 2, targetPlayer.name)

    # info = make_guildInfo(new_guild)

    # response.logic_response.set("info", info)


    # response.common_response.player.set("trainingHeroIds", player.trainingHeroIds)
    response.common_response.player.set("guild", player.guild.to_dict())

    return response


@handle_common
@require_player
def guildPositionUp(request, response):
    """
    职位变更
    """
    player = request.player

    category = getattr(request.logic_request, "category", 0)
    targetPlayerId = getattr(request.logic_request, "id", 0)

    targetPlayer = get_player(targetPlayerId)

    if not player.guild.isChairman:
        targetPlayer.self_release_lock()
        AlertHandler(player, response, AlertID.ALERT_GUILD_LIMIT_NOT_ENOUGH_TO_POSITION_UP, u"guildPositionUp your position is %s targert position is %s "%(player.guild.posiotn, targetPlayer.guild.position))
        return response

    guildInfo = player.guild.guildInfo

    # 升职。管理员给普通会员升职为副会长
    if category == 1:
        guildLevel = get_guild(guildInfo.level)
        #传职
        if targetPlayer.pk in guildInfo.viChairmanIds:
            player.guild.exchange_position(targetPlayer)
            create_loginfo(player.guildId, 3, player.name)
            create_loginfo(player.guildId, 5, targetPlayer.name)
        #会员变为副会长
        else:
            if guildInfo.viChairmanCount >= guildLevel.viceChairmanCount:
                targetPlayer.self_release_lock()
                guildInfo.self_release_lock()
                AlertHandler(player, response, AlertID.ALERT_GUILD_VICHAIRMAN_COUNT_HAS_TOP, u"guildPositionUp guild is level %s can has %s vichairmans now is %s "%(guildInfo.level, guildLevel.viceChairmanCount, guildInfo.viChairmanCount))
                return response
            player.guild.change_position(targetPlayer, Static.GUILD_VI_CHAIRMAN_POSITION)
            create_loginfo(player.guildId, 3, targetPlayer.name)

    #　降职
    elif category == 2:
        if not targetPlayer.guild.isViChairman:
            targetPlayer.self_release_lock()
            guildInfo.self_release_lock()
            return response

        player.guild.change_position(targetPlayer, Static.GUILD_NORMAL_POSITION)
        create_loginfo(player.guildId, 4, targetPlayer.name)

    else:
        targetPlayer.self_release_lock()
        guildInfo.self_release_lock()

    response.common_response.player.set("guild", player.guild.to_dict())

    return response


@handle_common
@require_player
def guildReName(request, response):
    """
    社团名变更
    """
    player = request.player

    param = getattr(request.logic_request, "name", "")
    level = getattr(request.logic_request, "level", 0)
    category = getattr(request.logic_request, "category", -1) # 1修改名字2修改头像3修改加入权限和等级

    ##if not player.guild.isChairman:
    if player.guild.isMember:
        return response

    guildInfo = player.guild.guildInfo

    if category == 1:
        if player.yuanbo < Static.RENAME_GUILD:
            guildInfo.self_release_lock()
            AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"guildReName:need diamond(%s) player has %s" %(Static.RENAME_GUILD, player.yuanbo))
            return response

        if get_guild_by_name(param):
            guildInfo.self_release_lock()
            AlertHandler(player, response, AlertID.ALERT_GUILD_ALREADY_EXITS,u"name already exits")
            return response

        guildInfo.change_name(param)
        guildInfo.save()
        player.sub_yuanbo(Static.RENAME_GUILD, info=u"公会改名")

    elif category == 2:
        guildInfo.change_icon(param)
        guildInfo.save()
    elif category == 3:
        if param:
            guildInfo.change_category(int(param))
        if level:
            guildInfo.change_limitLevel(int(level))
        guildInfo.save()

    else:
        guildInfo.self_release_lock()

    response.common_response.player.set("guild", player.guild.to_dict())
    return response

@handle_common
@require_player
def guildContribute(request, response):
    """
    社团捐献
    """
    player = request.player

    category = getattr(request.logic_request, "category", 0)

    #有效贡献次数
    if player.guild.dailyLeftContributionCount <= 0:
        # AlertHandler(player, response, AlertID.ALERT_GUILD_CONTRIBUTE_HAS_FULL, u"guildContribute you have contibuted no time")
        # return response
        if category == 2:
            #today = datetime.datetime.now().date()
            # if player.guild.updated_at.date() != today:
            #     player.guild.dailyCostContributionCount = 0
            #player.guild.dailyCostContributionCount += 1
            yuanbo_cost = Static.GUILD_CONTRIBUTE_DIAMOND_COUNT + player.guild.dailyCostContributionCount
            if player.yuanbo < yuanbo_cost:
                AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"guildContribute need diamond %s you have %s" %(Static.GUILD_CONTRIBUTE_DIAMOND_COUNT, player.yuanbo))
                return response                
            player.guild.contribute(False, category, 0, Static.GUILD_DIAMOND_GET, u"社团捐献")
            player.sub_yuanbo(yuanbo_cost, info=u"社团捐献")           
    else:
        # 金币捐献
        if category == 1:
            if player.gold < Static.GUILD_CONTRIBUTE_GOLD_COUNT:
                AlertHandler(player, response, AlertID.ALERT_GOLD_NOT_ENOUGH, u"guildContribute need gold %s you have %s" %(Static.GUILD_CONTRIBUTE_GOLD_COUNT, player.gold))
                return response

            player.guild.contribute(True, category, Static.GUILD_CONTRIBUTE_GOLD_XP, Static.GUILD_GOLD_GET, u"社团捐献")

            player.sub_gold(Static.GUILD_CONTRIBUTE_GOLD_COUNT, info=u"社团捐献")

        #钻石捐献
        elif category == 2:
            if player.yuanbo < Static.GUILD_CONTRIBUTE_DIAMOND_COUNT:
                AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"guildContribute need diamond %s you have %s" %(Static.GUILD_CONTRIBUTE_DIAMOND_COUNT, player.yuanbo))
                return response

            player.guild.contribute(True, category, Static.GUILD_CONTRIBUTE_DIAMOND_XP, Static.GUILD_DIAMOND_GET, u"社团捐献")
            player.sub_yuanbo(Static.GUILD_CONTRIBUTE_DIAMOND_COUNT, info=u"社团捐献")


        if player.guild.dailyLeftContributionCount == 0:
            player.guild.dailyCostContributionCount = 1

    player.dailytask_going(Static.DAILYTASK_CATEGORY_GUILD_CONTRIBUTE, number=1, is_incr=True, is_series=True)

    response.common_response.player.set("guild", player.guild.to_dict())
    return response

@handle_common
@require_player
def guildLevelUp(request, response):
    """
    社团升级
    """
    player = request.player

    category = getattr(request.logic_request, "category", 0)

    # 金币捐献
    if not player.guild.isChairman and not player.guild.isViChairman:
        return response

    nextGuildLevel = get_guild(player.guild.guildInfo.level + 1)

    if not nextGuildLevel:
        return response

    guildLevel = get_guild(player.guild.guildInfo.level)
    if player.yuanbo < guildLevel.levelUpCost:
            AlertHandler(player, response, AlertID.ALERT_DIAMOND_NOT_ENOUGH, u"guildLevelUp need diamond %s you have %s" %(guildLevel.levelUpCost, player.yuanbo))
            return response

    #经验值不足
    if player.guild.guildInfo.xp < guildLevel.level:
        return response

    player.sub_yuanbo(guildLevel.levelUpCost, info=u"社团升级")
    player.guild.level_up(guildLevel)

    #公会升级后 添加相应的公会副本
    allGuildInstanceLevels = get_all_guildinstancelevels() # 获取所有公会副本
    sysGuildInstances = get_sysguild_instances(player.guildId) # 获取当前公会所有存在副本
    instanceIds = [i.instanceId for i in sysGuildInstances]
    for guildInstanceLevel in allGuildInstanceLevels:
        if player.guild.guildInfo.level >= guildInstanceLevel.guildLevelLimit and guildInstanceLevel.pk not in instanceIds:
            sysGuildInstance = create_sysguildinstance(player, guildInstanceLevel.pk)
    #if player.guild.guildInfo.instanceIsOpen and not player.guild.guildInfo.createdInstance:
    #    allGuildInstanceLevels = get_all_guildinstancelevels()

    #    guildInfo = player.guild.guildInfo

    #    chairmanLastInstanceId  = player.lastInstance["lastLevelId"]
    #    lastInstanceLevel = get_instancelevel(chairmanLastInstanceId)
    #    for guildInstanceLevel in allGuildInstanceLevels:
            #如果是章节最后一关并且通关 or 当前章节没有通关
    #        if (lastInstanceLevel.levelIndex == 10 and player.lastInstance["lastFinished"] and int(str(chairmanLastInstanceId)[2:4]) >= guildInstanceLevel.id[2:4]) or int(str(chairmanLastInstanceId)[2:4]) > guildInstanceLevel.id[2:4]:
                #guildInfo.instanceIds.append(guildInstanceLevel.id)
    #            guildInfo.createdInstance = 1
    #            create_guildinstance(player, guildInstanceLevel.id)
    #            guildInfo.save()

    response.common_response.player.set("guild", player.guild.to_dict())
    return response

@handle_common
@require_player
def guildShopInit(request, response):
    """
    公会商店刷新
    """
    player = request.player

    category = getattr(request.logic_request, "category", -1)

    # 平时不刷新
    if category == 2:
        info = u"公会商店刷新"
        player.guildshop.refresh()

        if player.guild.gold <= 0:
            AlertHandler(player, response, AlertID.ALERT_GUILD_GOLD_NOT_ENOUGH,u"guildShopInit / refresh need guild_gold %s now player has %s " %(1, player.guild.gold))
            return response
        player.guild.sub_gold(500, info=info)
        response.common_response.player.set("guild", player.guild.to_dict())
    response.common_response.player.set("guildShop", player.guildshop.to_dict())
    return response



@handle_common
@require_player
def guildShopBuy(request, response):
    """
    公会商店购买
    """
    player = request.player

    shopId = getattr(request.logic_request, "shopId", 0)

    info = u"公会商店购买"

    # 获取商店的信息。
    guildShop = get_guildshop(shopId)

    if not player.guildshop.can_buy(shopId):
        return response

    if player.guild.gold < guildShop.cost:
        AlertHandler(player, response, AlertID.ALERT_GUILD_GOLD_NOT_ENOUGH,u"guildShopBuy  need guild_gold %s now player has %s" %(guildShop.cost, player.guild.gold))
        return response

    player.guildshop.buy(shopId)

    if guildShop.is_item:
        acquire_item(player, guildShop.itemId, number=guildShop.count, info=info)
    elif guildShop.is_equipfragment:
        acquire_equipfragment(player, guildShop.itemId, guildShop.count, info=info)
    elif guildShop.is_artifactfragment:
        acquire_artifactfragment(player, guildShop.itemId, number=guildShop.count, info=info)
    elif guildShop.is_soul:
        acquire_soul(player, guildShop.itemId, guildShop.count, info=info)
    else:
        raise ErrorException(player, u"mysteryShopBuy:arenashop(%s) is error" % (guildShop.itemId))


    player.guild.sub_gold(guildShop.cost, info=info)

    rewards = []

    rewards.append({"type": guildShop.itemId,"count": guildShop.count})
    response.common_response.player.set("guild", player.guild.to_dict())
    response.common_response.player.set("guildShop", player.guildshop.to_dict())
    response.logic_response.set("rewards", rewards)

    return response


@handle_common
@require_player
def addHeroToTraining(request, response):
    """
    添加英雄到训练所
    """
    playerhero_id = getattr(request.logic_request, "playerHeroId", 0)
    trainingPosition = getattr(request.logic_request, "trainingPosition", 0)

    player = request.player
    playerhero = player.heroes.get(playerhero_id)

    trainingPosition += 1

    if not playerhero:
        return response

    openPosCount = 0

    if player.vip_level >= 3:
        openPosCount += 1

    if player.vip_level >= 8:
        openPosCount += 1

    if player.level >= 21:
        openPosCount += 1

    if player.level >= 30:
        openPosCount += 1

    if player.level >= 40:
        openPosCount += 1

    if player.level >= 50:
        openPosCount += 1

    if player.level >= 55:
        openPosCount += 1

    if player.level >= 60:
        openPosCount += 1

    if trainingPosition > openPosCount:
        return response

    if player.guild.trainingHeroIds[trainingPosition - 1]:
        response.common_response.player.set("guild", player.guild.to_dict(True))
        return response

    # 如果这个英雄正在训练所进行训练，那么不能再次添加它
    if playerhero.pk in player.guild.trainingHeroIds:
        response.common_response.player.set("guild", player.guild.to_dict(True))
        return response

    player.guild.training_hero(playerhero, trainingPosition)
    response.common_response.player.set("guild", player.guild.to_dict())

    return response


@handle_common
@require_player
def deleteHeroFromTraining(request, response):
    """
    删除英雄训练所
    """
    playerhero_id = getattr(request.logic_request, "playerHeroId", 0)
    player = request.player
    playerhero = player.heroes.get(playerhero_id)

    if not playerhero:
        return response

     # 如果这个英雄正在训练所进行训练，那么不能再次添加它

    if playerhero_id not in player.guild.trainingHeroIds:
        return response

    player.guild.untraining_hero(playerhero)
    response.common_response.player.set("guild", player.guild.to_dict())

    return response


@handle_common
@require_player
def speedUpHero(request, response):
    """
    为社团成员加速
    """
    player = request.player
    targetPlayerId = getattr(request.logic_request, "targetPlayerId", 0)
    category = getattr(request.logic_request, "category", 0)



    # 每人每天的加速和被加速的次数是有限制的
    # if player.speedCount <= 0:
    #     AlertHandler(player, response, AlertID.ALERT_PLAYER_HAS_NO_SPEEDING_COUNT,  u"speedUpHero　PLAYER has no speeding count %s" %player.id)
    #     return response

    #每日最多加速5次
    if player.guild.isMaxSpeed:
        response.common_response.player.set("guild", player.guild.to_dict())
        return response

    targetPlayer = None
    if targetPlayerId:
        if targetPlayerId == player.id:
            return response
        targetPlayer = get_player(targetPlayerId)
        if not targetPlayer:
            return response
        #不在公会
        if targetPlayerId not in player.guild.guildInfo.membersIds:
            player.guild.guildInfo.self_release_lock()
            targetPlayer.self_release_lock()
            response.common_response.player.set("guild", player.guild.to_dict(True))
            return response

        #modify by ljdong 同一个用户可以被多次加速
        #if targetPlayerId in player.guild.speedPlayerIds:
            #response.common_response.player.set("guild", player.guild.to_dict(True))
            #return response

        #每日最多被加速5次
        if targetPlayer.guild.isMaxSpeeded:
            player.guild.guildInfo.self_release_lock()
            targetPlayer.self_release_lock()
            response.common_response.player.set("guild", player.guild.to_dict(True))
            return response
    else:
        memberIds = copy.copy(player.guild.guildInfo.membersIds)
        random.shuffle(memberIds)
        for memberId in memberIds:
            #modify by ljdong
            #if memberId in player.guild.speedPlayerIds:
                #continue
            if memberId == player.id:
                continue
            targetPlayer = get_player(memberId)
            #每日最多被加速5次
            if targetPlayer.guild.isMaxSpeeded:
                targetPlayer.self_release_lock()
                continue

            targetPlayerId = memberId
            break

        if not targetPlayerId:
            return response

    guildLevel = get_guild(player.guild.guildInfo.level)

    player.guild.speed(targetPlayer)

    contents = []
    contents.append({
        "content": "fytext_301171",
        "paramList": [player.guild.guildInfo.name, targetPlayer.name],
    })

    send_system_mail(player, None, "fytext_301173", contents=contents, rewards=guildLevel.speedRewards)
    contents = []
    contents.append({
        "content": "fytext_301172",
        "paramList": [player.guild.guildInfo.name, player.name],
    })
    send_system_mail(targetPlayer, None, "fytext_301173", contents=contents, rewards=guildLevel.speedRewards)
    response.common_response.player.set("guild", player.guild.to_dict())

    return response


@handle_common
@require_player
def displayGuildAucInfo(request, response):
    """
    展示拍卖信息
    """

    # 展示的信息包括，这件物品还剩余多长时间。物品当前的状态可以竞拍/已经被别人拍走。
    player = request.player

    #guild = get_guild_by_id(player.guildId)

    aucInfos = []

    #TODO没有instanceId 从mongo里面读取
    maxinfos = get_guildauctionmaxinfos(player.guildId)
    for maxinfo in maxinfos:
        aucInfos.append(maxinfo.to_dict())

    response.logic_response.set("aucInfos", aucInfos)
    response.common_response.player.set("guild", player.guild.to_dict())

    return response


@handle_common
@require_player
def startGuildAuc(request, response):
    """
    开始拍卖
    """
    # 这个接口的功能，一个玩家出价，拍卖商品，把价格信息更新到max  和 all里面。
    # max里面每次比较新的值和老的值如果新的值比较大，更新
    # all每次都会把数据插入到这个表里面
    from guild.tasks import task_balance_guildauctionmaxinfo


    price = abs(int(getattr(request.logic_request, "price", 0)))
    aucRewardId = int(getattr(request.logic_request, "aucRewardId", 0))

    player = request.player

    aucInfo = get_guildmaxinfo(aucRewardId)

    #itemallinfo = getitemallinfo(player.guildId, itemId, instanceId)

    # 这件商品拍卖时间到了，被删除掉。
    if not aucInfo or not aucInfo.isAuctioning:
        AlertHandler(player, response, AlertID.ALERT_AUCTION_HAS_CLOSED, u"")

    else:
        if price > aucInfo.auctionReward.maxPrice:
            price = aucInfo.auctionReward.maxPrice

        if aucInfo.isOffer(player.id):
            AlertHandler(player, response, AlertID.ALERT_AUCTION_HAS_AUCED,u"")
        elif price > player.guild.gold:
            AlertHandler(player, response, AlertID.ALERT_GUILD_GOLD_NOT_ENOUGH,u"startGuildAuc need guild_gold %s now player has %s " %(price , player.guild.gold))
        else:
            info = u"拍卖"
            player.guild.sub_gold(price, info)
            aucInfo.auction(player,price)
            if not aucInfo.isAuctioning:
                task_balance_guildauctionmaxinfo.delay(aucInfo.id)#异步发奖
    aucInfos = []

    #TODO没有instanceId 从mongo里面读取
    maxinfos = get_guildauctionmaxinfos(player.guildId)
    for maxinfo in maxinfos:
        aucInfos.append(maxinfo.to_dict())

    response.common_response.player.set("guild", player.guild.to_dict())
    response.logic_response.set("aucInfos", aucInfos)

    return response

@handle_common
@require_player
def guildFireCheckStatus(request, response):
    """
    公会火堆升级
    """
    player = request.player
    fireIndex = getattr(request.logic_request, "index", 0)

    #if player.guild.isMember:
    #    AlertHandler(player, response, AlertID.ALERT_GUILD_LIMIT_NOT_ENOUGH, u"guildFireLevelUp:only chairman can create fire")
    #    return response

    guildInfo = player.guild.guildInfo
    fire = guildInfo.get_fire_by_index(fireIndex)
    #火堆不存在
    if not fire:
        guildInfo.self_release_lock()
        return response

    #火堆未开启
    if fire["status"] == 0:
        guildInfo.self_release_lock()
        return response

    #fireLevelconf = get_guildfirelevel(fire["level"])

    #火堆经验不足
    #if fire["xp"] < fireLevelconf.xp:
        #AlertHandler(player, response, AlertID.ALERT_GUILD_LIMIT_NOT_ENOUGH, u"guildFireLevelUp:only chairman can create fire")
    #    return response

    player.guild.guildInfo.fire_check(fireIndex)
    guildInfo.self_release_lock() 
    response.common_response.player.set("guild", player.guild.to_dict())

    return response

@handle_common
@require_player
def guildFireStopBuff(request, response):
    """
    停止火堆燃烧
    """
    player = request.player

    fireIndex = getattr(request.logic_request, "index", 0)
    category = getattr(request.logic_request, "category", -1)

    if player.guild.isMember:
        AlertHandler(player, response, AlertID.ALERT_GUILD_LIMIT_NOT_ENOUGH, u"guildFireStopBuff:only chairman can create fire")
        return response   
     
    guildInfo = player.guild.guildInfo
    fire = getattr(guildInfo, "fire%s" % fireIndex)

    guildFire = guildInfo.get_fire_by_index(fireIndex)
    if not guildFire:
        guildInfo.self_release_lock()
        return response

    if not fire["buffLevel"]:
        AlertHandler(player, response, AlertID.ALERT_GUILD_FIRE_NOT_SET, u"guildFireStopBuff:guild fire buff not set")
        return response 
        
    if category == 0:
        guildInfo.stop_fire_buring(fireIndex)
    if category == 1:
        guildInfo.start_fire_buring(fireIndex)
        
    response.common_response.player.set("guild", player.guild.to_dict())  

    return response 

@handle_common
@require_player
def guildFireBuffSettings(request, response):
    """
    新建或者选择类别
    """
    player = request.player

    fireIndex = getattr(request.logic_request, "index", 0)
    buffType = getattr(request.logic_request, "buffType", 0)
    buffLevel = getattr(request.logic_request, "buffLevel", 0)
    hour = abs(int(getattr(request.logic_request, "hour", 0)))

    if player.guild.isMember:
        AlertHandler(player, response, AlertID.ALERT_GUILD_LIMIT_NOT_ENOUGH, u"guildFireBuffSettings:only chairman can create fire")
        return response

    if hour < 1:
        hour = 1

    if hour > 24:
        hour = 24

    # 取得静态的火堆数据
    firebuff = get_guildfirebuff(buffType)
    guildInfo = player.guild.guildInfo
    guildFire = guildInfo.get_fire_by_index(fireIndex)

    if not guildFire:
        guildInfo.self_release_lock()
        return response
    levelconf = firebuff.get_bufflevel(guildFire["level"], buffLevel)
    woodCost = hour * levelconf.woodCost
    if woodCost > player.guild.guildInfo.wood:
        guildInfo.self_release_lock()
        AlertHandler(player, response, AlertID.ALERT_WOOD_NOT_ENOUGH, u"guildFireBuffSettings:wood is not enough")
        return response

    guildInfo.set_fire_settings(fireIndex, buffType, buffLevel, hour, woodCost)
    response.common_response.player.set("guild", player.guild.to_dict())


    # woodCost = staticFire.woodCost

    # #　取得动态的火堆数据
    # fireInfo = get_fireinfo_by_guildId(player.guildId)

    # fireInfo = fireInfo[0]

    # if not fireInfo:
    #     # 如果没有就新建一个火堆
    #     create_fireinfo(player.guildId, buffType, buffLevel, guild.guildLevel, 0, woodCost)
    # else:
    #     # 修改类型，级别等信息，重新存储
    #     # 在选择的时候先把之前燃烧的木头结算掉，再赋值新类型，更新时间

    #     woodLeft = fireInfo.woodLeft - ((datetime.datetime.now() - fireInfo.startTime.replace(tzinfo=None)).total_seconds() / 60 * fire.woodCost)
    #     if woodLeft <= 0:
    #         woodLeft = 0
    #     fireInfo.woodLeft = woodLeft
    #     fireInfo.startTime = datetime.datetime.now()


    #     fireInfo.buffType = buffType
    #     fireInfo.buffLevel = buffLevel
    #     fireInfo.fireLevel = guild.guildLevel
    #     fireInfo.woodCost = woodCost

    # response.logic_response.set("fireInfo", [make_fireInfo(fireInfo)])

    return response

@handle_common
@require_player
def contributeGuildFire(request, response):
    """
    向火堆捐献木头
    """

    player = request.player

    wood = getattr(request.logic_request, "count", 0)

    #fire = get_fireinfo_by_guildId(player.guildId)
    info = u'捐献木头到公会火堆'

    # if not fire:
    #     # 当前你的公会没有火堆
    #     return response
    # else:
        # fire = fire[0]
        # 这个代表按照固定数量捐
        #if category == 1:
    if player.wood < wood:
        AlertHandler(player, response, AlertID.ALERT_WOOD_NOT_ENOUGH,  u"contributeGuildFire need (%s) now you have (%s)" %(wood, player.wood))
        return response

    player.guild.contribute_wood(wood)
    player.sub_wood(wood, info=info)
        # # 这个代表捐献自己当前全部的
        # elif category == 2:
        #     fire.woodLeft += player.wood
        #     player.sub_wood(player.wood, info=info)

    # fireInfo = []

    # fireInfo.append(make_fireInfo(fire))

    # response.logic_response.set("fireInfo", fireInfo)
    response.common_response.player.set("guild", player.guild.to_dict())

    return response

@handle_common
@require_player
def displayGuildLogInfo(request, response):
    """
    展示日志信息
    """

    player = request.player

    # 日志记录了公会相应的操作记录，在每次有操作变动的情况下，在日志的数据库里面就插入一条。

    loginfos = get_loginfo_by_guildId(player.guildId)

    infos = []

    for info in loginfos:

        infos.append(make_logInfo(info))

    response.logic_response.set("logInfo", infos)

    return response

@handle_common
@require_player
def displayGuildInstance(request, response):
    """
    展示副本信息
    TODO
    #两个地方需要更新公会副本  1：公会会长 副本通关   2：公会会长移交公会
    """
    #TODO
    player = request.player

    # guildChairman = get_player(player.guild.guildInfo.chairmanId, False)
    # chairmanLastInstanceId  = guildChairman.lastInstance["lastLevelId"]
    # lastInstanceLevel = get_instancelevel(chairmanLastInstanceId)

    # instanceInfos = []
    # guildInstanceLevels = get_all_guildinstancelevels() #获取所有公会副本
    sysGuildInstances = get_sysguild_instances(player.guildId) #获取当前公会所有存在副本
    # sysGuildInstanceDicts = dict([(i.instanceId, i) for i in sysGuildInstances])
    # for guildInstanceLevel in guildInstanceLevels:
    #     #如果是章节最后一关并且通关 or 当前章节没有通关
    #     if (lastInstanceLevel.levelIndex == 10 and guildChairman.lastInstance["lastFinished"] and int(str(chairmanLastInstanceId)[2:4]) >= int(str(guildInstanceLevel.id)[2:4])) or int(str(chairmanLastInstanceId)[2:4]) > int(str(guildInstanceLevel.id)[2:4]):
    #         if guildInstanceLevel.pk not in sysGuildInstanceDicts:
    #             sysGuildInstance = create_sysguildinstance(player, guildInstanceLevel.pk)
    #         else:
    #             sysGuildInstance = sysGuildInstanceDicts[guildInstanceLevel.pk] #

    #         instanceInfos.append(sysGuildInstance.to_dict())

    response.logic_response.set("instanceInfos", [sysGuildInstance.to_dict() for sysGuildInstance in sysGuildInstances])

    return response


@handle_common
@require_player
def getGuildSiegeBattleStatus(request, response):
    """
    获取公会团战的状态信息
    """
    player = request.player
    # 根据时间来判断当前公会战斗应该处于什么样的状态。
    # 0代表休战, 1代表报名　2 代表匹配 3代表配兵 4行军，5战斗 6预览
    response.common_response.player.set("guild", player.guild.to_dict())

    return response


@handle_common
@require_player
def guildSiegeBattleEnter(request, response):
    """
    获取公会团战的报名
    """
    player = request.player

    #身份检查 只有会长和副会长才能报名
    if not player.guild.isChairman or not player.guild.isViChairman:
        # TODO：更换 AlertID
        AlertHandler(player, response, AlertID.ALERT_GUILD_LIMIT_NOT_ENOUGH, u"guildSiegeBattleEnter:only chairman or vice-chairman can sign up")
        return response
    guildSiege = get_sysguildsiege()
    #检查公会战当前状态
    if not guildSiege.stage_sign_up:
        # TODO：更换 AlertID
        AlertHandler(player, response, AlertID.ALERT_GUILD_LIMIT_NOT_ENOUGH, u"guildSiegeBattleEnter:current stage can not be registered")
        return response       
    #报名
    guildSiege.join(player.guildId)

    return response


@handle_common
@require_player
def guildSiegeBattleConfigGet(request, response):
    """
    显示公会团战的配置
    """
    player = request.player

    configinfo = get_guildsiegeconfiginfo_by_playerid(player.pk)
    if not configinfo:
        configinfo = create_guildsiegeconfiginfo(player.pk)


    response.logic_response.set("configinfo", configinfo.to_dict())
    return response


@handle_common
@require_player
def guildSiegeBattleConfig(request, response):
    """
    公会团战的配置
    """
    player = request.player
    heroIds = getattr(request.logic_request, "heroIds", [])
    category = getattr(request.logic_request, "category", 0) # 上中下，1 2 3
    group = getattr(request.logic_request, "group", 0) # 一组 二组，1 2
    power = getattr(request.logic_request, "power", 0)

    if (int(category) not in range(1,4)) or (int(group) not in range(1,3)):
        raise ErrorException(player, u"guildSiegeBattleConfigGet: parameter is error, category(%s) or group(%s)" % (category, group))

    configinfo = get_guildsiegeconfiginfo_by_playerid(player.pk)
    if not configinfo:
        configinfo = create_guildsiegeconfiginfo(player.pk)

    if category == 1:
        configinfo.setLeftArmy(group, heroIds, power)
    elif category == 2:
        configinfo.setMiddleArmy(group, heroIds, power)
    elif category == 3:
        configinfo.setRightArmy(group, heroIds, power)

    response.logic_response.set("configinfo", configinfo.to_dict())
    return response


