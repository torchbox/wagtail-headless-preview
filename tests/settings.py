import os


DEBUG = "INTERACTIVE" in os.environ

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = "fake_secret_key_to_run_tests"  # pragma: allowlist secret

INSTALLED_APPS = [
    "tests.testapp",
    "wagtail_headless_preview",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.images",
    "wagtail.documents",
    "wagtail.admin",
    "wagtail.core",
    "wagtail.api.v2",
    "taggit",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
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

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}}

ALLOWED_HOSTS = ["*"]

USE_TZ = True

ROOT_URLCONF = "tests.urls"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

WAGTAIL_HEADLESS_PREVIEW_ROOT = os.path.dirname(__file__)
STATIC_ROOT = os.path.join(WAGTAIL_HEADLESS_PREVIEW_ROOT, "test-static")
MEDIA_ROOT = os.path.join(WAGTAIL_HEADLESS_PREVIEW_ROOT, "test-media")
MEDIA_URL = "/media/"
STATIC_URL = "/static/"

WAGTAIL_SITE_NAME = "wagtail-headless-preview test"

WAGTAIL_HEADLESS_PREVIEW = {"CLIENT_URLS": {"default": "http://localhost:8020/"}}

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r"^/api/v2/"
