"""
Django settings for shipment project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", '').split(" ")

# DEBUG = os.environ.get('DEBUG')
# SECRET_KEY = os.environ.get('SECRET_KEY')

SECRET_KEY = 'django-insecure-p5r-r-vxqwrwig22!gve-(0e@t7ki)b@rrz&bsty8s00@35p3d'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'http://localhost:3000']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # third party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'phonenumber_field',
    'corsheaders',
    'drf_yasg',
    "django_extensions",
    "django_celery_results",

    # apps
    'users',
    'orders',
    'products',
    'checkoutdetails',
    'checkoutcom',
    'location',
    'shipping',
    'currency',
    'payment',
    'contactus',
    'tarif_breakdown'
]

# only if django version >= 3.0
X_FRAME_OPTIONS = 'SAMEORIGIN'
SILENCED_SYSTEM_CHECKS = ['security.W019']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SITE_ID = 1

ROOT_URLCONF = 'shipment.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# rest_framework settings
REST_FRAMEWORK = {
     'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    # 'TEST_REQUEST_DEFAULT_FORMAT': 'json'
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle"
    ],
    'DEFAULT_THROTTLE_RATES': {
        "anon": "100/day",
        "user": "1500/day",
        # "auto-suggest": "2/sec"
    }
    
}

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_MAX_EMAIL_ADDRESSES = 1

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'api.v1.serializers.auth.CustomRegisterSerializer',
    'PASSWORD_RESET_SERIALIZER': 'api.v1.serializers.auth.CustomPasswordResetSerializer',
}

OLD_PASSWORD_FIELD_ENABLED = True

WSGI_APPLICATION = 'shipment.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': os.environ.get('POSTGRES_DB', 'deyarat_db'),
        # 'USER': os.environ.get('POSTGRES_USER', 'admin'),
        # 'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'admin'),
        # 'HOST': os.environ.get('POSTGRES_HOST', '127.0.0.1'),
        # 'PORT': os.environ.get('POSTGRES_PORT', 5432),
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'testdb',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# Auth-user
AUTH_USER_MODEL = 'users.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# smtplib
# Gmail SMTP Server
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

PROJECT_HOST = os.environ.get('PROJECT_HOST')
ACCOUNT_ADAPTER = 'shipment.adapter.CustomActivateUrlAdapter'

# Celery
CELERY_BROKER_URL=os.environ.get('CELERY_BROKER')
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']

# Aramex
ARAMEX_RATE_CALCULATOR_URL = "https://ws.dev.aramex.net/ShippingAPI.V2/RateCalculator/Service_1_0.svc?wsdl"
ARAMEX_SHIPPING_URL = "https://ws.dev.aramex.net/ShippingAPI.V2/Shipping/Service_1_0.svc?singleWsdl"
# Aramex creds
ARAMEX_USERNAME = os.environ.get('ARAMEX_USERNAME')
ARAMEX_PASSWORD = os.environ.get('ARAMEX_PASSWORD')
ARAMEX_ACCOUNT_NUMBER = os.environ.get('ARAMEX_ACCOUNT_NUMBER')
ARAMEX_ACCOUNT_PIN = os.environ.get('ARAMEX_ACCOUNT_PIN')
ARAMEX_ACCOUNT_ENTITY = os.environ.get('ARAMEX_ACCOUNT_ENTITY')
ARAMEX_ACCOUNT_COUNTRY_CODE = os.environ.get('ARAMEX_ACCOUNT_COUNTRY_CODE')

# Checkoutcom
CHECKOUTCOM_SECRET_KEY = os.environ.get('CHECKOUTCOM_SECRET_KEY')
CHECKOUTCOM_PUBLIC_KEY = os.environ.get('CHECKOUTCOM_PUBLIC_KEY')

# DHL
DHL_API_URL = os.environ.get('DHL_API_URL')
DHL_API_URN_RATES = os.environ.get('DHL_API_URN_RATES')
DHL_AUTH = os.environ.get('DHL_AUTH')  # Basic authentication
DHL_PASSWORD = os.environ.get('DHL_PASSWORD')
DHL_API_URN_SHIPMENTS = os.environ.get('DHL_API_URN_SHIPMENTS')

# Currency
# USD is considered as main currency
# USD_CURRENCY_ID = 1
USD_CURRENCY_NAME = "USD"
USD_CURRENCY_RATE = 1.0

EUR_CURRENCY_NAME = "EUR"
EUR_CURRENCY_RATE = 0.91

SAR_CURRENCY_NAME = "SAR"
SAR_CURRENCY_RATE = 3.75

#  django admin
DJANGO_ADMIN_USER = os.environ.get("DJANGO_ADMIN_USER")
DJANGO_ADMIN_PASSWORD = os.environ.get("DJANGO_ADMIN_PASSWORD")

# Countries for shipping
SHIPPING_COUNTRIES = ["US", "AE", "BH", "CN", "SA"]

COMPANY_NAME = os.environ.get('COMPANY_NAME', 'Waarid')
