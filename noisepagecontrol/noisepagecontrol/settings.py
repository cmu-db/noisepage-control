import os
from pathlib import Path

from noisepagecontrol.constants import (
    SERVER_MODE_ENV_VAR_KEY,
    SERVER_MODE_CONTROL_PLANE,
    SERVER_MODE_PRIMARY_WORKER,
    SERVER_MODE_EXPLORATORY_WORKER,
)

SERVER_MODE = os.environ[SERVER_MODE_ENV_VAR_KEY]

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-)^1mg$booh%m$8(8c629(b(v82$is9r=k%09448kra$r8((v9("

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

"""
    Include installed apps based on the server mode
"""
if SERVER_MODE == SERVER_MODE_CONTROL_PLANE:
    INSTALLED_APPS += ["control_plane"]
elif SERVER_MODE == SERVER_MODE_PRIMARY_WORKER:
    INSTALLED_APPS += ["primary_worker"]
elif SERVER_MODE == SERVER_MODE_EXPLORATORY_WORKER:
    INSTALLED_APPS += ["exploratory_worker"]
else:
    raise Exception("SERVER_MODE not recognised %s" % (SERVER_MODE))

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "noisepagecontrol.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "noisepagecontrol.wsgi.application"


"""
Housekeeping database config (postgres). Setup:
    - CREATE USER cmudb WITH superuser ENCRYPTED PASSWORD 'cmudb@2021';
    - CREATE DATABASE noisepage_control WITH OWNER cmudb ENCODING 'UTF8';

Setup admin only on CONTROL_PLANE
"""
if SERVER_MODE == SERVER_MODE_CONTROL_PLANE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "noisepage_control",
            "USER": "cmudb",
            "PASSWORD": "cmudb@2021",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
