import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ["158.160.65.32", "127.0.0.1", "localhost", "boaruzhan-foodgram.sytes.net", "backend"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'recipes.apps.RecipesConfig',
    'users',
    'ingredients.apps.IngredientsConfig',
    'tags.apps.TagsConfig',
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

ROOT_URLCONF = 'foodgram.urls'

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

WSGI_APPLICATION = 'foodgram.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

#Для локального
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'foodgramlocal',
        'USER': 'postgres',
        'PASSWORD': '19216812',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

#Для Докера
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': os.getenv('POSTGRES_DB', ''),
#        'USER': os.getenv('POSTGRES_USER', ''),
#        'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
#        'HOST': os.getenv('DB_HOST', ''),
#        'PORT': os.getenv('DB_PORT', 5432)
#    }
#}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'SEARCH_PARAM': 'name'
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#AUTHENTICATION_BACKENDS = (
#   "django.contrib.auth.backends.ModelBackend",
#   "allauth.account.auth_backends.AuthenticationBackend"
#)


DJOSER = {
    'SERIALIZERS': {
        'user_create': 'users.serializers.UsersCreateSerializer',
        'user': 'users.serializers.UsersSerializer',
        'current_user': 'users.serializers.UsersSerializer',
    },
    #'PERMISSIONS': {
    #    'user': ['rest_framework.permissions.AllowAny'],
    #    'user_list': ['rest_framework.permissions.AllowAny']
    #},
    'LOGIN_FIELD': 'email',
    'HIDE_USERS': False,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': False,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': False,
    'SEND_CONFIRMATION_EMAIL': False,
    'SEND_ACTIVATION_EMAIL': False
}
