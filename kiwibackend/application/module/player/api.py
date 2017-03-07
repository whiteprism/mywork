# -*- coding: utf-8 -*- 
from module.player.docs import Player
from django.conf import settings
from common.static import Static
import random
from utils import random_name, _check_name
from module.hero.api import get_heroskill
from playerinstance.api import unlock_player_instancelevel, _debug_open_player_instance_at_instance_id
from module.building.api import get_buildingradar, get_building
from playerbuilding.api import acquire_building
import datetime

def get_player(pk, lock=True):
    if lock:
        while True:
            if Player.acquire_lock(pk, 2):
                break

    try:
        pk = int(pk)
        player = Player.objects.get(pk = pk)
    except Player.DoesNotExist:
        player = None

    if lock and not player:
        Player.release_lock(pk)
    return player

def get_players_by_ids(pks):
    players = list(Player.objects.filter(pk__in = pks))
    return dict([(player.pk, player) for player in players])

def get_player_by_userid(userid, serverid, lock=True):
    player_id = serverid * 1000000000 + userid
    return get_player(player_id, lock)

def get_all_player():
    players = Player.objects.all()
    return players

def create_player(request, *args, **argvs):
    from playerhero.api import acquire_hero

    userid = request.common_request.playerId
    player_id = settings.SERVERID * 1000000000 + userid
    player = Player(pk = player_id, userid = userid, serverid = settings.SERVERID)
    #if settings.OPEN_TUTORIAL:
    #    player.name = u""
    #    player.gold = 5000
    #    player.wood = 5000
    #    player.level = 40
    #    player.yuanbo = settings.DIAMOND
    #    player.vip = settings.VIP_INFO
    #else:
    player.name = u"" 
    player.vip["chargeCount"] = 0
    player.vip["vipLevel"] = 0
    player.level = 1
    player.firstIn = 1
    player.yuanbo = 0
    player.gold = 2000
    player.wood = 200

    player.channel = request.common_request.channel
    player.init_tasks()
    player.init_seven_days_tasks()

    #主角
    all_h = []
    #if not settings.OPEN_TUTORIAL:
    h1 = acquire_hero(player, 111000100, level=1, star=1, upgrade = 0, skill1Level=1, skill2Level=1, skill3Level=1,skill4Level=1)
    h15 = acquire_hero(player, 115000300, level=1, star=1, upgrade = 0, skill1Level=1, skill2Level=1, skill3Level=1,skill4Level=1)
    h22 = acquire_hero(player, 114000700, level=1, star=1, upgrade = 0, skill1Level=1, skill2Level=1, skill3Level=1,skill4Level=1)

    all_h.append(h1)
    all_h.append(h15)
    all_h.append(h22)

    defenseList = []
    i = 0
    default_poses = Static.HERO_DEFENCE_POS
    for a_h in all_h[0:5]:
        defenseList.append(a_h.id)
        defenseList.append(default_poses[i])
        i += 1
    player.defenseHeroLayout = defenseList
    defenseHeroIds = player.defenseHeroLayout[0:len(player.defenseHeroLayout):2]
    # dd.append(1120004)
    player.update_hero_defenseHeroIds(defenseHeroIds)

    player.update_siege_defenseSoldierIds([-1 for i in range(0,5)])

    unlock_player_instancelevel(player, Static.FIRST_INSTANCE_BOSS_LEVEL_ID)
    unlock_player_instancelevel(player, Static.FIRST_INSTANCE_LEVEL_ID)
    #_debug_open_player_instance_at_instance_id(player, 1100)


    playerbuilding = acquire_building(player, 1001001, level = 1 , centerX = 8, centerY = 8, status = 0)
    playerbuilding = acquire_building(player, 1001002, centerX = 8, centerY = 13, status = 0)
    playerbuilding = acquire_building(player, 1001011, centerX = 13, centerY = 9, status = 0)

    tower1 = acquire_building(player, 1002001, centerX = 0, centerY = 0, status = 0)
    tower2 = acquire_building(player, 1002001, centerX = 1, centerY = 0, status = 0)

    # 兵营解锁小兵的操作
    building = get_building(1001011)
    player.update_hero_warriorIds(building, 1)
    player.armies.set_horde(True)
    player.update_castlelevel(1)
    player.SiegeBattle.update()
    player.save()

    return player

