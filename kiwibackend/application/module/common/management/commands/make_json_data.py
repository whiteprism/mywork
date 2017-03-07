# -*- coding: utf8 -*-
from django.core.management.base import BaseCommand
from django.db import models
from optparse import make_option
from django.conf import settings
import json
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import msgpack
from messages.globals import Globals
from module.activity.api import get_activities
from module.skill.api import get_flag_configs, get_skills, get_conditions_all
from module.hero.api import get_herocombats, get_warriors,get_heroskills, get_herolevels, get_herostarupgrades, get_heromasters, get_herostars, get_herodestinies, get_cards, get_heroteams, get_heroteamlevels, get_herobubbles

from module.soul.api import get_souls
from module.instance.api import get_all_instancelevels, get_all_eliteinstancelevels,get_level_data, get_elite_data, get_instances, get_raidinstances, get_raidlevels, get_elementtowerinstances, get_elementtowerbuffs
from module.equip.api import get_equips, get_equipenhances, get_equipfragments, get_equipsuits, get_equiprefines
#from module.gem.api import get_gems, get_gemfragments, get_gemshop_items
from module.building.api import get_buildings, get_buildingresourceprotecteds, get_buildingradars, get_buildinggoldhands, get_buildingfragments, get_buildingplants
from module.attr.api import get_attrs
from module.levelconf.api import get_levels
from module.item.api import get_items, get_storeitems, get_itemcomposes, get_couragepointstores,  get_towerstores
from module.task.api import get_dailytasks, get_tasks, get_seven_days_tasks, get_dailytask_activities, get_sevenDaysHalfPrices
from module.artifact.api import get_artifacts, get_artifactenhances, get_artifactfragments, get_artifactrefines
from module.vip.api import get_vips
from module.arenashop.api import get_arenashops
from module.mysteryshop.api import get_mysteryshops, get_mysteryshopgrids
from module.gashapon.api import get_taverns
from module.common.powerrank import PowerRank
from module.icon.api import get_icons
from module.yuanbo.api import get_yuanbos
from module.tutorial.api import get_tutorials, get_tutorialdetails, get_plots
from module.pvp.api import get_pvpRanks, get_pvpScenes
from module.guild.api import get_guilds,get_guildshops, get_guildfirebuffs, get_guildfirelevels, get_guildauctionrewards, get_guildsiegebattlerewards
from module.instance.api import get_zones, get_triggers, get_guildinstanceLevels
from module.offlinebonus.api import get_offlinebonuslevels, get_offlinebonusdays

