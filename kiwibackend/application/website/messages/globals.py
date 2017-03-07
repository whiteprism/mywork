# -*- coding: utf-8 -*-
from common.static import Static
from messages import BaseMessage
class Globals(BaseMessage):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.heroResetLevelRatio = 0
        self.set("heroResetLevelRatio", Static.HERO_RESET_COST_YUANBO_LEVEL_RATIO)
        self.heroResetUpgradeRatio = 0
        self.set("heroResetUpgradeRatio", Static.HERO_RESET_COST_YUANBO_UPGRADE_RATIO)
        self.heroEnhanceSkillGoldRatio = 0
        self.set("heroEnhanceSkillGoldRatio", Static.HERO_ENHANCE_HERRO_SKILL_COST_GOLD_RATIO)
        self.artifactEnhanceXpRatio = 0
        self.set("artifactEnhanceXpRatio", Static.ARTIFACT_ENHANCE_XP_RATIO)
        self.powerRecoverTime = 0
        self.set("powerRecoverTime", Static.PLAYER_POWER_FLUCTUATION_SECOND)
        self.staminaRecoverTime = 0
        self.set("staminaRecoverTime", Static.PLAYER_STAMINA_FLUCTUATION_SECOND)
        self.allianceProSoldierRatio = 0
        self.set("allianceProSoldierRatio", Static.BUILDING_ALLIANCEBARRACK_PRODUCE_SOLDIER_RATIO)
        self.hordeProSoldierRatio = 0
        self.set("hordeProSoldierRatio", Static.BUILDING_ALLIANCEBARRACK_PRODUCE_SOLDIER_RATIO)
        self.honorStoneId = 0
        self.set("honorStoneId", Static.ITEM_HONORSTONE_ID)
        self.starChestOpenCounts = []
        self.set("starChestOpenCounts", Static.STAR_CHEST_OPEN_COUNTS)
        self.refreshTicketId = 0
        self.set("refreshTicketId", Static.ITEM_REFRESH_TICKET_ID)
        self.mysteryShopRefreshDiamond = 0
        self.set("mysteryShopRefreshDiamond", Static.MYSTERYSHOP_REFRESH_YUANBO)
        self.arenaDeleteCDTimeCostDiamond = 0
        self.set("arenaDeleteCDTimeCostDiamond", Static.PVP_DELETE_CD_TIME_COST)
        self.siegeDeleteCDTimeCostDiamond = 0
        self.set("siegeDeleteCDTimeCostDiamond", Static.SIEGE_DELETE_CD_TIME_COST)
        self.arenaStartLevel = 0 
        self.set("arenaStartLevel", Static.PVP_LEVEL)
        self.raidMaxCout = 0
        self.set("raidMaxCout", Static.RAID_MAX_COUNT)
        self.itemPowerId = 0 #体力id
        self.set("itemPowerId", Static.ITEM_POWER_ID)
        self.itemPowerIds = []
        self.set("itemPowerIds", Static.ITEM_POWER_IDS)
        self.itemSpId = 0 #耐力id
        self.set("itemSpId", Static.ITEM_SP_ID)
        self.itemSpIds = []
        self.set("itemSpIds", Static.ITEM_SP_IDS)
        self.itemTutorialXpId = 0 #耐力id
        self.set("itemTutorialXpId", Static.ITEM_TUTORIAL_XP_ID)
        self.itemGoldHandId = 0 #点金手id
        self.set("itemGoldHandId", Static.ITEM_GOLDHAND_ID)
        self.itemWoodHandId = 0 #点金手id
        self.set("itemWoodHandId", Static.ITEM_WOODHAND_ID)
        # self.itemWarAvoidTicketId = 0 #免战id
        # self.set("itemWarAvoidTicketId", Static.ITEM_WARAVOID_TICKET_ID)
        self.itemGoldBoxId = 0 #金宝箱ID
        self.set("itemGoldBoxId", Static.ITEM_GOLD_BOX_ID)
        self.refreshInstanceCost = 0 #刷新副本次数的消耗
        self.set("refreshInstanceCost", Static.REFRESH_INSTANCE_COST)
        self.pvpStaminaCost = 0 #PVP耐力的消耗
        self.set("pvpStaminaCost", Static.PVP_SUB_STAMINA)
        self.lootStaminaCost = 0 #掠夺耐力的消耗
        self.set("lootStaminaCost", Static.LOOT_SUB_STAMINA)
        self.siegeStaminaCost = 0 #攻城战耐力的消耗
        self.set("siegeStaminaCost", Static.SIEGE_SUB_STAMINA)
        self.siegeFortCdTime = 0 #攻城战运输堡垒cd时间
        self.set("siegeFortCdTime", Static.SIEGE_FORT_CD_TIME)
        self.siegeRefreshCostGold = 0 #攻城战刷新对手消耗
        self.set("siegeRefreshCostGold", Static.SIEGE_REFRESH_COST_GOLD)
        self.sweepItemId = 0 #扫荡卷id
        self.set("sweepItemId", Static.ITEM_SWEEP_ID)
        self.goldId = 0 #金币id
        self.set("goldId", Static.GOLD_ID)
        self.woodId = 0 #木头id
        self.set("woodId", Static.WOOD_ID)
        self.mojoId = 0 #钻石id
        self.set("mojoId", Static.YUANBO_ID)
        self.sweepOpenLevel = 0
        self.set("sweepOpenLevel", Static.SWEEP_OPEN_LEVEL)
        self.sweepCost = 0 #扫荡cost
        self.set("sweepCost", Static.SWEEP_INSTANCE_COST)
        self.growGoldCost = 0 #购买成长基金花费
        self.set("growGoldCost", Static.GROW_GOLD_ACTIVITY_MOJO)
        self.shopMaxBuyCount = 0 #购买成长基金花费
        self.set("shopMaxBuyCount", Static.SHOP_MAX_BUY_COUNT)
        self.pvpLevel = 0 #pvp 开启等级
        self.set("pvpLevel", Static.PVP_LEVEL)
        self.dailytaskCategoryVipSweep = 0 #日常任务扫荡券
        self.set("dailytaskCategoryVipSweep", Static.DAILYTASK_CATEGORY_VIP_SWEEP)
        self.dailytaskCategoryLanch = 0 #日常任务豪华午餐
        self.set("dailytaskCategoryLanch", Static.DAILYTASK_CATEGORY_LANCH)
        self.dailytaskCategoryDinner = 0 #日常任务豪华晚餐
        self.set("dailytaskCategoryDinner", Static.DAILYTASK_CATEGORY_DINNER)
        self.dailytaskCategorySupper = 0 #日常任务豪华夜宵
        self.set("dailytaskCategorySupper", Static.DAILYTASK_CATEGORY_SUPPER)

        self.dailytaskCategoryWeekCard = 0 #日常任务周卡
        self.set("dailytaskCategoryWeekCard", Static.DAILYTASK_CATEGORY_WEEK_CARD)
        self.dailytaskCategoryMonthCard = 0 #日常任务月卡
        self.set("dailytaskCategoryMonthCard", Static.DAILYTASK_CATEGORY_MONTH_CARD)
        self.dailytaskCategoryPermanentCard = 0 #日常任务永久卡
        self.set("dailytaskCategoryPermanentCard", Static.DAILYTASK_CATEGORY_PERMANENT_CARD)

        self.itemXpList = []
        self.set("itemXpList", Static.ITEM_XP_LIST)

        self.heroUpgradePowerRanks = []
        self.set("heroUpgradePowerRanks", Static.HERO_UPGRADE_POWERRANKS)
        #self.heroStarPowerRanks = []
        #self.set("heroStarPowerRanks", Static.HERO_STAR_POWERRANKS)
        self.heroBigSpellPowerRankRatio = 0
        self.set("heroBigSpellPowerRankRatio", Static.HERO_BIGSPELL_POWERRANK_RATIO)
        self.heroSmallSpellPowerRankRatio = 0
        self.set("heroSmallSpellPowerRankRatio", Static.HERO_SMALLSPELL_POWERRANK_RATIO)
        self.artifactUpgradePowerRankRatio = 0
        self.set("artifactUpgradePowerRankRatio", Static.ARTIFACT_UPGRADE_POWERRANK_RATIO)
        self.artifactLevelPowerRankRatio = 0
        self.set("artifactLevelPowerRankRatio", Static.ARTIFACT_LEVEL_POWERRANK_RATIO)
        self.heroDestinyList = []
        self.set("heroDestinyList", Static.HERO_DESTINY_LIST)
        self.heroDestinyLevel = 0
        self.set("heroDestinyLevel", Static.HERO_DESTINY_LEVEL)
        self.heroDestinyCostRatio = 0
        self.set("heroDestinyCostRatio", Static.HERO_DESTINY_COST_RATIO)
        self.sweepVipLevel = 0
        self.set("sweepVipLevel", Static.SWEEP_VIP_LEVEL)
        self.itemRefineId = []
        self.set("itemRefineId", Static.ITEM_REFINE_ID)
        self.itemTrainId = 0
        self.set("itemTrainId", Static.ITEM_TRAIN_ID)
        self.artifactRefineList = []
        self.set("artifactRefineList", Static.ARTIFACRT_REFINE_LIST)
        self.artifactXpList = []
        self.set("artifactXpList", Static.ARTIFACRT_XP_LIST)
        self.defaultArtifactIDs = []
        self.set("defaultArtifactIDs", Static.ARTIFACT_FRAGMENG_GRAB_LIST)
        self.danCost = 0
        self.set("danCost", Static.ARTIFACRT_XP_LIST)
        self.equipRemeltGoldRatio = 0
        self.set("equipRemeltGoldRatio", Static.EQUIP_GOLD_RATIO)
        self.trainingHeroPerMinXps = 0
        self.set("trainingHeroPerMinXps", Static.HERO_TRAINING_PER_MINUTE_XPS)
        self.guildFireOpenLevels = 0
        self.set("guildFireOpenLevels", Static.GUILD_FIRE_OPEN_LEVELS)
        self.arenaShopDiamondRefresh = 0
        self.set("arenaShopDiamondRefresh", Static.HONORSHOP_REFRESH_YUANBO)
        self.itemDiamondGashaponId = 0
        self.set("itemDiamondGashaponId", Static.ITEM_DIAMOND_GASHAPON_ID)
        self.elementTowerChoiceBuffCosts = 0
        self.set("elementTowerChoiceBuffCosts", Static.ELEMENTTOWER_CHOCIE_BUFF_COSTS)
        self.siegeBasePVPRatio = 0
        self.set("siegeBasePVPRatio", Static.SIEGE_BASE_PVP_RATIO)
        self.siegeFortPVPRatio = 0
        self.set("siegeFortPVPRatio", Static.SIEGE_FORT_PVP_RATIO)




