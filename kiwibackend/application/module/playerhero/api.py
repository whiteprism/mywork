# -*- coding: utf-8 -*-
from playerhero.docs import PlayerHero
from hero.models import Warrior
from hero.api import get_warrior
from module.utils import is_digits
from module.common.actionlog import ActionLogWriter
from module.soul.api import get_soul
from module.hero.api import get_heroskill
from module.playersoul.api import acquire_soul
from module.common.static import Static

def get_tutorial_heroes(player):
    tutorial_hero_ids = [111000109,114000709,115000309]
    tutorial_heroes = []
    i = -1
    for hero_id in tutorial_hero_ids:
        warrior = get_warrior(hero_id)
        skillhero = get_heroskill(warrior.cardId)
        argvs = {}
        argvs["normSkillGid"] = skillhero.skill0
        argvs["normSkillLevel"] = skillhero.skill0Lv
        argvs["level"] = 60

        # for i in range(0, len(skillhero.skillinfo)/3):
        #     argvs["skill%sGid" %(i+1)],_,_ = skillhero.skillinfo[i*3:(i+1)*3]
        #     argvs["skill%sLevel" %(i+1)] = 1

        playerhero = PlayerHero(

            # player_id = player.pk,
            warrior_id = hero_id,
            cardId = warrior.cardId,
            **argvs
        )
        playerhero.pk = i
        i -= 1
        playerhero.level = 15
        playerhero.star = 5
        playerhero.upgrade = 3


        for i in range(0, len(skillhero.skillinfo)/3):
            skillGild,_,upgrade = skillhero.skillinfo[i*3:(i+1)*3]
            if upgrade > playerhero.upgrade:

                setattr(playerhero, "skill%sGid" %(i+1), skillGild)
                setattr(playerhero, "skill%sLevel" %(i+1), 0)
            else:
                setattr(playerhero, "skill%sGid" %(i+1), skillGild)
                setattr(playerhero, "skill%sLevel" %(i+1), 2)


        tutorial_heroes.append(playerhero)

    return tutorial_heroes

def acquire_hero(player, warrior_or_warrior_id, info="", **argvs):
    ''' 
    acquire player hero
    return playerhero
    return playersoulfragment
    '''
    if isinstance(warrior_or_warrior_id, Warrior):
        warrior = warrior_or_warrior_id
    elif is_digits(warrior_or_warrior_id):
        warrior = get_warrior(warrior_or_warrior_id)
        if not warrior:
            return None
    if player.heroes.get(warrior.cardId):
        soul = get_soul(warrior.hero.soulId)
        playersoul = acquire_soul(player, warrior.hero.soulId, soul.breakCost, info=info)
        return playersoul

    skillhero = get_heroskill(warrior.cardId)
    argvs["normSkillGid"] = skillhero.skill0
    argvs["normSkillLevel"] = skillhero.skill0Lv

    for i in range(0, len(skillhero.skillinfo)/3):
        skillGiId,_,upgrade = skillhero.skillinfo[i*3:(i+1)*3]
        if upgrade == 0:
            argvs["skill%sLevel" %(i+1)] = 1
        else:
            argvs["skill%sLevel" %(i+1)] = 0
        argvs["skill%sGid" %(i+1)] = skillGiId

    playerhero = player.heroes.create(pk=warrior.cardId, cardId = warrior.cardId, warrior_id = warrior.id, **argvs)

    heroteamId = playerhero.warrior.hero.heroTeamId
    playerheroteam = player.heroteams.get(heroteamId)
    if not playerheroteam:
        playerheroteam = player.heroteams.create(pk=heroteamId, teamId = heroteamId)
        player.update_heroteam(playerheroteam, True)

    player.update_hero(playerhero, True)

    player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_ACQUIRE_HREO, number=1, is_incr=True, is_series=True)
    ActionLogWriter.hero_acquire(player, playerhero.id, warrior.id, warrior.cardId, info=info)

    # 获得也可以获得高星级的英雄。同时这个也算是完成相应的任务，七天乐或者成就等
    if playerhero.star >= 3:
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_HERO_STAR_UP_GREEN3, number=1, is_incr=True, is_series=True)

    if playerhero.star >= 5:
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_HERO_STAR_UP_GREEN5, number=1, is_incr=True, is_series=True)

    if playerhero.star >= 6:
        player.task_going(Static.TASK_CATEGORY_HERO_STAR2_UPGRADE, number=1, is_incr=True, is_series=True)

    if playerhero.star >= 7:
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_HERO_STAR_UP_BLUE2, number=1, is_incr=True, is_series=True)

    if playerhero.star >= 10:
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_HERO_STAR_UP_BLUE5, number=1, is_incr=True, is_series=True)

    if playerhero.star >= 11:
        player.task_going(Static.TASK_CATEGORY_HERO_STAR3_UPGRADE, number=1, is_incr=True, is_series=True)
        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_HERO_STAR_UP_PURPLE, number=1, is_incr=True, is_series=True)

    if playerhero.star >= 16:
        player.task_going(Static.TASK_CATEGORY_HERO_STAR5_UPGRADE, number=1, is_incr=True, is_series=True)

    return playerhero

