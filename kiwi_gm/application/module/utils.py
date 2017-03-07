# -*- coding: utf-8 -*-
import random
from random import randint
from datetime import datetime, timedelta
from functools import wraps
import logging
import msgpack
from time import mktime
import re
import hashlib
from django.conf import settings
from django.db import models
import inspect


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

def is_over_24h(date_time):
    '''
    时间相差24小时
    '''
    delta = datetime.now() - date_time
    return delta.days > 0
    

def get_past_days(date_time):
    '''
    时间差
    '''
    date_time = to_ingame_datetime(date_time)
    dt = datetime.now()
    dt = to_ingame_datetime(dt)
    return dt.day - date_time.day

def is_past_day(date_time):
    '''
    是否为今天以前的时间
    '''
    days = get_past_days(date_time)
    return days > 0

def is_game_today(check_datetime):
    now = datetime.now() # 今
    today = now
    tomorrow = now + timedelta(1) # 明日
    start_datetime = datetime(today.year, today.month, today.day) 
    end_datetime = datetime(tomorrow.year, tomorrow.month, tomorrow.day) 
    if check_datetime >= start_datetime and check_datetime < end_datetime:
        return True
    else:
        return False

def is_digits(number):
    '''
    是否为整形
    '''
    return isinstance(number, long) or isinstance(number, int)

def clamp(value, min_value, max_value):
    return min(max(value, min_value), max_value)

# test_bit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.

def test_bit(int_type, offset):
    mask = 1 << offset
    return(int_type & mask)

# set_bit() returns an integer with the bit at 'offset' set to 1.

def set_bit(int_type, offset):
    mask = 1 << offset
    return(int_type | mask)

# clear_bit() returns an integer with the bit at 'offset' cleared.

def clear_bit(int_type, offset):
    mask = ~(1 << offset)
    return(int_type & mask)

# toggle_bit() returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0.

def toggle_bit(int_type, offset):
    mask = 1 << offset
    return(int_type ^ mask)

def count_bit(integer):
    count = 0
    for b in range(32):
        mask = 1 << b
        if integer & mask:
            count += 1
    return count

def bit_index_list(integer):
    result = []
    for b in range(32):
        mask = 1 << b
        if integer & mask:
            result.append(b)

    return result


def getcallerinfo(depth=0):
    fr = inspect.currentframe()
    try:
        depth = 1 + depth # この場所が取れても仕方ないのでデフォルトで1つはたどる
        for i in range(depth):
            fr = fr.f_back
            if fr is None:
                return '<no caller>'
        fi = inspect.getframeinfo(fr, 0)
        if fi[2] == '<module>':
            return '(%s:%d)' % (fi[0], fi[1])
        else:
            return '%s() (%s:%d)' % (fi[2], fi[0], fi[1])
    finally:
        del fr

def get_weight(obj, weight_property):
    weight = 0
    if isinstance(obj, dict):
        weight = obj.get(weight_property, 0)
    elif isinstance(obj, (tuple, list)):
        if isinstance(weight_property, int) and weight_property < len(obj):
            weight = obj[weight_property]
    else:
        weight = obj.getattr(weight_property, 0)
    try:
        return int(weight)
    except:
        return 0

def w_choice(choice_weight = None, choices = None, weight_property = 'weight'):
    if choices and weight_property:
        possibility = random.randint(1, sum([get_weight(i, weight_property) for i in choices]))
        for i in choices:
            possibility -= get_weight(i, weight_property)
            if possibility <= 0:
                return i
        return i
    elif choice_weight:
        possibility = random.randint(1, sum(choice_weight.itervalues()))
        for value, weight in choice_weight.iteritems():
            possibility -= weight
            if possibility <= 0:
                return value
        return value
    return None

SETTINGS_NAME_TODAY = 'TODAY'
DATE_FORMAT = '%Y/%m/%d'
DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'

def get_today():
    """
       TODAY = '2010/09/01'
       TODAY = '2010/09/01 12:34:56'
    """
    if hasattr(settings, SETTINGS_NAME_TODAY):
        datestr = getattr(settings, SETTINGS_NAME_TODAY)
        if len(datestr) == 10:
            return datetime.strptime(datestr, DATE_FORMAT)
        else:
            return datetime.strptime(datestr, DATETIME_FORMAT)

    return datetime.today()
