import os
from pathlib import Path
import subprocess

from constants import (
    SERVER_MODE_ENV_VAR_KEY,
    SERVER_MODE_CONTROL_PLANE,
    SERVER_MODE_PRIMARY_WORKER,
    SERVER_MODE_EXPLORATORY_WORKER,
    AMPQ_USER_ENV_VAR_KEY,
    AMPQ_PASSWORD_ENV_VAR_KEY,
    AMPQ_URL_ENV_VAR_KEY,
    AMPQ_PORT_ENV_VAR_KEY,
    CONTROL_PLANE_URL_ENV_KEY,
    CONTROL_PLANE_PORT_ENV_KEY,
    TUNING_ID_ENV_VAR_KEY,
    LAUNCH_EVENT_NAME_ENV_VAR_KEY,
    PRIMARY_DB_PORT_ENV_VAR_KEY,
    REPLICA_DB_PORT_ENV_VAR_KEY,
    PRIMARY_DB_USERNAME_ENV_VAR_KEY,
    REPLICA_DB_USERNAME_ENV_VAR_KEY,
)

SERVER_MODE = os.environ.get(SERVER_MODE_ENV_VAR_KEY, None)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR.parent / "scripts"

# Scripts executed through different views
START_DATABASE_LOGGING_SCRIPT = SCRIPTS_DIR / "start_database_logging.sh"
STOP_DATABASE_LOGGING_SCRIPT = SCRIPTS_DIR / "stop_database_logging.sh"
GET_DATABASE_LOGGING_DIR_SCRIPT = SCRIPTS_DIR / "get_database_logging_directory.sh"
GET_DATABASE_DATA_DIR_SCRIPT = SCRIPTS_DIR / "get_database_data_directory.sh"

POSTGRES_USER = "postgres"

# Control plane specific configurations
if SERVER_MODE == SERVER_MODE_CONTROL_PLANE:

    # TODO: Make this config?
    PRIMARY_WORKER_PORT = "8001"
    EXPLORATORY_WORKER_PORT = "8002"

    """
    Messaging infrastructure (Presently uses RabbitMQ)
    """
    AMPQ_USER = os.environ[AMPQ_USER_ENV_VAR_KEY]
    AMPQ_PASSWORD = os.environ[AMPQ_PASSWORD_ENV_VAR_KEY]
    AMPQ_URL = os.environ[AMPQ_URL_ENV_VAR_KEY]
    AMPQ_PORT = os.environ[AMPQ_PORT_ENV_VAR_KEY]
    RESOURCE_DIR = BASE_DIR / "control_plane" / "resources"

else:  # Configurations for all workers

    """
    TODO: Control plane discovery is an open problem. Currently
    we pass a hardcoded URL/PORT via env vars; need to fix
    this when we move from local to multiple machine setup
    """
    CONTROL_PLANE_URL = os.environ[CONTROL_PLANE_URL_ENV_KEY]
    CONTROL_PLANE_PORT = os.environ[CONTROL_PLANE_PORT_ENV_KEY]
    TUNING_ID = os.environ[TUNING_ID_ENV_VAR_KEY]
    LAUNCH_EVENT_NAME = os.environ[LAUNCH_EVENT_NAME_ENV_VAR_KEY]

# Primary worker specific configurations
if SERVER_MODE == SERVER_MODE_PRIMARY_WORKER:
    PRIMARY_DB_PORT = os.environ[PRIMARY_DB_PORT_ENV_VAR_KEY]
    PRIMARY_DB_USERNAME = os.environ[PRIMARY_DB_USERNAME_ENV_VAR_KEY]
    WORKLOAD_CAPTURE_DIR = BASE_DIR / "primary_worker" / "workload_captures"

# Exploratory worker specific configurations
if SERVER_MODE == SERVER_MODE_EXPLORATORY_WORKER:
    REPLICA_DB_PORT = os.environ[REPLICA_DB_PORT_ENV_VAR_KEY]
    REPLICA_DB_USERNAME = os.environ[REPLICA_DB_USERNAME_ENV_VAR_KEY]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-)^1mg$booh%m$8(8c629(b(v82$is9r=k%09448kra$r8((v9("

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

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

LOGGING_DIR = BASE_DIR / "logs"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "control_plane_info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOGGING_DIR / "control_plane_info.log",
            "formatter": "verbose",
        },
        "control_plane_debug": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOGGING_DIR / "control_plane_debug.log",
            "formatter": "verbose",
        },
        "primary_worker_info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOGGING_DIR / "primary_worker_info.log",
            "formatter": "verbose",
        },
        "primary_worker_debug": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOGGING_DIR / "primary_worker_debug.log",
            "formatter": "verbose",
        },
        "exploratory_worker_info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOGGING_DIR / "exploratory_worker_info.log",
            "formatter": "verbose",
        },
        "exploratory_worker_debug": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOGGING_DIR / "exploratory_worker_debug.log",
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "control_plane": {
            "handlers": ["control_plane_info", "control_plane_debug"],
            "level": "DEBUG",
            "propagate": True,
        },
        "primary_worker": {
            "handlers": ["primary_worker_info", "primary_worker_debug"],
            "level": "DEBUG",
            "propagate": True,
        },
        "exploratory_worker": {
            "handlers": ["exploratory_worker_info", "exploratory_worker_debug"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
