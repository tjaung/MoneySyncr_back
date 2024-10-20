"""
Django settings for budgetTracker project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import sys
import dj_database_url
from pathlib import Path
from os import getenv, path
import dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# environment vars
dotenv_file = BASE_DIR / '.env'
# config = None
# if path.isfile(dotenv_file):
#     config = dotenv.dotenv_values(dotenv_file)
dotenv_file = BASE_DIR / '.env.local'

if path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

DEVELOPMENT_MODE = getenv('DEVELOPMENT_MODE', 'False') == 'True'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&=ijq=o8=v#*6*_3k^3idtz01082@n9mcjx)9_i!+qnylxj99)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = getenv('DJANGO_ALLOWED_HOSTS',
                       '127.0.0.1,localhost').split(',')

CORS_ALLOWED_ORIGINS = [
    'https://localhost:3000',  # Example: frontend origin
]

CORS_ALLOW_CREDENTIALS = True

#env("DJANGO_ALLOWED_HOSTS", '127.0.0.1:8000,localhost').split(',')


# Application definition

INSTALLED_APPS = [
    'users',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'djoser',
    'corsheaders',
    'storages'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'budgetTracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'budgetTracker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if DEVELOPMENT_MODE is True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": path.join(BASE_DIR, "db.sqlite3"),
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "default": dj_database_url.parse(getenv("DATABASE_URL")),
    }



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Email
EMAIL_BACKEND = 'django_ses.SESBackend'
DEFAULT_FROM_EMAIL = getenv('AWS_SES_FROM_EMAIL')
AWS_SES_ACCESS_KEY_ID=getenv('AWS_SES_ACCESS_KEY_ID')
AWS_SES_SECRET_ACCESS_KEY=getenv('AWS_SES_SECRET_ACCESS_KEY')
USE_SES_V2 = True

AWS_SES_REGION_ENDPOINT=f'email.us-{getenv('AWS_SES_REGION_NAME')}.amazonaws.com'
AWS_SES_FROM_EMAIL = getenv('AWS_SES_FROM_EMAIL')

DOMAIN = getenv("DOMAIN")
SITE_NAME = 'MoneySyncr'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

'''
{
    "firstName": "John",
    "lastName": "Doe",
    "address": "1 Main st",
    "city": "NYC",
    "state": "NY",
    "zipCode": "01010",
    "phone": "1112223333",
    "email": "johndoe@gmail.com",
    "username": "jd243",
    "password": "Password@111"
}
'''

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
if DEVELOPMENT_MODE:
    STATIC_URL = 'static/'
    STATIC_ROOT = BASE_DIR / 'static'
    MEDIA_URL = 'media/'
    MEDIA_ROOT = BASE_DIR / 'media'
else: 
    AWS_S3_ACCESS_KEY_ID = getenv('AWS_S3_ACCESS_KEY_ID')
    AWS_S3_SECRET_ACCESS_KEY = getenv('AWS_S3_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = getenv('AWS_S3_REGION_NAME')
    AWS_S3_ENDPOINT_URL = f'https://{AWS_S3_REGION_NAME}.digitaloceanspaces.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400'
    }
    AWS_DEFAULT_ACL = 'public-read'
    AWS_LOCATION = 'static'
    AWS_MEDIA_LOCATION = 'media'
    AWS_S3_CUSTOM_DOMAIN = getenv('AWS_S3_CUSTOM_DOMAIN')
    STORAGES = {
        'default': {'BACKEND': 'custom_storages.CustomS3Boto3Storage'},
        'staticfiles': {'BACKEND': 'storages.backends.s3boto3.S3StaticStorage'}
    }

# Rest framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'users.authentication.CustomJWTAuthentication'
    ]
}

AUTH_COOKIE = 'access'
AUTH_COOKIE_ACCESS_MAX_AGE = 60 * 5 # 5 min
AUTH_COOKIE_REFRESH_MAX_AGE = 60 * 60 * 24 # 24 hours
AUTH_COOKIE_SECURE = False
AUTH_COOKIE_HTTP_ONLY = True
AUTH_COOKIE_PATH = '/'
AUTH_COOKIE_SAMESITE = 'None' # cross origin



DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    #If True, you need to pass re_new_password to /users/reset_password_confirm/ endpoint in order to validate password equality.
    'SEND_ACTIVATION_EMAIL': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    #URL to your frontend activation page. It should contain {uid} and {token} placeholders, e.g. #/activate/{uid}/{token}. You should pass uid and token to activation endpoint.
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    #If True, you need to pass re_new_password to /users/reset_password_confirm/ endpoint in order to validate password equality.
    'LOGOUT_ON_PASSWORD_CHANGE': True,
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': False,
    'TOKEN_MODEL': None,
    'SERIALIZERS': {
        'user_create': 'users.serializers.UserCreateSerializer',  # Pointing to your custom serializer
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',  # Change this to 'INFO' or 'ERROR' as needed
        },
        'djoser': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.UserAccount'