# -*- coding: utf-8 -*-
from common.urlresolvers import patterns,url

custom_urls = patterns("")

#共同
custom_urls += patterns('mobile.views.common',
    url("sync", action=1000), #同步消息
    url("wakeup", action=1004), #唤醒
)

#初始化接口
custom_urls += patterns('mobile.views.root',
    url("init", action=1001), #初始化接口    init
    url("setting", action=1002), #用户设置
    url("vipRewardsGet", action=1003), #vip礼包
)

#活动
custom_urls += patterns('mobile.views.activity',
    url("activityReward", action=1011), #活动奖励领取
    url("loginBoxReward", action=1012), #活动奖励领取
    url("offlineRewardGet", action=1013), #离线奖励领取
)

#成长任务&日程任务
custom_urls += patterns('mobile.views.task',
    url("taskReward", action=1021), #任务奖励领取
    url("taskDailyReward", action=1031), #日常任务奖励领取
    url("sevenDaysTaskReward", action=1032), #七天乐任务
    url("dailyTaskActivityReward", action=1033), #活跃度奖励
    url("sevenDaysHalfBuy", action=1034), # 半价购买
)

#邮件
custom_urls += patterns('mobile.views.mail',
    url("mailsGet", action=1051),
    url("mailRead", action=1052),
    url("mailRewardsGet", action=1053),
    url("mailDelete", action=1054),
    url("mailsDelete", action=1055),
    url("recordsGet", action=1056),
)

#生成订单
custom_urls += patterns('mobile.views.payment',
    url("paymentOrder", action=10001), #支付,生成订单
    url("paymentCheck", action=10002), #支付,检查支付结果
)

#英雄
custom_urls += patterns('mobile.views.hero',
    url("heroGacha", action=1101), #抽奖  heroGacha
    url("heroUpgrade", action=1102), #进阶   heroUpgrade
    url("heroDecompose", action=1103), #献祭 heroDecompose
    url("heroSkillLevelUp", action=1104), #技能升级
    url("heroCompose", action=1105), #合成
    #url("heroInit", action=1106), #重生
    #url("heroUp", action=1107), #英雄上阵
    url("heroStarUpgrade", action=1108), #升星
    url("heroDestiny", action=1109), #天命
    url("heroLevelUp", action=1110), #英雄升级
    # url("heroTrain", action=1111), #英雄培养
    # url("heroTrainConfirm", action=1112), #英雄培养确认
    # url("heroTeamLevelUp", action=1113), #英雄组队升级


    url("debugGetAllHeroes", action=6001), #测试添加英雄
)

#装备
custom_urls += patterns('mobile.views.equip',
    url("equipUp", action=1201), #英雄装备
    url("equipDown", action=1202), #英雄卸下装备
    url("equipLevelUp", action=1203), #装备强化
    url("equipCompose", action=1205), #装备合成
    url("equipAutoLevelUp", action=1206), #装备一键强化
    url("heroEquipsAutoLevelUp", action=1207), #英雄装备一键强化
    url("equipRefine", action=1209), #英雄装备精炼
    url("equipMelt", action=1210), #英雄装备回炉
    url("equipDecompose", action=1211), #英雄装备分解
)

#神器
custom_urls += patterns('mobile.views.artifact',
    url("artifactCompose", action=1301), #神器合成
    url("artifactLevelUp", action=1302), #神器强化
    url("artifactRefine", action=1303), #神器精炼
    url("artifactMelt", action=1304), #神器回炉
)


#物品
custom_urls += patterns('mobile.views.item',
    url("itemBuy", action=1501), #道具购买
    url("itemUse", action=1502), #道具使用
    url("itemCompose", action=1503), #道具合成
    url("couragePointStoreBuy", action=1504), #勇气商店购买
    url("itemBuyAndUse", action=1505), #道具购买并使用
    url("itemTowerBuy", 1507), # 爬塔商店
)

#副本
custom_urls += patterns('mobile.views.instance',
    url("instanceSetUp", action=2001), #进入关卡，请求敌军数据
    url("instanceStart", action=2002), #关卡结算
    url("instanceReset", action=2003), #重置副本次数
    url("instanceSweep", action=2004), #扫荡副本
    url("instanceBoxOpen", action=2005), #开宝箱
    url("eliteInstanceSetUp", action=2011), #进入精英关卡，请求敌军数据
    url("eliteInstanceStart", action=2012), #关卡精英结算
    url("raceInstanceSetUp", action=2021), #活动副本阵容
    url("raceInstanceStart", action=2022), #活动副本结算
    url("guildInstanceSetUp", action=2032), # 公会副本请求战斗
    url("guildInstanceOpen", action=2033),
    url("guildInstanceStart", action=2034),
    url("guildInstanceReset", action=2035),
    url("guildInstanceCancel", action=2036),
    url("smallGameFinish", action=2701), #闯关小游戏
    url("elementTowerOpen", action=2801), #元素之塔开启
    url("elementTowerReset", action=2802), #元素之塔重置
    url("elementTowerInstanceSetUp", action=2803), #元素之塔获取当前关卡敌军
    url("elementTowerInstanceStart", action=2804), #元素之塔结算
    url("elementTowerBoxOpen", action=2805), #元素之塔开箱子
    url("elementTowerChoiceBuff", action=2806), #元素之塔选择buff
    url("elementTowerInstanceSweep", action=2807), #元素之塔扫荡
)

