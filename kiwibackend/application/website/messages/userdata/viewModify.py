# -*- encodings:utf8 -*-
from messages.userdata import BaseUserData

class ViewUpdate(BaseUserData):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.buyRecords = []
        self.artifacts = []
        self.buildings = []
        self.buildingFragments = []
        self.buildingPlants = []
        self.dailytasks = []
        self.sevenDaystasks = []
        self.equipFragments = []
        self.equips = []
        self.artifactFragments = []
       # self.gemFragments = []
       # self.gems = []
        self.heroes = []
        self.heroTeams = []
        self.items = []
        self.souls = []
        self.tasks = []
        self.mails = []
        self.battlerecords = []
        self.activities = []
        self.friends = []
        self.friendRelations = []
        self.defenseHeroIds=[] 
        self.defenseSiegeIds=[]
        self.defenseSiegeSoldierIds = []
        #self.playerWarriorIds=[]
        self.wallWarriorIds = []
        self.safedTime = 0
        # self.endLockedTime = 0

class ViewDelete(BaseUserData):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.artifacts = []
        self.buildings = []
        self.buildingFragments = []
        self.buildingPlants = []
        self.equipFragments = []
        self.equips = []
        self.artifactFragments = []
        #self.gemFragments = []
        #self.gems = []
        self.souls = []
        self.tasks = []
        self.mails = []
        self.battlerecords = []
        self.heroes = []
        self.heroteams = []
        self.items = []
        self.friends = []
        self.friendRelations = [] 
        self.dailytasks = []
        self.sevenDaystasks = []
        

