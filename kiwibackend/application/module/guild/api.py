# -*- coding: utf-8 -*-
from guild.docs import GuildSiegeConfigInfo, GuildSiegeInfo, GuildLogInfo, SysGuildInfo, SysGuildInstanceInfo, GuildAuctionsMaxInfo, SysGuildSiege
from guild.models import Guild,GuildShop, GuildFireBuff, GuildFireBuffLevel, GuildFireLevel, GuildAuctionReward, GuildSiegeBattleReward
import datetime
from django.conf import settings
from rewards.models import CommonReward

def update_guild_cache():
    Guild.create_cache()
    GuildShop.create_cache()
    GuildFireBuff.create_cache()
    GuildFireBuffLevel.create_cache()
    GuildFireLevel.create_cache()

def get_guild(pk):
    return Guild.get(int(pk))

def get_guilds():
    return Guild.get_all_list()

def get_guildshop(pk):
    return GuildShop.get(int(pk))

def get_guildshops():
    return GuildShop.get_all_list()

def get_guildfirebuffs():
    return GuildFireBuff.get_all_list()

def get_guildfirebuff(pk):
    return GuildFireBuff.get(int(pk))

def get_guildfirelevels():
    return GuildFireLevel.get_all_list()

def get_guildfirelevel(pk):
    return GuildFireLevel.get(int(pk))

def get_guildauctionrewards():
    return GuildAuctionReward.get_all_list()

def get_guildauctionreward(pk):
    return GuildAuctionReward.get(int(pk))

# 创建公会的最高拍卖信息
def create_guildauctionmaxinfo(guildId, aucRewardId, instanceid):
    maxinfo = GuildAuctionsMaxInfo(
        player_id=-1,
        guildId = guildId,
        aucRewardId = aucRewardId,
        instanceId=instanceid,
        maxPrice=0,
        maxPlayerId = 0,
    )

    maxinfo.save()
    from .tasks import task_add_balance_guildauctionmaxinfo
    task_add_balance_guildauctionmaxinfo(maxinfo)

    

# # 记录公会所有出价的信息
# def create_guildauctionallinfo(guildId, aucRewardId, instanceid):

#     allinfo = GuildAuctionsAllInfo(
#         player_id=-1,
#         guildId=guildId,
#         aucRewardId=aucRewardId,
#         instanceId=instanceid,
#         playerIds=[],
#         prices=[],
#         auTime=[]
#     )
#     allinfo.save()



# 一个物品如果过时或者拍卖完成那么就把他删除掉
# def delete_guildauctionmaxinfo(guildId, itemId, instanceid):
#     maxinfo = GuildAuctionsMaxInfo.objects.get(guildId=guildId, itemId = itemId, instanceId=instanceid)
#     maxinfo.delete()


# # 如果一件物品拍卖完成 就把他删除掉
# def delete_guildauctionallinfo(guildId, itemId, instanceid):
#     allinfo = GuildAuctionsAllInfo.objects.get(guildId=guildId, itemId = itemId, instanceId=instanceid)
#     allinfo.delete()

def get_guildauctionmaxinfos(guildId):
    maxinfo = list(GuildAuctionsMaxInfo.objects.filter(guildId=guildId))
    return maxinfo


# def getguildauctionmaxinfo(guildId, instanceid):
#     maxinfo = GuildAuctionsMaxInfo.objects.filter(guildId=guildId, instanceId=instanceid)
#     return maxinfo

# def getguildauctionallinfo(guildId, instanceid):
#     allinfo = GuildAuctionsAllInfo.objects.filter(guildId=guildId, instanceId=instanceid)
#     return allinfo

def get_guildmaxinfo(pk, lock=True):
    if lock:
        while GuildAuctionsMaxInfo.acquire_lock(pk, 2):
            break
    try:
        info = GuildAuctionsMaxInfo.objects.get(pk=int(pk))
    except:
        info = None

    if lock and not info:
        GuildAuctionsMaxInfo.release_lock(pk)
    return info


# def getitemallinfo(guildId, itemId, instanceid):
#     allinfo = GuildAuctionsAllInfo.objects.get(guildId=guildId, itemId=itemId, instanceId=instanceid)
#     return allinfo



def create_sysguildinstance(player, instanceid):
    guildinstance = SysGuildInstanceInfo(
        player_id = 0,
        instanceId=instanceid,
        guildId=player.guildId,
        openStatus=0,
        bossHp=0,
        isFighting=0,
        startTime=datetime.datetime.max
    )
    guildinstance.save()
    return guildinstance


