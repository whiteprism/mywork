# -*- coding: utf-8 -*-
from mongoengine import *
from common.docs import PlayerDataBase
from common.decorators.memoized_property import memoized_property
from module.item.api import get_item
import datetime
from utils import datetime_to_unixtime


class PlayerBattleRecords(PlayerDataBase):
    """
    战斗记录
    """

    isWin = BooleanField()
    category = IntField(default = 0) # 1 竞技场 2 攻城战
    # playerScore = IntField(default = 0)
    # targetPlayerScore = IntField(default = 0)
    # playerRank = IntField(default = 0)
    # targetPlayerRank = IntField(default = 0)
    addScore = IntField(default = 0)
    # targetPlayerId = IntField(default = 0)
    # playerIcon = IntField(default = 0)
    # targetPlayerIcon = IntField(default = 0)
    # playerVip = IntField(default = 0)
    # targetPlayerVip = IntField(default = 0)
    # #----------------------------------------
    # # 目前只有攻城战用上的字段
    # playerGuildName = StringField(default = "")
    # targetGuildName = StringField(default = "")
    # playerHeroes = ListField(default=[]) # [{"heroId": x, "level": x, "star": x, "upgrade": x}, ]
    # targetHeroes = ListField(default=[]) # [{"heroId": x, "level": x, "star": x, "upgrade": x}, ]
    # playerSoldiers = ListField(default=[]) # [{"soldierId": x, "soldierLevel": x, "count": x}, ]
    # targetSoldiers = ListField(default=[]) # [{"soldierId": x, "soldierLevel": x, "count": x}, ]
    playerPvpRank = DictField(default = {})
    targetPvpRank = DictField(default = {})
    playerPowerRank = IntField(default = 0)
    targetPowerRank  = IntField(default = 0)
    playerHeroes = DictField(default = {})
    targetHeroes = DictField(default = {})
    playerSimple = DictField(default = {})
    targetSimple = DictField(default = {})
    playerWallSoldiers = ListField(default=[])
    targetWallSoldiers = ListField(default=[])

    resource = DictField(default={}) # {"wood": x, "gold": x, "arrivalTime": x}
    #++++++++++++++++++++++++++++++++++++++++


    meta = {
        'ordering': ["-id"],
        "indexes": ["player_id"],
        'shard_key': ["player_id"], 
    }
    @memoized_property
    def targetPlayer(self):
        from module.player.api import get_player
        targetPlayer = get_player(self.targetPlayerId, False)
        return targetPlayer

    @memoized_property
    def player(self):
        from module.player.api import get_player
        player =  get_player(self.player_id, False)
        return player

    def to_dict(self):
        dicts = super(PlayerBattleRecords, self).to_dict()
        # dicts["targetPlayer"] = self.sender
        return dicts
