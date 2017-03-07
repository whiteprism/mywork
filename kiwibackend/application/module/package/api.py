# -*- coding: utf-8 -*-
from package.models import Package, PackageReward, PackageCode
from django.conf import settings
import simplejson
import random
import datetime
from utils import datetime_to_unixtime

def update_package_cache():
    Package.create_cache()
    PackageReward.create_cache()

def get_package(pk):
    return Package.get(pk)

def get_package_code(pk):
    try:
        package_code = PackageCode.objects.get(pk=pk)
    except:
        package_code = None

    return package_code

def generate_package_code(package):
    """
    根据礼包生成激活码
    """

    codes = []
    random_strs = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"

    while len(codes) < package.code_count:
        random_str = random.sample(random_strs, 1)+ random.sample(random_strs, 1)+random.sample(random_strs, 1)+random.sample(random_strs, 1)+random.sample(random_strs, 1)+random.sample(random_strs, 1)
        code = "".join(random_str)
        
        if code in codes:
            continue

        codes.append(code)

    code_txt_file = "%s/../data/json/%s/packages/package_%s.txt" % (settings.ROOT_PATH, package.tag, package.pk)
    code_json_file = "%s/../data/json/%s/packages/package_%s.json" % (settings.ROOT_PATH, package.tag, package.pk)

    code_txt_handle = open(code_txt_file, "w")
    code_json_handle = open(code_json_file, "w")
    code_jsons = []

    for _code in codes:
        code = "%s%s" %(package.pk, _code)
        code_txt_handle.write(code)
        code_txt_handle.write("\n")
        
        code_jsons.append({
            "pk":code,
            "model":"package.packagecode",
            "fields":{
                "package_id": package.pk,
                "is_use": False,
                "use_serverid": "",
                "use_playerid": 0,
                "created_at": str(datetime.datetime.now()),
                "used_at": str(datetime.datetime.now()),
            }
        })

    code_txt_handle.close()

    code_json_handle.write(simplejson.dumps(code_jsons,indent=1))
    code_json_handle.close()