def get_sysguild_instances(guildId):
    """
    查找公会副本
    """
    sysGuildInstances = list(SysGuildInstanceInfo.objects.filter(guildId=guildId))
    for sysGuildInstance in sysGuildInstances:
        sysGuildInstance.check_status()

    return sysGuildInstances

def get_sysguildinstanceInfo(instanceId, guildId, lock=True):
    """
    查找公会副本
    """
    if lock:
        while SysGuildInstanceInfo.acquire_lock(SysGuildInstanceInfo.lock_key(instanceId, guildId), 2):
            break

    sysGuildInstance = None
    try:
        sysGuildInstance = SysGuildInstanceInfo.objects.get(guildId=guildId,instanceId=int(instanceId))
        sysGuildInstance.check_status()
    except:
        sysGuildInstance = None

    if lock and not sysGuildInstance:
        SysGuildInstanceInfo.release_lock(SysGuildInstanceInfo.lock_key(instanceId, guildId))

    return sysGuildInstance

def reset_sysguildinstance(guildInstancelevelInfo):
    """
    重置公会副本
    """

    guildInstancelevelInfo.openStatus = 1
    guildInstancelevelInfo.bossHp = 0
    guildInstancelevelInfo.isFighting = 0
    guildInstancelevelInfo.startTime = datetime.datetime.now()
    guildInstancelevelInfo.memberList = []
    guildInstancelevelInfo.startFightTime = datetime.datetime.max

    guildInstancelevelInfo.save()
    return guildInstancelevelInfo

# 通过名字进行模糊查询
def get_guildinfos(guildName=None):
    """
    查找公会
    """
    #modify by ljdong
    #all_guilds = list(SysGuildInfo.objects.filter(guildName__icontains=guildName, serverid__in = settings.ALL_SERVERS))
    all_guilds = list(SysGuildInfo.objects.filter(name__icontains=guildName, serverid__in=settings.ALL_SERVERS))
    guilds = []
    for guild in all_guilds:

        guilds.append(guild)
    return guilds


def get_all_guilds():
    all_guilds = list(SysGuildInfo.objects.all())
    return  all_guilds

def get_guild_by_id(pk, lock=True):
    """
    查找公会通过公会id
    """

    guild = SysGuildInfo.get_guild(pk, lock)

    return guild

# def get_guilds_by_playerid(playerid):
#     """
#     查找公会通过玩家ｉｄ
#     """
#     guilds = list(SysGuildInfo.objects.filter(membersIds__contains=playerid))

#     return guilds

# def get_guild_by_chairman_id(pk):
#     """
#     查找公会通过公会id
#     """
#     guild = SysGuildInfo.objects.get(player_id=int(pk))

#     return guild

def get_guild_by_name(name):
    try:
        guildInfo = SysGuildInfo.objects.get(name=name)
    except:
        guildInfo = None
    return guildInfo


# def add_guild_xp(guild, xp):
#     #if not datetime.datetime.now().day == guild.contributeTime.day:
#     #    guild.dailyXp = 0

#     guild.dailyXp += xp
#     guild.totalXp += xp

#     currentLevel = get_guild(guild.guildLevel)
#     if guild.totalXp >= currentLevel.xp:
#         guild.guildLevel += 1
#         guild.totalXp -= currentLevel.xp


#     #guild.contributeTime = datetime.datetime.now()
#     guild.save()
#     return guild

# def positionUp(guild, player_id):
#     guild.viChairmanIds.append(player_id)
#     guild.save()
#     return guild

# def changePosition(guild,targetPlayerid, player_id):

#     if targetPlayerid in guild.viChairmanIds:
#         guild.viChairmanIds.remove(targetPlayerid)
#         guild.viChairmanIds.append(player_id)
#     guild.chairmanId = targetPlayerid
#     guild.save()
#     return guild

# def create_fireinfo(guildId, buffType, buffLevel, fireLevel, woodLeft, woodCost):

#     fireinfo = GuildFireInfo(
#         player_id=-1,
#         guildId=guildId,
#         buffType=buffType,
#         buffLevel=buffLevel,
#         fireLevel=fireLevel,
#         woodLeft=woodLeft,
#         woodCost=woodCost,
#         startTime=datetime.datetime.now()
#     )
#     fireinfo.save()

# def get_fireinfo_by_guildId(guildId):
#     return GuildFireInfo.objects.filter(guildId=guildId)


