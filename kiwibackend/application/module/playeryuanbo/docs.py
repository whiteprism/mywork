# -*- coding: utf-8 -*-
import datetime
from mongoengine import *
from common.docs import PlayerDataBase, PlayerRelationBase, PlayerRedisDataBase

class PlayerYuanboShop(PlayerRedisDataBase):
    """
    玩家元宝
    """
    yuanbos = DictField(default={})

    def is_first_buy(self, yuanbo_id):
        return str(yuanbo_id) not in self.yuanbos

    def buy(self, yuanbo_id):
        yuanbo_id = str(yuanbo_id)
        if yuanbo_id not in self.yuanbos:
            self.yuanbos[yuanbo_id] = {"count": 0, "lastTime": None}
        self.yuanbos[yuanbo_id]["count"] += 1
        self.yuanbos[yuanbo_id]["lastTime"] = datetime.datetime.now()
        self.update()

    def to_dict(self):
        return [int(i) for i in self.yuanbos.keys()]

class PlayerYuanboLog(PlayerDataBase):
    amount = IntField()
    type = IntField(default = 1)
    info = StringField(default = '')
    serverid = IntField(default = 0)
    meta = {
        'indexes': ["serverid"],
        'shard_key': ["serverid"],
    }

class PurchaseOrder(Document):
    """
    支付订单号
    """
    order_id = StringField(primary_key=True)
    yuanbo_id = IntField()
    player_id = LongField()  #玩家id
    osuser_id = StringField(default="")
    notify_data = StringField(default="")
    status = IntField(default=0)
    is_first = BooleanField(default=False)
    yuanbo = IntField(default=0)
    plat_order_id = StringField(default="")
    channel = StringField(default="")
    created_at = DateTimeField(default = datetime.datetime.now)  #作成日時
    updated_at = DateTimeField()
    serverid = IntField(default=0)
    price = IntField(default=0)

    meta = {
        'indexes': ["serverid", "plat_order_id"],
        'shard_key': ["serverid"],
    }

    @property
    def is_waiting(self):
        return self.status == 0

    @property
    def is_success(self):
        return self.status == 1

    def success(self):
        self.status = 1

    @property
    def is_failure(self):
        return self.status == 2

    def failure(self):
        self.status = 2

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        super(PurchaseOrder, self).save(*args, **kwargs)

    def to_dict(self):
        _dict = {}
        _dict["orderId"] = self.order_id
        _dict["yuanboId"] = self.yuanbo_id
        _dict["playerId"] = self.player_id
        _dict["osuserId"] = self.osuser_id
        _dict["notifyData"] = self.notify_data
        _dict["status"] = self.status
        _dict["yuanbo"] = self.yuanbo
        _dict["platOrderId"] = self.plat_order_id
        _dict["channel"] = self.channel
        _dict["createAt"] = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        _dict["finishAt"] = self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        _dict["serverId"] = self.serverid
        _dict["price"] = self.price

        return _dict
