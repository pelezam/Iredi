"""
WSGI config for iredi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from iredi.settings import production 

from django.core.wsgi import get_wsgi_application

if production.DEBUG:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iredi.settings.dev")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iredi.settings.production")

application = get_wsgi_application()
