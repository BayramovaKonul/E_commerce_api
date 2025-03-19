from .base import * 

DEBUG = True

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DB_HOST"),
        'PORT': os.environ.get("DB_PORT"),
    }}

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")

AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME='ecommerceapibucket2'
AWS_S3_CUSTOM_DOMAIN='%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS={
   'CacheControl': 'max-age=86400',
}
AWS_LOCATION='static'
STATIC_URL= 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN,AWS_LOCATION)


STORAGES = {
   "default": {
       "BACKEND": "config.storage_backend.MediaStorage",
   },
 
   "staticfiles": {
       "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
   },
}


