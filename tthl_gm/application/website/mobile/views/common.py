# -*- coding: utf-8 -*
import urllib2

def url_request_handler(url):
    req = urllib2.Request(url)
    msg = {}
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError, e:
        msg = {"error":'URLError:%s' % str(e.reason)}
    except urllib2.HTTPError, e:
        msg = {"error":u'HTTP错误码:%s' % str(e.code)}
    except Exception,e:
        msg = {"error":str(e)}
    if msg:
        return (False,msg)
    else:
        return (True,response)
