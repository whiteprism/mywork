# -*- coding: utf-8 -*-
from hero.models import Card, HeroBubble, Hero, HeroEvolveCosts, HeroSkill, Warrior, WarriorLevel, HeroLevel, HeroStarUpgrade, HeroMaster, HeroAttribute,HeroDestiny, HeroStar, HeroTeam, HeroTeamLevel,HeroCombat

def update_hero_cache():
    Card.create_cache()
    Hero.create_cache()
    HeroEvolveCosts.create_cache()
    HeroSkill.create_cache()
    Warrior.create_cache()
    WarriorLevel.create_cache()
    HeroLevel.create_cache()
    HeroStarUpgrade.create_cache()
    HeroMaster.create_cache()
    HeroAttribute.create_cache()
    HeroDestiny.create_cache()
    HeroStar.create_cache()
    # HeroTrain.create_cache()
    HeroTeam.create_cache()
    HeroTeamLevel.create_cache()
    HeroBubble.create_cache()
    HeroCombat.create_cache()

def get_card(pk):
    return Card.get(int(pk))

def get_cards():
    return Card.get_all_list()

# def get_heroequipfateattr(pk):
#     return HeroEquipFatesAttr.get(int(pk))

# def get_heroequipfateattrs():
#     return HeroEquipFatesAttr.get_all_list()

def get_warrior_by_upgrade(warrior_id, upgrade):
    pk = warrior_id * 100 + upgrade
    return Warrior.get(int(pk))

def get_warrior(pk):
    return Warrior.get(int(pk))

def get_warriorlevel(warrior_id, level):
    pk = warrior_id * 100 + level
    return WarriorLevel.get(int(pk))

def get_warriors():
    return Warrior.get_all_list()

def get_warrior_level(warrior_or_warrior_id, level):
    warrior = get_warrior(warrior_or_warrior_id)
    return warrior.levels[level-1]

def get_hero(pk):
    return Hero.get(int(pk))

def get_card(pk):
    return Card.get(int(pk))

def get_heromasters_by_catergory(herocategory, enhancetype):
    category = int(herocategory * 10 + enhancetype)
    return HeroMaster.get_heromasters_by_catergory(category)

def get_heroskills():
    return HeroSkill.get_all_list()

def get_heroskill(pk):
    return HeroSkill.get(int(pk))

def get_herolevel(pk):
    return HeroLevel.get(pk)

def get_herolevels():
    return HeroLevel.get_all_list()

def get_herostarupgrade(star):
    return HeroStarUpgrade.get(int(star))

def get_herostarupgrades():
    return HeroStarUpgrade.get_all_list()

def get_heromaster(category, level):
    pk = str(category * 1000 + level)
    return HeroMaster.get(int(pk))

def get_heromasters():
    return HeroMaster.get_all_list()

def get_herodestiny(level):
    return HeroDestiny.get(int(level +1))

def get_herodestinies():
    return HeroDestiny.get_all_list()


def get_herostar(card_id, star):
    herostar_id = int(card_id*100 + star)
    return HeroStar.get(herostar_id)

def get_herostars():
    return HeroStar.get_all_list()

# def get_herotrain(pk):
#     return HeroTrain.get(int(pk))

# def get_herotrains():
#     return HeroTrain.get_all_list()

def get_heroteams():
    return HeroTeam.get_all_list()

def get_heroteam(pk):
    return HeroTeam.get(int(pk))

def get_heroteamlevels():
    return HeroTeamLevel.get_all_list()

def get_heroteamlevel_by_teamid_level(teamId,  level):
    pk = teamId * 1000 + level
    return HeroTeamLevel.get(int(pk))

def get_heroteamlevel(pk):
    return HeroTeamLevel.get(int(pk))

def get_herobubble(pk):
    return HeroBubble.get(int(pk))

def get_herobubbles():
    return HeroBubble.get_all_list()

def get_herocombat(pk):
    return HeroCombat.get(int(pk))

def get_herocombats():
    return HeroCombat.get_all_list()
