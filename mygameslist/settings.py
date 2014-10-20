"""
Django settings for mygameslist project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import steam
import dj_database_url
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_PROJ = os.path.join(BASE_DIR, 'mygameslist')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
    os.path.join(BASE_PROJ, 'templates'),
)

ALLOWED_HOSTS = ['*']

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'compressor',
    'crispy_forms',
    'django_countries',
    'django_summernote',
    'friendship',
    'imagekit',
    'qhonuskan_votes',
    'social.apps.django_app.default',
    'storages',
    # My Games list
    'mygameslist.app',
    'mygameslist.friends',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mygameslist.urls'

WSGI_APPLICATION = 'mygameslist.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config()
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'

COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

# If in production
if not 'COMPRESS_OFFLINE' in os.environ:
    COMPRESS_OFFLINE = True
    AWS_QUERYSTRING_AUTH = False
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
    AWS_BUCKET_URL = 'http://s3.amazonaws.com/{0}/'.format(
        AWS_STORAGE_BUCKET_NAME)
    MEDIA_URL = AWS_BUCKET_URL + 'media/'
    DEFAULT_FILE_STORAGE = 'mygameslist.s3utils.MediaRootS3BotoStorage'

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "social.backends.steam.SteamOpenId",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

SOCIAL_AUTH_TWITTER_LOGIN_URL = '/account/signup'
SOCIAL_AUTH_LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_SIGNUP_FORM_CLASS = 'mygameslist.app.forms.SignupForm'

SUMMERNOTE_CONFIG = {
    'inplacewidget_external_css': (
        '//netdna.bootstrapcdn.com/font-awesome/'
        '4.0.3/css/font-awesome.min.css',
    ),
    'inplacewidget_external_js': (),
}

steam_key = os.environ.get('STEAM_API_KEY')
steam.api.key.set(steam_key)
SOCIAL_AUTH_STEAM_API_KEY = steam_key
SOCIAL_AUTH_STEAM_EXTRA_DATA = ['player']

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'