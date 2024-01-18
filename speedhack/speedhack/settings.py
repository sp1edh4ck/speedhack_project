import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-insecure-p+ok_!mpq-%$j!@-hg7(%0gpnb37g7t&e((cda7bg_f=9d%8sy'

DEBUG = False

ALLOWED_HOSTS = ['158.160.127.162', '*', 'speedhack.ru', 'speedhack.online']

CSRF_TRUSTED_ORIGINS = ['http://localhost', 'http://localhost:8000', 'http://158.160.127.162']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
    'forum.apps.ForumConfig',
    'users.apps.UsersConfig',
    'market.apps.MarketConfig',
    'tools.apps.ToolsConfig',
    'sorl.thumbnail',
    'fontawesomefree',
    'django_cleanup.apps.CleanupConfig',
]

AUTHENTICATION_BACKENDS = (
    'users.backends.MyBackend',
    'django.contrib.auth.backends.ModelBackend',
)

WSGI_APPLICATION = 'speedhack.wsgi.application'

AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.ActiveUserMiddleware',
    # 'django_ratelimit.middleware.RatelimitMiddleware',
]

ROOT_URLCONF = 'speedhack.urls'

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
                'tools.context_processors.year.year',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('POSTGRES_USER', 'user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432')
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache'),
    },
}

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

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'forum:index'

# RATELIMIT_VIEW = 'forum.views.ratelimited'

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_HOST_USER = 'speedhack_sup@mail.ru'
EMAIL_HOST_PASSWORD = 'TP4ZqnL4Egpd00B08v2X'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

MEDIA_URL = 'static/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')

STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    MEDIA_URL = 'images/'
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
