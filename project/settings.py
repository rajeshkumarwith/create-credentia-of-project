"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d2auczr*%m$^$lr(emwu6#gc+i7l8hv)=1__zz%^y1_0sv*ef^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'rest_framework',
    'corsheaders',
    'rest_framework_swagger',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_filters',
    'oauth2_provider',
    # 'social_django',
    'drf_social_oauth2',
    'rest_framework.authtoken',
    'rest_auth',
    'doddle',

]


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]
SOCIALACCOUNT_LOGIN_ON_GET=True


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}


AUTH_USER_MODEL = 'doddle.User'


SITE_ID = 1
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'




REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'drf_social_oauth2.authentication.SocialAuthentication',
        
      )
}
AUTHENTICATION_BACKENDS = (
   'social_core.backends.google.GoogleOAuth2',
   'drf_social_oauth2.backends.DjangoOAuth2',
   'django.contrib.auth.backends.ModelBackend',
)


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '286943146870-h21okc0jtogcva4mrmi28h4fpkcaagum.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}
GOOGLE_CLIENT_ID = '286943146870-h21okc0jtogcva4mrmi28h4fpkcaagum.apps.googleusercontent.com'
SOCIAL_SECRET = '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'
SITE_ID = 1

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '286943146870-3n2anft2m2ths4lkdfk5a0qh1mld70sf.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET ='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'

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

SOCIAL_AUTH_URL_NAMESPACE = 'social'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    
]
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://psd2htmlx.com:5050',
    'https://accounts.google.com',
    'https://app.doddlehq.com',
    

]

ROOT_URLCONF = 'project.urls'
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
            'django.template.context_processors.request',
            'social_django.context_processors.backends',
            'social_django.context_processors.login_redirect',

        ],
    },
},]


WSGI_APPLICATION = 'project.wsgi.application'

SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False



# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STAR_RATINGS_RERATE = True 
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




