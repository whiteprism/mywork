# -*- coding: utf8 -*-
from django.core.management.base import BaseCommand
from optparse import make_option
from django.conf import settings
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from module.activity.api import update_activity_cache
from module.arenashop.api import update_arenashop_cache
from module.artifact.api import update_artifact_cache
from module.attr.api import update_attr_cache
from module.building.api import update_building_cache
from module.equip.api import update_equip_cache
from module.gashapon.api import update_gashapon_cache
#from module.gem.api import update_gem_cache
from module.hero.api import update_hero_cache
from module.icon.api import update_icon_cache
from module.instance.api import update_instance_cache
from module.item.api import update_item_cache
from module.levelconf.api import update_level_cache
from module.mysteryshop.api import update_mysteryshop_cache
from module.pvp.api import update_pvp_cache
from module.skill.api import update_skill_cache
from module.soul.api import update_soul_cache
from module.task.api import update_task_cache
from module.tutorial.api import update_tutorial_cache
from module.vip.api import update_vip_cache
from module.yuanbo.api import update_yuanbo_cache
from module.package.api import update_package_cache
from module.loginbonus.api import update_loginbonus_cache
from module.guild.api import update_guild_cache
from module.robot.api import update_robot_cache
from module.offlinebonus.api import update_offlinebonus_cache

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not settings.ENABLE_REDIS_CACHE:
            return

        update_activity_cache()
        update_arenashop_cache()
        update_artifact_cache()
        update_attr_cache()
        update_building_cache()
        update_equip_cache()
        update_gashapon_cache()
        update_hero_cache()
        #update_gem_cache()
        update_icon_cache()
        update_instance_cache()
        update_item_cache()
        update_level_cache()
        update_mysteryshop_cache()
        update_pvp_cache()
        update_skill_cache()
        update_soul_cache()
        update_task_cache()
        update_tutorial_cache()
        update_vip_cache()
        update_yuanbo_cache()
        update_package_cache()
        update_loginbonus_cache()
        update_robot_cache()
        update_offlinebonus_cache()
