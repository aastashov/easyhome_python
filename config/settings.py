from pathlib import Path

import django_stubs_ext
import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

django_stubs_ext.monkeypatch()

# BASE
# ----------------------------------------------------------------------------
BASE_DIR = Path(__file__).parents[1]  # hsearch/
APPS_DIR = BASE_DIR / "hsearch"  # hsearch/hsearch

# ENVIRONMENT
# ----------------------------------------------------------------------------
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
)
environ.Env.read_env(str(BASE_DIR.joinpath(".env")))

DEBUG = env.bool("DJANGO_DEBUG", default=False)

# SECURITY
# ----------------------------------------------------------------------------
SECRET_KEY = env("DJANGO_SECRET_KEY", default="123") if DEBUG else env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = ["*"] if DEBUG else env.list("DJANGO_ALLOWED_HOSTS")

# APPLICATIONS
# ----------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_results",
    "hsearch.common",
    "hsearch.hsearch",
    "hsearch.parser",
    "social_django",
]

# MIDDLEWARE
# ----------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
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
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
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
        "NAME": env("DJANGO_DB_NAME", default="hsearch"),
        "USER": env("DJANGO_DB_USER", default="hsearch_srv"),
        "PASSWORD": env("DJANGO_DB_PASSWORD", default="pass1234"),
        "HOST": env("DJANGO_DB_HOST", default="127.0.0.1"),
        "PORT": env.int("DJANGO_DB_PORT", default=25432),
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

AUTHENTICATION_BACKENDS = [
    "social_core.backends.telegram.TelegramAuth",
    "django.contrib.auth.backends.ModelBackend",
]

SOCIAL_AUTH_TELEGRAM_BOT_TOKEN = env("TG_TOKEN", default="")
SOCIAL_AUTH_STRATEGY = "hsearch.sso.strategy.SSOStrategy"
USER_FIELDS = [
    "username",
    "uid",
    "first_name",
    "last_name",
    "fullname",
]

LOGIN_REDIRECT_URL = "/"

SESSION_COOKIE_DOMAIN = "127.0.0.1" if DEBUG else ".reloc.kg"

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
RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_PUBLIC_KEY", default="")
RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_PRIVATE_KEY", default="")

# Telegram
# ----------------------------------------------------------------------------
TG_NAME = env("TG_NAME", default="hsearch_dev_bot")
TG_CHAT_ID = env.int("TG_CHAT_ID", default=-1001248414108)
TG_LOGIN_REDIRECT_URL = "/auth/complete/telegram/"

# Sentry
# ----------------------------------------------------------------------------
SENTRY_DSN = env("DJANGO_SENTRY_DSN", default="")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
    )

# Celery
# ----------------------------------------------------------------------------
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", default="redis://localhost:26379/0")
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND", default="redis://localhost:26379/1")

# Parser
# ----------------------------------------------------------------------------
AIOHTTP_REQUEST_LIMIT = env.int("AIOHTTP_REQUEST_LIMIT", default=15)
