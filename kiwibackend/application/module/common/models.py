# -*- encoding:utf8 -*-
import datetime

class CommonStaticModels(object):
    "静态数据抽象类"
    #def __getattribute__(self, name):  
    #    if name.endswith("_list"):
    #        name = "%s_str" % name[0:-5]
    #        value = object.__getattribute__(self, name)
    #        return [] if not value.strip() else value.strip().split(",")
    #    else:
    #        return object.__getattribute__(self, name)


    def to_dict(self):
        values = self.__dict__
        dicts = {}

        for name, value in values.items():
            if name.startswith("_"):
                continue
                
            if name.endswith("_str"):
                name = name[0:-4]
                dicts[name] = [] if not value.strip() else [ str(i) for i in value.strip().split(",") if i.strip()]
            elif name.endswith("_float"):
                name = name[0:-6]
                dicts[name] = [] if not value.strip() else [ float(i) for i in value.strip().split(",") if i.strip()]
            elif name.endswith("_int"):
                name = name[0:-4]
                dicts[name] = [] if not value.strip() else [ int(float(i)) for i in value.strip().split(",") if i.strip()]
            else:
                if isinstance(value, datetime.datetime):
                    continue
                dicts[name] = value.strip() if type(value) in [str, unicode] else value

        return dicts

