# -*- coding: utf-8 -*-

from django.conf import settings
from module.common.decorators.except_mail_admins import except_mail_admins
import datetime
import logging
logger = logging.getLogger("actions")

class ActionLogWriter(object):
    """
    日志自定义类
    """

    @classmethod
    def send_message(cls, category1, category2, player_id, message, user_id):
        server_id = settings.SERVERID
        message = str(message)
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_str = "\t".join([str(server_id), str(user_id), str(player_id), str(category1), str(category2), message, created_at])

        logger.info(log_str)

    # ---- PLAYER ----
    @classmethod
    def player_levelup(cls, player, before_level, after_level, add_xp, info):
        message = {
            'before': before_level,
            'after': after_level,
            'add_xp': add_xp,
            'info': info,
        }
        cls.send_message("PLAYER", "levelup", player.pk, message, player.userid)

    # ---- HERO ----
    @classmethod
    def hero_acquire(cls, player, player_hero_id, hero_id, card_id, info):
        message = {
            'card_id': card_id,
            'hero_id': hero_id,
            'player_hero_id': player_hero_id,
            'info': info,
        }
        cls.send_message("HERO", "acquire", player.pk, message, player.userid)

    @classmethod
    def hero_levelup(cls, player, player_hero_id, hero_id, card_id, before_level, after_level, xp, info):
        message = {
            'card_id': card_id,
            'hero_id': hero_id,
            'player_hero_id': player_hero_id,
            'before': before_level,
            'after': after_level,
            'xp': xp,
            'info': info,
        }
        cls.send_message('HERO', "levelup", player.pk, message, player.userid)

    @classmethod #没用
    def hero_reset(cls, player, player_hero_id, hero_id, card_id, level, xp, star, info):
        message = {
            'card_id': card_id,
            'hero_id': hero_id,
            'player_hero_id': player_hero_id,
            'level': level,
            'xp': xp,
            'star': star,
            'info': info,
        }
        cls.send_message('HERO', "reset", player.pk, message, player.userid)

    @classmethod
    def hero_evolve(cls, player, player_hero_id, hero_id, next_hero_id, star, next_star, card_id, info):
        message = {
            'card_id': card_id,
            'hero_id': hero_id,
            'next_hero_id': next_hero_id,
            'star': star,
            'next_star': next_star,
            'player_hero_id': player_hero_id,
            'info': info,
        }
        cls.send_message('HERO', "evolve", player.pk, message, player.userid)

    @classmethod
    def hero_skilllevelup(cls, player, player_hero_id, hero_id, pos, skill_id ,before_level, after_level, card_id, info):
        message = {
            'card_id': card_id,
            'hero_id': hero_id,
            'pos': pos,
            'skill_id': skill_id,
            'before': before_level,
            'after': after_level,
            'player_hero_id': player_hero_id,
            'info': info,
        }
        cls.send_message('HERO', "killlevelup", player.pk, message, player.userid)

    @classmethod
    def hero_stargrade(cls, player, player_hero_id, hero_id, before_star, after_star, info):
        message = {
            'before': before_star,
            'after': after_star,
            'hero_id': hero_id,
            'player_hero_id': player_hero_id,
            'info': info,
        }
        cls.send_message('HERO', "stargrade", player.pk, message, player.userid)

    @classmethod
    def hero_destiny(cls, player, player_hero_id, hero_id, before_destiny, after_destiny, info):
        message = {
            'before': before_destiny,
            'after': after_destiny,
            'hero_id': hero_id,
            'player_hero_id': player_hero_id,
            'info': info,
        }
        cls.send_message('HERO', "destiny", player.pk, message, player.userid)
    # ---- SOUL ----
    @classmethod
    def soul_add(cls, player, soul_id, before_number, after_number, info):
        message = {
            'soul_id': soul_id,
            'before': before_number,
            'after': after_number,
            'info': info,
        }
        cls.send_message('SOUL', "add", player.pk, message, player.userid)

    @classmethod
    def soul_cost(cls, player, soul_id, before_number, after_number, info):
        message = {
            'soul_id': soul_id,
            'before': before_number,
            'after': after_number,
            'info': info,
        }
        cls.send_message('SOUL', "cost", player.pk, message, player.userid)
    # ---- ITEM ----
    @classmethod
    def item_acquire(cls, player, item_id, before_number, after_number, info):
        message = {
            'item_id': item_id,
            'before': before_number,
            'after': after_number,
            'info': info,
        }
        cls.send_message('ITEM', "acquire", player.pk, message, player.userid)

    @classmethod
    def item_cost(cls, player, item_id, before_number, after_number, info):
        message = {
            'item_id': item_id,
            'before': before_number,
            'after': after_number,
            'info': info,
        }
        cls.send_message('ITEM', "cost", player.pk, message, player.userid)

    @classmethod
    def item_goldhand(cls, player, money, before_gold, after_gold, info):
        message = {
            'money': money,
            'before': before_gold,
            'after': after_gold,
            'info': info,
        }

        cls.send_message('ITEM', "goldhand", player.pk, message, player.userid)

    @classmethod
    def item_woodhand(cls, player, wood, before_wood, after_wod, info):
        message = {
            'wood': wood,
            'before': before_wood,
            'after': after_wod,
            'info': info,
        }

        cls.send_message('ITEM', "woodhand", player.pk, message, player.userid)

    @classmethod
    def item_buyrecord(cls, player, item_id, before_number, after_number, totalcount, info):
        message = {
            'item_id': item_id,
            'before': before_number,
            'after': after_number,
            'totalcount': totalcount,
            'info': info,
        }

        cls.send_message('ITEM', "buyrecord", player.pk, message, player.userid)

    @classmethod
    def item_buytowerrecord(cls, player, item_id, before_number, after_number, totalcount, info):
        message = {
            'item_id': item_id,
            'before': before_number,
            'after': after_number,
            'totalcount': totalcount,
            'info': info,
        }

        cls.send_message('ITEM', "buyrecord", player.pk, message, player.userid)

    # ---- EQUIP ----
    @classmethod
    def equip_acquire(cls, player, player_equip_id, equip_id, info):
        message = {
            'equip_id': equip_id,
            'player_equip_id': player_equip_id,
            'info': info,
        }

        cls.send_message('EQUIP', "acquire", player.pk, message, player.userid)

    @classmethod
    def equip_delete(cls, player, player_equip_id, equip_id, info):
        message = {
            'equip_id': equip_id,
            'player_equip_id': player_equip_id,
            'info': info,
        }

        cls.send_message('EQUIP', "delete", player.pk, message, player.userid)

    @classmethod
    def equip_enhance(cls, player, player_equip_id, equip_id, before_level, after_level, info):
        message = {
            'equip_id': equip_id,
            'player_equip_id': player_equip_id,
            'player_level': player.level,
            'before':before_level,
            'after': after_level,
            'info': info,
        }

        cls.send_message('EQUIP', "enhance", player.pk, message, player.userid)

    # @classmethod
    # def equip_upgrade(cls, player, player_equip_id, equip_id, next_equip_id, info):
    #     message = {
    #         'equip_id': equip_id,
    #         'next_equip_id': next_equip_id,
    #         'player_equip_id': player_equip_id,
    #         'info': info,
    #     }

    #     cls.send_message('EQUIP', "upgrade", player.pk, message)

    @classmethod
    def equipfragment_cost(cls, player, equipfragment,before_num,after_num,info):
        message = {
            'equipfragment_id':equipfragment.id,
            'before':before_num,
            'after':after_num,
            'info': info,
        }
        cls.send_message('EQUIPFRAGMENT', "cost", player.pk, message, player.userid)



    @classmethod
    def equip_refinelevelup(cls, player,playerequip, before_refinelevel, after_refinelevel, info):
        message = {
            'playerequip_id': playerequip.id,
            'playerequip_level': playerequip.level,
            'before': before_refinelevel,
            'after': after_refinelevel,
            'info': info,
        }
        cls.send_message('EQUIP', "refinelevelup", player.pk, message, player.userid)


    #----------------ARTIFACT----------------
    @classmethod
    def artifact_acquire(cls, player, player_artifact_id, artifact_id, info):
        message = {
            'player_artifact_id':player_artifact_id,
            'artifact_id':artifact_id,
            'info': info,
        }
        cls.send_message('ARTIFACT', "acquire", player.pk, message, player.userid)

    @classmethod
    def artifact_delete(cls, player, playerartifact_id, artifact, info):
        message = {
            'playerartifact_id':playerartifact_id,
            'artifact_id':artifact.id,
            'info': info,
        }
        cls.send_message('ARTIFACT', "delete", player.pk, message, player.userid)

    @classmethod
    def artifact_levelup(cls, player, playerartifact, before_level, after_level, info):
        message = {
            'artifact_id': playerartifact.artifact_id,
            'playerartifact_id': playerartifact.id,
            'player_level': player.level,
            'before': before_level,
            'after': after_level,
            'info': info,
        }
        cls.send_message('ARTIFACT', "levelup", player.pk, message, player.userid)

    @classmethod
    def artifact_refine(cls, player, playerartifact, before_level, after_level, info):
        message = {
            'artifact_id': playerartifact.artifact_id,
            'playerartifact_id': playerartifact.id,
            'player_level': player.level,
            'before': before_level,
            'after': after_level,
            'info': info,
        }
        cls.send_message('ARTIFACT', "refine", player.pk, message, player.userid)

    @classmethod
    def artifact_melt(cls, player, playerartifact, info):
        message = {
            'artifact_id': playerartifact.artifact_id,
            'playerartifact_id': playerartifact.id,
            'info': info,
        }
        cls.send_message('ARTIFACT', "melt", player.pk, message, player.userid)

    @classmethod
    def artifactfragment_cost(cls, player, artifactfragment,before_num,after_num,info):
        message = {
            'artifactfragment_id':artifactfragment.id,
            'before':before_num,
            'after':after_num,
            'info': info,
        }
        cls.send_message('ARTIFACTFRAGMENT', "cost", player.pk, message, player.userid)

    # ---- BUILDING ----
    @classmethod
    def building_create(cls, player, player_building_id, building_id, info):
        message = {
            'player_level':player.level,
            'building_id': building_id,
            'player_building_id': player_building_id,
            'info': info,
        }

        cls.send_message('BUILDING', "create", player.pk, message, player.userid)

    @classmethod
    def building_delete(cls, player, player_building_id, building_id, info):
        message = {
            'player_level':player.level,
            'building_id': building_id,
            'player_building_id': player_building_id,
            'info': info,
        }

        cls.send_message('BUILDING', "delete", player.pk, message, player.userid)

    @classmethod
    def building_upgrade(cls, player, player_building_id, building_id, before_level, after_level, info):
        message = {
            'player_level':player.level,
            'building_id': building_id,
            'before': before_level,
            'after': after_level,
            'player_building_id': player_building_id,
            'info': info,
        }

        cls.send_message('BUILDING', "upgrade", player.pk, message, player.userid)

    @classmethod
    def buildingfragment_cost(cls, player, buildingfragment,before_num,after_num,info):
        message = {
            'buildingfragment_id':buildingfragment.id,
            'before':before_num,
            'after':after_num,
            'info': info,
        }
        cls.send_message('BUILDINGFRAGMENT', "cost", player.pk, message, player.userid)

    # ---- GOLD ----
    @classmethod
    def gold_add(cls, player, before_number, after_number, gold, info):
        message = {
            'before':before_number,
            'after':after_number,
            'gold': gold,
            'info': info,
        }

        cls.send_message('GOLD', "add", player.pk, message, player.userid)

    @classmethod
    def gold_cost(cls, player, before_number, after_number, gold, info):
        message = {
            'before':before_number,
            'after':after_number,
            'gold': gold,
            'info': info,
        }

        cls.send_message('GOLD', "cost", player.pk, message, player.userid)

    # ---- WOOD ----
    @classmethod
    def wood_add(cls, player, before_number, after_number, wood, info):
        message = {
            'before':before_number,
            'after':after_number,
            'wood': wood,
            'info': info,
        }

        cls.send_message('WOOD', "add", player.pk, message, player.userid)

    @classmethod
    def wood_cost(cls, player, before_number, after_number, wood, info):
        message = {
            'before':before_number,
            'after':after_number,
            'wood': wood,
            'info': info,
        }

        cls.send_message('WOOD', "cost", player.pk, message, player.userid)

    # ---- YUANBO ----
    @classmethod
    def yuanbo_add(cls, player, before_number, after_number, yuanbo, info):
        message = {
            'before':before_number,
            'after':after_number,
            'yuanbo': yuanbo,
            'info': info,
        }

        cls.send_message('DIAMOND', "add", player.pk, message, player.userid)

    @classmethod
    def yuanbo_cost(cls, player, before_number, after_number, yuanbo, info):
        message = {
            'before':before_number,
            'after':after_number,
            'yuanbo': yuanbo,
            'info': info,
        }

        cls.send_message('DIAMOND', "cost", player.pk, message, player.userid)
    # ---- COURAGEPOINT ----
    @classmethod
    def couragepoint_add(cls, player, before_number, after_number, couragepoint, info):
        message = {
            'before':before_number,
            'after':after_number,
            'couragepoint': couragepoint,
            'info': info,
        }

        cls.send_message('COURAGEPOINT', "add", player.pk, message, player.userid)

    @classmethod
    def couragepoint_cost(cls, player, before_number, after_number, couragepoint, info):
        message = {
            'before':before_number,
            'after':after_number,
            'couragepoint': couragepoint,
            'info': info,
        }

        cls.send_message('COURAGEPOINT', "cost", player.pk, message, player.userid)

    # ---- HONOR ----
    @classmethod
    def honor_add(cls, player, before_number, after_number, honor, info):
        message = {
            'before':before_number,
            'after':after_number,
            'honor': honor,
            'info': info,
        }

        cls.send_message('HONOR', "add", player.pk, message, player.userid)

    @classmethod
    def honor_cost(cls, player, before_number, after_number, honor, info):
        message = {
            'before':before_number,
            'after':after_number,
            'honor': honor,
            'info': info,
        }

        cls.send_message('HONOR', "cost", player.pk, message, player.userid)

    # ---- GUILD ----
    @classmethod
    def guild_add(cls, player, before_number, after_number, count, info):
        message = {
            'before':before_number,
            'after':after_number,
            'gold': count,
            'info': info,
        }

        cls.send_message('GUILDGOLD', "add", player.pk, message, player.userid)

    @classmethod
    def guild_cost(cls, player, before_number, after_number, count, info):
        message = {
            'before':before_number,
            'after':after_number,
            'gold': count,
            'info': info,
        }

        cls.send_message('GUILDGOLD', "cost", player.pk, message, player.userid)

    # ---- TOWER ----
    @classmethod
    def tower_add(cls, player, before_number, after_number, count, info):
        message = {
            'before':before_number,
            'after':after_number,
            'towerGold': count,
            'info': info,
        }

        cls.send_message('TOWERGOLD', "add", player.pk, message, player.userid)

    @classmethod
    def tower_cost(cls, player, before_number, after_number, count, info):
        message = {
            'before':before_number,
            'after':after_number,
            'towerGold': count,
            'info': info,
        }

        cls.send_message('TOWERGOLD', "cost", player.pk, message, player.userid)
