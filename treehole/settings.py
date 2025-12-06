"""
PROJECT CONFIGURATION FILE

This file controls all Django settings:
- Which apps are installed
- Database connection
- Security settings (DEBUG, SECRET_KEY, CSRF, etc.)
- Static files location
- Template directory location

When you need to:
- Add a new app → Update INSTALLED_APPS
- Change database → Update DATABASES
- Add environment variable → Use config() function

For more information: https://docs.djangoproject.com/en/5.2/topics/settings/
"""

from pathlib import Path
from urllib.parse import urlparse

import dj_database_url
from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-change-me')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)

def _clean_host_values(raw_hosts: str) -> list[str]:
    hosts: list[str] = []
    for raw_host in raw_hosts.replace(';', ',').split(','):
        host = raw_host.strip()
        if not host:
            continue
        if '://' in host:
            parsed = urlparse(host)
            host = parsed.netloc or parsed.path
        host = host.split('/')[0].strip()
        if host:
            hosts.append(host)
    return hosts


def _host_to_origins(host: str) -> set[str]:
    host = host.strip()
    if not host:
        return set()
    if host.startswith('.'):
        return {f'https://*{host}'}
    if host in {'localhost', '127.0.0.1', '[::1]'}:
        return {f'http://{host}', f'https://{host}'}
    return {f'https://{host}'}


_raw_allowed_hosts = config(
    'DJANGO_ALLOWED_HOSTS',
    default='localhost,127.0.0.1,.onrender.com',
)
ALLOWED_HOSTS = _clean_host_values(_raw_allowed_hosts)
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

_raw_csrf_trusted = config('DJANGO_CSRF_TRUSTED_ORIGINS', default='')
_csrf_hosts = _clean_host_values(_raw_csrf_trusted)
_csrf_origin_set: set[str] = set()

if _csrf_hosts:
    for host in _csrf_hosts:
        _csrf_origin_set.update(_host_to_origins(host))
else:
    for host in ALLOWED_HOSTS:
        _csrf_origin_set.update(_host_to_origins(host))

CSRF_TRUSTED_ORIGINS = sorted(_csrf_origin_set)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SAMESITE = config('DJANGO_SESSION_COOKIE_SAMESITE', default='Lax')
CSRF_COOKIE_SAMESITE = config('DJANGO_CSRF_COOKIE_SAMESITE', default='Lax')
SESSION_COOKIE_HTTPONLY = config('DJANGO_SESSION_COOKIE_HTTPONLY', default=True, cast=bool)
CSRF_COOKIE_HTTPONLY = config('DJANGO_CSRF_COOKIE_HTTPONLY', default=True, cast=bool)
SESSION_COOKIE_SECURE = config('DJANGO_SESSION_COOKIE_SECURE', default=not DEBUG, cast=bool)
CSRF_COOKIE_SECURE = config('DJANGO_CSRF_COOKIE_SECURE', default=not DEBUG, cast=bool)
SECURE_SSL_REDIRECT = config('DJANGO_SECURE_SSL_REDIRECT', default=not DEBUG, cast=bool)
_hsts_default = 0 if DEBUG or not SECURE_SSL_REDIRECT else 31536000
SECURE_HSTS_SECONDS = config('DJANGO_HSTS_SECONDS', default=_hsts_default, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    'DJANGO_HSTS_INCLUDE_SUBDOMAINS',
    default=SECURE_HSTS_SECONDS > 0,
    cast=bool,
)
SECURE_HSTS_PRELOAD = config(
    'DJANGO_HSTS_PRELOAD',
    default=SECURE_HSTS_SECONDS >= 31536000,
    cast=bool,
)
SECURE_REFERRER_POLICY = config('DJANGO_SECURE_REFERRER_POLICY', default='strict-origin')
X_FRAME_OPTIONS = config('DJANGO_X_FRAME_OPTIONS', default='DENY')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auth_landing',
    'posting',
    'moderation_ranking',
    'profile_settings',
    'analytics',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'treehole.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'treehole.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {}

DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=config('DB_CONN_MAX_AGE', default=600, cast=int),
        ssl_require=config('DB_SSL_REQUIRE', default=not DEBUG, cast=bool),
    )
else:
    db_engine = config('DB_ENGINE', default='django.db.backends.sqlite3')
    if db_engine == 'django.db.backends.sqlite3':
        DATABASES['default'] = {
            'ENGINE': db_engine,
            'NAME': BASE_DIR / config('SQLITE_NAME', default='db.sqlite3'),
        }
    else:
        DATABASES['default'] = {
            'ENGINE': db_engine,
            'NAME': config('DB_NAME', default='treehole'),
            'USER': config('DB_USER', default='treehole'),
            'PASSWORD': config('DB_PASSWORD', default='treehole-password'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = []
if (BASE_DIR / 'static').exists():
    STATICFILES_DIRS.append(BASE_DIR / 'static')

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File upload size limits (10MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

LOGIN_REDIRECT_URL = 'posting:home'
LOGOUT_REDIRECT_URL = 'auth_landing:landing'
LOGIN_URL = 'auth_landing:login'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'treehole@yale.edu'

ALLOWED_EMAIL_DOMAINS = config('ALLOWED_EMAIL_DOMAINS', default='yale.edu', cast=Csv())

# OpenAI API Configuration (for content moderation)
OPENAI_API_KEY = config('OPENAI_API_KEY', default=None)

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
