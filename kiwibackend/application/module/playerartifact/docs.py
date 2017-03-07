# -*- coding: utf-8 -*-
from mongoengine import *
from common.docs import PlayerDataBase, PlayerRedisDataBase, PlayerRedisDataListBase
from common.decorators.memoized_property import memoized_property
from module.artifact.api import get_artifact, get_artifactenhance, get_artifactrefine, get_artifactfragment
from module.common.actionlog import ActionLogWriter
from django.conf import settings
from module.utils import random_item_pick 

class PlayerArtifact(PlayerRedisDataBase):
    """
    用户圣物
    """
    artifact_id = IntField() #圣物ID
    playerhero_id = LongField(default=0) #英雄
    level = IntField(default=1) #level
    refineLevel = IntField(default=0)
    xp = IntField(default=0)
    skillId = IntField(default=0)#圣物所带的技能Id

    def __unicode__(self):
        return u"%s:%s(%s)" %(self.id, self.artifact_id, self.level)

    @memoized_property
    def artifact(self):
        return get_artifact(self.artifact_id)
    
    # @memoized_property
    # def equip(self):
    #     return get_artifact(self.artifact_id)

    @property
    def obj_id(self):
        return self.artifact_id

    def level_up(self, xps):
        """
        升级
        """
        self.xp += int(xps)
        before_level = self.level
        while True:
            artifactenhance = get_artifactenhance(self.artifact.quality, self.level)
            next_artifactenhance = get_artifactenhance(self.artifact.quality, self.level + 1)
            if not next_artifactenhance:
                if self.xp > artifactenhance.xp:
                    self.xp = artifactenhance.xp
                break
            else:
                if artifactenhance.playerLevel > self.player.level:
                    self.xp = artifactenhance.xp if self.xp >= artifactenhance.xp else self.xp
                    break
                if artifactenhance.xp > self.xp:
                    break
                self.level += 1
                self.xp -= artifactenhance.xp
        info = u"圣物强化:%s" % self.pk
        ActionLogWriter.artifact_levelup(self.player, self, before_level, self.level, info)
        return self.level - before_level

    @property
    def is_weared(self):
        """
        检查精炼材料是否是穿戴的状态
        """
        return self.playerhero_id > 0

    def refine(self):
        """
        精炼
        """
        info = u'圣物精炼'
        before_refineLevel = self.refineLevel
        self.refineLevel += 1
        ActionLogWriter.artifact_refine(self.player, self, before_refineLevel, self.refineLevel, info)

    @property
    def can_melt(self):
        return not (self.level == 1 and self.refineLevel == 0)

    def melt(self):
        self.level = 1
        self.refineLevel = 0
        self.xp = 0

    def get_random_skill(self, artifact):
        skill, _ = random_item_pick(artifact.skillIds)
        self.skillId = skill

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["artifactId"] = self.artifact_id
        dicts["heroId"] = self.playerhero_id
        del dicts["artifact_id"]
        del dicts["playerhero_id"]
        return dicts

class PlayerArtifactFragment(PlayerRedisDataListBase):
    """
    用户圣物碎片
    """
    @memoized_property
    def artifactfragment(self):
        return get_artifactfragment(self.artifactfragment_id)

    @property
    def artifactfragment_id(self):
        return self.obj_id

    @property
    def is_artifactfragment(self):
        return True
        
    def sub(self,delta_number=1, info=u""):
        """
        使用圣物碎片
        """
        before_number = self.count
        self.count -= delta_number
        if self.display:
            self.player.update_artifactfragment(self, True)
        else:
            self.player.delete_artifactfragment(self.artifactfragment_id, True)

        ActionLogWriter.artifactfragment_cost(self.player, self.artifactfragment, before_number, self.count, info)

    def add(self,delta_number=1, info=u""):
        before_number = self.count
        self.count += delta_number
        after_number = self.count

    def to_dict(self):
        dicts = super(self.__class__, self).to_dict()
        dicts["artifactFragmentId"] = self.obj_id
        return dicts
