from pathlib import Path
import os
from datetime import timedelta
# from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


SECRET_KEY = os.environ.get('SECRET_KEY')
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')

ALLOWED_HOSTS=["127.0.0.1","localhost","18.185.86.217","epicbazaar.store","www.epicbazaar.store"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    #my apps
    "e_commerce",
    "account",
    "store",
    "products",
    # installed apps
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'django_celery_beat',
    'corsheaders',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Baku"

USE_I18N = True

USE_TZ = True

LANGUAGES = [("en", "English"), ("az", "Azerbaijan")]
LOCALE_PATHS = [
    BASE_DIR / "locale",
]


# Static files (CSS, JavaScript, Images)

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static/")]
# tells Django where to look for static files aside from the app-specific static/ directories.


# Base url to serve media files
MEDIA_URL = "/media/"

# Path where media is stored'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

STATIC_URL = "/static/"
# the URL prefix for serving static files during development.
STATIC_ROOT = BASE_DIR / "staticfiles"
# where static files should be collected when you run the collectstatic command. This is typically used in production.

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

}

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "account.CustomUserModel"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # 'filters': {
    #     'request_id': {
    #         '()': 'log_request_id.filters.RequestIDFilter'
    #     }
    # },
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",  # json configuration
            "format": "{asctime} {levelname} {name} {message} {filename} {funcName} {lineno}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            # "filters": ["request_id"]
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": os.environ.get("LOG_FILE_PATH", "/var/log/django_app.log"),
            "formatter": "json",
            # "filters": ["request_id"]
        },
    },
    "loggers": {
        "general": {"level": "DEBUG", "handlers": ["console", "file"]},
        # "error_logger": {
        #     "level": "ERROR"
        # }
    },
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),  # Default is 5 minutes; increase as needed
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # Default is 1 day
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}



SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',  # This is where the token will be passed
            'in': 'header'  # The token is sent in the header
        }
    },
    'USE_SESSION_AUTH': False, 
}

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Use SMTP for real email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")  # This will be the "from" email address

# url for password reset

RESET_PASSWORD_URL = os.environ.get("RESET_PASSWORD_URL", "http://example.com/forgot-password")
VALIDATE_USER_URL = os.environ.get("VALIDATE_USER_URL", "http://example.com/validate-user")


# use redis for caching proccesses in throttling
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    },
    "alternate": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379",
        "OPTIONS": {
            "DB": 1,
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5 MB

CORS_ALLOWED_ORIGINS=["https://epicbazaar.store", "https://www.epicbazaar.store"]

