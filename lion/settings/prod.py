from .base import *
import os

ALLOWED_HOSTS = ["13.124.78.53"]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = []
DEBUG = False