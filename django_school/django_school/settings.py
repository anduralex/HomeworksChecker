"""
Django settings for django_school project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd$pxg6fisc4iwzk&vz^s_d0lkf&k63l5a8f!obktw!jg#4zvp3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # crispy to ignore as_p,as_list
    'crispy_forms',
    # My app
    'classroom',
    # Codemirror
    'djangocodemirror',

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

ROOT_URLCONF = 'django_school.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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

WSGI_APPLICATION = 'django_school.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# Custom Django auth settings

AUTH_USER_MODEL = 'classroom.User'

LOGIN_URL = 'login'

LOGOUT_URL = 'logout'

LOGIN_REDIRECT_URL = 'home'

LOGOUT_REDIRECT_URL = 'home'


# Messages built-in framework

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


# Third party apps configuration

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# ==============================================================================
# CODE MIRROR SETTINGS
# ==============================================================================
# Template string for HTML Code to instanciate CodeMirror for a field.
CODEMIRROR_FIELD_INIT_JS = (u"""<script>var {varname} = """
                            """CodeMirror.fromTextArea("""
                            """document.getElementById("{inputid}"),"""
                            """{settings});</script>""")

# Available CodeMirror configurations.
CODEMIRROR_SETTINGS = {

    'empty': {},

    'javascript': {
        'modes': ['javascript'],
        'theme': 'neat',
        'matchBrackets': True,
        'continueComments': "Enter",
        'extraKeys': {"Ctrl-Q": "toggleComment"},
        'addons': [
            "CodeMirror/addon/edit/matchbrackets.js",
            "CodeMirror/addon/comment/continuecomment.js",
            "CodeMirror/addon/comment/comment.js",
        ],
    },

    'restructuredtext': {
        'mode': 'rst',
        'modes': ['python', 'stex', 'rst'],
        'theme': 'neat',
        'addons': [
            "CodeMirror/addon/mode/overlay.js",
        ],
    },

    'html': {
        'mode': 'htmlmixed',
        'modes': ['xml', 'javascript', 'css', 'vbscript', 'htmlmixed'],
        'theme': 'neat',
    },

    'django': {
        'mode': 'django',
        'modes': ['xml', 'javascript', 'css', 'vbscript', 'htmlmixed',
                  'django'],
        'theme': 'neat',
        'addons': [
            "CodeMirror/addon/mode/overlay.js",
        ],
    },

    'css': {
        'modes': ['css'],
        'theme': 'neat',
        'matchBrackets': True,
        'extraKeys': {"Ctrl-Space": "autocomplete"},
        'addons': [
            "CodeMirror/addon/edit/matchbrackets.js",
            "CodeMirror/addon/hint/show-hint.js",
            "CodeMirror/addon/hint/css-hint.js",
        ],
        'extra_css': [
            "CodeMirror/addon/hint/show-hint.css",
        ],
    },

    'scss': {
        'mode': 'text/x-scss',
        'modes': ['css'],
        'theme': 'neat',
        'matchBrackets': True,
        'addons': [
            "CodeMirror/addon/edit/matchbrackets.js",
        ],
    },

    'python': {
        'mode': {
            'name': "python",
            'version': 3,
            'singleLineStringErrors': False,
        },
        'modes': ['python'],
        'theme': 'neat',
        'matchBrackets': True,
        'addons': [
            "CodeMirror/addon/edit/matchbrackets.js",
        ],
    },
}

# List of CodeMirror Javascript base files that will be loaded before every
# other CodeMirror Javascript components.
CODEMIRROR_BASE_JS = ["CodeMirror/lib/codemirror.js"]

# List of CodeMirror CSS base files that will be loaded before themes.
CODEMIRROR_BASE_CSS = ["CodeMirror/lib/codemirror.css"]

# Available CodeMirror CSS Theme files.
CODEMIRROR_THEMES = {
    "ambiance": "CodeMirror/theme/ambiance.css",
    'theme': 'neat',
}

# Available CodeMirror Javascript mode files.
CODEMIRROR_MODES = {
    "css": "CodeMirror/mode/css/css.js",
    "django": "CodeMirror/mode/django/django.js",
    "htmlmixed": "CodeMirror/mode/htmlmixed/htmlmixed.js",
    "javascript": "CodeMirror/mode/javascript/javascript.js",
    "python": "CodeMirror/mode/python/python.js",
    "rst": "CodeMirror/mode/rst/rst.js",
    "stex": "CodeMirror/mode/stex/stex.js",
    "vbscript": "CodeMirror/mode/vbscript/vbscript.js",
    "xml": "CodeMirror/mode/xml/xml.js",
}

# HTML element to load a Javascript asset
CODEMIRROR_JS_ASSET_TAG = (u'<script type="text/javascript" '
                           'src="{url}"></script>')

# HTML element to load a CSS asset
CODEMIRROR_CSS_ASSET_TAG = u'<link rel="stylesheet" href="{url}">'

# Template string for Javascript bundle names
CODEMIRROR_BUNDLE_CSS_NAME = "dcm-{settings_name}_css"

# Template string for CSS bundle names
CODEMIRROR_BUNDLE_JS_NAME = "dcm-{settings_name}_js"

# Option arguments used to build CSS bundles with ``django-assets``.
CODEMIRROR_BUNDLE_CSS_OPTIONS = {
    'filters': 'yui_css',
    'output': 'css/dcm-{settings_name}.min.css',
}

# Option arguments used to build Javascript bundles with ``django-assets``.
CODEMIRROR_BUNDLE_JS_OPTIONS = {
    'filters': 'yui_js',
    'output': 'js/dcm-{settings_name}.min.js',
}

#
# DjangoCodemirror settings
#
from djangocodemirror.settings import *
from djangocodemirror.helper import codemirror_settings_update

CODEMIRROR_SETTINGS = codemirror_settings_update(CODEMIRROR_SETTINGS, {
    'lineWrapping': True,
    'lineNumbers': True,
    'theme': 'neat',
})
