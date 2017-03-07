# -*- coding: utf-8 -*-
from mongoengine import *
from common.docs import PlayerRedisDataBase
from common.decorators.memoized_property import memoized_property
from module.utils import is_digits
from building.models import Building
from common.static import Static
from module.hero.api import get_heromasters_by_catergory, get_heroteam, get_hero, get_warrior, get_card, get_herolevel
from module.utils import random_item_pick
import  datetime
from utils import datetime_to_unixtime
from module.utils import delta_time
from module.common.actionlog import ActionLogWriter

class PlayerArmy(PlayerRedisDataBase):
    """
    小兵
    """
    armies = DictField(default={}) #小兵
    has_alliance = BooleanField(default=False)
    has_horde = BooleanField(default=False)
    has_dragonhome = BooleanField(default=False)
    drill_armies = DictField(default={}) #正在生产的小兵

    def set_alliance(self, value):
        self.has_alliance = value
        self.player.armies.update()

    def set_horde(self, value):
        self.has_horde = value
        self.player.armies.update()

    def set_dragonhome(self, value):
        self.has_dragonhome = value
        self.player.armies.update()

    @property
    def population(self):
        population = 0
        for w, v in self.armies.items():
            warrior = get_card(int(w)).warrior
            population += warrior.population*v["num"]
        for w, v in self.drill_armies.items():
            warrior = get_card(int(w)).warrior
            population += warrior.population*v
        return population

    def drill_start(self, warrior_id, number=1):
        warrior_id = str(warrior_id)
        if warrior_id not in self.drill_armies:
            self.drill_armies[warrior_id] = 0
        self.drill_armies[warrior_id] += number
        self.player.armies.update()

    def drill_end(self, warrior_id, number=1):
        warrior_id = str(warrior_id)
        if warrior_id not in self.drill_armies:
            return False
        self.drill_armies[warrior_id] -= number
        if self.drill_armies[warrior_id] == 0:
            del self.drill_armies[warrior_id]  
        self.player.armies.update()

    def to_dict(self):
        _dict = {}
        _dict["hasSoldierLevel"] = True
        _dict["hasSoldiers"] = True
        _dict["key"] = self.pk
        _dict["soldiers"] = []#[{"type": int(k), "count":v["num"]} for k,v in self.armies.items()]
        _dict["soldierLevel"] = []#[{"type": int(k), "level":v["level"]} for k,v in self.armies.items()]

#        if self.has_alliance or self.has_horde or self.has_dragonhome:
        if True:
            _soldiers = []
#            if self.has_horde:
            _soldiers += Building.hordebarrack_soldiers()


            for k in _soldiers:
                if str(k) not in self.armies:
                    num = 0
                    level = 1
                else:
                    num = self.armies[str(k)]["num"]
                    level = self.armies[str(k)]["level"]

                _dict["soldiers"].append({"type": k, "count": num})
                _dict["soldierLevel"].append({"type": k, "level":level})
                    
        return _dict


    def number(self, warrior_id):
        warrior_id = str(warrior_id)
        if warrior_id not in self.armies:
            return 0
        else:
            return self.armies[warrior_id]["num"]

    def level(self, warrior_id):
        warrior_id = str(warrior_id)
        if warrior_id not in self.armies:
            return 1
        else:
            return self.armies[warrior_id]["level"]

    def level_up(self, warrior_id, delta_level=1):
        warrior_id = str(warrior_id)
        if warrior_id not in self.armies:
            self.armies[warrior_id] = {"num": 0, "level":1}

        self.armies[warrior_id]["level"] += 1
        self.player.armies.update()
        return True



    def acquire(self, warrior_id, number):
        """
        建造小兵
        return 建造成功，是否为第一次建造
        """

        warrior_id = str(warrior_id)
        
        if warrior_id not in self.armies:
            self.armies[warrior_id] = {"num": 0, "level":1}

        self.armies[warrior_id]["num"] += number
        self.player.armies.update()

        return True
            
    def lost(self, warrior_id, number):
        """
        lost小兵
        """

        warrior_id = str(warrior_id)
        
        if warrior_id not in self.armies or self.armies[warrior_id]["num"] < number:
            return False

        self.armies[warrior_id]["num"] -= number
        self.player.armies.update()

        return True

