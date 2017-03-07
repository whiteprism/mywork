# -*- coding: utf-8 -*-
from django.conf import settings
from opensocial.http import HttpResponseJson
import re
import logging
import hashlib
from oauth.oauth import escape, _utf8_str

def _get_sign_parameters_str(params, span_with=""):
    """Return a string that contains the parameters that must be signed."""
    key_values = []
    for k, v in params.iteritems():
        key_values.append((k,v))
    # Sort lexicographically, first after key, then after value.
    key_values.sort()
    # Combine key value pairs into a string.
    return span_with.join(['%s=%s' % (k, v) for k, v in key_values])


def generate_sign(params):
    """
    验证加密串
    """
    sign_str = _get_sign_parameters_str(params, span_with="&")
    sign_str = "%s%s" % (sign_str, settings.SECRET_KEY) 
    return hashlib.md5(sign_str).hexdigest()
