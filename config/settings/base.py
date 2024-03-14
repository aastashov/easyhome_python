from __future__ import annotations

from pathlib import Path

import django_stubs_ext
import environ

django_stubs_ext.monkeypatch()

# BASE
# ----------------------------------------------------------------------------
BASE_DIR = Path(__file__).parents[2]  # easyhome/
APPS_DIR = BASE_DIR / "easyhome"  # easyhome/easyhome

# ENVIRONMENT
# ----------------------------------------------------------------------------
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
)
environ.Env.read_env(str(BASE_DIR.joinpath(".env")))

DEBUG = env.bool("DJANGO_DEBUG", default=True)
RELEASE = env.str("RELEASE", default="latest")

# SECURITY
# ----------------------------------------------------------------------------
SECRET_KEY = env("DJANGO_SECRET_KEY", default="123")
ALLOWED_HOSTS = ["*"]

# APPLICATIONS
# ----------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "easyhome.common",
    "easyhome.easyhome",
    "easyhome.parser",

    "corsheaders",
    "elasticapm.contrib.django",
    "graphene_django",
]

# MIDDLEWARE
# ----------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URLS
# ----------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
LOGOUT_REDIRECT_URL = "/"

# TEMPLATES
# ----------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# WSGI
# ----------------------------------------------------------------------------
WSGI_APPLICATION = "config.wsgi.application"

# DATABASES
# ----------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("DB_NAME", default="easyhome"),
        "USER": env.str("DB_USER", default="easyhome_srv"),
        "PASSWORD": env.str("DB_PASSWORD", default="pass1234"),
        "HOST": env.str("DB_HOST", default="127.0.0.1"),
        "PORT": env.int("DB_PORT", default=25432),
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# AUTHENTICATION
# ----------------------------------------------------------------------------
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

LOGIN_REDIRECT_URL = "/"
SESSION_COOKIE_DOMAIN = "127.0.0.1"

# ELASTIC
# ----------------------------------------------------------------------------
PROJECT_NAME = env.str("PROJECT_NAME", default="EasyHome")

APM_SERVER_URL = env.str("ELASTIC_APM_SERVER_URL", default="")
ENABLE_APM = bool(APM_SERVER_URL)

ELASTIC_APM = {
    "DISABLE_SEND": not ENABLE_APM,
    "ENABLED": ENABLE_APM,
    "SERVICE_NAME": PROJECT_NAME.replace(" ", "_").lower(),
    "SECRET_TOKEN": env.str("ELASTIC_APM_SECRET_TOKEN", default=""),
    "SERVER_URL": APM_SERVER_URL,
    "TRANSACTION_SAMPLE_RATE": env.float("ELASTIC_APM_TRANSACTION_SAMPLE_RATE", default=1.0),
}

# LOGGING
# ----------------------------------------------------------------------------
LOG_LEVEL = env.str("DJANGO_LOG_LEVEL", default="INFO")
LOGGING = {
    "version": 1,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {filename}::{funcName}() {message}",
            "style": "{",
        },
        "filebeat": {"()": "ecs_logging.StdlibFormatter"},
    },
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
        "sentry": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
        },
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "verbose" if DEBUG else "filebeat",
        },
        # "elasticapm": {
        #     "level": "WARNING",
        #     "class": "elasticapm.contrib.django.handlers.LoggingHandler",
        # },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "easyhome": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
        "django.server": {
            "handlers": ["null"],
        },
        "apscheduler": {
            "handlers": ["null"],
        },
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "sentry.errors": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
        # Log errors from the Elastic APM module to the console (recommended)
        "elasticapm.errors": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# LOCALIZATION
# ----------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# STATIC
# ----------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

# django-captcha-admin
# ----------------------------------------------------------------------------
RECAPTCHA_PUBLIC_KEY = env.str("RECAPTCHA_PUBLIC_KEY", default="")
RECAPTCHA_PRIVATE_KEY = env.str("RECAPTCHA_PRIVATE_KEY", default="")

# Telegram
# ----------------------------------------------------------------------------
TG_NAME = env.str("TG_NAME", default="easyhome_dev_bot")
TG_TOKEN = env.str("TG_TOKEN", default="")
TG_CHAT_ID = env.int("TG_CHAT_ID", default=-1001248414108)
TG_LOGIN_REDIRECT_URL = "/auth/complete/telegram/"

# Scheduler
# ----------------------------------------------------------------------------
SCHEDULER_LALAFO_ENABLED = env.bool("SCHEDULER_LALAFO_ENABLED", default=False)
SCHEDULER_DIESEL_ENABLED = env.bool("SCHEDULER_DIESEL_ENABLED", default=False)
SCHEDULER_ENABLED = SCHEDULER_LALAFO_ENABLED or SCHEDULER_DIESEL_ENABLED
SCHEDULER_PARSE_INTERVAL = env.int("SCHEDULER_PARSE_INTERVAL", default=1)

# Parser
# ----------------------------------------------------------------------------
AIOHTTP_REQUEST_LIMIT = env.int("AIOHTTP_REQUEST_LIMIT", default=15)

# graphene-django
# ----------------------------------------------------------------------------
GRAPHENE = {
    "SCHEMA": "easyhome.graph_ql.queries.schema",
}

# django-cors-headers
# ----------------------------------------------------------------------------
CORS_ORIGIN_REGEX_WHITELIST = [
    r"^http://(127.0.0.1|localhost):[0-9]00[0-9]",
]

CORS_ALLOW_CREDENTIALS = True
