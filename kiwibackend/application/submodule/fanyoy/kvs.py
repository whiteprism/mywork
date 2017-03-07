# -*- coding: utf-8 -*-

#
# KVS ラッパークラス
# for Django
#

from django.conf import settings
from django.core.cache import cache
from tokyotyrant import get_client

import cPickle as pickle

# settings.pyに項目KVS_KEYNAME_PREFIXを設定すると、キー名の頭にその値が付加される
# 設定例
# KVS_KEYNAME_PREFIX = 'TestApp::'

SETTINGS_NAME='KVS_KEYNAME_PREFIX'


class KVSBase(object):
    """
    KVS基底クラス
    """
    KEY_FORMAT = None # デフォルトキーフォーマット（要オーバーライド）
    TIMEOUT = None # デフォルトタイムアウト
    def __init__(self, keyvalue=None, keyformat=None, instance=None, timeout=None, **argv):
        self._keyformat = keyformat if keyformat else self.KEY_FORMAT

        self._keyprefix = ''
        if hasattr(settings, SETTINGS_NAME):
            self._keyprefix = getattr(settings, SETTINGS_NAME)

        if self._keyformat:
            self._key = self._keyprefix + (self._keyformat % keyvalue)
        else:
            raise ValueError('Require key format.')

        self._instance = instance
        self._timeout = timeout if timeout else self.TIMEOUT

    @property
    def keyformat(self):
        """
        キーフォーマット
        """
        return self._keyformat

    @property
    def keyprefix(self):
        """
        キープリフィックス
        """
        return self._keyprefix

    @property
    def key(self):
        """
        キー名
        """
        return self._key

    @property
    def instance(self):
        """
        KVSインスタンス
        """
        return self._instance

    @property
    def timeout(self):
        """
        タイムアウト値
        """
        return self._timeout

    def setkey(self, keyvalue):
        """
        キー名設定
        """
        self._key = self.keyprefix + (self.keyformat % keyvalue)

    def get(self, default=None):
        """
        値の取得
        要オーバーライド
        """
        raise NotImplementedError

    def set(self, value):
        """
        値の設定
        要オーバーライド
        """
        raise NotImplementedError

    def add(self, value):
        """
        値の加算
        """
        raise NotImplementedError

    def delete(self):
        """
        値の削除
        要オーバーライド
        """
        raise NotImplementedError

    """
    アクセッサ
    """
    def _valueset(self, value):
        self.set(value)
    def _valueget(self):
        return self.get(None)
    value = property(_valueget, _valueset)



class TTStr(KVSBase):
    """
    TokyoTyrant 文字列 クラス
    """
    def __init__(self, keyvalue, keyformat=None, **argv):
        super(TTStr, self).__init__(keyvalue, keyformat, get_client(), **argv)

    def get(self, default=None):
        return self.instance.get(self.key, default)

    def set(self, value):
        self.instance.put(self.key, value)
        return value

    def delete(self):
        self.instance.out(self.key)

class TTObj(KVSBase):
    """
    TokyoTyrant オブジェクト クラス
    """
    def __init__(self, keyvalue, keyformat=None, **argv):
        super(TTObj, self).__init__(keyvalue, keyformat, get_client(), **argv)

    def get(self, default=None):
        s = self.instance.get(self.key, None)
        if s is None:
            return default
        return self._deserialize(s)

    def set(self, value):
        s = self._serialize(value)
        self.instance.put(self.key, s)
        return value

    def delete(self):
        self.instance.out(self.key)

    def _serialize(self, value):
        return pickle.dumps(value)

    def _deserialize(self, value):
        return pickle.loads(value)


class TTInt(KVSBase):
    """
    TokyoTyrant 整数 クラス
    """
    def __init__(self, keyvalue, keyformat=None, **argv):
        super(TTInt, self).__init__(keyvalue, keyformat, get_client(), **argv)

    def get(self, default=None):
        return self.instance.getint(self.key, default)

    def set(self, value):
        self.instance.putint(self.key, value)
        return value

    def add(self, value):
        self.instance.addint(self.key, value)
        return value

    def delete(self):
        self.instance.out(self.key)

class DjangoCache(KVSBase):
    """
    Django cache クラス
    """
    def __init__(self, keyvalue, keyformat=None, **argv):
        super(DjangoCache, self).__init__(keyvalue, keyformat, **argv)

    def get(self, default=None):
        return cache.get(self.key, default)

    def set(self, value):
        if self.timeout:
            cache.set(self.key, value, self.timeout)
        else:
            cache.set(self.key, value)
        return value

    def delete(self):
        cache.delete(self.key)

class DummyCache(KVSBase):
    """
    ダミー cache クラス
    実際にはキャッシュを行わない
    """
    def __init__(self, keyvalue, keyformat=None, **argv):
        super(DummyCache, self).__init__(keyvalue, keyformat, **argv)

    def get(self, default=None):
        return default

    def set(self, value):
        return value

    def delete(self):
        pass


def TEST():
    """
    テストコード
    """
    # KVSクラス定義
    class TestDjangoCcaheKVS(DjangoCache):
        KEY_FORMAT = "DjangoCache::%d"
    class TestTTIntKVS(TTInt):
        KEY_FORMAT = "TTInt::%d"
    class TestTTStrKVS(TTStr):
        KEY_FORMAT = "TTStr::%d"
    class TestTTObjKVS(TTObj):
        KEY_FORMAT = "TTObj::%d"
    class TestDummyKVS(DummyCache):
        KEY_FORMAT = "Dummy::%d"

    classes = {
        TestDjangoCcaheKVS: "TEST value",
        TestTTIntKVS: 1234,
        TestTTStrKVS: "TEST value",
        TestTTObjKVS: { "TEST":1234 },
        TestDummyKVS: { "TEST":1234 },
        }

    for cls, value in classes.iteritems():
        for key in xrange(5):
            kvs = cls(key)
            kvs.value = value
            kvs.delete()

if __name__ == "__main__":
    TEST()
