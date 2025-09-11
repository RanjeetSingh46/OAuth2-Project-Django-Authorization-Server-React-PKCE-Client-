import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-dev')
DEBUG = True  
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'rest_framework','oauth2_provider','corsheaders','users','client_backend',
]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
ROOT_URLCONF = 'auth_server.urls'
TEMPLATES = [{ 'BACKEND': 'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates'],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'auth_server.wsgi.application'
DATABASES = {'default': {'ENGINE': os.environ.get('DB_ENGINE','django.db.backends.sqlite3'),'NAME': os.environ.get('DB_NAME', BASE_DIR / 'db.sqlite3'),'USER': os.environ.get('DB_USER',''),'PASSWORD': os.environ.get('DB_PASSWORD',''),'HOST': os.environ.get('DB_HOST',''),'PORT': os.environ.get('DB_PORT',''),}}
AUTH_USER_MODEL = 'users.User'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
}
OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': int(os.environ.get('ACCESS_TOKEN_EXPIRE_SECONDS', 3600)),
    'REFRESH_TOKEN_EXPIRE_SECONDS': int(os.environ.get('REFRESH_TOKEN_EXPIRE_SECONDS', 60*60*24*14)),
    'AUTHORIZATION_CODE_EXPIRE_SECONDS': int(os.environ.get('AUTHORIZATION_CODE_EXPIRE_SECONDS', 300)),
    'ROTATE_REFRESH_TOKEN': True,
    'SCOPES': {'read': 'Read', 'write': 'Write'},
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.OAuthLibCore',
    'ALLOWED_REDIRECT_URI_SCHEMES': ['http','https'],
    'ERROR_RESPONSE_WITH_SCOPES': False,
}
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS','http://localhost:3000').split(',')
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False  # Set True for development
CORS_ALLOWED_ORIGIN_REGEXES = []
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE','False')=='True'
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE','False')=='True'
CSRF_COOKIE_SAMESITE = os.environ.get('CSRF_COOKIE_SAMESITE','Lax')
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT','False')=='True'
CSRF_TRUSTED_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'oauth2_provider': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'oauthlib': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