class PlayerRampartSoldiers(PlayerRedisDataBase):
    """
    城墙士兵
    """
    soldierId = IntField(default=0)
    soldierLevel = IntField(default=0)
    endDatetime = DateTimeField(default=datetime.datetime.now) 
    startDatetime = DateTimeField(default=datetime.datetime.now)

    @property
    def canLevelUp(self):
        return self.soldierLevel < 10

    def levelUp(self):
        """
        士兵升级
        """
        self.soldierLevel += 1;

    @property
    def timeLeft(self):
        over_time = delta_time(self.startDatetime, self.endDatetime)
        return over_time if over_time > 0 else 0

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["timeLeft"] = self.timeLeft
        del dicts["startDatetime"]
        del dicts["endDatetime"]
        return dicts
 
class PlayerHero(PlayerRedisDataBase):
    """
    用户卡牌
    """
    cardId = IntField(default=0) #前端的gid
    artifact1Id = IntField(default=0) #攻击神器
    artifact2Id = IntField(default=0) #防御神器
    equip1Id = IntField(default=0) #武器
    equip2Id = IntField(default=0) #头盔
    equip3Id = IntField(default=0) #衣服
    equip4Id = IntField(default=0) #裤子

    warrior_id = IntField()
    level = IntField(default=1) #level
    normSkillGid = IntField(default=0) #normSkillGid
    normSkillLevel = IntField(default=1) #normSkillLevel
    skill1Gid = IntField(default=0) #英雄带着的技能
    skill1Level = IntField(default=0) #skill1Level
    skill2Gid = IntField(default=0) #skill2Gid
    skill2Level = IntField(default=0) #skill2Level
    skill3Gid = IntField(default=0) #skill3Gid
    skill3Level = IntField(default=0) #skill3Level
    skill4Gid = IntField(default=0) #skill4Gid
    skill4Level = IntField(default=0) #skill4Level
    star = IntField(default=0) #英雄的star
    upgrade = IntField(default=0) #upgrade
    xp = IntField(default=0) #经验
    
    destinyLevel = IntField(default=0) #天命等级

    equipEnhanceMasterId = IntField(default=0)
    equipRefineMasterId = IntField(default=0)
    artifactEnhanceMasterId = IntField(default=0)
    artifactRefineMasterId = IntField(default=0)

    #trainHp = FloatField(default=0)
    #trainAttack = FloatField(default=0)
    #trainPhysicalArmor = FloatField(default=0)
    #trainMagicArmor = FloatField(default=0)

    #trainAddHp = FloatField(default=0)
    #trainAddAttack = FloatField(default=0)
    #trainAddPhysicalArmor = FloatField(default=0)
    #trainAddMagicArmor = FloatField(default=0)
    hpLeftForRaid = FloatField(default=-1)
    mpLeftForRaid = FloatField(default=-1)

    #trainingStartTime = DateTimeField(default=datetime.datetime.max) # 训练开始时间
    # speedStartTime = DateTimeField(default=datetime.datetime.max) # 训练开始时间
    #trainingXp = IntField(default=0) #经验
    trainingAt = DateTimeField()
    # isSpeeding = IntField(default=0)
    # speedAddXp = IntField(default=0)


    def __init__(self, **argvs):
        super(PlayerHero, self).__init__(**argvs)
        self.is_new = False #是否为第一次获得

    #抽奖id
    @property
    def obj_id(self):
        return self.cardId 

    @property
    def is_hero(self):
        return True

    @property
    def is_soul(self):
        return False

    def __unicode__(self):
        return u"%s:%s(%s:quality:%s)" %(self.warrior.hero.name,self.id, self.warrior_id, self.quality)

    @memoized_property
    def warrior(self):
        return get_warrior(self.warrior_id)

    def get_skill_info(self, pos):
        """
        获取对应位置技能
        """
        if not hasattr(self, "skill%sGid" % pos) or not hasattr(self, "skill%sLevel" % pos):
            return None, None

        _id = getattr(self, "skill%sGid" % pos)
        _level = getattr(self, "skill%sLevel" % pos)

        return _id, _level

    def skill_levelup(self, pos):
        """
        POS位置技能升级
        """
        _id = getattr(self, "skill%sGid" % pos)
        _level = getattr(self, "skill%sLevel" % pos)
        setattr(self, "skill%sLevel" % pos , _level+1)
        return True


    def skill_can_levelup(self, pos):
        """
        对应位置技能是否能升级
        """
    
        if not hasattr(self, "skill%sGid" % pos) or not hasattr(self, "skill%sLevel" % pos):
            return False

        _id = getattr(self, "skill%sGid" % pos)
        _level = getattr(self, "skill%sLevel" % pos)
        
        if not _id:
            return False

        return True

    @property
    def quality(self):
        return self.warrior.quality

    def get_equip(self, pos):
        if pos == 1:
            return self.equip1Id
        elif pos == 2:
            return self.equip2Id
        elif pos == 3:
            return self.equip3Id
        elif pos == 4:
            return self.equip4Id
        elif pos == 5:
            return self.artifact1Id
        elif pos == 6:
            return self.artifact2Id

    def set_equip(self, pos, playerequip_or_playerequip_id=None):
        if not playerequip_or_playerequip_id:
            _id = 0
        elif is_digits(playerequip_or_playerequip_id):
            _id = playerequip_or_playerequip_id
        else:
            _id = playerequip_or_playerequip_id.pk

        if pos == 1:
            self.equip1Id =  _id
        elif pos == 2:
            self.equip2Id = _id
        elif pos == 3:
            self.equip3Id = _id
        elif pos == 4:
            self.equip4Id = _id 
        elif pos == 5:
            self.artifact1Id = _id
        elif pos == 6:
            self.artifact2Id = _id

        if pos < 5:
            self.check_equip_enhancemaster()
            self.check_equip_refinemaster()
        else:
            self.check_artifact_enhancemaster()
            self.check_artifact_refinemaster()

    def add_xp(self, xp, player=None):
        levelup = False
        self.xp += xp
        info = u'英雄升级'
        while True:
            herolevel = get_herolevel(self.level)

            if self.xp >= herolevel.xp:
                if self.level >= self.player.level:
                    self.xp = herolevel.xp
                    break
                else:
                    before_level = self.level
                    self.level += 1
                    ActionLogWriter.hero_levelup(self.player, self.pk, self.warrior_id, self.cardId, before_level, self.level, xp, info)
                    if self.level == 26:
                        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_FIVE_HERO_LEVELUP26, number=1, is_incr=True, with_top=False, is_series=False)
                    elif self.level == 28:
                        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_FIVE_HERO_LEVELUP28, number=1, is_incr=True, with_top=False, is_series=False)
                    elif self.level == 30:
                        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_FIVE_HERO_LEVELUP30, number=1, is_incr=True, with_top=False, is_series=False)
                    elif self.level == 32:
                        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_FIVE_HERO_LEVELUP32, number=1, is_incr=True, with_top=False, is_series=False)
                    elif self.level == 34:
                        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_FIVE_HERO_LEVELUP34, number=1, is_incr=True, with_top=False, is_series=False)
                    elif self.level == 36:
                        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_FIVE_HERO_LEVELUP36, number=1, is_incr=True, with_top=False, is_series=False)
                    elif self.level == 38:
                        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_FIVE_HERO_LEVELUP38, number=1, is_incr=True, with_top=False, is_series=False)
                    elif self.level == 40:
                        player.seven_days_task_going(Static.SEVEN_TASK_CATEGORY_FIVE_HERO_LEVELUP40, number=1, is_incr=True, with_top=False, is_series=False)

                    levelup = True
                    self.xp -= herolevel.xp
            else:
                break

        player.update_hero(self, True)
        return levelup

    def check_equip_enhancemaster(self):
        old_equipEnhanceMasterId = self.equipEnhanceMasterId
        self.equipEnhanceMasterId = 0
        if self.equip1Id and self.equip2Id and self.equip3Id and self.equip4Id:
            heromasters = get_heromasters_by_catergory(self.warrior.hero.category, Static.HERO_EQUIP_ENHANCE_ID)
            heromasters.sort(key=lambda x: x.level, reverse=True)
            playerequip1 = self.player.equips.get(self.equip1Id)
            playerequip2 = self.player.equips.get(self.equip2Id)
            playerequip3 = self.player.equips.get(self.equip3Id)
            playerequip4 = self.player.equips.get(self.equip4Id)

            min_level = min([playerequip1.level, playerequip2.level, playerequip3.level, playerequip4.level])
            # directed by shuaifu
            min_level = min_level / 12

            for heromaster in heromasters:
                if min_level >= heromaster.level:
                    self.equipEnhanceMasterId = heromaster.id
                    break
        return old_equipEnhanceMasterId != self.equipEnhanceMasterId

    def check_equip_refinemaster(self):
        old_equipRefinMasterId = self.equipRefineMasterId
        self.equipRefineMasterId = 0
        if self.equip1Id and self.equip2Id and self.equip3Id and self.equip4Id:
            heromasters = get_heromasters_by_catergory(self.warrior.hero.category, Static.HERO_EQUIP_REFINE_ID)
            heromasters.sort(key=lambda x: x.level, reverse=True)
            playerequip1 = self.player.equips.get(self.equip1Id)
            playerequip2 = self.player.equips.get(self.equip2Id)
            playerequip3 = self.player.equips.get(self.equip3Id)
            playerequip4 = self.player.equips.get(self.equip4Id)

            min_level = min([playerequip1.refineLevel, playerequip2.refineLevel, playerequip3.refineLevel, playerequip4.refineLevel])
            # directed by shuaifu
            min_level = min_level / 3

            for heromaster in heromasters:
                if min_level >= heromaster.level:
                    self.equipRefineMasterId = heromaster.id
                    break
        return old_equipRefinMasterId != self.equipRefineMasterId


    def check_artifact_enhancemaster(self):
        old_artifactEnhanceMasterId = self.artifactEnhanceMasterId
        self.artifactEnhanceMasterId = 0
        if self.artifact1Id and self.artifact2Id:
            heromasters = get_heromasters_by_catergory(self.warrior.hero.category, Static.HERO_ARTIFACT_ENHANCE_ID)
            heromasters.sort(key=lambda x: x.level, reverse=True)
            playerartifact1 = self.player.artifacts.get(self.artifact1Id)
            playerartifact2 = self.player.artifacts.get(self.artifact2Id)

            min_level = min([playerartifact1.level, playerartifact2.level])
            # directed by shuaifu
            min_level = min_level / 12

            for heromaster in heromasters:
                if min_level >= heromaster.level:
                    self.artifactEnhanceMasterId = heromaster.id
                    break

        return old_artifactEnhanceMasterId != self.artifactEnhanceMasterId

    def check_artifact_refinemaster(self):
        old_artifactRefineMasterId = self.artifactRefineMasterId
        self.artifactRefineMasterId = 0
        if self.artifact1Id and self.artifact2Id:
            heromasters = get_heromasters_by_catergory(self.warrior.hero.category, Static.HERO_ARTIFACT_REFINE_ID)
            heromasters.sort(key=lambda x: x.level, reverse=True)
            playerartifact1 = self.player.artifacts.get(self.artifact1Id)
            playerartifact2 = self.player.artifacts.get(self.artifact2Id)

            min_level = min([playerartifact1.refineLevel, playerartifact2.refineLevel])
            # directed by shuaifu
            min_level = min_level / 3

            for heromaster in heromasters:
                if min_level >= heromaster.level:
                    self.artifactRefineMasterId = heromaster.id
                    break

        return old_artifactRefineMasterId != self.artifactRefineMasterId


    def to_simple_dict(self):
        dicts = {}
        dicts["heroId"] = self.cardId
        dicts["level"] = self.level
        dicts["star"] = self.star
        dicts["upgrade"] = self.upgrade
        return dicts


    # def training_dict(self):
    #     dicts = {}
    #     is_speeding = False


    #     dicts["id"] = self.cardId
    #    # dicts["isInTraining"] = self.isInTraining
    #     #dicts["trainingPosition"] = self.trainingPosition

    #     trainingStartAt = self.trainingStartAt.replace(tzinfo=None)

    #     # 如果开始时间大于当前时间，起始是非法的数据，训练所里面英雄的开始时间不会比当前的大这是一定的。

    #         # 判断从开始到现在查看一共经过了多少秒
    #         deltatime = (datetime.datetime.now()-trainingStartAt).total_seconds()
    #         # 重新计算开始时间。赋值为当前时间
    #         self.trainingStartTime = datetime.datetime.now()
    #     # 如果自身处于加速状态
    #     if self.isSpeeding:

    #         noInfoTime = self.speedStartTime.replace(tzinfo=None)
    #         # 计算从加速到现在经历了多久时间
    #         speeddel = (datetime.datetime.now() - noInfoTime).total_seconds()
    #         # 如果超过一个小时了
    #         if speeddel >= 3600:
    #             # 急速状态清除
    #             self.isSpeeding = 0
    #             # 最后总增量经验设置为一个小时减去上一次查看的时间差
    #             speedxp = 3600 - self.speedAddXp
    #             self.speedAddXp = 0
    #         else:
    #             # 如果不到一个小时的话,
    #             lastprocess = self.speedAddXp
    #             self.speedAddXp = speeddel
    #             #　计算的方法就是　加速开始的时间是固定的若干时间以后计算一次时间差，再查看再计算一次时间差。
    #             # 并把上次的时间差记录下来，看看两次之间间隔了多久就知道应该加多少经验了。
    #             #　如果某一次的时间差超过一个小时，就走进上一个判断的分支
    #             speedxp = self.speedAddXp - lastprocess
    #             is_speeding = True
    #     else:
    #         speedxp = 0

    #     dicts["deltaTime"] = deltatime
    #     # 每分钟增加２０点经验
    #     self.add_xp(int((deltatime + speedxp) * 0.33), self.player)
    #     dicts["xp"] = self.xp
    #     dicts["xp"] = self.xp
    #     dicts["level"] = self.level

    #     return dicts, is_speeding

    def training(self):
        """
        开始训练
        """
        # self.isInTraining = 1
       # self.trainingPosition = position
        self.trainingAt = datetime.datetime.now()

    def untraining(self):
        now = datetime.datetime.now()
        if not self.trainingAt:
            self.trainingAt = now
        deltaTime = (now - self.trainingAt.replace(tzinfo=None)).total_seconds()
        deltaXp = deltaTime / 60 * Static.HERO_TRAINING_PER_MINUTE_XPS
        self.add_xp(deltaXp, self.player)


    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["heroId"] = self.cardId
        dicts["id"] = self.cardId
        del dicts["warrior_id"]
        del dicts["cardId"]
        if self.trainingAt:
            dicts["trainingAt"] = int(datetime_to_unixtime(self.trainingAt))
        # del dicts["trainingStartTime"]
        # del dicts["speedStartTime"]
        return dicts

    def destiny(self):
        before_destiny = self.destinyLevel
        self.destinyLevel += 1
        info = u'英雄天命'
        ActionLogWriter.hero_destiny(self.player, self.pk, self.warrior_id, before_destiny, self.destinyLevel, info)

    def start_upgrade(self):
        before_star = self.star
        self.star += 1
        info = u'英雄升星'
        ActionLogWriter.hero_stargrade(self.player, self.pk, self.warrior_id, before_star, self.star, info)
    # def train(self, train_type, herotrain, count):
    #     """
    #     培养
    #     """


    #     self.trainAddAttack = 0
    #     self.trainAddPhysicalArmor = 0
    #     self.trainAddMagicArmor = 0
    #     self.trainAddHp = 0

    #     for i in range(0, count):
    #         trainattack, _ = random_item_pick(herotrain.train_attackvalues(train_type))
    #         trainphysicalArmor, _ = random_item_pick(herotrain.train_physicalvalues(train_type))
    #         trainmagicArmor, _ = random_item_pick(herotrain.train_magicvalues(train_type))
    #         trainhp, _ = random_item_pick(herotrain.train_hpvalues(train_type))

    #         self.trainAddAttack += trainattack
    #         self.trainAddPhysicalArmor += trainphysicalArmor
    #         self.trainAddMagicArmor += trainmagicArmor
    #         self.trainAddHp += trainhp




    #     if self.warrior.hero.trainAttackMax < self.trainAttack + self.trainAddAttack:
    #         self.trainAddAttack = self.warrior.hero.trainAttackMax - self.trainAttack
    #     if self.trainAttack + self.trainAddAttack < 0:
    #         self.trainAddAttack = -self.trainAttack

    #     if self.warrior.hero.trainPhysicalArmorMax < self.trainPhysicalArmor + self.trainAddPhysicalArmor:
    #         self.trainAddPhysicalArmor = self.warrior.hero.trainPhysicalArmorMax - self.trainPhysicalArmor
    #     if self.trainPhysicalArmor + self.trainAddPhysicalArmor < 0:
    #         self.trainAddPhysicalArmor = -self.trainPhysicalArmor


    #     if self.warrior.hero.trainMagicArmorMax < self.trainMagicArmor + self.trainAddMagicArmor:
    #         self.trainAddMagicArmor = self.warrior.hero.trainMagicArmorMax - self.trainMagicArmor
    #     if self.trainMagicArmor + self.trainAddMagicArmor < 0:
    #         self.trainAddMagicArmor = -self.trainMagicArmor


    #     if self.warrior.hero.trainHpMax < self.trainHp + self.trainAddHp:
    #         self.trainAddHp = self.warrior.hero.trainHpMax - self.trainHp
    #     if self.trainHp + self.trainAddHp < 0:
    #         self.trainAddHp = -self.trainHp



    # def train_confirm(self):
    #     """
    #     培养确认
    #     """
    #     self.trainHp += self.trainAddHp
    #     if self.trainHp >= self.warrior.hero.trainHpMax:
    #         self.trainHp = self.warrior.hero.trainHpMax

    #     self.trainAttack += self.trainAddAttack
    #     if self.trainAttack >= self.warrior.hero.trainAttackMax:
    #         self.trainAttack = self.warrior.hero.trainAttackMax

    #     self.trainPhysicalArmor += self.trainAddPhysicalArmor
    #     if self.trainPhysicalArmor >= self.warrior.hero.trainPhysicalArmorMax:
    #         self.trainPhysicalArmor = self.warrior.hero.trainPhysicalArmorMax

    #     self.trainMagicArmor += self.trainAddMagicArmor
    #     if self.trainMagicArmor >= self.warrior.hero.trainMagicArmorMax:
    #         self.trainMagicArmor = self.warrior.hero.trainMagicArmorMax

    #     self.trainAddAttack = 0
    #     self.trainAddPhysicalArmor = 0
    #     self.trainAddMagicArmor = 0
    #     self.trainAddHp = 0


class PlayerHeroTeam(PlayerRedisDataBase):
    """
    英雄分组
    """
    teamId = IntField(default=0)
    score = IntField(default=0)
    v = IntField(default=0)
    teamAttrId = IntField(default=0)
    level = IntField(default=1)

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        return dicts

    @memoized_property
    def heroteam(self):
        return get_heroteam(self.pk)

    def update_score(self):
        total_score = 0
        playerheroes = self.player.heroes.get_by_pks(self.heroteam.heroCardIds)
        for playerhero in playerheroes.values():
            total_score += playerhero.level * 10 + (playerhero.upgrade + 1) * 100 + playerhero.star * 60
        self.score = total_score

    def level_up(self, heroteamnextlevel):
        self.teamAttrId = heroteamnextlevel.pk
        self.level += 1
