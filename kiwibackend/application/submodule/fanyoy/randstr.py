# -*- coding: utf-8 -*-

import string
import random

alphabets = string.digits + string.letters

def randstr(n):
    '''
    ランダムな文字列をつくって返す（ワンタイムトークンとかに）
    '''
    return ''.join(random.choice(alphabets) for i in xrange(n))
