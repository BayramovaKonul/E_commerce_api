from pathlib import Path
import os
from datetime import timedelta
# from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS=["127.0.0.1","localhost"]

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
    # installed apps
    'rest_framework',
    # "debug_toolbar",
    'rest_framework_simplejwt',
    # 'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    # 'django_celery_beat',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     # 'rest_framework.throttling.AnonRateThrottle',   # IP based checking
    #     # 'rest_framework.throttling.UserRateThrottle',    # pk based checking after login, keep rate in cache-backend
    #     'rest_framework.throttling.ScopedRateThrottle',   # general scope for all api's
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     # 'anon': '3/min',
    #     # 'user': '10/min',
    #     'create_article': '3/min',
    #     'regular_user':'5/hour',
    #     'admin': '10/hour',
    #     'update_profile' : '5/hour',
    #     'add_bookmark' : '5/min',
    #     'delete_bookmark' : '20/min',
    #     'adding_follower':'15/min',
#     },
#     'THROTTLE_CACHE':'alternate'
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
            "filename": "logs/general_logs.log",
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

# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=45),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
#     "ROTATE_REFRESH_TOKENS": False,  #create refreh and access token when you send refresh token
#     "BLACKLIST_AFTER_ROTATION": False,  # write previous refresh token to the blacklist
#     "UPDATE_LAST_LOGIN": False,


#     "TOKEN_OBTAIN_SERIALIZER": "account.serializers.CustomTokenObtainPairSerializer",
#     "TOKEN_REFRESH_SERIALIZER": "account.serializers.CustomTokenRefreshSerializer",
# }

# SWAGGER_SETTINGS = {
#     'SECURITY_DEFINITIONS': {
#         'Bearer': {
#             'type': 'apiKey',
#             'name': 'Authorization',  # This is where the token will be passed
#             'in': 'header'  # The token is sent in the header
#         }
#     },
#     'USE_SESSION_AUTH': False,  # Disable session auth if you're using token-based auth
# }

# CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
# CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Use SMTP for real email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")  # This will be the "from" email address


# CELERY_BEAT_SCHEDULE = {
#     'send-user-count-every-midnight': {
#         'task': 'account.task.send_user_count_to_admin',
#         'schedule': crontab(minute=0, hour=12)  # Runs at 12:00 PM every day
#     },
# }

# # use redis for caching proccesses in throttling
# CACHES = {
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    # },
#     "alternate": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://redis:6379",
#         "OPTIONS": {
#             "DB": 1,
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

