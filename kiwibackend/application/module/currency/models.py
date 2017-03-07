# -*- coding: utf-8 -*-

class Currency(object):
    """
    货币
    """
    def __init__(self, gid):
        self.type = gid
        self.quality = 0

    @property
    def is_yuanbo(self):
        return self.get_idType(self.type) == 51

    @property
    def is_gold(self):
        return self.get_idType(self.type) == 50

    @property
    def is_couragepoint(self):
        return self.get_idType(self.type) == 52

    @property
    def is_honorpoint(self):
        return self.get_idType(self.type) == 53

    #@property
    #def is_gempowder(self):
    #    return self.get_idType(self.type) == 54

    @property
    def is_xp(self):
        return self.get_idType(self.type) == 55

    def get_idType(self, Id):
        return int(str(Id)[0:2])

    @property
    def obj_id(self):
        return self.type

def get_currency(pk):
    return Currency(pk) 
