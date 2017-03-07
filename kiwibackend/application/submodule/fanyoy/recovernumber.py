# -*- coding: utf-8 -*-
"""
時間とともに増減する値を保持するクラス RecoverNumber
データは TyokyoTyrant に持つ
幕末系の OepratorBase に相当する機能のリライト
"""
import time
from tokyotyrant import tt_operator

class RecoverNumber(object):
    def __init__(self, key):
        self.key = key

    def _set_val(self, v):
        """
        値の設定
            v: [cur_num, max_num, recover_term, last_up]
            cur_num: 現在の値
            max_num: 最大値
            recover_term: 回復間隔（秒） 180なら3分で cur_num をインクリメント
            last_up: 最終更新日付時刻 unix time
        """
        tt_operator.set_list(self.key, v)

    def _get_val(self):
        "値の取得。内容は _set_val() 参照"
        v = tt_operator.get_list(self.key)
        if not v:
            return [-1,-1,0,0]
        return v

    def set_max(self, max_num, recover_term=None, cur_num=None):
        """
        最大値と回復間隔を設定
            get_current() 呼ぶ前には呼ばれる必要がある
            最初に少なくとも一回は recover_term は指定する必要がある
            cur_num=None の場合、現在の値を取得して設定
            recover_term=None の場合、現在の値を取得して設定
        """
        last_up = int(time.time())
        if recover_term is None or cur_num is None:
            old_all = self._get_val()
            if recover_term is None:
                if old_all:
                    recover_term = old_all[2]
            if cur_num is None:
                cur_num = old_all[0] if old_all and old_all[0] != -1 else max_num
        v = [int(cur_num), int(max_num), int(recover_term), int(last_up)]
        self._set_val(v)

    def add_max(self, num):
        """
        最大値を num 増加させる
            num: 増やす値
        """
        v = self._get_val()
        v[1] += num # max_num
        self._set_val(v)

    def dec_max(self, num, min=1):
        """
        最大値を num 減少させる
            num: 減らす値
            min: 最大値のとりうる一番小さい値
            Return:
                成功: True
                失敗: False
        """
        assert min > 0
        v = self._get_val()
        if v[1] - num < min:
            return False

        v[1] -= num
        if v[0] > v[1]: # cur_num が max_num を超えてたら max_num に設定
            v[0] = v[1]
        self._set_val(v)
        return True

    def get_current(self):
        """
        回復も考慮した現在値の取得
        初期化してない(set_max()を呼んでない）場合は -1 を返す
        """
        cur_num, max_num, recover_term, last_up = self._get_val()
        if max_num < 0: # set_max() で初期化していない
            return -1
        current = cur_num + (int(time.time())-last_up) / recover_term
        if current > max_num:
            current = max_num
        return current
    
    def get_consume_current(self):
        """
        回復も考慮した現在値の取得
        初期化してない(set_max()を呼んでない）場合は -1 を返す
        """
        cur_num, min_num, recover_term, last_up = self._get_val()
        if min_num < 0: # set_max() で初期化していない
            return 1
        current = cur_num - (int(time.time())-last_up) / recover_term
        if current < min_num:
            current = min_num
        return current

    def get_max(self):
        """
        最大値の取得
        初期化してない場合は -1 を返す
        """
        v = self._get_val()
        return v[1]

    def get_recover_time(self):
        """
        体力全回復所用時間
        """
        cur_num, max_num, recover_term, last_up = self._get_val()
        if self.get_current() == max_num:
            return 0
        else:
            return (last_up+((max_num-cur_num) * recover_term)) - int(time.time())

    def recover(self, recover_num):
        """
        体力回復
            recover_num: 回復値
        """
        cur_num, max_num, recover_term, last_up = self._get_val()
        time_bonus = int(int(time.time()) - last_up) / recover_term
        current = cur_num + time_bonus + recover_num
        last_up = last_up + time_bonus * recover_term   
        if current > max_num:
            current = max_num
        v = [current, max_num, recover_term, last_up]
        self._set_val(v)

    def recover_all(self):
        """
        体力全回復
        """
        cur_num, max_num, recover_term, last_up = self._get_val()
        last_up = int(time.time())
        v = [max_num, max_num, recover_term, last_up]
        self._set_val(v)

    def recover_percentage(self, recover_percentage):
        """
        回復量をパーセンテージで指定して回復
            recover_percentage: 回復量（%)
        """
        cur_num, max_num, recover_term, last_up = self._get_val()
        time_bonus = int(int(time.time()) - last_up) / recover_term
        cur_num = cur_num + time_bonus + max_num * recover_percentage / 100
        last_up = last_up + time_bonus * recover_term   
        v = [cur_num, max_num, recover_term, last_up]
        self._set_val(v)


    def consume(self, consume_num, zero=False):
        """
        消費する
            consume_num: 消費量
            zero: True なら 0 まで消費、Falseなら消費せずエラー
            Return:
                成功: 消費した数
                失敗: 0
        """
        cur_num, max_num, recover_term, last_up = self._get_val()
        if self.get_current() == max_num:
            last_up = int(time.time())
            current = max_num
        else:
            time_bonus = int(int(time.time()) - last_up) / recover_term
            last_up = last_up + time_bonus * recover_term
            current = cur_num + time_bonus

        if current > max_num:
            current = max_num
        if current - consume_num >=0:   # 足りてる
            current = current - consume_num
        elif zero:  # 足りてないけど 0 まで消費
            consume_num = current
            current = 0
        else:
            return 0
        v = [current, max_num, recover_term, last_up]
        self._set_val(v)
        return consume_num
