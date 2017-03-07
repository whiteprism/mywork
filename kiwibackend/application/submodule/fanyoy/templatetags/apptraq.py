# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
import urllib
import urllib2
import md5
import time

from django.template import Node, TemplateSyntaxError
from django.utils.encoding import smart_str

register = template.Library()

"""
PHP sample code 
function sap_send($function, $params) {  
    if( !$params ) return false;  
    $SA_API_KEY = '231';  
    $SA_SECRET_KEY = 'bc907e88';  
    $SA_API_URL = 'http://bsap.nakanohito.jp/';  
    $SA_VERSION = 'v1';  
      
    $sig = null;  
    $params['ts']= gmdate("Y-m-d+H:i:s");  
    if( !isset($params['tp']) ) $params['tp'] = 'i';  
    if( $params['tp'] == 'i' )  $params['guid'] = 'ON';  
      
    parse_str(http_build_query($params,'', '&'), $formatted_params);  
    ksort($formatted_params);  
      
    foreach ($formatted_params as $key =>$val){ $sig .= $key.'='.urlencode($val).'&'; }  
    $formatted_params['sg'] = md5($sig.$SA_SECRET_KEY);  
    $query = http_build_query($formatted_params, '', '&'.'amp;');  
    $url = $SA_API_URL . $SA_VERSION .'/'. $SA_API_KEY .'/' . $function . '/?'. $query;  
      
    if( $params['tp'] == 'i' ) {  
        echo '<img src="'.$url.'" width="1" height="1" alt="" />';  
    } else {  
        file_get_contents($url);  
    }  
} 
"""

API_URL = 'http://bsap.nakanohito.jp'
API_VERSION = 'v1'

def escape(s):
    """Escape a URL including any /."""
    return urllib.quote(s, safe='~')

def _utf8_str(s):
    """Convert unicode to utf-8."""
    if isinstance(s, unicode):
        return s.encode("utf-8")
    else:
        return str(s)

class ApptraqNode(Node):
    """ AppTraqの解析タグを扱うノード
    """
    def __init__(self, message_type, params):
        self.message_type = message_type
        self.params = params

    def render(self, context):
        api_key = settings.APPTRAQ_API_KEY
        secret_key = settings.APPTRAQ_SECRET_KEY

        params = dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.params.items()])

        params['ts']= time.strftime('%Y-%m-%d+%H:%M:%S', time.gmtime())

        if 'tp' not in params:
            params['tp'] = 'i'
        if params['tp'] == 'i':
            params['guid'] = 'ON'

        # Escape key values before sorting.
        key_values = [(escape(_utf8_str(k)), escape(_utf8_str(v))) \
                          for k,v in params.items()]
        # Sort lexicographically, first after key, then after value.
        key_values.sort()

        # Combine key value pairs into a string.
        base_string = '&'.join(['%s=%s' % (k, v) for k, v in key_values])

        # create security code
        key_values.append(('sg', md5.new(base_string + secret_key).hexdigest()))

        query = '&amp;'.join(['%s=%s' % (k, v) for k, v in key_values])
        
        url = "%s/%s/%s/%s/?%s" % (
            API_URL, API_VERSION, api_key, self.message_type, query)
        
        if params['tp'] == 'i':
            return '<img src="%s" width="1" height="1" alt="" />' % url
        else:
            # API を直接コールする
            try:
                r = urllib2.urlopen(url)
            except urllib2.HTTPError, e:
                import logging
                logging.debug('HTTPError code:%d' % (e.code, ))
            return ''

def _apptraq_tokenizer(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (message_type)" % bits[0])
    message_type = bits[1]
    params = {}
    if len(bits) > 2:
        bits = iter(bits[2:])
        for bit in bits:
            for arg in bit.split(","):
                k, v = arg.split('=', 1)
                k = k.strip()
                params[k] = parser.compile_filter(v)
    return message_type, params

def apptraq(parser, token):
    """
    AppTraq解析タグを発行する
    http://apptraq.com/home/applications/tag

    configuration::
        {% apptraq message_type name1=value1,name2=value2 %}

    message_type : メッセージタイプ
                   aca : アクションの取得
                   vsa : アプリケーションの追加
                   adr : アプリケーションの削除
                   vsu : プロフィールの更新
                   ada : 広告の取得
                   cva : コンバージョンの取得
                   smu : ユーザーの総数の更新
    """
    message_type, params = _apptraq_tokenizer(parser, token)
    return ApptraqNode(message_type, params)

apptraq = register.tag(apptraq)