def _rightNodeId2Left(nodeid):
    row = nodeid / 60
    col = nodeid % 30
    newNodeid = 29 - col + 60 * row
    return newNodeid

def create_ai_player(robot):
    from playerhero.api import acquire_hero

    player = Player(pk = robot.pk, serverid=0)
    while True:
        name = random_name()
        if _check_name(name) == 1:
            player.name = name
            break

    player.level = robot.level

    player.gold = player.level * 500 + 5000
    player.wood = player.level * 200 + 2000
    player.iconId = random.choice(Static.HERO_HERO_ICON_ID)
    player.powerRank = robot.powerRank

    # 新手引导专用机器人,其他类似于建筑物以后再修改
    if player.id == -1:
        player.endLockedTime = datetime.datetime.max

    defenseList = []
    powerrank = 0

    #
    # 机器人默认建筑
    # 要塞
    playerbuilding = acquire_building(player, 1001001, level = robot.cityLevel ,centerX = 8, centerY = 8, status = 0)
    # 防御塔
    tower1 = acquire_building(player, 1002001, level = robot.towerLevel, centerX = 0, centerY = 0, status = 0)
    tower2 = acquire_building(player, 1002001, level = robot.towerLevel, centerX = 1, centerY = 0, status = 0)

    default_poses = Static.HERO_DEFENCE_POS
    i = 0
    for hero in robot.heroes:
        # todo 假数据-----------------------
        playerhero = acquire_hero(player, int("%s%s" % (hero, str(robot.heroUpgrades[i]).rjust(2,"0"))), star=robot.heroStars[i])

        playerhero.level = robot.heroLevels[i]
        playerhero.star = robot.heroStars[i]
        playerhero.upgrade = robot.heroUpgrades[i]
        skillhero = get_heroskill(hero)

        # todo 暂时假设 ，以后修改

        powerrank += playerhero.warrior.hero.powerRank + Static.HERO_STAR_POWERRANKS[int(playerhero.star/5)+1][int(playerhero.warrior.hero.quality-3)] * playerhero.level + Static.HERO_UPGRADE_POWERRANKS[int(playerhero.upgrade)]

        for j in range(0, len(skillhero.skillinfo)/3):
            skillGid,_,upgrade = skillhero.skillinfo[j*3:(j+1)*3]
            if upgrade <= playerhero.upgrade:
                setattr(playerhero, "skill%sLevel" %(j+1), robot.heroSkillLevels[i])
                if j == 0:
                    powerrank += (robot.heroSkillLevels[i]+1) * Static.HERO_BIGSPELL_POWERRANK_RATIO
                else:
                    powerrank += (robot.heroSkillLevels[i]+1) * Static.HERO_SMALLSPELL_POWERRANK_RATIO
                
            setattr(playerhero, "skill%sGid" %(j+1), skillGid)

                
        player.update_hero(playerhero, True)
        defenseList.append(playerhero.pk)
        defenseList.append(default_poses[i])
        i += 1

    player.defenseHeroLayout = defenseList
    defenseHeroIds = player.defenseHeroLayout[0:len(player.defenseHeroLayout):2]
    player.update_hero_defenseHeroIds(defenseHeroIds)


   # if player.id > -10000 and player.level >= Static.PVP_LEVEL:
   #     player.PVP.add_score(robot.score-player.PVP.score)

    #player.PVP.update()
    player.save()
    return player

def player_name_exsited(name):
    try:
       Player.objects.get(name=name)
       return True
    except:
       return False

#这函数没用上——snn
def filter_robots_by_level(player, limit = 10, start_level=None,  end_level=None):
    """
    获取机器人对战数据
    """
    robot_players = []


    robot_players = Player.objects.filter(
        id__lt = -10000,
        level__gte = start_level, 
        level__lte = end_level 
    ).only("id", "iconId", "updated_at", "level", "name", "vip", "defenseHeroLayout")

    robots = list(robot_players)
    random.shuffle(robots)
    return robots[0:limit]
