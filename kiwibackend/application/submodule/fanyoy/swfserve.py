# -*- coding: utf-8 -*-
import struct
import sys
import zlib

def _h32(v):
    return struct.pack('<L', v)

def _h16(v):
    return struct.pack('<H', v)

def _calctaglen(d, encode_option):
    num = 0
    for k in d:
        value = unicode(d[k]).encode(encode_option, 'ignore')
        num += len(k) + len(value) + 11
    return num + 1

def _maketag(d, encode_option):
    tag = '\x3f\x03'
    tag += _h32(_calctaglen(d, encode_option))
    for k in d:
        value = unicode(d[k]).encode(encode_option, 'ignore')
        tag += '\x96' + _h16(len(k)+2) + '\x00' + k + '\x00'
        tag += '\x96' + _h16(len(value)+2) + '\x00' + value + '\x00'
        tag += '\x1d'
    tag += '\x00'
    return tag

def create_swf(base_swf, params, encode=None):
    "パラメーターを埋め込んだ Flash lite 1.1/2.0 ファイルを生成"
    # 圧縮されている場合は展開する
    decomp_swf = decompress(base_swf)    
    
    # パラメーターを埋め込む
    if encode:
        tag = _maketag(params, encode)
    else:
        tag = _maketag(params, get_encode(decomp_swf))
    rectbit = ord(decomp_swf[8]) >> 3
    head_len = int(((( 8 - ((rectbit*4+5)&7) )&7)+ rectbit*4 + 5 )/8) + 12 + 5;
    head = decomp_swf[:head_len]
    tail = decomp_swf[head_len:]
    newhead = head[:4] + _h32(len(decomp_swf) + len(tag)) + head[8:]
    out_swf = newhead + tag + tail

    # もし圧縮されていた場合は、圧縮し直す
    out_swf = compress(out_swf)
    return out_swf    

def get_encode(base_swf):
    """
    4バイト目の Flash のバージョンを読み取り判定
    Flash ver.6 以降は、UTF-8
    See https://secure.m2osw.com/swf_tag_file_header
    4バイト目が必要なだけので、base_swf は header でも swf 本体でも良い
    """
    if base_swf[3] < '\x06': # Flash version 6未満 (Flash Lite 1.1) -> cp932
        return 'cp932'
    else:                    # Flash version 6以上 (Flash Lite 2.0) -> utf-8
        return 'utf-8'

def compress(base_swf):
    "圧縮フラグが付いている場合は、圧縮する"
    header = base_swf[:8]
    tail   = base_swf[8:]
    if   header[:3] == 'FWS': # not compressed
        new_tail = tail
    elif header[:3] == 'CWS': # compressed
        new_tail = zlib.compress(tail)
    return header + new_tail

def decompress(base_swf):
    "圧縮フラグが付いている場合は、展開する"
    header = base_swf[:8]
    tail   = base_swf[8:]
    if   header[:3] == 'FWS': # not compressed
        new_tail = tail
    elif header[:3] == 'CWS': # compressed
        # tail を zlib 展開
        # See http://ne.tc/2008/03/13/
        new_tail = zlib.decompress(tail)
    return header + new_tail    

def swf_serve(request, path, params, filename=None, encode=None):
    """
    パラメータを埋め込んだ Flash を Response として返す
    """
    from django.core.cache import cache
    from django.http import HttpResponse

    try:
        v = cache.get(path, None)
    except: # memcache が壊れている場合の保険
        v = None
    if v:
        head, tail = v
    else:
        base_swf = open(path, 'rb').read()
        decomp_swf = decompress(base_swf)

        rectbit = ord(decomp_swf[8]) >> 3
        head_len = int(((( 8 - ((rectbit*4+5)&7) )&7)+ rectbit*4 + 5 )/8) + 12 + 5;
        head = decomp_swf[:head_len]
        tail = decomp_swf[head_len:]
        try:
            cache.set(path, [head, tail])
        except: # memcache が壊れている場合の保険
            pass
    
    if encode:
        tag = _maketag(params, encode)
    else:
        tag = _maketag(params, get_encode(head))
    ln = _h32(len(head)+len(tail)+len(tag))
    newhead = head[:4] + ln + head[8:]
    out_swf = newhead + tag + tail
    # 圧縮フラグが付いている場合、圧縮をかける
    out_swf = compress(out_swf)
    
    response = HttpResponse(mimetype='application/x-shockwave-flash')
    if filename:
        response['Content-Disposition'] = 'attachment; filename=' + filename
    response.write(out_swf)
    return response

if __name__ == '__main__':
    import urllib2
    # See http://libpanda.s18.xrea.com/test_insert/sample.html
    
    base_swf = urllib2.urlopen(
       'http://libpanda.s18.xrea.com/test_insert/x/base.swf').read()
    
    # base_swf = open(sys.argv[1]).read()

    params = {
        'serif': u'じゃんぷー',
        'jumpsound': u'どかーーん',
    }

    out_file = open('output.swf', 'w')
    out_file.write(create_swf(base_swf, params))

