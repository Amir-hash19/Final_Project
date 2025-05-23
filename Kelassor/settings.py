from pathlib import Path
from datetime import timedelta
from decouple import config
import kavenegar


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-06cxzy&g13tl2jq3nncijv@u51+(=k#eri=8=x8^wv@xp^%6i1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'anymail',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account.apps.AccountConfig',
    'billing.apps.BillingConfig',
    'blog.apps.BlogConfig',
    'bootcamp.apps.BootcampConfig',
    'support.apps.SupportConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Kelassor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Kelassor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "kelassor_db",
        "USER": "admin",
        "PASSWORD": "amir112233",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'


USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # استفاده از JWT
    ],
    "DEFAULT_THROTTLE_RATES": {
        "otp": "5/hour",
        },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

}    


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=4), 
}


AUTH_USER_MODEL = 'account.CustomUser'



KAVENEGAR_API_KEY = config('KAVENEGAR_API_KEY')
KAVENEGAR_SENDER = config('KAVENEGAR_SENDER')






CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'




CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'



CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # مثلاً Redis DB شماره 1
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}





# EMAIL_BACKEND = 'anymail.backends.sendgrid.EmailBackend'
# DEFAULT_FROM_EMAIL = "amirhosein.hydri1381@gmail.com"
# ADMIN_EMAIL = "amirhosein.hydri1381@gmail.com"




LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',  # فقط خطاها به فایل ذخیره می‌شوند
            'class': 'logging.FileHandler',
            'filename': 'error_log.txt',  # مسیر فایل لاگ
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],  # ارسال به فایل
            'level': 'ERROR',  # سطح لاگ‌ها
            'propagate': True,
        },
    },
}




CELERY_BEAT_SCHEDULE = {
    'check-tickets-every-day': {
        'task': 'tickets.tasks.check_and_update_ticket_status',
        'schedule': 86400.0,
    },
}    
