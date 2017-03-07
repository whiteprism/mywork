class PBCommonResponse():
    def __init__(self):
        self.activityConfs = []
        self.city = None #PBViewUser
        self.conf = None #PBConf
        self.create = None #PBViewCreate
        self.delete = None #PBViewDelete
        self.error = -1
        self.hasActConf = false
        self.hasActivationCode = false
        self.hasMailId = false
        self.hasMojoConf = false
        self.mailIds = []
        self.mojoConfs = []
        self.notifications = []
        self.server = ""
        self.serverTimestamp = -1
        self.success = false
        self.update = None #PBViewUpdate
