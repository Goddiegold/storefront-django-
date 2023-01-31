import os
from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = []
