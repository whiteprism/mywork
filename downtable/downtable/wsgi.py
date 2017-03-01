"""
WSGI config for downtable project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

print os.getcwd()
print os.path.abspath("../")
paths = (
    os.path.abspath('../downup'),
    os.path.abspath('../'),
    )

for path in paths:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "downtable.settings")

application = get_wsgi_application()
