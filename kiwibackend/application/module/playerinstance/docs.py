# -*- coding: utf-8 -*-
from mongoengine import *
from common.docs import PlayerDataBase, PlayerRelationBase, PlayerRedisDataBase
from common.decorators.memoized_property import memoized_property
from module.instance.api import get_instancelevel, get_eliteinstancelevel,get_raidinstance, get_instance, get_raidlevel, get_elementtowerinstance, get_elementtowerbuffs, get_elementtowerbuff
import datetime
from module.experiment.api import check_player_in_experiment_by_experimentname
from common.static import Static
import random
from rewards.models import CommonReward
from module.rewards.api import reward_send
from module.vip.api import get_vip

class PlayerInstanceLevelBase(PlayerRedisDataBase):
    """
    副本数据
    """
    # 已经刷新的次数
    refreshCount = IntField(default=0)
    # 已经挑战成功的次数
    succeedCount = IntField(default=0)
    # 星级
    star = IntField(default=0)
    # 获得过的奖励
    getRewardIds = ListField(default=[])

    meta = {
        'abstract': True,
    }

    # 玩家关卡的id
    @property
    def level_id(self):
        return self.pk




    def load(self, player):
        self.player = player
        self.player = player
        self.refresh()

    # 重置副本所做的操作
    def refresh(self):
        now = datetime.datetime.now()
        if now.date() != self.updated_at.date():
            self.refreshCount = 0
            self.succeedCount = 0
            self.getRewardIds = []


    def refresh_count(self):
        '''
        刷新挑战次数
        '''
        self.refreshCount += 1
        self.succeedCount = 0
        self.getRewardIds = []

    # 挑战成功增加次数
    def add_count(self):
        '''
        增加副本次数
        '''
        self.succeedCount += 1


    def make_instance_rewards(self):
        '''
        获取章节的随机奖励
        '''
        data = {}
        instance = get_instance(self.instancelevel.instance_id)
        rewardData = instance.rewardData
        probability = rewardData["probability"] * 1000000
        i = random.randint(1,1000000)
        if i < probability:
            data["type"] = random.choice(rewardData["type"])
            index = rewardData["type"].index(data["type"])
            data["count"] = rewardData["count"][index]

        return data

    # 精英的获取章节的奖励
    def make_elite_instance_rewards(self):
        '''
        获取章节的随机奖励
        '''
        data = {}
        elite_instance = get_instance(self.eliteInstancelevel.instance_id)
        rewardData = elite_instance.rewardData
        probability = rewardData["probability"] * 1000000
        i = random.randint(1,1000000)
        if i < probability:
            data["type"] = random.choice(rewardData["type"])
            index = rewardData["type"].index(data["type"])
            data["count"] = rewardData["count"][index]

        return data



