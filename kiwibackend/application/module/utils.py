# -*- coding: utf-8 -*-
import random
#from random import randint
from datetime import datetime, timedelta
import xml.dom.minidom, sys, os
#from functools import wraps
#import logging
#import msgpack
from website.mobile.views.namefilter import BAN_NAMES
from time import mktime
import math
import re
#import hashlib
#from django.conf import settings
#from django.db import models
#import inspect


PART_1_NAMES = []
PART_2_NAMES = []

def datetime_to_unixtime(t):
    """
    datetime -> unix时间戳
    """
    return mktime(t.timetuple())+1e-6*t.microsecond

def unixtime_to_datetime(t):
    """
    unix时间戳 -> datetime
    """
    return datetime.fromtimestamp(t)

def random_items_pick(item_list, number=1):
    ''' 
    [('a', 1), ('b', 2)] 
    '''
    
    items = []
    for i in range(0, number):
        item, index = random_item_pick(item_list)
        items.append(item)
        del item_list[index]

        if len(item_list) == 0:
            break
    return items

def random_item_pick(item_list):
    ''' 
    [('a', 1), ('b', 2)] 
    '''

    index = 0
    item = 0

    total_probalibity = 0 
    for item, item_probability in item_list:
        total_probalibity += item_probability
    x = random.uniform(0, total_probalibity)

    cumulative_probability = 0 

    for item, item_probability in item_list:
        # 確率加算
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
        index += 1
    return item, index

#def is_over_24h(date_time):
#    '''
#    时间相差24小时
#    '''
#    delta = datetime.now() - date_time
#    return delta.days > 0
#    
#
#def get_past_days(date_time):
#    '''
#    时间差
#    '''
#    date_time = to_ingame_datetime(date_time)
#    dt = datetime.now()
#    dt = to_ingame_datetime(dt)
#    return dt.day - date_time.day
#
#def is_past_day(date_time):
#    '''
#    是否为今天以前的时间
#    '''
#    days = get_past_days(date_time)
#    return days > 0
#
#def is_game_today(check_datetime):
#    now = datetime.now() # 今
#    today = now
#    tomorrow = now + timedelta(1) # 明日
#    start_datetime = datetime(today.year, today.month, today.day) 
#    end_datetime = datetime(tomorrow.year, tomorrow.month, tomorrow.day) 
#    if check_datetime >= start_datetime and check_datetime < end_datetime:
#        return True
#    else:
#        return False
#
def is_digits(number):
    '''
    是否为整形
    '''
    return isinstance(number, long) or isinstance(number, int)
#
#def clamp(value, min_value, max_value):
#    return min(max(value, min_value), max_value)
#
## test_bit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.
#
#def test_bit(int_type, offset):
#    mask = 1 << offset
#    return(int_type & mask)
#
## set_bit() returns an integer with the bit at 'offset' set to 1.
#
#def set_bit(int_type, offset):
#    mask = 1 << offset
#    return(int_type | mask)
#
## clear_bit() returns an integer with the bit at 'offset' cleared.
#
#def clear_bit(int_type, offset):
#    mask = ~(1 << offset)
#    return(int_type & mask)
#
## toggle_bit() returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0.
#
#def toggle_bit(int_type, offset):
#    mask = 1 << offset
#    return(int_type ^ mask)
#
#def count_bit(integer):
#    count = 0
#    for b in range(32):
#        mask = 1 << b
#        if integer & mask:
#            count += 1
#    return count
#
#def bit_index_list(integer):
#    result = []
#    for b in range(32):
#        mask = 1 << b
#        if integer & mask:
#            result.append(b)
#
#    return result
#
#
#def getcallerinfo(depth=0):
#    fr = inspect.currentframe()
#    try:
#        depth = 1 + depth
#        for i in range(depth):
#            fr = fr.f_back
#            if fr is None:
#                return '<no caller>'
#        fi = inspect.getframeinfo(fr, 0)
#        if fi[2] == '<module>':
#            return '(%s:%d)' % (fi[0], fi[1])
#        else:
#            return '%s() (%s:%d)' % (fi[2], fi[0], fi[1])
#    finally:
#        del fr
#
#def get_weight(obj, weight_property):
#    weight = 0
#    if isinstance(obj, dict):
#        weight = obj.get(weight_property, 0)
#    elif isinstance(obj, (tuple, list)):
#        if isinstance(weight_property, int) and weight_property < len(obj):
#            weight = obj[weight_property]
#    else:
#        weight = obj.getattr(weight_property, 0)
#    try:
#        return int(weight)
#    except:
#        return 0
#
#def w_choice(choice_weight = None, choices = None, weight_property = 'weight'):
#    if choices and weight_property:
#        possibility = random.randint(1, sum([get_weight(i, weight_property) for i in choices]))
#        for i in choices:
#            possibility -= get_weight(i, weight_property)
#            if possibility <= 0:
#                return i
#        return i
#    elif choice_weight:
#        possibility = random.randint(1, sum(choice_weight.itervalues()))
#        for value, weight in choice_weight.iteritems():
#            possibility -= weight
#            if possibility <= 0:
#                return value
#        return value
#    return None
#
#SETTINGS_NAME_TODAY = 'TODAY'
#DATE_FORMAT = '%Y/%m/%d'
#DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'
#
#def get_today():
#    """
#       TODAY = '2010/09/01'
#       TODAY = '2010/09/01 12:34:56'
#    """
#    if hasattr(settings, SETTINGS_NAME_TODAY):
#        datestr = getattr(settings, SETTINGS_NAME_TODAY)
#        if len(datestr) == 10:
#            return datetime.strptime(datestr, DATE_FORMAT)
#        else:
#            return datetime.strptime(datestr, DATETIME_FORMAT)
#
#    return datetime.today()

def step_count(init_value, step_value, number):
    """
    递增
    """
    total_value = 0
    end_value = init_value
    for n in range(number):
        total_value += end_value 
        end_value += step_value
    return end_value, total_value  

def delta_time(start_datetime, end_datetime=None):
    '''
    现在距离date_time的时间差
    返回时间戳
    '''
    start_time = mktime(start_datetime.timetuple())
    if not end_datetime:
        end_datetime = datetime.now()
    end_time = mktime(end_datetime.timetuple())
    return int(math.ceil(end_time - start_time))

def random_name():
    '''
    随机名字
    '''
    if not PART_1_NAMES and not PART_2_NAMES:
        path = os.path.dirname(__file__) + "/../../data/name.xml"
        nameXml = xml.dom.minidom.parse(path)
        root =nameXml.getElementsByTagName("root")[0]
        all_name = root.getElementsByTagName("i")
        for name in all_name:
            k = name.getElementsByTagName("k")[0].firstChild.data
            name_type, _ = str(k).split("_")
            zh = name.getElementsByTagName("zh")[0].firstChild.data
            if name_type == "familyName":
                PART_1_NAMES.append(zh)
            elif name_type == "firstName":
                PART_2_NAMES.append(zh)
    r_name = random.choice(PART_1_NAMES) + random.choice(PART_2_NAMES)
    if _check_name(r_name) != 1:
        return random_name()
    return r_name

def _check_name(name):
    status = 1
    if len(name) < 2 or len(name) > 6:
        status = 3
    else:
        match = re.match(ur'[\u4e00-\u9fa5\w]+', name)
        if not match or match.group(0) != name:
            status = 4
        else:
            if name in BAN_NAMES:
                status = 5
            if u"强奸" in name or u"钓鱼岛" in name or u"尖阁列岛" in name:
                status = 5
            from player.api import player_name_exsited
            if player_name_exsited(name):
                status = 2
    return status
