from __future__ import absolute_import, unicode_literals

import os

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DATABASE_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("DATABASE_NAME", "wagtail_review"),
        "USER": os.environ.get("DATABASE_USER", None),
        "PASSWORD": os.environ.get("DATABASE_PASS", None),
        "HOST": os.environ.get("DATABASE_HOST", None),
        "TEST": {"NAME": os.environ.get("DATABASE_NAME", None)},
    }
}


SECRET_KEY = "not needed"

ROOT_URLCONF = "wagtail_headless_preview.tests.urls"

STATIC_URL = "/static/"

STATICFILES_FINDERS = ("django.contrib.staticfiles.finders.AppDirectoriesFinder",)

USE_TZ = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
            "debug": True,
        },
    }
]

# Django 1.11
MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.core.middleware.SiteMiddleware",
)

# Django 2.x
MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.core.middleware.SiteMiddleware",
)

INSTALLED_APPS = (
    "wagtail_headless_preview",
    "wagtail_headless_preview.tests.testapp",
    "wagtail.search",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.images",
    "wagtail.documents",
    "wagtail.admin",
    "wagtail.core",
    "wagtail.api.v2",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)

PASSWORD_HASHERS = (
    "django.contrib.auth.hashers.MD5PasswordHasher",  # don't use the intentionally slow default password hasher
)

WAGTAIL_SITE_NAME = "wagtail-headless-preview test"
BASE_URL = "http://test.local"

HEADLESS_PREVIEW_CLIENT_URLS = {"default": "http://localhost:8020/"}

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r"^/api/v2/"
