from .base import *
import os 

DEBUG = False
ALLOWED_HOSTS = ['app.doddlehq.com']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS=['https://dev.findahousechurch.com',]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
