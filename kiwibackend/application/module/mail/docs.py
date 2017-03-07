# -*- coding: utf-8 -*-
from mongoengine import *
from common.docs import PlayerDataBase
from common.decorators.memoized_property import memoized_property
from module.item.api import get_item
import datetime
from utils import datetime_to_unixtime


class PlayerMail(PlayerDataBase):
    """
    用户邮件
    """
    status = IntField(default = 0)  #状态
    title = StringField(default="") #标题
    sender_id = LongField(default=0) #0为系统发送
    playerName = StringField(default="") #名字1
    senderName = StringField(default="") #名字2
    attachments = ListField(default=[]) #奖励
    contents = ListField(default=[])
    category = IntField(default=0)   #系统1 进攻2 防守3
    playback = DictField()
    isWin = BooleanField()
    mailType = IntField()

    meta = {
        'ordering': ["-id"],
        'indexes': ["player_id", ('player_id','status')],
        'shard_key': ["player_id"],
    }


    @property
    def is_system(self):
        return self.category == 1

    @property
    def sender(self):
        if self.sender_id != 0:
            from module.player.api import get_player
            sender = get_player(self.sender_id, False)
            return sender.userSimple_dict()
        else:
            return {}

    @property
    def is_new(self):
        return self.status == 0

    @property
    def is_read(self):
        return self.status == 1

    def set_is_read(self):
        self.status = 1

    def pass_day(self, day=7):
        now = datetime.datetime.now()
        delta_time = now - self.updated_at
        if delta_time.days >= day:
            return True
        return False

    @property
    def is_timeout(self):
        if (self.is_system and self.is_accept) or not self.is_system:
            if self.pass_day(3):
                return True
        else:
            if self.pass_day(30):
                return True
        return False

    @property
    def is_accept(self):
        if self.is_system:
            if (self.status == 2 or len(self.attachments) == 0):
                return True
            else:
                return False
        return True


    def set_is_accept(self):
        self.status = 2

    def to_dict(self):
        dicts = super(PlayerMail, self).to_dict()
        dicts["createdAt"] = int(datetime_to_unixtime(self.created_at))
        dicts["updatedAt"] = self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        dicts["sender"] = self.sender
        del dicts["sender_id"]
        return dicts
