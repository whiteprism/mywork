# -*- coding: utf-8 -*-
from mongoengine import *
from common.docs import PlayerRedisDataBase
from common.decorators.memoized_property import memoized_property
from module.gashapon.api import get_gashapon
from gashapon.models import Gashapon
from playerhero.api import acquire_hero
from playerequip.api import acquire_equip, acquire_equipfragment
from playeritem.api import acquire_item
from playerartifact.api import acquire_artifactfragment
from soul.api import get_soul
from module.playerhero.docs import PlayerHero
from playersoul.api import acquire_soul
import copy
import random
from common.static import Static

class PlayerGashapon(PlayerRedisDataBase):
    """
    用户抽奖
    """
    gashapon_id = IntField()
    count = IntField(default=0)
    #抽到英雄重置计数
    #topreward_count = IntField(default=0)
    #抽到史诗英雄重置十连抽次数
    topreward_count = IntField(default=0)

    def __unicode__(self):
        return u"%s:%s(%s)" %(self.id, self.gashapon_id, self.count)

    @memoized_property
    def gashapon(self):
        return get_gashapon(self.gashapon_id)

    # def acquire(self, player, gashapon, count=1):
    #     """
    #     玩家抽奖
    #     [(unit, is_new),(unit, is_new)]
    #     """

    #     data_list = []
    #     for i in range(1, count + 1):

    #         #if (player.tenDiamondCount + 1) % 10 == 0:
    #         if gashapon.topreward_number and self.topreward_count2 + 1 >= gashapon.topreward_number * 10:
    #             rarity = Gashapon.get_random_rarity(gashapon, rarity=gashapon.topreward_rarity, quality=gashapon.topreward_quality)
    #             target = Gashapon.get_random_target(gashapon, rarity)
    #             #player.tenDiamondCount += 1
    #             #player.set_update("tenDiamondCount")


    #         elif gashapon.topreward_number and self.topreward_count + 1 >= gashapon.topreward_number:
    #             rarity = Gashapon.get_random_rarity(gashapon, rarity=gashapon.topreward_rarity, quality=0)
    #             target = Gashapon.get_random_target(gashapon, rarity)
    #         else:
    #             rarity = Gashapon.get_random_rarity(gashapon)
    #             target = Gashapon.get_random_target(gashapon, rarity)



    #         info = u"%s" %(gashapon.name)
    #         if target.gashapon_hero:
    #             # if player.firstIn == 0 and target.target_id in Static.HERO_INIT_ACQUIRE:
    #             #     target.target_id =random.choice(Static.HERO_REPLACE_IDS)
    #             #     player.firstIn = 2
    #             # 直接抽出高星级的英雄
    #             # 和策划约定好后两位代表星级。
    #             star = int(str(target.target_id)[-2:])
    #             new_id = target.target_id / 100 * 100

    #             unit = acquire_hero(player, new_id, info=info, star=star)
    #         elif target.gashapon_soul:
    #             unit = acquire_soul(player, target.target_id, target.number, info=info)
    #         elif target.gashapon_equip:
    #             unit = acquire_equip(player, target.target_id, info=info)
    #         elif target.gashapon_item:
    #             unit = acquire_item(player, target.target_id, number=target.number, info=info)
    #         elif target.gashapon_artifactfragment:
    #             unit = acquire_artifactfragment(player, target.target_id, number=target.number, info=info)
    #         elif target.gashapon_equipfragment:
    #             unit = acquire_equipfragment(player, target.target_id, target.number, info=info)
    #         elif target.gashapon_currency:
    #             if target.is_yuanbo:
    #                 player.add_yuanbo(target.number, info=info)
    #                 unit = target
    #             else:
    #                 raise
    #         else:
    #             raise


    #         unit = copy.copy(unit)


    #         if target.gashapon_hero:
    #             if isinstance(unit, PlayerHero):
    #                 unit.gashapon_number = target.number
    #             else:
    #                 soul = get_soul(unit.soul_id)
    #                 unit.gashapon_number = soul.breakCost
    #                 unit.from_hero = True
    #         else:
    #             unit.gashapon_number = target.number

    #         self.count += 1
    #         if gashapon.topreward_number:
    #             self.topreward_count += 1
    #             if self.topreward_count >= gashapon.topreward_number:
    #                 self.topreward_count = 0
    #             else:
    #                 if gashapon.topreward_reset:
    #                 #     if gashapon.topreward_rarity and gashapon.topreward_quality:
    #                 #         if rarity.rarity == gashapon.topreward_rarity and rarity.quality == gashapon.topreward_quality:
    #                 #             self.topreward_count = 0
    #                 #     elif gashapon.topreward_rarity:
    #                 #         if rarity.rarity == gashapon.topreward_rarity:
    #                 #             self.topreward_count = 0
    #                 #     elif gashapon.topreward_quality:
    #                 #         if rarity.quality == gashapon.topreward_quality:
    #                 #             self.topreward_count = 0

    #                     if gashapon.topreward_rarity:
    #                         if rarity.rarity == gashapon.topreward_rarity:
    #                             self.topreward_count = 0
    #                     elif gashapon.topreward_quality:
    #                         if rarity.quality == gashapon.topreward_quality:
    #                             self.topreward_count = 0

    #                     if gashapon.topreward_rarity and gashapon.topreward_quality:
    #                         if rarity.rarity == gashapon.topreward_rarity and rarity.quality == gashapon.topreward_quality:
    #                             self.topreward_count2 = 0
    #         data_list.append(unit)

    #     return data_list

    def acquire(self, player, gashapon, count=1):
        """
        玩家抽奖
        [(unit, is_new),(unit, is_new)]
        """
        choices_list = []
        data_list = []
        super_hero = False
        include_hero = False

        for i in range(1, count + 1):
            rarity = Gashapon.get_random_rarity(gashapon)
            target = Gashapon.get_random_target(gashapon, rarity)
            target.rarit = rarity
            data_list.append(target)

        print data_list
        if count == 10:
            self.topreward_count += 1
            if self.topreward_count == 10:
                for data in data_list:
                    print data
                    if data.rarit.rarity == gashapon.topreward_rarity and data.rarit.quality == gashapon.topreward_quality:
                        super_hero = True
                        break
                if not super_hero:
                    rarity = Gashapon.get_random_rarity(gashapon, rarity=gashapon.topreward_rarity, quality=gashapon.topreward_quality)
                    target = Gashapon.get_random_target(gashapon, rarity)
                    target.rarit = rarity
                    rand = random.randint(0,len(data_list) - 1)
                    data_list[rand] = target

            for data in data_list:
                if data.gashapon_hero:
                    include_hero = True
                    break

            if not include_hero:
                rarity = Gashapon.get_random_rarity(gashapon, rarity=gashapon.topreward_rarity, quality=0)
                target = Gashapon.get_random_target(gashapon, rarity)
                target.rarit = rarity
                rand = random.randint(0,len(data_list) - 1)
                data_list[rand] = target


        for target in data_list:
            info = u"%s" %(gashapon.name)
            if target.gashapon_hero:
                # if player.firstIn == 0 and target.target_id in Static.HERO_INIT_ACQUIRE:
                #     target.target_id =random.choice(Static.HERO_REPLACE_IDS)
                #     player.firstIn = 2
                # 直接抽出高星级的英雄
                # 和策划约定好后两位代表星级。
                star = int(str(target.target_id)[-2:])
                new_id = target.target_id / 100 * 100

                unit = acquire_hero(player, new_id, info=info, star=star)
            elif target.gashapon_soul:
                unit = acquire_soul(player, target.target_id, target.number, info=info)
            elif target.gashapon_equip:
                unit = acquire_equip(player, target.target_id, info=info)
            elif target.gashapon_item:
                unit = acquire_item(player, target.target_id, number=target.number, info=info)
            elif target.gashapon_artifactfragment:
                unit = acquire_artifactfragment(player, target.target_id, number=target.number, info=info)
            elif target.gashapon_equipfragment:
                unit = acquire_equipfragment(player, target.target_id, target.number, info=info)
            elif target.gashapon_currency:
                if target.is_yuanbo:
                    player.add_yuanbo(target.number, info=info)
                    unit = target
                else:
                    raise
            else:
                raise

            unit = copy.copy(unit)

            if target.gashapon_hero:
                if isinstance(unit, PlayerHero):
                    unit.gashapon_number = target.number
                else:
                    soul = get_soul(unit.soul_id)
                    unit.gashapon_number = soul.breakCost
                    unit.from_hero = True
            else:
                unit.gashapon_number = target.number

            self.count += 1

            if gashapon.topreward_reset:
                if gashapon.topreward_rarity and gashapon.topreward_quality:
                    if target.rarit.rarity == gashapon.topreward_rarity and target.rarit.quality == gashapon.topreward_quality:
                        self.topreward_count = 0

            choices_list.append(unit)

        return choices_list
