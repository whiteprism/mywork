# -*- coding:utf-8 -*-

class Static(object):
    #活动对应ID
    CONTINUOUS_LOGIN = 10010001
    NEWER_LEVEL = 10030001
    USER_GROW_UP = 10100001
    #LEVEL_RANK
    #活动对应TYPE
    CONTINUOUS_LOGIN_TYPE = 1001
    NEWER_LOGIN_TYPE = 1002
    NEWER_LEVEL_TYPE = 1003
    MOJO_BUG_TYPE = 1004
    MOJO_COST = 1005
    RANK = 1006
    MONTH_CARD = 1007
    EXCHANGE_ACTIVITY = 1008
    FIRST_PAY = 1009
    USER_GROW_UP = 1010

    POWER_RANK = 1020
    LEVEL_RANK = 1021
    NEW_SERVER = 1022

    #副本
    REFRESH_INSTANCE_COST = 30
    SWEEP_INSTANCE_COST = 1
    SWEEP_OPEN_LEVEL = 10

    FIRST_ELITE_INSTANCE_LEVEL_ID = 110101 # 第一章的精英关卡默认值
    FIRST_INSTANCE_LEVEL_ID = 100101 # 第一章关卡对应的默认值
    FIRST_INSTANCE_BOSS_LEVEL_ID = 1 #boss 副本
    NEW_PLAYER_LEVEL = 50 #10级开始消耗小兵


    #抽奖分类
    GASHAPON_RARITY_HERO = 1
    GASHAPON_RARITY_SOUL = 2
    GASHAPON_RARITY_EQUIP = 3
    GASHAPON_RARITY_ITEM = 4
    GASHAPON_RARITY_ARTIFACTFRAGMENT = 7
    GASHAPON_RARITY_EQUIPFRAGMENT = 8
    GASHAPON_RARITY_CURRENCY = 9

    #抽奖种类
    GASHAPON_GOLD = 1
    GASHAPON_DIAMOND = 2
    GASHAPON_SPACETIME_FLIP = 401


    HERO_DEFENCE_POS = [136, 141, 145, 149, 151]
    SIEGE_DEFENCE_INIT = [1110001, 1140007, 1150003, 1120004, 1160004] # 攻城战开启后英雄布阵的初始阵容
    SIEGE_RAMPART_SOLDIERS = [1902041, 1902042, 1902043]
    HERO_WARRIOR_CATEGORY_WARRIOR = [0, 4, 5, 6] #小兵
    HERO_WARRIOR_CATEGORY_HERO = 1 #英雄
    HERO_WARRIOR_CATEGORY_BOSS = 2 #boss
    HERO_WARRIOR_CATEGORY_WALL = 3 #城墙
    HERO_RESET_COST_YUANBO_LEVEL_RATIO = 5 #英雄重生消耗元宝的等级系数
    HERO_RESET_COST_YUANBO_UPGRADE_RATIO = 10 #英雄重生消耗元宝的进阶系数
    HERO_ENHANCE_HERRO_SKILL_COST_GOLD_RATIO = 1000 #英雄技能升级耗钱系数
    HERO_EQUIP_ENHANCE_ID = 1
    HERO_EQUIP_REFINE_ID = 2
    HERO_ARTIFACT_ENHANCE_ID = 3
    HERO_ARTIFACT_REFINE_ID = 4
    HERO_DESTINY_LEVEL = 30
    HERO_DESTINY_COST_RATIO = 10
    HERO_DESTINY_LIST = [2621304]
    HERO_HERO_ICON_ID = [1110001, 1110002, 1110003, 1110005, 1130003, 1120002, 1120004, 1120005, 1120006, 1120007,
                         1130001, 1140002, 1140003, 1140004, 1140005, 1140006, 1150002, 1150003, 1150004, 1150005,
                         1160001, 1160004, 1160005, 1140007, 1160007, 1120008]


    HERO_INIT_ACQUIRE = [1111000100, 112000400, 116000400, 114000700, 115000300]
    HERO_REPLACE_IDS = [114000400, 114000500, 116000300, 114000300, 112000700]
    HERO_TRAINING_PER_MINUTE_XPS = 6 #英雄训练每分钟6点经验


    MAX_LEVEL = 60 #装备等级上限
    PVP_LEVEL = 10 #pvp开启等级
    SIEGE_LEVEL = 14 #攻城战开启等级
    PVP_FRAGMENT_LEVEL = 18 #碎片抢夺开启等级
    PVP_FRAGMENT_START_HOUR = 10 #碎片抢夺开启时间
    PVP_CD_TIME = 180 #pvp 一场冷却时间
    PVP_DELETE_CD_TIME_COST = 50 # 冷却钻石花费

    SIEGE_PVP_CD_TIME = 300 #攻城战冷却时间
    SIEGE_DELETE_CD_TIME_COST = 50 #攻城战冷却钻石花费
    SIEGE_FORT_CD_TIME = 3600 #攻城战运输堡垒cd冷却时间
    SIEGE_REFRESH_COST_GOLD = 10000 #攻城战刷新对手消耗金币
    SIEGE_BASE_PVP_RATIO = 0.16 #攻城战英雄掠夺比率
    SIEGE_FORT_PVP_RATIO = 0.36 #攻城战移动堡垒掠夺比率
    SIEGE_REWARD_GASHAPON_ID = 4 #攻城战随机奖励抽奖ID

    CREATE_GUILD = 300
    RENAME_GUILD = 500
    JOIN_GUILD_LEVEL = 11 #11级允许加入公会
    GUILD_FIRE_OPEN_LEVELS = [1,5,10] #公会火炉开启需要公会等级
    RAID_MAX_COUNT = 2
    #PVP
    UPDATE_TIME_OPPONENTS = 3600 #秒
    #UPDATE_TIME_OPPONENTS = 600 #秒
    UPDATE_TIME_SERIE_WIN = 600
    SERIE_WIN_ADD_HONOR = 5
    SERIE_WIN_MAX_COUNT = 10
    CREATE_GUILD_LEVEL = 11
    GUILD_CONTRIBUTE_GOLD_COUNT = 20000
    GUILD_CONTRIBUTE_GOLD_XP = 50
    GUILD_CONTRIBUTE_DIAMOND_COUNT = 20
    GUILD_CONTRIBUTE_DIAMOND_XP = 5000 # 2017 2 20修改 原来值是100 测试要求临时改成5000
    GUILD_GOLD_GET = 30
    GUILD_DIAMOND_GET = 60
    GUILD_CHAIRMAN_POSITION = 1
    GUILD_VI_CHAIRMAN_POSITION = 2
    GUILD_NORMAL_POSITION = 3

    PVP_STOP_HOUR = 8 #10点
    PVP_STOP_WEEK = 1 #星期一
    PVP_WIN_HONOR = 50
    PVP_LOSE_HONOR = 10
    PVP_WIN_EXP = 0
    PVP_WIN_HERO_EXP = 0
    PVP_WIN_GOLDS = 1000
    PVP_INIT_SCORE = 1000
    PVP_SCORE_K = 50
    PVP_SUB_STAMINA = 0
    LOOT_SUB_STAMINA = 2
    SIEGE_SUB_STAMINA = 3

    PVP_RANK_RULE = [[2, 0.4, 0.1, 0, 15], [2, 0.5, 0.4, 5, 10], [1, 0.75, 0.5, 20, 5]]

    ITEM_TYPE_POWER = 1         #体力
    ITEM_TYPE_SP = 2            #耐力
    ITEM_TYPE_GOLD = 3          #金币
    ITEM_TYPE_SWEEP = 4         #扫荡卷
    ITEM_TYPE_KEY = 5           #宝箱钥匙
    ITEM_TYPE_BOX = 6           #宝箱
    ITEM_TYPE_XP = 7            #经验
    # ITEM_TYPE_WARAVOID = 8      #免战
    ITEM_TYPE_REFRESH_TICKET = 9#商店刷新劵
    ITEM_TYPE_HONORSTONE = 10   #荣誉石
    ITEM_TYPE_GOLDHAND = 11     #点金手
    ITEM_TYPE_EQUIPREFINESTONE = 15 #装备精炼石
    ITEM_TYPE_MATERIALCORE = 16 #元素之核
    ITEM_TYPE_PACEKAGE_ALL = 20  #多选包
    ITEM_TYPE_PACEKAGE_SINGLE = 21  #单选包
    ITEM_TYPE_FRUIT_FLOWER = 24  #花的果实
    ITEM_TYPE_FRUIT_TREE = 25  #树的果实

    ITEM_TYPE_WOODHAND = 999  #点木手

    STAR_CHEST_OPEN_COUNTS = [10,20,30] #领取宝箱获得星星限制
    ELITE_STAR_CHEST_OPEN_COUNTS = [7,14,21] #领取宝箱获得星星限制

    ITEM_HONORSTONE_ID = 2620801 #荣誉石
    ITEM_SWEEP_ID = 2620603 #扫荡券
    #ITEM_SWEEP_DIAMOND = 10
    ITEM_REFRESH_TICKET_ID = 2620601 #刷新劵
    ITEM_POWER_ID = 2620402 #体力
    ITEM_POWER_IDS = [2620401, 2620402, 2620403] #小中大鸡腿
    ITEM_SP_ID = 2620502 #耐力
    ITEM_SP_IDS = [2620501, 2620502, 2620503] #小中大啤酒
    ITEM_GOLDHAND_ID = 2621101#点金手
    ITEM_SLIVER_BOX_ID = 2620202 #银箱子
    ITEM_GOLD_BOX_ID = 2620203 #金箱子
    ITEM_WOODHAND_ID = 2621102#
    ITEM_TUTORIAL_XP_ID = 2620102 #强效经验药水
    ITEM_MIN_XP_ID = 2620101 #最小经验药水
    # ITEM_WARAVOID_TICKET_ID = 2620602 # 免战劵
    ITEM_GOLDHAND_INFO = [(1,5000), (2,2500), (3,1500), (5,700), (10,300)] #点金手暴击概率
    ITEM_WOODHAND_INFO = [(1,4000), (2,3000), (3,1000), (4,1000), (5,1000)]#点木手暴击概率
    ITEM_HERO_UPGRADE_ID = 2621201 #英雄升星特殊道具
    ITEM_TEAMSTONE_ID = 2621202
    ITEM_REFINE_ID = 2623101#精炼石
    ITEM_DIAMOND_GASHAPON_ID = 2610001#钻石单抽卡

    ELEMENTTOWER_CHOCIE_BUFF_COSTS = [3, 6, 9] #buff 消耗星星


    #ID
    GOLD_ID = 500000
    YUANBO_ID = 510000
    WOOD_ID = 600000
    XP_ID = 550000
    HONOR_ID = 530000
    GEMPOWDER = 540000
    SCORE_ID = 570000
    GUILDGOLD_ID = 770000 #公会币
    ITEM_XP_LIST = [2620105, 2620104, 2620103, 2620102, 2620101]
    ITEM_TRAIN_ID = 2627001
    ARTIFACRT_REFINE_LIST = [2624101]
    DEFAULT_ARTIFACRT_LIST = [1411505, 1412505, 1417505]
    ARTIFACRT_XP_LIST = [1409909, 1406909, 1403909, 1401909]

    #装备回炉是用于计算消耗钻石数量的系数，公式为  diamond = EQUIP_QUALITY_RATIO *  quality + EQUIP_LEVEL_RATIO * level + EQUIP_REFINELEVEL_RATIO * refineLevel
    EQUIP_QUALITY_RATIO = 100
    EQUIP_LEVEL_RATIO = 10
    EQUIP_REFINELEVEL_RATIO = 1
    EQUIP_GOLD_RATIO = 0.9
    EQUIP_ENHANCE_STEP = 5


    #圣物回炉是用于计算消耗钻石数量的系数，公式为  diamond = ARTIFACT_QUALITY_RATION *  quality + ARTIFACT_LEVEL_RATIO * level + ARTIFACT_REFINELEVEL_RATION * refineLevel

    ARTIFACT_QUALITY_RATION = 100
    ARTIFACT_LEVEL_RATIO = 10
    ARTIFACT_REFINELEVEL_RATION = 1

    PLAYER_POWER_FLUCTUATION_SECOND = 300 #体力5分钟回复1点
    PLAYER_STAMINA_FLUCTUATION_SECOND = 1800 #耐力30分钟回复1点
    PLAYER_BATTLEPOINT_FLUCTUATION_SECOND = 1800 #战斗点

    BUILDING_ALLIANCEBARRACK_PRODUCE_SOLDIER_RATIO = 32 #联盟兵营造兵容量
    BUILDING_HORDEBARRACK_PRODUCE_SOLDIER_RATIO = 32 #部落兵营造兵容量

    DAILYTASK_CATEGORY_GOLDHAND = 10 #点石成金
    DAILYTASK_CATEGORY_GASHAPON = 20 #召唤大师
    DAILYTASK_CATEGORY_INSTANCE = 30 #副本挑战
    DAILYTASK_CATEGORY_ELIT_INSTANCE = 31 #精英副本挑战
    DAILYTASK_CATEGORY_ENHANCE = 42 #装备强化
    DAILYTASK_CATEGORY_REFINE = 44 #装备精炼
    DAILYTASK_CATEGORY_TRAIN = 46 #英雄培养
    DAILYTASK_CATEGORY_WOOD = 48 #木材商人
    DAILYTASK_CATEGORY_PK_ARTIFACTFRAGMENT = 50 #圣物碎片抢夺
    DAILYTASK_CATEGORY_PK = 60 #竞技场挑战
    DAILYTASK_CATEGORY_ARRIFACT_UPGRADE = 70 #圣物强化
    DAILYTASK_CATEGORY_SMALLGAME = 79 #小游戏
    DAILYTASK_CATEGORY_ELEMENTTOWER_FIGHT = 80 #元素之塔
    DAILYTASK_CATEGORY_GUILD_CONTRIBUTE = 90 #公会捐献
    DAILYTASK_CATEGORY_RACE_INSTANCE = 100 #上古遗迹
    DAILYTASK_CATEGORY_HERO_LEVELUP = 110 #英雄技能升级
    DAILYTASK_CATEGORY_WELFARE = 120 #每日福利
    DAILYTASK_CATEGORY_VIP_SWEEP = 130 #vip扫荡券
    DAILYTASK_CATEGORY_PERMANENT_CARD = 140 #永久卡
    DAILYTASK_CATEGORY_MONTH_CARD = 150 #月卡
    DAILYTASK_CATEGORY_WEEK_CARD = 160 #周卡
    DAILYTASK_CATEGORY_BUY_POWER = 170 #双人套餐
    DAILYTASK_CATEGORY_LANCH = 180 #每日12:00至14:00可领取60点体力
    DAILYTASK_CATEGORY_DINNER = 190 #每日18:00至19:00可领取60点体力
    DAILYTASK_CATEGORY_SUPPER = 200 #每日21:00至24:00可领取60点体力

    TASK_CATEGORY_LEVELUP = 10 #升级系列任务
    TASK_CATEGORY_INSTANCE = 20 #普通副本
    TASK_CATEGORY_ELIT_INSTANCE = 30 #精英副本
    TASK_CATEGORY_HERO_STAR2_UPGRADE = 40 #英雄升星2
    TASK_CATEGORY_HERO_STAR3_UPGRADE = 50 #英雄升星3
    TASK_CATEGORY_HERO_STAR5_UPGRADE = 60 #英雄升星5
    TASK_CATEGORY_HERO_EVOLVE_UPGRADE_GREEN = 70 #英雄进阶绿色
    TASK_CATEGORY_HERO_EVOLVE_UPGRADE_BLUE = 80 #英雄进阶蓝色
    TASK_CATEGORY_HERO_EVOLVE_UPGRADE_PURPLE = 90 #英雄进阶紫色
    TASK_CATEGORY_ARENA_PK_SUCCESS = 140 #竞技场挑战胜利
    TASK_CATEGORY_CASTLE_LEVELUP = 300 # 要塞升級
    TASK_CATEGORY_SIEGE_TOTAL_COUNT = 320 # 攻城勝利
    TASK_CATEGORY_RAICE_WAVE_COUNT = 310 # 時空任務
    TASK_CATEGORY_WOOD_HARVEST = 290#木材场
    TASK_CATEGORY_GOLDENMINE_HARVEST = 200#金矿
    TASK_CATEGORY_RECHARGE = 230 #累计充值钻石
    TASK_CATEGORY_ARTIFACT_LEVELUP = 280 #提升任意圣物等级

    SEVEN_TASK_OVER = 8
    SEVEN_TASK_DAILY_BONUS_START_ID = 000
    SEVEN_TASK_CATEGORY_INSTANCE = 700 #副本
    SEVEN_TASK_CATEGORY_ALL_EQUIP_ENHANCE10 = 710
    SEVEN_TASK_CATEGORY_ALL_EQUIP_ENHANCE20 = 720
    SEVEN_TASK_CATEGORY_ALL_EQUIP_ENHANCE30 = 730
    SEVEN_TASK_CATEGORY_ALL_EQUIP_ENHANCE40 = 740
    SEVEN_TASK_CATEGORY_PVP_RANK = 750
    SEVEN_TASK_CATEGORY_EQUIP_COMPOSE = 760
    SEVEN_TASK_CATEGORY_ELEMENTTOWER_SUCCESS = 770 #元素之塔
    SEVEN_TASK_CATEGORY_GRAB_ARTIFACT = 780
    SEVEN_TASK_CATEGORY_FIVE_HERO_LEVELUP26 = 790
    SEVEN_TASK_CATEGORY_FIVE_HERO_LEVELUP28 = 800
    SEVEN_TASK_CATEGORY_FIVE_HERO_LEVELUP30 = 810
    SEVEN_TASK_CATEGORY_FIVE_HERO_LEVELUP32 = 820
    SEVEN_TASK_CATEGORY_FIVE_HERO_LEVELUP34 = 830
    SEVEN_TASK_CATEGORY_FIVE_HERO_LEVELUP36 = 840
    SEVEN_TASK_CATEGORY_FIVE_HERO_LEVELUP38 = 850
    SEVEN_TASK_CATEGORY_FIVE_HERO_LEVELUP40 = 860
    SEVEN_TASK_CATEGORY_ONE_EQUIP_REFINE = 870
    SEVEN_TASK_CATEGORY_ALL_EQUIP_REFINE5 = 880
    SEVEN_TASK_CATEGORY_ALL_EQUIP_REFINE10 = 890
    SEVEN_TASK_CATEGORY_GASHAPON = 910
    SEVEN_TASK_CATEGORY_BATTLE_POWER = 1010
    SEVEN_TASK_CATEGORY_HERO_UPGRADE_GREEN1 = 920
    SEVEN_TASK_CATEGORY_HERO_UPGRADE_GREEN2 = 930
    SEVEN_TASK_CATEGORY_HERO_UPGRADE_BLUE = 940
    SEVEN_TASK_CATEGORY_ACQUIRE_HREO = 950
    SEVEN_TASK_CATEGORY_HERO_STAR_UP_GREEN3 = 960
    SEVEN_TASK_CATEGORY_HERO_STAR_UP_GREEN5 = 970
    SEVEN_TASK_CATEGORY_HERO_STAR_UP_BLUE2 = 980
    SEVEN_TASK_CATEGORY_HERO_STAR_UP_BLUE5 = 990
    SEVEN_TASK_CATEGORY_HERO_STAR_UP_PURPLE = 1000

    # SEVEN_TASK_CATEGORY_ONE_HERO_DESTINY_LEVEL = 1020
    # SEVEN_TASK_CATEGORY_FIVE_HERO_DESTINY_LEVEL5 = 1030
    # SEVEN_TASK_CATEGORY_FIVE_HERO_DESTINY_LEVEL8 = 1040
    SEVEN_TASK_CATEGORY_HERO_DESTINY_LEVEL1 = 1020
    SEVEN_TASK_CATEGORY_HERO_DESTINY_LEVEL3 = 1030
    SEVEN_TASK_CATEGORY_HERO_DESTINY_LEVEL5 = 1040

    SEVEN_TASK_CATEGORY_RECHARGE_LIST = [1070, 1080, 1090, 1100, 1110, 1120,1130,1140, 1180, 1190, 1200, 1210, 1320]
    #第一天累计充值
    SEVEN_TASK_CATEGORY_RECHARGE1 = 1070
    #第二天累计消费
    SEVEN_TASK_CATEGORY_COST2 = 1090
    #第三天单冲
    SEVEN_TASK_CATEGORY_SINGLE_RECHARGE3_6 = 1110
    SEVEN_TASK_CATEGORY_SINGLE_RECHARGE3_12 = 1120
    SEVEN_TASK_CATEGORY_SINGLE_RECHARGE3_30 = 1130
    SEVEN_TASK_CATEGORY_SINGLE_RECHARGE3_50 = 1140
    #第四天累计充值
    SEVEN_TASK_CATEGORY_RECHARGE4 = 1080

    #第五天累计消费
    SEVEN_TASK_CATEGORY_COST5 = 1100

    #第六天单冲
    SEVEN_TASK_CATEGORY_SINGLE_RECHARGE6_6 = 1180 #6元
    SEVEN_TASK_CATEGORY_SINGLE_RECHARGE6_12 = 1190 #12元
    SEVEN_TASK_CATEGORY_SINGLE_RECHARGE6_30 = 1200 #30元
    SEVEN_TASK_CATEGORY_SINGLE_RECHARGE6_50 = 1210 #50元

    #第七天
    SEVEN_TASK_CATEGORY_COST7 = 1320 #累计充值

    TUTORIAL_ID_INIT_1 = 200  # 初始化
    # TUTORIAL_ID_INSTANCE_2 = 300 # 暂时没有用到
    TUTORIAL_ID_GASHAPON_2 = 400 #　抽奖小那家
    TUTORIAL_ID_INSTANCE_1ST_3 = 500
    TUTORIAL_ID_EQUIP_UP_4 = 600
    TUTORIAL_ID_BLACK_SMITH_5 = 700
    TUTORIAL_ID_EQUIP_ENHANCE_6 = 701
    TUTORIAL_ID_GOLDEN_7 = 800
    TUTORIAL_ID_LOGFIELD_8 = 801
    TUTORIAL_ID_TAVERN_9 = 1000
    TUTORIAL_ID_HEROCOMPOSE_10 = 1001
    TUTORIAL_ID_HEROCOMPOSE2_11 = 1002
    TUTORIAL_ID_ADD_XP_12 = 1100
    TUTORIAL_ID_SKILL_LEVELUP_13 = 1200
    TUTORIAL_ID_HERO_UPGRADE_15 = 1400
    TUTORIAL_ID_CASTLE_LEVELUP_16 = 1500
    TUTORIAL_ID_ARENA_BUILD_17 = 1501
    TUTORIAL_ID_CASTLE_LEVELUP3_18 = 1600
    TUTORIAL_ID_INSTANCE_16 = 1700
    TUTORIAL_ID_INSTANCE_17 = 1800
    TUTORIAL_ID_INSTANCE_18 = 1900
    #TUTORIAL_ID_INSTANCE_19 = 2000
    TUTORIAL_ID_ELITE_INSTANCE = 21110



    TUTORIAL_ID_MAIL = 99999999

    GROW_GOLD_ACTIVITY_MOJO = 999

    TUTORIALS = [TUTORIAL_ID_GASHAPON_2, TUTORIAL_ID_INSTANCE_1ST_3,  TUTORIAL_ID_EQUIP_UP_4, TUTORIAL_ID_BLACK_SMITH_5, TUTORIAL_ID_EQUIP_ENHANCE_6, TUTORIAL_ID_GOLDEN_7,TUTORIAL_ID_LOGFIELD_8, TUTORIAL_ID_TAVERN_9, TUTORIAL_ID_HEROCOMPOSE_10,TUTORIAL_ID_HEROCOMPOSE2_11 , TUTORIAL_ID_ADD_XP_12,
                 TUTORIAL_ID_SKILL_LEVELUP_13,TUTORIAL_ID_HERO_UPGRADE_15, TUTORIAL_ID_CASTLE_LEVELUP_16, TUTORIAL_ID_ARENA_BUILD_17, TUTORIAL_ID_MAIL]

    DAILYTASK_MEALS_INFO = {DAILYTASK_CATEGORY_LANCH: [12, 14], DAILYTASK_CATEGORY_DINNER:[18, 19], DAILYTASK_CATEGORY_SUPPER:[21, 24]}




    GEMSHOP_REFRESH_YUANBO = 40 #宝石商店刷新消耗元宝
    MYSTERYSHOP_REFRESH_YUANBO = 50 #神秘商店刷新消耗元宝
    MYSTERYSHOP_MAX_GRID = 24 #神秘商店格子数量
    SHOP_MAX_BUY_COUNT = 9999

    HONORSHOP_REFRESH_YUANBO = 200 #荣誉商店刷新消耗钻石
    #HONORSHOP_REFRESH_HONOR = 800 #荣誉商店刷新消耗荣誉


    ARTIFACT_ENHANCE_XP_RATIO = 0.6 #圣物强化已有经验折算
    ARTIFACT_FRAGMENG_GRAB_LIST = [1401909, 1403909, 1406909, 1409909] #圣物碎片可任意抢夺列表

    WARRIOR_WALL_ID = 190000000

    HERO_UPGRADE_POWERRANKS = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,11000,12000]
    HERO_STAR_POWERRANKS = [[80,86,92],[100,112,124],[120,138,156],[144,168,192],[168,198,228],[196,232,268],[224,266,308],[252,300,348],[280,334,388],[336,396,456],[400,466,533]]
    HERO_BIGSPELL_POWERRANK_RATIO = 80 #技能大招系数
    HERO_SMALLSPELL_POWERRANK_RATIO = 40 #技能小招系数
    ARTIFACT_UPGRADE_POWERRANK_RATIO = 100 #圣物品质系数
    ARTIFACT_LEVEL_POWERRANK_RATIO = 2 #圣物等级系数

    SWEEP_VIP_LEVEL = 4 #vip 扫荡等级

    STATUE_SMALL_MAX_COUNT = 3 #可建造神像的最大数量
    STATUE_RESUPERIOR_MAX_COUNT = 2
    STATUE_BEST_MAX_COUNT = 1

