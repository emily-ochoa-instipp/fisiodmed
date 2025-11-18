from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-h&gf+p-tm5ziy$emk2h9z@r)=@pnmo5h^fpq!ziww$r8=a8e*$'
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-h&gf+p-tm5ziy$emk2h9z@r)=@pnmo5h^fpq!ziww$r8=a8e*$')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.getenv('DEBUG', 'True') == 'True'

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.pacientes',
    'apps.pagos',
    'apps.servicios',
    'apps.usuarios',
    'apps.citas',
    'apps.inicio',
    'apps.dashboard',
    'apps.reportes',
    'apps.autenticacion',
    'apps.especialidades',
    'apps.medicos',
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

ROOT_URLCONF = 'fisiodmed_project.urls'

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

WSGI_APPLICATION = 'fisiodmed_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

#DATABASES = {
 #   'default': {
  #      'ENGINE': 'django.db.backends.postgresql_psycopg2',
   #     'NAME': 'BD-Fisiodmed',
    #    'USER': 'postgres',
     #   'PASSWORD': '1234',
      #  'HOST': 'localhost',
       # 'PORT': '5432',
        #'ATOMIC_REQUESTS': True,
    #}
#}

# Detectar si estamos en GitHub Actions
if os.getenv("GITHUB_ACTIONS") == "true":
    TEST_DB_PATH = "/home/runner/work/test_db.sqlite3"
else:
    TEST_DB_PATH = BASE_DIR / "db.sqlite3"


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': TEST_DB_PATH,
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS=[
    STATIC_DIR
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = 'index'

#AUTHENTICATION_BACKENDS = [
 #   'apps.autenticacion.backends.MultiFieldAuthBackend',
  #  'django.contrib.auth.backends.ModelBackend',
#]