# def make_fireInfo(fire):


#     woodLeft = fire.woodLeft - ((datetime.datetime.now() - fire.startTime.replace(tzinfo=None)).total_seconds() / 60 * fire.woodCost)
#     if woodLeft <= 0:
#         woodLeft = 0
#     fire.woodLeft = woodLeft

#     info = {}
#     info["buffType"] = fire.buffType
#     info["buffLevel"] = fire.buffLevel
#     info["fireLevel"] = fire.fireLevel
#     info["woodLeft"] = fire.woodLeft
#     info["woodCost"] = fire.woodCost
#     info["timeLeft"] = fire.timeLeft

#     fire.startTime = datetime.datetime.now()
#     fire.save()

#     return info


def create_loginfo(guildId, logType, contextParams):

    loginfo = GuildLogInfo(
        player_id=-1,
        guildId=guildId,
        logType=logType,
        contextParams=contextParams,
        logTime=datetime.datetime.now()
    )
    loginfo.save()


def get_loginfo_by_guildId(guildId):
    return GuildLogInfo.objects.filter(guildId=guildId)


def make_logInfo(log):

    info = {}
    info["guildId"] = log.guildId
    info["logType"] = log.logType
    info["contextParams"] = log.contextParams
    info["logTime"] = str(log.logTime)

    return info
# TODO：删除
# def get_guild_siegebattle():
#     now = datetime.datetime.now()
#     year, week, day = now.isocalendar()
#     try:
#         guildSiegeInfo = GuildSiegeInfo.objects.get(pk=week)
#     except:
#         guildSiegeInfo = None
#     return guildSiegeInfo
# TODO：删除
# def enterGuildSiegeBattle(week, guildId):
#     """
#         报名公会战
#     """
#     try:
#         guildSiegeInfo  = GuildSiegeInfo.objects.get(pk=week)
#         if guildId not in guildSiegeInfo.guildIds:
#             guildSiegeInfo.guildIds.append(guildId)
#             guildSiegeInfo.save()

#     except:
#         guildSiegeInfo = GuildSiegeInfo.objects.create(pk=week, guildIds=[guildId], player_id=-1)

#     return guildSiegeInfo

# def get_config_by_id_week(guildId, week):
#     try:
#         config = GuildSiegeConfigInfo.objects.get(guildId=str(guildId), week=week)
#     except:
#         config = None
#     return config


# def create_configInfo_by_id_week(player, week, heroIds, powerRanks, positions):
#     try:
#         config = GuildSiegeConfigInfo.objects.get(guildId=player.guildId, week=week)
#     except:
#         config = None

#     if config:
#             # 左路
#             if positions == 1:
#                 config.leftArmy["heroInfos"].append({"playerName": player.name, "heroIds": heroIds})
#                 config.leftArmy["powerRank"] += powerRanks
#             # 中路
#             elif positions == 2:
#                 config.middleArmy["heroInfos"].append({"playerName": player.name, "heroIds": heroIds})
#                 config.middleArmy["powerRank"] += powerRanks
#             else:
#                 config.rightArmy["heroInfos"].append({"playerName": player.name, "heroIds": heroIds})
#                 config.rightArmy["powerRank"] += powerRanks

#     else:
#         config = GuildSiegeConfigInfo(
#             player_id=-1,
#             guildId=player.guildId,
#             week=week,
#             leftArmy={"heroInfos": [{"playerName": player.name, "heroIds": heroIds}], "powerRank": powerRanks} if positions == 1 else {"heroInfos": [], "powerRank": 0},
#             middleArmy={"heroInfos": [{"playerName": player.name, "heroIds": heroIds}], "powerRank": powerRanks} if positions == 2 else {"heroInfos": [], "powerRank": 0},
#             rightArmy={"heroInfos": [{"playerName": player.name, "heroIds": heroIds}], "powerRank": powerRanks} if positions == 3 else {"heroInfos": [], "powerRank": 0},
#         )

#     config.save()
#     return config

def create_guildsiegeconfiginfo(playerId):
    '''
    创建公会配置信息
    '''
    config = GuildSiegeConfigInfo(player_id = playerId, serverId = settings.SERVERID)
    config.save()
    return config

def get_guildsiegeconfiginfo_by_playerid(playerId):
    try:
        config = GuildSiegeConfigInfo.objects.get(pk=playerId)
    except:
        return None
    return config