class ErrorID(object):
    #前后台数据不一致
    SUCCESS = 200
    ERROR_DATA_ERROR = 500
    ERROR_SIGN = 10000  #加密错误
    ERROR_LOGIN_TIMEOUT = 1000  #不提示，直接重新登录
    ERROR_LOGIN_ERROR_USER = 1001  #登录用户不匹配，直接重新登录
    ERROR_TIME_CHANGED_ERROR = 1002 #修改时间
    ERROR_TIME_ERROR = 1003  #使用加速器
    ERROR_ACCOUNT_LOGIN_ON_OTHER_DEVICE = 1004  #多设备检查
    ERROR_BANNED = 1005 # 封号中

class AlertID(object):
    ALERT_GOLD_NOT_ENOUGH = 1 #金币不足
    ALERT_DIAMOND_NOT_ENOUGH = 2 #钻石不足
    ALERT_COURAGEPOINT_NOT_ENOUGH = 3 #勇气勋章不足
    ALERT_HONOR_NOT_ENOUGH = 4 #荣誉勋章不足
    ALERT_LEVEL_NOT_ENOUGH = 5 #当前英雄等级不足
    ALERT_GEMCOIN_NOT_ENOUGH = 6 #宝石粉末不足
    ALERT_SOUL_NOT_ENOUGH = 7 #灵魂石不足
    ALERT_POWER_NOT_ENOUGH = 8 #体力不足
    ALERT_STAMINA_NOT_ENOUGH =9 #耐力不足
    ALERT_LEVEL_SHORTAGE = 10 #等级不足
    ALERT_GEM_NOT_ENOUGH = 11 #宝石不存在
    ALERT_UPGRADE_NOT_ENOUGH = 12 #当前阶级不足
    ALERT_SCORE_NOT_ENOUGH = 13 #当前积分不足
    ALERT_TEAMLEVEL_NOT_ENOUGH = 14 #当前组队等级不足
    ALERT_PLAYER_LEVEL_NOT_ENOUGH = 15 #玩家等级不足
    ALERT_PLAYER_VIP_LEVEL_NOT_ENOUGH = 16 #玩家VIP等级不足
    ALERT_RESET_PVP_COUNT_NOT_ENOUGH = 17 #每日重置竞技场次数已经用完。
    ALERT_WOOD_NOT_ENOUGH = 18 #木材不足。
    ALERT_GUILD_GOLD_NOT_ENOUGH = 19 #公会币不足。
    ALERT_TOWER_GOLD_NOT_ENOUGH = 20 #元素币不足。



    #物品相关
    ALERT_ITEM_NOT_ENOUGH = 100  #数量不足
    ALERT_ITEM_LIMITBUY = 101 #购买超出上限

    #荣誉商店
    ALERT_ARENASHOP_CAN_NO_EXCHANGE = 150 #无法兑换

    #圣物
    ALERT_ARTIFACT_COMPOSE_MATERIAL_NOT_ENOUGH = 200 #圣物合成材料不足

    #建筑
    ALERT_BUILDING_MATERIAL_NOT_ENOUGH = 250  #材料不足
    ALERT_BUILDING_BUILD_OVER_MAX_NUMBER = 251 #数量已达上限
    ALERT_BUILDING_IS_UPGRADING = 252 #正在升级
    ALERT_BUILDING_IS_PRODUCING = 253 #正在造兵
    ALERT_BUILDING_IS_NOT_UPGRADING = 254 #未开始升级
    ALERT_BUILDING_POPULATION_OVER_MAX_NUMBER = 255 #训练士兵超过人口上限
    ALERT_BUILDING_SOLDIER_OVER_MAX_NUMBER = 256 #训练士兵超过训练上限
    ALERT_BUILDING_SOLDIER_DRILL_MATERIAL_NOT_ENOUGH = 257 #训练士兵材料不足
    ALERT_BUILDING_SPEED_CAN_NOT = 258 #无法加速
    ALERT_BUILDING_HARVEST_CAN_NOT = 259 #无法采集
    ALERT_BUILDING_CASTLE_LEVEL_NOT_ENOUGH = 260 #主城等级不足
    ALERT_BUILDING_HORDELAB_LEVEL_NOT_ENOUGH = 261 #图腾等级不足


    #装备
    ALERT_EQUIP_HERO_TYPE_ERROR = 300 #该装备与英雄类型不匹配
    ALERT_ARTIFACT_CAN_NOT_WEAR = 301 #圣物无法穿戴
    ALERT_EQUIP_CAN_NOT_WEAR = 302 #装备无法穿戴
    ALERT_EQUIP_UPGRADE_GEM_NOT_ENOUGH = 303 #进阶条件不足
    ALERT_EQUIP_COMPOSE_FRAGMENT_NOT_ENOUGH = 304 #装备碎片数量不足
    ALERT_EQUIP_GEM_IN_ERROR = 305 #宝石镶嵌错误
    ALERT_EQUIP_GEM_NOT_ENOUGH = 306 #宝石数量不足
    ALERT_EQUIP_BINDING_OTHER_HERO = 307 #装备已经和其他英雄绑定
    ALERT_EQUIP_IS_ON_HERO = 308 #装备已穿戴，请卸下再解绑
    ALERT_EQUIP_IS_ALREADY_UNBINDING = 309 #装备未绑定，无法解绑
    ALERT_EQUIP_CAN_NOT_MELT = 310 #装备无法回炉
    ALERT_EQUIP_CAN_NOT_DECOMPOSE = 311 #装备无法分解

    ALERT_ARTIFACT_CAN_NOT_REFINE = 312  #圣物无法精炼
    ALERT_ARTIFACT_CAN_NOT_MELT = 313  #圣物无法回炉
    ALERT_EQUIP_CAN_NOT_REFINE = 314  #装备无法精炼
    ALERT_EQUIP_IS_NOT_EXISTS = 315 #装备不存在


    #宝石
    ALERT_GEM_COMPOSE_NOT_ENOUGH = 350 #宝石合成数量不足
    ALERT_GEM_SHOP_CAN_NOT_EXCHANGE = 351 #无法兑换
    ALERT_GEM_SHOP_DIAMOND_REFRESH_OVER_TIME = 352 #钻石刷新超过上限

    #英雄
    ALERT_HERO_INIT_ERROR = 400 #无法重生
    ALERT_HERO_COMPOSE_SOUL_NUMBER_NOT_ENOUGH = 401 #灵魂碎片数量不足
    ALERT_HERO_ALREADY_EXSIT = 402 #英雄已存在
    ALERT_HERO_UPGRADE_LEVEL_NOT_ENOUGH = 403 #英雄进阶等级不足
    ALERT_HERO_UPGRADE_PLAYER_LEVEL_NOT_ENOUGH = 404 #玩家等级不足，暂时无法进阶
    ALERT_HERO_UPGRADE_MATERIAL_NOT_ENOUGH = 405 #英雄进阶材料不足
    ALERT_HERO_SKILL_LEVELUP_ERROR = 406 #英雄技能无法升级
    ALERT_HERO_SKILL_LEVELUP_LEVEL_NOT_ENOUGH = 407 #英雄等级不足，技能无法升级
    ALERT_HERO_SKILL_LEVELUP_MATERIAL_NOT_ENOUGH = 408 #技能升级材料不足
    ALERT_HERO_STAR_UPGRADE_MATERIAL_NOT_ENOUGH = 409 #素材不足（万能碎片不足）
    ALERT_HERO_POS_HAS_EQUIP = 410 #请先卸下该位置装备
    ALERT_HEROTEAM_LEVEL_IS_MAX = 411 #战队等级已经是最高
    ALERT_HERO_HP_NOT_ENOUGH = 412 #英雄血量已空无法上阵

    #神秘商店
    ALERT_MYSTERYSHOP_CAN_NOT_EXCHANGE = 450 #无法兑换
    ALERT_MYSTERYSHOP_DIAMOND_REFRESH_OVER_TIME = 451 #神秘商店刷新超过上限
    #vip
    ALERT_VIP_CAN_NOT_BUY = 500 #无法购买VIP礼包

    #任务
    ALERT_DAILYTASK_UNDONE = 550 #每日任务未达成
    ALERT_TASK_UNDONE = 551 #任务未达成
    ALERT_DAILYTASK_REWARD_RECEIVED=552 # 奖励已经领取，今日不可再次领取
    ALERT_DAILYTASK_ACTIVITY_NOT_ENOUGH = 553 # 活跃度不够暂时不能打开此宝箱
    ALERT_SEVENDAYS_IS_NOT_ALLOWED = 554 # 当前时间不在打开宝箱的时间范围内
    ALERT_SEVENDAYS_ONLY_ONCE = 555 # 半价商品只允许购买一次

    #PVP
    ALERT_PVP_FRAGMENT_HOUR_OVERTIME = 600 #pvp抢夺碎片0-8点无法抢夺真人
    ALERT_PVP_FRAGMENT_CAN_NOT_FIGHT = 601 #碎片无法抢夺
    ALERT_IS_IN_GUILD = 602 # 已经加入某个公会，无法创建
    ALERT_GUILD_ALREADY_EXITS = 603 # 公会名字已经存在请更换
    ALERT_PLAYER_HAS_NO_INSPEEDING_HERO = 604 # 选择的玩家没有英雄处于训练加速状态
    ALERT_AUCTION_PRICE_IS_TOP = 605 # 选择的商品已经被其他玩家拍得。
    ALERT_AUCTION_HAS_AUCED = 606 # 您已经对这件商品出价过，不允许再次对出价。
    ALERT_AUCTION_HAS_CLOSED = 607 # 这件商品已经下架，请更新信息。
    ALERT_GUILD_LIMIT_NOT_ENOUGH = 608 # 只有社长才可以创建或者更改火堆。
    ALERT_GUILD_NOT_ALLOWED_JOIN = 609 # 此公会被设置为不允许加入
    ALERT_PLAYER_HAS_NO_SPEEDING_COUNT = 610 # 您今日为他人加速次数已经用完。
    ALERT_PLAYER_HAS_NO_BE_SPEEDED_COUNT = 611 # 选择的玩家的被加速已经用完。

    ALERT_GUILD_LIMIT_CAN_NOT_KICK_MEMBERS = 612 # 您的权限不可以踢出被选玩家。
    ALERT_GUILD_LIMIT_CAN_NOT_OPEN_INSTANCE = 613 # 您的权限不可以开启副本。
    ALERT_GUILD_CHAIRMEN_INSTANCE_NOT_ENOUGH = 614 # 会长未通关相应章节的普通副本。

    ALERT_GUILD_INSTANCE_IS_FIGHTING = 615 # 公会副本有人正在攻打
    ALERT_GUILD_INSTANCE_HAS_ALREADY_FIGHTED = 616 # 公会副本已经挑战过，不可以再次挑战
    ALERT_GUILD_INSTANCE_HAS_ALREADY_EXPIRED = 617 # 公会副本已经关闭。
    ALERT_GUILD_INSTANCE_HAS_NOT_OPEN = 618 #　管理员还未开启此副本
    ALERT_GUILD_MEMBERS_HAS_FULL = 619 #　此公会已经满员了
    ALERT_GUILD_CONTRIBUTE_HAS_FULL = 620 #　今日捐献的次数已经用完
    ALERT_GUILD_LIMIT_NOT_ENOUGH_TO_POSITION_UP = 621 # 权限不可以给对方升职
    ALERT_SPEED_CAN_NOT_FOR_SELF = 622 # 不可以为自己进行加速
    ALERT_PLAYER_IS_SPEEDING_NOW = 623 # 您所选择的玩家正处在被加速状态，不可重复尽心加速
    ALERT_GUILD_VICHAIRMAN_COUNT_HAS_TOP = 624 # 副会长个数达到上限，不可以升职。
    ALERT_GUILD_HAD_APPLIED_ALREADY = 625 #已经申请加入该工会
    ALERT_GUILD_INSTANCE_LEVEL_LIMIT = 626  #公会等级达到2级才能开启副本

    ALERT_SIEGE_BATTLE_PLAYER_ONLINE = 630 #玩家在线
    ALERT_SIEGE_BATTLE_PLAYER_SAME_GUILD = 631 #玩家同工会
    # ALERT_SIEGE_BATTLE_PLAYER_IN_WARAVOID = 632 #玩家免战
    ALERT_SIEGE_BATTLE_PLAYER_IS_REFRESH = 633 #列表已刷新。请重新选择对手


    #副本
    ALERT_INSTANCE_NOT_OPEN = 650 #副本为开启
    ALERT_INSTANCE_MINI_ALREADY_FIGHT = 651 #该关卡无法战斗
    ALERT_INSTANCE_FIGHT_COUNT_EXCEED_MAX = 652 #关卡战斗次数超过上限
    ALERT_INSTANCE_CAN_NOT_SWEEP = 653 #难度不足，无法扫荡
    ALERT_INSTANCE_SWEEP_VIP_ERROR = 654 #VIP等级不足，无法使用钻石扫荡
    ALERT_INSTANCE_ITEM_SWEEP_NOT_ENOUGH = 655 #扫荡券不足，无法扫荡
    ALERT_INSTANCE_REFRESH_COUNT_EXCEED_MAX = 656 #刷新次数超过上限
    ALERT_INSTANCE_CHEST_CAN_NOT_OPEN = 657 #宝箱无法打开
    ALERT_INSTANCE_CHEST_ALREADY_OPEN = 658 #宝箱已经打开
    ALERT_RAID_INSTANCE_IS_NOT_OPEN = 659 #活动副本暂未开启
    ALERT_SPACETIME_FLIP_NUMBER_NOT_ENOUGH = 670 #时空之穴寻宝次数不足
    ALERT_SPACETIME_FLIP_POS_IS_FLIPED = 671 #时空之穴对应位置已经开启，无法再次寻宝
    ALERT_SPACETIME_RESET_NUMBER_NOT_ENOUGH = 672 #时空之穴刷新次数超过上限
    ALERT_SPACETIME_FIGHT_STAGE_ERROR = 673 #时空之穴只能打当前关卡
    ALERT_SPACETIME_FIGHT_STAGE_OVER = 674 #时空之穴关卡已通关

class ErrorCode(object):
    """
        后台错误码
    """
    ERROR_PLAYER_IS_NONE = 100 # 用户不存在
    ERROR_SET_FAILED = 101 # 设置失败
    ERROR_PARAMETER_FORMAT = 102 # 参数的合适不正确
    