class PlayerInstanceLevel(PlayerInstanceLevelBase):
    '''
    普通
    '''

    rewardBoxes = ListField(default=[])

    @memoized_property
    def instancelevel(self):
        # self.level_id 继承子父类，就是玩家关卡的id
        return get_instancelevel(self.level_id)

    @classmethod
    def unlock(cls, player, level_id):
        """
        解锁关卡
        """
        _, playerinstancelevel = player.instancelevels.get_or_create(level_id)
        # 这里面的id是下一关的id
        player.lastInstance["lastFinished"] = False
        #　设置下一关未解锁的ｉｄ
        player.lastInstance["lastLevelId"] = level_id
        # 更新
        player.set_update("lastInstance")
        player.update_instancelevel(playerinstancelevel, True)
        return playerinstancelevel

    def success(self, star):
        """
        挑战成功
        """
        unlock_new_instance = False
        # 星级赋值这里有什么用？？
        if star > self.star:
            self.star = star

        # 这个是最后的副本id
        # lastInstance = DictField(default = {"lastFinished":False, "lastLevelId":Static.FIRST_INSTANCE_LEVEL_ID})
        # 会初始化一个ｉｄ但是默认的是ｆａｌｓｅ，在这里给他赋值的ｔｒｕｅ记录玩家当前的关卡进度
        if self.level_id == self.player.lastInstance["lastLevelId"]:
            self.player.lastInstance["lastFinished"] = True
            # 更新相关信息　更新属性的字段值　这么使用
            self.player.set_update("lastInstance")
            # 如果有下一个关卡
            if self.instancelevel.nextInstanceId:
                # 取得下一个关卡通过　nextInstanceId
                next_instancelevel = get_instancelevel(self.instancelevel.nextInstanceId)

                # 如果没有下一关证明，已经是副本的最后一关了.那么就返回当前的关卡。
                if not next_instancelevel:
                    return self.instancelevel
                # 如果玩家的等级满足条件就去解锁下一个
                if self.player.level >= next_instancelevel.minUserLevel:
                    # 这个是传入的下一个关卡id，目的是为了打通一关为新的信息赋值
                    unlock_new_instance = PlayerInstanceLevel.unlock(self.player, next_instancelevel.pk)
                #普通副本第一章节通关开启第一章节精英副本
                # 判断当前关的章节ｉｄ和下一关的章节ｉｄ不同。证明这是某一章的最后一关。
                if self.instancelevel.instance_id != next_instancelevel.instance_id:

                    # 如果是第2章普通关卡全部完成，那么开启精英的关卡
                    if self.instancelevel.instance_id == 2:

                        # 解锁相应的精英关卡，这里的id需要重新设置。
                        PlayerEliteInstanceLevel.unlock(self.player, Static.FIRST_ELITE_INSTANCE_LEVEL_ID)
                        self.player.start_tutorial_by_id(Static.TUTORIAL_ID_ELITE_INSTANCE)
                    else:
                        # 如果已经不是第一章完成了。是第二章或者第三章。
                        # 最后一个精英关已经完成
                        if self.player.lastEliteInstance["lastEliteFinished"]:
                            # 拿到当前解锁的最后一关
                            eliteinstancelevel = get_eliteinstancelevel(self.player.lastEliteInstance["lastEliteLevelId"])
                            # 如果有下一关就取下一个。
                            if eliteinstancelevel.eliteNextInstanceId:
                                next_eliteinstancelevel = get_eliteinstancelevel(eliteinstancelevel.eliteNextInstanceId)
                                # 当前的精英关章节id 和 下一关的精英章节id不同，说明当前是某一章的最后一个精英关。这里就需要普通关卡和精英的章节对应起来。
                                if eliteinstancelevel.instance_id != next_eliteinstancelevel.instance_id and next_instancelevel.instance_id >= next_eliteinstancelevel.instance_id:
                                    # 对应解锁下一关精英
                                    PlayerEliteInstanceLevel.unlock(self.player, next_eliteinstancelevel.id)
        # 返回的是下一关的对象信息
        return unlock_new_instance

    def make_rewards(self):
        '''
        获取关卡的奖励
        '''

        # 这是配置必出奖励
        rewards_data = self.instancelevel.rewardData
        max_player_count = self.instancelevel.maxPlayCount
        if self.succeedCount > max_player_count - len(rewards_data["mustId"]) and self.succeedCount <= max_player_count:
            rewardId = rewards_data["mustId"][max_player_count- self.succeedCount]

            if rewardId not in self.getRewardIds:
                index = rewards_data["type"].index(rewardId)
                rCount = rewards_data["count"][index]
                tempDict = {}
                tempDict["type"] = rewardId
                tempDict["count"] = rCount
                self.rewardBoxes.append(tempDict)
                self.getRewardIds.append(rewardId)

        return self.rewardBoxes


    # 在战前就将礼物准备好，保存起来，战后直接加到身上
    def make_rewards_before_fight(self):

        self.rewardBoxes = []

        rewards_data = self.instancelevel.rewardData
        # 这是每一个副本关具体的奖励
        x = 0
        for index, probability in enumerate(rewards_data["probability"]):
            x = probability * 1000000
            i = random.randint(1,1000000)
            if i < x:
                rewardId = rewards_data["type"][index]
                rCount = rewards_data["count"][index]
                tempDict = {}
                tempDict["type"] = rewardId
                tempDict["count"] = rCount
                self.rewardBoxes.append(tempDict)
                if rewardId not in self.getRewardIds:
                    self.getRewardIds.append(rewardId)

        # 这是章节的随机奖励
        instance_reward = self.make_instance_rewards()
        if instance_reward:
            self.rewardBoxes.append(instance_reward)

        return self.rewardBoxes




    def fight(self, star, isWin):
        """
        战斗结算
        """
        # 普通副本
        data = {"star": 0}
        rewards = []
        hero_levelup_ids = []

        if isWin:

            data["star"] = star
            #　这都是继承自父类的方法


            golds = int(self.instancelevel.golds[0])
            woods = int(self.instancelevel.woods[0])
            hero_exp = int(self.instancelevel.heroExp[0])
            exp = self.instancelevel.playerExp

            #　随机的奖励在这里操作
            # 这个rewards 是具体要发到玩家身上的奖励
            rewards = self.make_rewards()

            if golds:
                rewards.append({"type":Static.GOLD_ID, "count":golds})
            if exp:
                rewards.append({"type":Static.XP_ID, "count":exp})
            if woods:
                rewards.append({"type":Static.WOOD_ID, "count":woods})

            # 根据上面的数据直接拿到奖励,然后发放
            for rewardDict in rewards:
                rewardTemp = CommonReward(rewardDict["type"], rewardDict["count"], 0)
                reward_send(self.player, rewardTemp, info=u"副本结算:%s" % self.level_id)


            for i in range(0, len(self.player.heroLayout)):
                playerhero = self.player.heroes.get(self.player.heroLayout[i])
                if playerhero.add_xp(hero_exp, self.player):
                    hero_levelup_ids.append(playerhero.id)
                self.player.update_hero(playerhero, True)


            self.add_count()
            self.success(star)


        data["rewards"] = rewards
        data["heroLevelUp"] = hero_levelup_ids
        return data

    def can_sweep(self):
        """
        是否可以扫荡
        """
        if self.star == 3:
            return True
        return False


    def sweep(self, count):
        """
        副本扫荡
        """
        rewards = []

        for i in range(0, count):
            exp = self.instancelevel.playerExp
            golds = int(self.instancelevel.golds[0])
            woods = int(self.instancelevel.golds[0])
            # 这里是＋＝　　还是＝　　待定
            # 增加挑战次数用的
            self.add_count()
            # 奖品的构成
            temp_list = self.make_rewards() + self.make_rewards_before_fight()
            self.rewardBoxes = []
            # 扫荡的奖励单独发放金币经验和木头
            temp_list.append({"type":Static.GOLD_ID, "count":golds})
            temp_list.append({"type":Static.XP_ID, "count":exp})
            temp_list.append({"type":Static.WOOD_ID, "count":woods})
            temp_list.append({"type":Static.ITEM_MIN_XP_ID, "count":1})
            rewards.append(temp_list)


        return rewards


#  和普通副本操作一样，具体流程参照普通副本
class PlayerEliteInstanceLevel(PlayerInstanceLevelBase):
    '''
    精英
    '''
    @memoized_property
    def eliteInstancelevel(self):
        # 这个level_id是父类的里面的的ｐｋ主键
        return get_eliteinstancelevel(self.level_id)

    @classmethod
    def unlock(cls, player, level_id) :
        """
        解锁关卡
        """
        _, playereliteinstancelevel = player.eliteinstancelevels.get_or_create(level_id)
        player.lastEliteInstance["lastEliteFinished"] = False
        player.lastEliteInstance["lastEliteLevelId"] = level_id
        player.set_update("lastEliteInstance")
        player.update_eliteinstancelevel(playereliteinstancelevel, True)
        return playereliteinstancelevel
    
    def success(self, star):
        """
        挑战成功
        """


        unlock_new_instance = False
        if star > self.star:
            self.star = star


        if self.level_id == self.player.lastEliteInstance["lastEliteLevelId"]:
            self.player.lastEliteInstance["lastEliteFinished"] = True
            self.player.set_update("lastEliteInstance")
            #有后续关卡
            if self.eliteInstancelevel.eliteNextInstanceId:
                next_eliteinstancelevel = get_eliteinstancelevel(self.eliteInstancelevel.eliteNextInstanceId)
                #开启同一章节关卡
                if self.eliteInstancelevel.instance_id == next_eliteinstancelevel.instance_id:
                    unlock_new_instance = PlayerEliteInstanceLevel.unlock(self.player, next_eliteinstancelevel.id)
                #开启下一章节关卡
                else:
                    #普通章节当前关卡已通关
                    if self.player.lastInstance["lastFinished"]:
                        unlock_new_instance = PlayerEliteInstanceLevel.unlock(self.player,next_eliteinstancelevel.id)

                    else:
                        instancelevel = get_instancelevel(self.player.lastInstance["lastLevelId"])
                        if instancelevel.instance_id > next_eliteinstancelevel.instance_id:
                            unlock_new_instance = PlayerEliteInstanceLevel.unlock(self.player,next_eliteinstancelevel.id)


        return unlock_new_instance

    def make_rewards(self):
        '''
        获取关卡的奖励
        '''
        
        rewards = []
        rewards_data = self.eliteInstancelevel.eliteRewardData
        max_player_count = self.eliteInstancelevel.eliteMaxPlayCount

        if self.succeedCount > max_player_count - len(rewards_data["mustId"]) and self.succeedCount <= max_player_count:
            rewardId = rewards_data["mustId"][max_player_count- self.succeedCount]

            if rewardId not in self.getRewardIds:
                index = rewards_data["type"].index(rewardId)
                rCount = rewards_data["count"][index]
                tempDict = {}
                tempDict["type"] = rewardId
                tempDict["count"] = rCount
                rewards.append(tempDict)
                self.getRewardIds.append(rewardId)

        x = 0
        for index, probability in enumerate(rewards_data["probability"]):
            x = probability * 1000000
            i = random.randint(1,1000000)
            if i < x:
                rewardId = rewards_data["type"][index]
                rCount = rewards_data["count"][index]
                tempDict = {}
                tempDict["type"] = rewardId
                tempDict["count"] = rCount
                rewards.append(tempDict)
                if rewardId not in self.getRewardIds:
                    self.getRewardIds.append(rewardId)

        instance_reward = self.make_elite_instance_rewards()
        if instance_reward:
            rewards.append(instance_reward)

        return rewards


    # 在战前就将礼物准备好，保存起来，战后直接加到身上
    def make_elite_rewards_before_fight(self):

        self.rewardBoxes = []

        eliteRewards_data = self.eliteInstancelevel.eliteRewardData
        # 这是每一个副本关具体的奖励
        x = 0
        for index, probability in enumerate(eliteRewards_data["probability"]):
            x = probability * 1000000
            i = random.randint(1,1000000)
            if i < x:
                rewardId = eliteRewards_data["type"][index]
                rCount = eliteRewards_data["count"][index]
                tempDict = {}
                tempDict["type"] = rewardId
                tempDict["count"] = rCount
                self.rewardBoxes.append(tempDict)
                if rewardId not in self.getRewardIds:
                    self.getRewardIds.append(rewardId)

        # 这是章节的随机奖励
        elite_instance_reward = self.make_elite_instance_rewards()
        if elite_instance_reward:
            self.rewardBoxes.append(elite_instance_reward)

        return self.rewardBoxes


    def fight(self, star, isWin):
        """
        战斗结算
        """
        # 精英副本

        data = {}
        rewards = []
        hero_levelup_ids = []
        data["star"] = 0

        if isWin:


            self.add_count()
            self.success(star)

            golds = self.eliteInstancelevel.eliteGold
            woods = self.eliteInstancelevel.elitewoods[0]
            hero_exp = self.eliteInstancelevel.eliteHeroExp
            exp = self.eliteInstancelevel.elitePlayerExp


            rewards = self.make_rewards()

            if golds:
                rewards.append({"type":Static.GOLD_ID, "count":golds})
            if woods:
                rewards.append({"type":Static.WOOD_ID, "count":woods})
            if exp:
                rewards.append({"type":Static.XP_ID, "count":exp})

            
            for rewardDict in rewards:
                rewardTemp = CommonReward(rewardDict["type"], rewardDict["count"], 0)
                reward_send(self.player, rewardTemp, info=u"精英副本结算:%s" % self.level_id)

            for i in range(0, len(self.player.heroLayout)):
                playerhero = self.player.heroes.get(self.player.heroLayout[i])
                if playerhero.add_xp(hero_exp, self.player):
                    hero_levelup_ids.append(playerhero.id)
                self.player.update_hero(playerhero, True)


        data["rewards"] = rewards
        data["heroLevelUp"] = hero_levelup_ids
        return data

    def can_sweep(self):
        """
        是否可以扫荡
        """
        if self.star == 3:
            return True
        return False

    def sweep(self, count):
        """
        副本扫荡
        """
        rewards = []
        golds = 0
        exp = 0
        hero_exp = 0
        for i in range(0, count):
            exp = self.eliteInstancelevel.elitePlayerExp
            golds = self.eliteInstancelevel.eliteGold

            woods = self.eliteInstancelevel.elitewoods[0]

            hero_exp += self.eliteInstancelevel.eliteHeroExp

            self.add_count()
            #self.success(player, level_id, 0)
            temp_list = []
            temp_list = self.make_rewards()
            temp_list.append({"type":Static.GOLD_ID, "count":golds})
            temp_list.append({"type":Static.WOOD_ID, "count":woods})
            temp_list.append({"type":Static.XP_ID, "count":exp})
            #todo 按照5个英雄计算，小经验药水一瓶60点，给英雄经验那么多的经验
            # item_count = 0
            # if i + 1 == count:
            #     item_count = hero_exp * 5/60
            #     if item_count * 60 < hero_exp * 5:
            #         item_count += 1
            temp_list.append({"type":Static.ITEM_MIN_XP_ID, "count":1})
            rewards.append(temp_list)

        return rewards


