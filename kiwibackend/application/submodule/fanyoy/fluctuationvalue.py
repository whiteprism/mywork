# -*- coding: utf-8 -*-

#from kvs.generic import KVS
from submodule.kvs.generic import KVS
import time
import datetime
import logging
logging

class FluctuationObject(object):
    def __init__(self, value, updated_at):
        self.value = value
        self.updated_at = updated_at

def clamp(lowvalue, highvalue, driver):
    '''
    获得目标值
    '''
    if driver < lowvalue: driver = lowvalue
    elif driver > highvalue: driver = highvalue
    return driver

class FluctuationValue(object):
    '''
    恢复时间基类
    '''
    FLUCTUATION_SECOND = 1 # 变动间隔
    MAX_VALUE = 100        # 最大值
    MIN_VALUE = 0          # 最小值
    CACHE_KEY = u'fluctuation'
    STEP_VELUE = 1
    IS_INIT_MIN = False

    fluctuation_second = FLUCTUATION_SECOND
    max_value = MAX_VALUE
    min_value = MIN_VALUE

    def __init__(self,
                fluctuation_second=None,
                max_value=None,
                min_value=None,
                cache_key=None,
                step_value=1,
                is_init_min=False):
        self.fluctuation_second = fluctuation_second if fluctuation_second else self.FLUCTUATION_SECOND
        self.max_value = max_value if max_value else self.MAX_VALUE
        self.min_value = min_value if min_value else self.MIN_VALUE
        self.cache_key = cache_key if cache_key else self.CACHE_KEY
        self.step_value = step_value if step_value!=1 else self.STEP_VELUE
        self.is_init_min = is_init_min if is_init_min else self.IS_INIT_MIN

    def _get(self):
        '''
        获得值
        '''
        kvs = KVS(self.cache_key)
        if self.is_init_min:
            v = kvs.get((self.min_value, int(time.time())))
        else:
            v = kvs.get((self.max_value, int(time.time())))
        if v and not isinstance(v, tuple):
            if self.is_init_min:
                return self.min_value, int(time.time())
            return self.max_value, int(time.time())
        return v

    def _set(self, value_updated_at):
        '''
        参数为tuple时的存储
        '''
        kvs = KVS(self.cache_key)
        kvs.set(value_updated_at)

    def set(self, value):
        kvs = KVS(self.cache_key)
        t = (clamp(self.min_value, self.max_value, value), int(time.time()))
        kvs.set(t)

    def get(self):
        '''
        获得当前值
        '''
        value, updated_at = self._get() 
        now = int(time.time())
        #当前恢复值
        current = value + ((now - updated_at) / self.fluctuation_second) * self.step_value
        if current < self.min_value:
            current = self.min_value
        if current > self.max_value:
            current = self.max_value
        return int(current)

    def add(self, addend):
        '''
        加成相应值
        '''
        addend = abs(addend)
        value, updated_at = self._get()
        now = int(time.time())
        plus_value = (int(now - updated_at) / self.fluctuation_second) * self.step_value
        current = value + plus_value + addend
        updated_at = now
        if current > self.max_value:
            current = self.max_value
        self._set((current, updated_at))

    def sub(self, subtrahend):
        '''
        减去相应值 
        '''
        subtrahend = abs(subtrahend)
        value, updated_at = self._get()
        now = int(time.time())
        if self.get() == self.max_value:
            updated_at = int(time.time())
            current = self.max_value
        else:
            plus_value = (int(now - updated_at) / self.fluctuation_second) * self.step_value
            updated_at = now
            current = value + plus_value
        if current > self.max_value:
            current = self.max_value
        if current - subtrahend >= 0:
            current = current - subtrahend
        else:
            return 0
        self._set((current, updated_at))
        return subtrahend

    def full(self):
        '''
        全回复
        '''
        value, updated_at = self._get()
        updated_at = int(time.time())
        self._set((self.max_value, updated_at))

    def drain(self):
        '''
        枯渇
        '''
        self.set(self.min_value)

    def _rest_time(self):
        '''
        剩余时间
        '''
        value, updated_at = self._get()
        if self.get() >= self.max_value:
            return 0
        else:
            second = (updated_at + ((self.max_value-value) * self.fluctuation_second)) - int(time.time())
            logging.info(second)
            return second

    def rest_time(self):
        '''
        剩余时间datetime封装
        '''
        return datetime.datetime.now() + datetime.timedelta(seconds = self._rest_time())

    def is_stable(self):
        '''
        是否为恢复状态
        '''
        return self._rest_time() == 0


