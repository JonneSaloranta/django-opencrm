SECRET_KEY = "dy@4!z_)0wjh(l-n2=56ax(8s5pj*+@^=gg78er0hq*zttb$(b"
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "opencrm",
]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
USE_I18N = True
USE_L10N = True
USE_TZ = True