class PlayerRaidInstance(PlayerInstanceLevelBase):
    """
    关卡数据
    """
    def __unicode__(self):
        return u"%s-%s" % (self.id, self.level_id)

    @memoized_property
    def raidinstance(self):
        return get_raidinstance(self.level_id)
        
    def to_dict(self):
        dicts = super(PlayerRaidInstance, self).to_dict()
        return dicts
        
    def fight(self, raidlevel, isWin, percentage):
        '''
        活动副本结算
        '''
        #golds = 0
        exp = 0
        hero_exp = 0
        data = {}
        rewards = []
        hero_levelup_ids = []
        number = 1

        drop_count = (raidlevel.difficulty ** 2 *(percentage / (2 - percentage) + 0.1)) / 8.0
        exp = raidlevel.playerExp
        if exp:
            rewards.append({"type":Static.XP_ID, "count": int(exp * drop_count)})

        gold = raidlevel.gold
        if gold:
            rewards.append({"type":Static.GOLD_ID, "count": int(gold * drop_count)})

        hero_exp = int(raidlevel.heroExp * drop_count)
        self.add_count()

        rewards += self.make_rewards(raidlevel, percentage, isWin)
        if check_player_in_experiment_by_experimentname(self.player.id, self.raidinstance.experiment2):
            #双倍
            number = 2

        for i in range(0, len(self.player.heroLayout)):
            playerhero = self.player.heroes.get(self.player.heroLayout[i])
            if playerhero.add_xp(hero_exp, self.player):
                hero_levelup_ids.append(playerhero.id)
            self.player.update_hero(playerhero, True)


        data["rewards"] = rewards
        data["heroLevelUp"] = hero_levelup_ids
        data["number"] = number
        return data

    def make_rewards(self, raidlevel, percentage, isWin):
        '''
        获得活动副本奖励
        '''
        data = {}
        rewards = []
        data = raidlevel.rewardData
        x = 0
        if percentage == 100:
            if isWin:
                drop_count = 1
            else:
                drop_count = 0
        else:
            drop_count = raidlevel.difficulty ** 2 * (percentage / (2 - percentage)) / 8.0
        for index, probability in enumerate(data["probability"]):
            x = probability * 1000000
            i = random.randint(1,1000000)
            if i < x:
                rewardId = data["type"][index]
                rCount = random.uniform(data["minCount"][index], data["count"][index]+1)
                #rCount = data["count"][index]
                tempDict = {}
                tempDict["type"] = rewardId
                tempDict["count"] = int(round(rCount * drop_count + rCount * percentage))
                if  tempDict["count"] > 0:
                    rewards.append(tempDict)
        return rewards