#PVP
custom_urls += patterns('mobile.views.pvp',
    url("pvpSetUp", action=2101), #请求PVP阵容
    url("pvpStart", action=2102), #请求PVP列表
    url("pvpRank", action=2111), #请求PVP世界排名
    url("pvpOpps", action=2121), #请求PVP列表
    url("pvpEnemyData", action=2131), #请求敌军阵容数据
    # url("pvpFragmentOpps", action=2141), #抢夺碎片
    # url("pvpFragmentTenFight", action=2142), #十连抢夺
    url("pvpResetCount", action=2501), #通知扣除耐力
    url("pvpDefenseArmy", action=2143), #设置防守阵容
    url("siegeBattlePlayer", action=2144), #攻城战对手
    url("siegeBattleDelCDTime", action=2145), #攻城战对手
    url("pvpCDTimeDelete", action=2146), #清楚竞技场冷却时间
    url("siegeBattlePlayerLock", action=2132), #攻城战对手锁定
    url("siegeBattleFortReset", action=2133), #攻城战堡垒信息重置
    url("rampartSoldierLevelUp", action=2134), #攻城战城墙士兵升级
)

#公会
custom_urls += patterns('mobile.views.guilds',
    url("createGuild", action=2147), #创建社团
    url("searchGuild", action=2148), #搜索社团
    url("joinGuild", action=2149), # 加入社团
    url("quitGuild", action=2150), # 退出社团
    url("guildContribute", action=2151), # 社团捐献
    url("guildKickMembers", action=2152), # 踢出社团
    url("guildPositionUp", action=2153), # 社团变更
    url("guildReName", action=2154), # 社团改名
    url("guildShopInit", action=2155), # 商店刷新
    url("addHeroToTraining", action=2157), #
    url("deleteHeroFromTraining", action=2158), #
    url("speedUpHero", action=2159),
    url("displayGuildInstance", action=2160),
    url("displayGuildAucInfo", action=2161),
    url("startGuildAuc", action=2162),
    #url("finishGuildAuc", action=2163),
  #  url("displayGuildFireInfo", action=2164),
    url("guildFireBuffSettings", action=2165),
    url("contributeGuildFire", action=2166),
    url("displayAppMember", action=2167),
    url("allowedMemberJoinGuild", action=2168),
    url("guildShopBuy", action=2169),
    url("modifyGuildAttention", action=2170),
    url("confirmGuildAttention", action=2171),
    url("displayGuildLogInfo", action=2172),
    url("getGuildSiegeBattleStatus", action=2173),
    url("guildSiegeBattleEnter", action=2174),
    url("guildSiegeBattleConfig", action=2175),
    # url("decideSiegeBattleWinner", action=2176), TODO : 删除http文件
    url("guildSiegeBattleConfigGet", action=2177),
    url("guildIndex", action=2178),
    url("guildLevelUp", action=2179),
    url("guildFireCheckStatus", action=2180), #工会火堆升级
)

#荣誉商店
custom_urls += patterns('mobile.views.arenashop',
    url("honorShopBuy", action=2201), #兑换
    #url("honorShopInit", action=2202), #刷新
)

#神秘商店
custom_urls += patterns('mobile.views.mysteryshop',
    url("mysteryShopBuy", action=2301), #兑换
    url("mysteryShopInit", action=2302), #刷新
)

#建筑
custom_urls += patterns('mobile.views.building',
    url("buildingBuild", action=5001), #创建建筑
    url("buildingMove", action=5002), #移动建筑
    url("buildingSpeed", action=5003), #加速
    url("buildingProduce", action=5004), #建筑生产
    url("buildingHarvest", action=5005), #采集
    url("buildingCheck", action=5006), #升级结束
    url("buildingLevelUp", action=5007), #升级建筑
    url("buildingTutorialEnd", action=5008), #建筑引导结束
    url("buildingDismantle", action=5009), #建筑 拆除
)

#礼包
custom_urls += patterns('mobile.views.package',
    url("packageUse", action=5101), #领取礼包
    url("testPayInterface", action=5102), # 测试支付接口

)

#建筑植物
custom_urls += patterns('mobile.views.plant',
    url("buildingPlantBuild", action=5201), #创建植物
    url("buildingPlantHarvest", action=5203), #植物采摘
    url("buildingPlantDismantle", action=5204), #植物铲除
    url("buildingPlantPeriod", action=5205), #植物时期变化
)




