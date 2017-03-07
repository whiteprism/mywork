# -*- coding:utf-8 -*-
from django.core.cache import cache
import time

def day_cache(view_func):
    """
    一度だけしか実行されないようにロックする
    """
    def decorate(request, *args, **kwds):

        lockkey = 'Lockkey::OnceLock::%s::%s' % (request.path, str(request.osuser.userid))
        reskey = 'Reskey::OnceLockRes::%s::%s' % (request.path, str(request.osuser.userid))

        cache_res = cache.get(reskey, None)
        if cache_res:
            return cache_res

        # ロックチェック
        lock = cache.get(lockkey, None)
        if lock:
            for i in xrange(1000):
                #sleep(10ミリ秒指定)
                time.sleep(0.01)
                # キャッシュにレスポンスが入るまで待つ
                cache_res = cache.get(reskey, None)
                if cache_res:
                    return cache_res

        # ロック取得
        cache.set(lockkey, 1)

        # 該当viewを実行
        res = view_func(request, *args, **kwds)

        # 結果を一時的に保存(15秒)
        cache.set(reskey, res, 86400)
        # ロックを解除
        cache.delete(lockkey)
        return res
        decorate.__doc__ = view_func.__doc__
        decorate.__dict__ = view_func.__dict__
    return decorate
