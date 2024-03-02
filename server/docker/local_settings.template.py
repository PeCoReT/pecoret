from pecoret.settings import *

import os
# This is a minimal example settings file for PeCoReT docker
# it is created, if no file exists to make the app running on first boot


# Required settings:
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "http://localhost").split(",")
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', "http://localhost").split(",")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", 'backend').split(",")


DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'HOST': 'db',
    'NAME': os.environ.get('DB_NAME', 'pecoret'),
    'USER': os.environ.get('DB_USER', 'pecoret'),
    'PASSWORD': os.environ.get("DB_PASSWORD", "dontusethispassword"),
  }
}