class PlayerElementTower(PlayerRedisDataBase):
    """
    元素之塔
    """
    rewardCount = IntField(default=0) #通关塔赠送次数
    refreshCount = IntField(default=0) #免费刷新次数
    diamondCount = IntField(default=0) #钻石刷新次数
    towerId = IntField(default=0) #当前元素之塔ID
    star = IntField(default=0) #获得星星
    levelId = IntField(default=0) #当前元素之塔level
    levelStatus = IntField(default=0) #当前元素之塔level状态
    diamondBoxIndex = IntField(default=-1) #宝箱开启位置
    infos = DictField(default={}) #元素之塔信息 
    gold = IntField(default=0) #元素币
    buffs = DictField(default={})#buff数据
    tmpBuffs = ListField(default=[]) #可选择buff列表
    sweepInfo = DictField(default={})
    isSweep = BooleanField(default=False) #是否扫荡

    def load(self, player):
        super(self.__class__, self).load(player)

        now = datetime.datetime.now()
        if now.date() > self.updated_at.date():
            self.refreshCount = 0
            self.diamondCount = 0
            self.update() 
    
    def init(self):
        """
        刚开始创建默认刷新使用
        """
        self.refreshCount = 1
        self.update()
    
    def sub_star(self, star):
        """
        星星消耗
        """
        self.star -= star

    @property
    def refreshLeftCount(self):
        return 1 - self.refreshCount

    @property
    def diamondLeftCount(self):
        vip = get_vip(self.player.vip_level)
        leftCount = vip.timeGateCount - self.diamondCount
        return leftCount if leftCount > 0 else 0

    def reset(self, category):
        """
        重置
        """
        if category == 1:
            self.refreshCount += 1
        elif category == 2:
            self.rewardCount -= 1
        elif category == 3:
            self.diamondCount += 1

        self.towerId = 0
        self.levelId = 0
        self.levelStatus = 0
        self.star = 0
        self.diamondBoxIndex = 0
        self.isSweep = False
        self.buffs = {}
        self.update()


    def open(self, towerId):
        """
        开启
        """
        self.towerId = towerId
        self.levelId = 1
        self.levelStatus = 1
        self.star = 0
        self.diamondBoxIndex = 0
        self.isSweep = False
        self.buffs = {}
        self.sweepInfo = {
            "boxLevelIds": [],
            "buffLevelIds": [],
        }
        self.update()

    @property
    def tower(self):
        return get_elementtowerinstance(self.towerId)
    
    def fight(self, isWin, star):
        '''
        活动副本结算
        '''
        data = {}
        if isWin:
            tower = self.tower 
            self.star += star
            if str(self.towerId) not in self.infos:
                self.infos[str(self.towerId)] = []

            #第一次打到此level
            if len(self.infos[str(self.towerId)]) < self.levelId:
                self.infos[str(self.towerId)].append(star)
                if self.levelId >= len(tower.levels):
                    self.rewardCount += 1
            #设置最高星级
            else:
                if self.infos[str(self.towerId)][self.levelId - 1] < star:
                    self.infos[str(self.towerId)][self.levelId - 1] = star

            
            levelConf = tower.levels[self.levelId - 1]
            if self.levelId % 3 == 0:
                self.levelStatus = 2
                self.diamondBoxIndex = 0 #可以开0号宝箱
            else:
                self.levelStatus = 1
                self.levelId += 1

            data["rewards"] = levelConf.rewards[(star-1)*2:star*2]

            self.update()
        else:
            data["rewards"] = []

        return data

    def sweep(self):
        """
        扫荡
        """
        data = {
            "rewards": [],
            "freeBoxRewards": [],
        }
        tower = self.tower 
        towerLevelInfos = [] if str(self.towerId) not in self.infos else self.infos[str(self.towerId)]

        if self.levelId % 3 == 0 and self.boxCanOpen:
            #添加免费宝箱奖励 通三关但未开宝箱
            if self.diamondBoxIndex == 0:
                data["freeBoxRewards"].append(tower.levels[self.levelId - 1].diamondRewards[0])
                self.sweepInfo["boxLevelIds"].append([self.levelId, 1])
            else:
                self.sweepInfo["boxLevelIds"].append([self.levelId, self.diamondBoxIndex])

        buffs = get_elementtowerbuffs()
        if self.levelId % 3 == 0 and (self.boxCanOpen or self.buffCanChoice):
            _buffIds = []
            for i in range(0, 3):
                tmpBuff = random.choice(buffs)
                _buffIds.append(tmpBuff.pk)
            self.sweepInfo["buffLevelIds"].append((self.levelId, _buffIds))
        #排除遗落的箱子
        if self.boxCanOpen or self.buffCanChoice:
            if self.levelId < len(tower.levels):
                self.levelId += 1
                self.levelStatus = 1

        for index, levelStar in enumerate(towerLevelInfos[self.levelId-1:]):
            #非3星通关自动退出
            if levelStar < 3:
                break
            levelConf = tower.levels[self.levelId - 1]
            
            #每关固定奖励
            data["rewards"].append(levelConf.rewards[4:6])
            self.isSweep = True #扫荡成功
            #记住要刷新的宝箱和buff
            if self.levelId % 3 == 0:
                self.sweepInfo["boxLevelIds"].append([self.levelId, 1])
                data["freeBoxRewards"].append(tower.levels[self.levelId - 1].diamondRewards[0])
                if self.levelId < len(tower.levels):
                    _buffIds = []
                    for i in range(0, 3):
                        tmpBuff = random.choice(buffs)
                        _buffIds.append(tmpBuff.pk)
                    self.sweepInfo["buffLevelIds"].append((self.levelId, _buffIds))
                else:
                    self.levelStatus = 4 #通关
                    self.sweepInfo["buffLevelIds"] = []
                    break

            self.levelId += 1
            self.star += 3
            self.levelStatus = 1
        self.update()
        return data

    def openDiamondBox(self, status):
        rewards = []
        tower = self.tower
        if status:
            rewards.append(tower.levels[self.levelId - 1].diamondRewards[self.diamondBoxIndex])
            #存在下一个宝箱
            if self.diamondBoxIndex + 1 < len(tower.levels[self.levelId - 1].diamondRewards):
                self.diamondBoxIndex += 1
            #宝箱开启完
            else:
                #存在下一关
                if self.levelId < len(tower.levels):
                    #开始选择BUFF
                    self.levelStatus = 3
                    self._initTmpBuffs()
                else:
                    #通关
                    self.levelStatus = 4
        else:
            #存在下一关
            if self.levelId < len(tower.levels):
                #开始选择BUFF
                self.levelStatus = 3
                self._initTmpBuffs()
            else:
                #通关
                self.levelStatus = 4

        self.update()
        return rewards

    def openSweepDiamondBox(self, status, category, levelId):
        """
        开启扫到中的宝箱
        """
        rewards = []
        delBox = []
        tower = self.tower
        #开启
        if status:
            if category == 1:
                #开启一个宝箱
                for _i, [level, box] in enumerate(self.sweepInfo["boxLevelIds"]):
                    if level == levelId:
                        rewards.append(tower.levels[level - 1].diamondRewards[box])
                        box += 1
                        #存在下一个宝箱
                        if box < len(tower.levels[level - 1].diamondRewards):
                            self.sweepInfo["boxLevelIds"][_i] = [level, box]
                        else:
                            delBox.append(_i)
                    else:
                        continue
            elif category == 2:
                #全部开启一个
                for _i, [level, box] in enumerate(self.sweepInfo["boxLevelIds"]):
                    rewards.append(tower.levels[level - 1].diamondRewards[box])
                    box += 1
                    if box < len(tower.levels[level - 1].diamondRewards):
                        self.sweepInfo["boxLevelIds"][_i] = [level, box]
                    else:
                        delBox.append(_i)
            elif category == 3:
                #全部开启
                for _i, [level, box] in enumerate(self.sweepInfo["boxLevelIds"]):
                    while True:
                        rewards.append(tower.levels[level - 1].diamondRewards[box])
                        box += 1
                        if box < len(tower.levels[level - 1].diamondRewards):
                            self.sweepInfo["boxLevelIds"][_i] = [level, box]
                        else:
                            break
                self.sweepInfo["boxLevelIds"] = []  

            #删除开完的箱子
            delBox.reverse()
            for i in delBox:
                self.sweepInfo["boxLevelIds"].pop(i)
        #放弃所有付费宝箱
        else:
            self.sweepInfo["boxLevelIds"] = []
        self.update()
        return rewards

    def openSweepDiamondBoxCost(self, category, levelId):
        """
        开启钻石宝箱的花费计算
        """
        cost = 0
        tower = self.tower
        if category == 1:
            #开启一个宝箱
            for level, box in self.sweepInfo["boxLevelIds"]:
                if level == levelId:
                    cost = tower.levels[level - 1].diamondCosts[box]
                    break
                else:
                    continue
        elif category == 2:
            #全部开启一个
            for level, box in self.sweepInfo["boxLevelIds"]:
                cost += tower.levels[level - 1].diamondCosts[box]
        elif category == 3:
            #全部开启
            boxes = self.sweepInfo["boxLevelIds"][:]
            for _i, [level, box] in enumerate(boxes):
                while True:
                    cost += tower.levels[level - 1].diamondCosts[box]
                    box += 1
                    if box < len(tower.levels[level - 1].diamondRewards):
                        boxes[_i] = [level, box]
                    else:
                        break
        return cost

    def _initTmpBuffs(self):
        """
        初始化buff数据
        """
        buffs = get_elementtowerbuffs()
        self.tmpBuffs = []
        for i in range(0, 3):
            tmpBuff = random.choice(buffs)
            self.tmpBuffs.append(tmpBuff.pk)

    def choiceBuff(self, index):
        """
        选择buff
        """

        if 0 not in index :
            for i in index:
                buff = get_elementtowerbuff(self.tmpBuffs[i-1])
                for attrType,extras in buff.attrs:
                    if attrType not in self.buffs:
                        self.buffs[attrType] = 0
                    self.buffs[attrType] += extras[i-1]

        tower = self.tower
        if self.levelId < len(tower.levels):
            self.levelId += 1
            self.levelStatus = 1

        self.update()

    def choiceSweepBuff(self, index):
        """
        选择扫荡buff
        """
        
        if 0 not in index:
            levelId = self.sweepInfo["buffLevelIds"][0][0]
            buffIds = self.sweepInfo["buffLevelIds"][0][1]
            for i in index:
                buff = get_elementtowerbuff(buffIds[i-1])
                for attrType,extras in buff.attrs:
                    if attrType not in self.buffs:
                        self.buffs[attrType] = 0
                    self.buffs[attrType] += extras[i-1]
        self._initTmpBuffs()
        self.sweepInfo["buffLevelIds"].pop(0)
        self.update()

    @property
    def levelIsOpen(self):
        return self.levelStatus == 1

    @property
    def boxCanOpen(self):
        return self.levelStatus == 2

    @property
    def buffCanChoice(self):
        return self.levelStatus == 3

    @property
    def diamondResetCost(self):
        """
        花钱重置消耗
        """
        if self.diamondCount == 0:
            return 200
        elif self.diamondCount == 1:
            return 400
        else:
            return 1000 #以防万一

   

    @property
    def isInSweep(self):
        """
        是否处于扫荡状态中
        """
        return ("boxLevelIds" in self.sweepInfo and len(self.sweepInfo["boxLevelIds"]) > 0 ) or ("buffLevelIds" in self.sweepInfo and len(self.sweepInfo["buffLevelIds"]) > 0)

    def to_dict(self):
        dicts = {}
        dicts["rewardLeftCount"] = self.rewardCount
        dicts["refreshLeftCount"] = self.refreshLeftCount
        dicts["diamondCount"] = self.diamondCount
        dicts["towerId"] = self.towerId
        dicts["levelId"] = self.levelId
        dicts["levelStatus"] = self.levelStatus
        dicts["levelStars"] = [] if str(self.towerId) not in self.infos else self.infos[str(self.towerId)]
        dicts["diamondResetCost"] = self.diamondResetCost
        dicts["diamondBoxIndex"] = self.diamondBoxIndex
        dicts["isSweep"] = self.isSweep
        dicts["gold"] = self.gold
        dicts["star"] = self.star
        dicts["buffs"] = [] 
        buffs = self.buffs
        for attrType, extra in buffs.items():
            dicts["buffs"].append({
                "attrType": attrType,
                "extra":extra 
            })

        dicts["tmpBuffs"] = self.tmpBuffs

        dicts["sweepInfo"] = {}

        if  "boxLevelIds" in self.sweepInfo and len(self.sweepInfo["boxLevelIds"]) > 0:
            dicts["sweepInfo"]["status"] = 1
            dicts["sweepInfo"]["boxLevelIds"] = self.sweepInfo["boxLevelIds"]
        elif  "buffLevelIds" in self.sweepInfo and len(self.sweepInfo["buffLevelIds"]) > 0:
            dicts["sweepInfo"]["status"] = 2
            #dicts["sweepInfo"]["levelId"] = self.sweepInfo["buffLevelIds"][0][0]
            #dicts["sweepInfo"]["buffs"] = self.sweepInfo["buffLevelIds"][0][1]

        return dicts


