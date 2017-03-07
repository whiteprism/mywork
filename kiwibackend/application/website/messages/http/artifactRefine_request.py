# -*- encoding:utf8 -*-
from messages.http import  BaseHttp
class ArtifactRefineRequest(BaseHttp):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.itemIds = []
        self.artifactId = -1
        self.artifactIds = []