def get_guildsiege_power(guildId):
    '''
    获取公会战三条路的战斗力
    '''
    guild = SysGuildInfo.get_guild(guildId)
    siegeInfos = GuildSiegeConfigInfo.objects.filter(player_id__in = guild.membersIds)
    leftPower = 0
    middlePower = 0
    rightPower = 0
    for siegeInfo in siegeInfos:
        leftPower += siegeInfo.leftPower
        middlePower += siegeInfo.middlePower
        rightPower += siegeInfo.rightPower

    return [leftPower, middlePower, rightPower]

def get_guildsiege_allpower(guildId):
    '''
    获取公会战的总战斗力
    '''
    guild = SysGuildInfo.get_guild(guildId)
    siegeInfos = GuildSiegeConfigInfo.objects.filter(player_id__in = guild.membersIds)
    allPower = 0
    for siegeInfo in siegeInfos:
        allPower += siegeInfo.allPower

    return allPower

# TODO : 删除
# def calculate_winner_by_config(config_a, config_b):

#     winnerTimes = []
#     winnerPositions = []

#     if config_a.leftArmy["powerRank"] > config_b.leftArmy["powerRank"]:
#         winnerTimes.append(float(config_b.leftArmy["powerRank"]) / config_a.leftArmy["powerRank"])
#         winnerPositions.append((1, 1))
#     else:
#         winnerTimes.append(float(config_a.leftArmy["powerRank"]) / config_b.leftArmy["powerRank"])
#         winnerPositions.append((2, 1))

#     if config_a.middleArmy["powerRank"] > config_b.middleArmy["powerRank"]:
#         winnerTimes.append(float(config_b.middleArmy["powerRank"]) / config_a.middleArmy["powerRank"])
#         winnerPositions.append((1, 2))
#     else:
#         winnerTimes.append(float(config_a.middleArmy["powerRank"]) / config_b.middleArmy["powerRank"])
#         winnerPositions.append((2, 2))

#     if config_a.rightArmy["powerRank"] > config_b.rightArmy["powerRank"]:
#         winnerTimes.append(float(config_b.rightArmy["powerRank"]) / config_a.rightArmy["powerRank"])
#         winnerPositions.append((1, 3))
#     else:
#         winnerTimes.append(float(config_a.rightArmy["powerRank"]) / config_b.rightArmy["powerRank"])
#         winnerPositions.append((2, 3))

#     if winnerTimes:
#         index = winnerTimes.index(min(winnerTimes))

#     return winnerPositions[index]

def get_guildsiegebattlerewards():
    return GuildSiegeBattleReward.get_all_list()
    
def get_guildSiegeBattle_rewards(rank, level):
    """
        根据公会战排名和公会等级获取公会奖励
    """
    guildRewards = GuildSiegeBattleReward.get(pk = rank)
    if not guildRewards:
        return []
    return guildRewards.get_reward_by_level(level)

def guildsiege_join():
    """
    工会团战
    """
    guildsiege = SysGuildSiege.get()
    guildsiege.set_status_prematch()
    guildsiege.save()

    guildsiege.match_guilds()#开始匹配
    guildsiege.set_status_matched()
    guildsiege.save()

def get_sysguildsiege():
    return SysGuildSiege.get()

def decide_siegebattle_winner(guildIdA, guildIdB):
    """
    决定团战的胜利方
    return A 赢返回 True 否则 False
    """
    powerA_list = get_guildsiege_power(guildIdA)
    powerB_list = get_guildsiege_power(guildIdB)
    minPower = min(powerA_list + powerB_list)
    if minPower in powerA_list and minPower in powerB_list:
        # A B 同时存在最小战力的情况下 比较总战力, 总战力相等 默认A胜
        return get_guildsiege_allpower(guildIdA) >= get_guildsiege_allpower(guildIdB)
    else:
        # 有最小战力的公会失败
        return minPower not in powerA_list

def guild_siegebattle_reward(playerId, rewards):
    """
    公会团战个人奖励
    """
    from module.player.api import get_player
    player = get_player(playerId)
    config = get_guildsiegeconfiginfo_by_playerid(playerId)
    if not player or not config:
        return []

    #个人战斗力
    power = config.allPower
    #总战斗力
    powerRank = get_guildsiege_allpower(player.guildId)
    personal_reward = []
    for reward in rewards:
        count = round( power/float(powerRank),2) * reward.count
        _reward = CommonReward(reward.type, count, reward.level)
        personal_reward.append(_reward)

    return personal_reward
