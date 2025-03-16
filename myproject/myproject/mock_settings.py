# mock uses sqlite (easier than postgresql)
# see: https://docs.djangoproject.com/en/5.1/ref/settings/#databases

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-9o-%69r14(j89r36^72g9atb_6eh#3sfk(3zzj_@2(_37+v(p3"


DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "mockdatabase",
        "PORT": "5000",  # python3 manage.py runserver 5000 --settings=myproject.mock_settings
    }
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "helloapp",  # Add apps here
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "myproject.mock_urls"  # CHANGED FOR MOCK

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

STATIC_URL = "/static/"


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    # delete non-existent paths like 'helloapp'
]

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/"  # Standard-Weiterleitung nach Login
LOGOUT_REDIRECT_URL = "/"  # Standard-Weiterleitung nach Logout
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Sitzung endet mit dem Schließen des Browsers
SESSION_COOKIE_AGE = 3600  # Sitzung ist für 1 Stunde aktiv (in Sekunden)
