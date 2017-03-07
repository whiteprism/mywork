class PBGetServerListMessage_PBResponse():
    def __init__(self):
        self._account = None #PBViewUserAccount
        self.lastServerIdInt = -1
        self.lastServerIds = []
        self._ppacNotice = ""
        self.servers = []
        self._ssoToken = ""
        self.suggestServerIdInt = -1
        self.userServers = []
