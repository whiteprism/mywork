class PBViewInstance():
    def __init__(self):
        self.hasStarData = false
        self.history = []
        self.historyNew = []
        self.lastFinished = false
        self.lastLevelId = -1
        self.lastEliteFinished = false
        self.lastEliteLevelId = -1
        self.starData = []
        self.sweepCoolDown = -1
