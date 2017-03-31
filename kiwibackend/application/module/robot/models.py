# -*- coding: utf-8 -*-
from django.db import models
from module.hero.api import get_card
from module.equip.api import get_cardequip
from common.models import CommonStaticModels
from submodule.fanyoy.redis import StaticDataRedisHandler
from module.common.static import Static

class Robot(models.Model, StaticDataRedisHandler, CommonStaticModels):
    SHEET_NAME = u"机器人"
    level = models.IntegerField(u"机器人等级", default=0)
    heroes_int = models.CharField(u"机器人英雄", max_length=200, default="")
    heroLevels_int = models.CharField(u"英雄等级", max_length=200, default="")
    heroUpgrades_int = models.CharField(u"英雄阶段", max_length=200, default="")
    heroStars_int = models.CharField(u"英雄星级", max_length=200, default="")
    heroPoses_int = models.CharField(u"英雄位置", max_length=200, default="")
    heroSkillLevels_int = models.CharField(u"英雄技能等级", max_length=200, default="")
    equipLevel = models.IntegerField(u"装备等级", default=0)
    equipUpgrade = models.IntegerField(u"装备阶级", default=0)
    score = models.IntegerField(u"分数", default=0)
    powerRank = models.IntegerField(u"机器人战斗力", default=0)
    cityLevel =  models.IntegerField(u"主城等级", default=0)
    towerLevel =  models.IntegerField(u"防御塔等级", default=0)
    siegeSoldierIds_int = models.CharField(u"城墙兵站位", max_length=200, default="")
    siegeSoldierLevels_int = models.CharField(u"城墙兵等级", max_length=200, default="")
    siegeWood =  models.IntegerField(u"攻城战木材", default=0)
    siegeGold =  models.IntegerField(u"攻城战金币", default=0)
    
    @property
    def heroes(self):
        return [int(float(pk)) for pk in self.heroes_int.strip().split(",") if pk]

    @property
    def heroLevels(self):
        return [int(float(pk)) for pk in self.heroLevels_int.strip().split(",") if pk]

    @property
    def heroUpgrades(self):
        return [int(float(pk)) for pk in self.heroUpgrades_int.strip().split(",") if pk]

    @property
    def heroStars(self):
        return [int(float(pk)) for pk in self.heroStars_int.strip().split(",") if pk]

    @property
    def heroPoses(self):
        return [int(float(pk)) for pk in self.heroPoses_int.strip().split(",") if pk]

    @property
    def heroSkillLevels(self):
        return [int(float(pk)) for pk in self.heroSkillLevels_int.strip().split(",") if pk]

    @property
    def equip_infos(self):
        infos = {}
        for hero_id in self.heroes:
            card = get_card(hero_id)
            equips = get_cardequip(card.career)
            infos[hero_id] = []

            for i in range(1, 5):
                if self.equipLevel < 0:
                    infos[hero_id].append((-1, -1))
                else:
                    pos_equips = getattr(equips, "pos%s" % i)
                    infos[hero_id].append((pos_equips[self.equipUpgrade], self.equipLevel))
        return infos

    @property
    def siegeSoldierIds(self):
        return [int(float(pk)) for pk in self.siegeSoldierIds_int.strip().split(",") if pk]

    @property
    def siegeSoldierLevels(self):
        return [int(float(pk)) for pk in self.siegeSoldierLevels_int.strip().split(",") if pk]

    @property
    def wallWarriorIds(self):
        """
            机器人科技树
        """
        rst = []
        for _id in Static.HERO_WALL_SOLDIER_IDS:
            meta = {
                "soldierId": _id,
                "soldierLevel": 0,
                "count" : 0
            }
            rst.append(meta)

        for i in range(len(self.siegeSoldierIds)):
            for _soldier in rst:
                if _soldier["soldierId"] == self.siegeSoldierIds[i]:
                    _soldier["soldierLevel"] = self.siegeSoldierLevels[i]
                    _soldier["count"] += 1

        return rst