#这函数没用上——snn
def filter_players_by_level_and_ids(level, ids, limit = 10):
    players = []

    players = Player.objects.filter(
        id__gt = 0,
        id__lt = -10000,
        id__in = ids,
        level = level, 
    ).only("id")

    players = list(players)
    random.shuffle(players)
    return players[0:limit]

def refresh_siegebattle_players(player, replaceOppId=0):
    """
    攻城战对手刷新
    """
    minLevel = player.level - 5 if player.level - 5 > 15 else 15
    maxLevel = player.level + 5 if player.level + 5 < 60 else 60
    maxLevel = maxLevel if maxLevel >= 20 else 20
    _opps = player.SiegeBattle.opps

    opps = [None, None, None, None, None]
    realOppsNumber = 0
    aiOppsNumber = 0
    oppIds = []

    for index in range(0, 5):
        opp = _opps[index] if  index+1 <= len(_opps) else None
        if not opp:
            continue
        
        if replaceOppId:
            if opp["player_id"] != replaceOppId:
                opps[index] = opp
                oppIds.append(opp["player_id"])
                if opp["player_id"] > 0:
                    realOppsNumber += 1
                else:
                    aiOppsNumber += 1
        else:
            if opp["isLocked"]:
                opps[index] = opp
                oppIds.append(opp["player_id"])
                if opp["player_id"] > 0:
                    realOppsNumber += 1
                else:
                    aiOppsNumber += 1

    realOpps = []#[opp for opp in opps if opp["player_id"] > 0 and opp["isLocked"]]
    aiOpps = []#[opp for opp in opps if opp["player_id"] < 0 and opp["isLocked"]]

    if 3 - realOppsNumber > 0:

        players = Player.objects.filter(
            id__gt = 0,
            level__gte = minLevel,
            level__lte = maxLevel,
            isOpenSiege = True,
            endLockedTime__lt = datetime.datetime.now(),
            serverid__in = settings.ALL_SERVERS,
        )
        players=list(players)
        random.shuffle(players)
        now = datetime.datetime.now()

        for _player in players:
            if 3 - realOppsNumber <= 0:
                break

            if _player.pk == player.pk:
                continue

            #20分钟未登陆
            if _player.is_onLine:
                continue

            #同工会
            if player.guildId > 0 and player.guildId == _player.guildId:
                continue

            #免战
            #if _player.in_waravoid:
            #    continue

            #已经存在
            if _player.pk in oppIds:
                continue

            result = _player.calculate_siege_spoilrewards()
            oppIds.append(_player.pk)
            realOppsNumber += 1

            realOpps.append({
                "player_id": _player.pk, 
                "rewards": [{"type":Static.GOLD_ID, "count":result["gold"]}, {"type":Static.WOOD_ID, "count":result["wood"]}],
                "isLocked" : False,
            })

    if realOppsNumber + aiOppsNumber < 5:
        
        #机器人
        players = Player.objects.filter(
            id__lte = -10002,
            level__gte = minLevel,
            level__lte = maxLevel,
        )
        players=list(players)
        random.shuffle(players)

        for _player in players:
            if realOppsNumber + aiOppsNumber >= 5:
                break
            #已经存在
            if _player.pk in oppIds:
                continue
            result = _player.calculate_siege_spoilrewards()
            oppIds.append(_player.pk)
            aiOppsNumber += 1
            aiOpps.append({
                "player_id": _player.pk, 
                "rewards": [{"type":Static.GOLD_ID, "count":result["gold"]}, {"type":Static.WOOD_ID, "count":result["wood"]}],
                "isLocked" : False,
            })

    refreshOpps = realOpps + aiOpps
    random.shuffle(refreshOpps)
    for index, opp in enumerate(opps):
        if not opp:
            opps[index] = refreshOpps.pop()

    return [opp for opp in opps if opp]


def get_pvp_players(ids):
    """
    获得对战用户信息
    """
    
    players = Player.objects.filter(
        id__in = ids,
        serverid__in = settings.ALL_SERVERS
    ).only("id", "iconId", "updated_at", "level", "name", "vip", "defenseHeroLayout", "powerRank")
    return players
