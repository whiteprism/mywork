# -*- encoding:utf8 -*-
from messages.http import  BaseHttp

class Message(BaseHttp):
    def __init__(self):
        super(Message, self).__init__()
        self.messageId = -1
        self.sync = None
        self.wakeup = None
        self.init = None
        self.setting = None
        self.vipRewardsGet = None
        self.activityReward = None
        self.loginBoxReward = None
        self.offlineRewardGet = None
        self.taskReward = None
        self.taskDailyReward = None
        self.dailyTaskActivityReward = None
        self.sevenDaysTaskReward = None
        self.paymentOrder = None
        self.paymentCheck = None

        self.mailsGet = None
        self.mailRead = None
        self.mailRewardsGet = None
        self.mailDelete = None
        self.mailsDelete = None

        self.heroGacha = None
        self.heroUpgrade = None
        self.heroDecompose = None
        self.heroSkillLevelUp = None
        self.heroLevelUp = None
        self.heroCompose = None
        self.heroInit = None
        #self.heroUp = None
        self.heroStarUpgrade = None
        self.heroDestiny = None
        # self.heroTrain = None
        # self.heroTrainConfirm = None
        # self.heroTeamLevelUp = None

        self.equipUp = None
        self.equipDown = None
        self.equipLevelUp = None
        self.equipAutoLevelUp = None
        self.heroEquipsAutoLevelUp = None
        #self.equipUpgrade = None
        self.equipCompose = None
        self.equipRefine = None
        self.equipMelt = None
        self.equipDecompose = None
        #self.equipUnbinding = None

        self.artifactCompose = None
        self.artifactLevelUp = None
        self.artifactRefine = None
        self.artifactMelt = None

       # self.gemCompose = None
       # self.gemInlay = None
       # self.equipGemsInlay = None
       # self.gemDecompose = None
       # self.gemShopBuy = None
       # self.gemShopInit = None

        self.itemBuy = None
        self.itemUse = None
        self.itemCompose = None
        self.couragePointStoreBuy = None
        self.itemBuyAndUse = None
        self.itemTowerBuy = None

        self.instanceSetUp = None
        self.instanceStart = None
        self.instanceReset = None
        self.instanceSweep = None
        self.instanceBoxOpen = None
        self.eliteInstanceSetUp = None
        self.eliteInstanceStart = None
        self.raceInstanceSetUp = None
        self.raceInstanceStart = None
        self.elementTowerOpen = None
        self.elementTowerReset = None
        self.elementTowerInstanceSetUp = None
        self.elementTowerInstanceStart = None
        self.elementTowerBoxOpen = None
        self.elementTowerChoiceBuff = None
        self.elementTowerInstanceSweep = None

        self.smallGameFinish = None
        self.recordsGet = None

        self.pvpSetUp = None
        self.pvpStart = None
        self.pvpRank = None
        self.pvpOpps = None
        self.pvpEnemyData = None
        self.pvpFragmentOpps = None
        self.pvpFragmentTenFight = None
        self.pvpDefenseArmy = None
        self.siegeBattlePlayer = None
        self.siegeBattleDelCDTime = None
        self.siegeBattlePlayerLock = None
        self.siegeBattleFortReset = None
        self.rampartSoldierLevelUp = None
        self.pvpCDTimeDelete = None
        self.pvpResetCount = None
        self.createGuild = None
        self.searchGuild = None
        self.joinGuild = None
        self.quitGuild = None
        self.guildContribute = None
        self.guildKickMembers = None
        self.guildPositionUp = None
        self.guildReName = None
        self.guildShopInit = None
        self.speedUpHero = None
        self.honorShopBuy = None
        self.honorShopInit = None

        self.addHeroToTraining = None
        self.deleteHeroFromTraining = None
        self.displayGuildInstance = None
        self.guildInstanceSetUp = None
        self.guildInstanceOpen = None
        self.guildInstanceStart = None
        self.guildInstanceReset = None
        self.guildInstanceCancel = None
        self.displayGuildAucInfo = None
        self.startGuildAuc = None
        self.displayAppMember = None
        self.allowedMemberJoinGuild = None
        self.guildFireBuffSettings = None
        self.contributeGuildFire = None
        #self.finishGuildAucRequest = None
        self.guildShopBuy = None
        self.mysteryShopBuy = None
        self.mysteryShopInit = None
        self.buildingBuild = None
        self.buildingMove = None
        self.buildingSpeed = None
        self.buildingProduce = None
        self.buildingHarvest = None
        self.buildingCheck = None
        self.buildingLevelUp = None
        self.buildingTutorialEnd = None
        self.buildingDismantle = None
        self.buildingPlantBuild = None
        self.buildingPlantHarvest = None
        self.buildingPlantPeriod = None
        self.buildingPlantDismantle = None
        self.packageUse = None
        self.sevenDaysHalfBuy = None
        self.debugGetAllHeroes = None
        self.testPayInterface =None
        self.modifyGuildAttention = None
        self.confirmGuildAttention = None
        self.displayGuildLogInfo = None
        self.getGuildSiegeBattleStatus = None
        self.guildSiegeBattleEnter = None
        self.guildSiegeBattleConfig = None
        self.decideSiegeBattleWinner = None
        self.guildSiegeBattleConfigGet = None
        self.guildIndex = None
        self.guildLevelUp = None
        self.guildFireCheckStatus = None

class MessageRequest(Message):
    pass
class MessageResponse(Message):
    pass