class Command(BaseCommand):
    def handle(self, *args, **options):
        flags = get_flag_configs()
        activities = get_activities()
        skills = get_skills()
        warriors = get_warriors()
        conditions_all = get_conditions_all()
        heroskills = get_heroskills()
        herocombats = get_herocombats()
        herostarupgrades = get_herostarupgrades()
        heromasters = get_heromasters()
        herostars = get_herostars()
        herodestinies = get_herodestinies()
        cards = get_cards()
        # heroequipfateattrs = get_heroequipfateattrs()
        heroteams = get_heroteams()
        # herotrains = get_herotrains()
        heroteamlevels = get_heroteamlevels()
        herobubbles = get_herobubbles()

        souls = get_souls()
        equips = get_equips()
        equipsuits = get_equipsuits()
        equipenhances = get_equipenhances()
        equiprefines = get_equiprefines()
        equipfragments = get_equipfragments()
       # gems = get_gems()
       # gemfragments = get_gemfragments()
       # gemshop_items = get_gemshop_items()
        attrs = get_attrs()
        buildings = get_buildings()
        buildingresourceprotecteds = get_buildingresourceprotecteds()
        buildingradars = get_buildingradars()
        buildinghands = get_buildinggoldhands()
        buildingfragments = get_buildingfragments()
        buildingplants = get_buildingplants()
        items = get_items()
        towerstores = get_towerstores()

        storeitems = get_storeitems()
        instances = get_instances()
        dailytasks = get_dailytasks()
        dailytaskactivities = get_dailytask_activities()
        sevendaysprices = get_sevenDaysHalfPrices()

        sevendaystasks = get_seven_days_tasks()
        tasks = get_tasks()
        artifacts = get_artifacts()
        artifactenhances = get_artifactenhances()
        artifactfragments = get_artifactfragments()
        artifactrefines = get_artifactrefines()
        vips = get_vips()
        arenashops = get_arenashops()
        mysteryshops = get_mysteryshops()
        mysteryshopgrids = get_mysteryshopgrids()
        instancelevels = get_all_instancelevels()

        guildinstanceLevels = get_guildinstanceLevels()
        eliteinstancelevels = get_all_eliteinstancelevels()

        taverns = get_taverns()
        raidConfs = get_raidinstances()
        elementTowerInstances = get_elementtowerinstances()
        elementTowerBuffs = get_elementtowerbuffs()
        icons = get_icons()
        yuanbos = get_yuanbos()
        tutorials = get_tutorials()
        tutorialdetails = get_tutorialdetails()
        plots = get_plots()
        pvpRanks = get_pvpRanks()
        pvpScenes = get_pvpScenes()
        #siegeattactsoldierinfos = get_siegeAttactSoldierInfos()
        guilds = get_guilds()
        guildshops = get_guildshops()
        guildfirebuffs = get_guildfirebuffs()
        guildfirelevels = get_guildfirelevels()
        guildAuctionRewards = get_guildauctionrewards()
        guildSiegeBattleRewards = get_guildsiegebattlerewards()

        itemcomposes = get_itemcomposes()
        couragepointstores = get_couragepointstores()
        triggers = get_triggers()
        zones = get_zones()
        raidlevels = get_raidlevels()

        offlinebonuslevels = get_offlinebonuslevels()
        offlinebonusdays = get_offlinebonusdays()

        conf = {}
        conf["activities"] =  [activity.to_dict() for activity in activities]
        conf["skills"] =  [skill.to_dict() for skill in skills]
        conf["conditions"] =  [conditions.to_dict() for conditions in conditions_all]
        conf["flags"] = [flag.to_dict() for flag in flags]
        conf["warriors"] = [warrior.to_dict() for warrior in warriors]
        conf["heroSkills"] = [heroskill.to_dict() for heroskill in heroskills]
        conf["heroStarUpgrades"] = [upgrade.to_dict() for upgrade in herostarupgrades]
        conf["heroCombats"] = [herocombat.to_dict() for herocombat in herocombats]
        conf["heroStars"] = [herostar.to_dict() for herostar in herostars]
        conf["heroMasters"] = [master.to_dict() for master in heromasters]
        conf["heroDestinies"] = [herodestiny.to_dict() for herodestiny in herodestinies]
        conf["heroTeams"] = [heroteam.to_dict() for heroteam in heroteams]
        conf["heroTeamLevels"] = [heroteamlevel.to_dict() for heroteamlevel in heroteamlevels]
        conf["herobubbles"] = [herobubble.to_dict() for herobubble in herobubbles]
        conf["heroCards"] = [card.to_dict() for card in cards]
        # conf["heroEquipFatesAttrs"] = [heroequipfateattr.to_dict() for heroequipfateattr in heroequipfateattrs]
        # conf["heroTrains"] = [herotrain.to_dict() for herotrain in herotrains]
        conf["items"] = [item.to_dict() for item in items]

        conf["towerstores"] = [towerstore.to_dict() for towerstore in towerstores]

        conf["storeItems"] = [storeitem.to_dict() for storeitem in storeitems]
        conf["instances"] = [boxReward.to_dict() for boxReward in instances]
        conf["instanceLevels"] = [get_level_data(instancelevel.to_dict()) for instancelevel in instancelevels]
        conf["guildinstanceLevels"] = [guildinstanceLevel.to_dict() for guildinstanceLevel in guildinstanceLevels]
        conf["eliteInstanceLevels"] = [get_elite_data(eliteinstancelevel.to_dict()) for eliteinstancelevel in eliteinstancelevels]
        conf["triggers"] = [trigger.to_dict() for trigger in triggers]
        conf["raidlevels"] = [raidlevel.to_dict() for raidlevel in raidlevels]
        conf["elementTowerInstances"] = [elementTowerInstance.to_dict() for elementTowerInstance in elementTowerInstances]
        conf["elementTowerBuffs"] = [elementTowerBuff.to_dict() for elementTowerBuff in elementTowerBuffs]

        conf["zones"] = [zone.to_dict() for zone in zones]
        conf["equips"] =  [equip.to_dict() for equip in equips]
        conf["equipSuits"] =  [equipsuit.to_dict() for equipsuit in equipsuits]
        conf["equipFragments"] = [equipfragment.to_dict() for equipfragment in equipfragments]
        conf["equipEnhances"] =  [equipenhance.to_dict() for equipenhance in equipenhances]
        conf["equipRefines"] =  [equiprefine.to_dict() for equiprefine in equiprefines]
        conf["levels"] =  [level.to_dict() for level in get_levels()]
        conf["buildings"] =  [building.to_dict() for building in buildings ]
        conf["buildingResourceProtecteds"] =  [buildingresourceprotected.to_dict() for buildingresourceprotected in buildingresourceprotecteds ]
        conf["buildingRadars"] =  [buildingradar.to_dict() for buildingradar in buildingradars]
        conf["buildingHands"] =  [buildinghand.to_dict() for buildinghand in buildinghands]
        conf["buildingFragments"] =  [buildingfragment.to_dict() for buildingfragment in buildingfragments]
        conf["buildingPlants"] =  [buildingplant.to_dict() for buildingplant in buildingplants]
        conf["artifacts"] =  [artifact.to_dict() for artifact in artifacts]
        conf["artifactEnhances"] =  [artifactenhance.to_dict() for artifactenhance in artifactenhances]
        conf["artiFragments"] =  [artifactfragment.to_dict() for artifactfragment in artifactfragments ]
        conf["artifactRefines"] =  [artifactrefine.to_dict() for artifactrefine in artifactrefines ]
        conf["dailyTasks"] =  [dailytask.to_dict() for dailytask in dailytasks ]
        conf["sevenDaysTasks"] =  [sevendaystask.to_dict() for sevendaystask in sevendaystasks ]
        conf["tasks"] =  [task.to_dict() for task in tasks ]
        conf["dailytaskactivities"] =  [dailytaskactivitie.to_dict() for dailytaskactivitie in dailytaskactivities ]
        conf["sevendaysprices"] =  [sevendaysprice.to_dict() for sevendaysprice in sevendaysprices ]


        conf["vips"] =  [vip.to_dict() for vip in vips]
        conf["arenaRanks"] = [pvp.to_dict() for pvp in pvpRanks]
        conf["pvpScenes"] = [pvpScene.to_dict() for pvpScene in pvpScenes]
        conf["guilds"] = [guild.to_dict() for guild in guilds]
        conf["guildshops"] = [guildshop.to_dict() for guildshop in guildshops]
        conf["guildFireBuffs"] = [guildfirebuff.to_dict() for guildfirebuff in guildfirebuffs]
        conf["guildFireLevels"] = [guildfirelevel.to_dict() for guildfirelevel in guildfirelevels]
        conf["guildAuctionRewards"] = [guildAuctionReward.to_dict() for guildAuctionReward in guildAuctionRewards]
        conf["guildSiegeBattleRewards"] = [guildSiegeBattleReward.to_dict() for guildSiegeBattleReward in guildSiegeBattleRewards]
        conf["honorShops"] = [arenashop.to_dict() for arenashop in arenashops]
        conf["mysteryShops"] = [mysteryshop.to_dict() for mysteryshop in mysteryshops]
        conf["icons"] = [icon.to_dict() for icon in icons]
        conf["diamonds"] = [yuanbo.to_dict() for yuanbo in yuanbos]
        conf["tutorials"] = [tutorial.to_dict() for tutorial in tutorials]
        conf["tutorialDetails"] = [tutorialdetail.to_dict() for tutorialdetail in tutorialdetails]
        conf["plots"] = [plot.to_dict() for plot in plots]
        conf["globals"] =  Globals().for_response()
        conf["souls"] =  [soul.to_dict() for soul in souls]

        #conf["skillConf"] =  [skill.to_new_dict() for skill in skills]
        conf["attributes"] =  [attr.to_dict() for attr in attrs]
        conf["heroLevels"] =  [herolevel.to_dict() for herolevel in get_herolevels()]
        conf["taverns"] = [tavern.to_dict() for tavern in taverns]
        conf["powerRanks"] = PowerRank.to_dict()
        conf["raids"] = [raid.to_dict() for raid in raidConfs]
        conf["itemComposes"] = [itemcompose.to_dict() for itemcompose in itemcomposes]
        conf["couragePointStores"] = [couragepointstore.to_dict() for couragepointstore in couragepointstores]
        #conf["siegeAttactSoldierInfos"] = [siegeattactsoldierinfo.to_dict() for siegeattactsoldierinfo in siegeattactsoldierinfos]

        conf_file = "%s/website/mobile/conf/pbconf.bytes" % settings.ROOT_PATH
        f = open(conf_file, "w")
        data = msgpack.packb(conf)
        f.write(data)
        f.close()
