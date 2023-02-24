import os
from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

REDIS_URL = os.environ['REDIS_URL']

ALLOWED_HOSTS = ["storefront-django.onrender.com"]

CELERY_BROKER_URL = 'redis://localhost:6379/1'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        'TIMEOUT':10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
