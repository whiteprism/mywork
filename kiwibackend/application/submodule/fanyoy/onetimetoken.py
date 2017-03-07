# -*- coding: utf-8 -*-
"""
ワンタイムトークンを扱うモジュール

使用用途として、例えばFlashの不正アクセスを防ぐために使える

必要条件：
 CACHE_BACKENDを設定している必要がある

# トークンを生成する
>>> ot = OnetimeToken()

# トークンを取得する
>>> token = ot.get_token()

# 生成したキーを使用する
>>> ot = OnetimeToken(token)

# トークンを使用する。成功すればTrue
>>> ot.use()
True

# トークンの使用に成功するとアクセスキーが生成される
>>> access_key = ot.get_access_key()

# アクセスキーを検証する
>>> ak = AccessKey(access_key)
>>> ak.is_valid()
True

"""

from uuid import uuid4
from django.core.cache import cache

TOKEN_EXPIRE_TIME = 60
ACCESS_KEY_EXPIRE_TIME = 60*60

def _create_token():
    """ セッションキーを発行する
    """
    token = str(uuid4())
    cache.set(token, 1, TOKEN_EXPIRE_TIME)
    return token

class OnetimeToken(object):
    def __init__(self, token=None):
        self._access_key = None
        if token is None:
            self._token = _create_token()
        else:
            self._token = token

    def get_token(self):
        """ トークンを返す
        instanceを生成した時点で何らかの値が入っている。
        トークンを取得
        >>> ot = OnetimeToken()

        トークンの初期値には何か値が入っている
        >>> ot.get_token() is not None
        True

        >>> ot.get_token() == ot.get_token()
        True

        """
        return self._token

    def get_access_key(self):
        """ アクセスキーを返す
        validateに成功すると値が入る
        validateしていない、lまたはvalidateに失敗していたらNone

        >>> ot = OnetimeToken()

        アクセスキーの初期値はNone
        >>> ot.get_access_key() is None
        True
        
        使用すると値が入る
        >>> ot.use()
        True
        >>> ot.get_access_key is None
        False

        """
        return self._access_key

    def use(self):
        """ トークンを使用する
        成功したらTrue、失敗したらFalse
        成功するとaccess_keyが発行され、get_access_key()で取得できるようになる

        >>> ot = OnetimeToken()
        >>> ot.use()
        True

        1度しか使えない
        >>> ot.use()
        False

        一度使用したトークンは使えない
        >>> ot2 = OnetimeToken(ot.get_token())
        >>> ot2.use()
        False

        """
        if cache.get(self.get_token(), None):
            cache.delete(self.get_token())
            access_key = str(uuid4())
            cache.set(access_key, self.get_token(), ACCESS_KEY_EXPIRE_TIME)
            self._access_key=access_key
            return True
        else:
            return False
        
class AccessKey(object):
    """
    アクセスキー
    """
    def __init__(self, access_key):
        """
        access_keyの値が正しいか検証し、OKならフラグをたてる
        キャッシュの有効期限が切れるまで何回も認証できる

        """
        self._access_key = access_key
        exist = cache.get(access_key, None)
        if exist:
            self._is_valid = True
        else:
            self._is_valid = False
        
    def get_access_key(self):
        """ アクセスキーを返す
        >>> ak = AccessKey('foobar')
        >>> ak.get_access_key()
        'foobar'
        """
        return self._access_key

    def is_valid(self):
        """ 検証に成功しているか
        >>> valid_token = OnetimeToken().get_token()
        >>> ak = AccessKey(valid_token)
        >>> ak.is_valid()
        True
        >>> ak.is_valid()
        True

        >>> ak2 = AccessKey('foobar')
        >>> ak2.is_valid()
        False
        """
        is_valid = self._is_valid
        cache.delete(self._access_key)
        return is_valid


def _test():
  import doctest
  doctest.testmod()

if __name__ == "__main__":
  _test()
