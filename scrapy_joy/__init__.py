import django.contrib.auth
from django.conf import settings
from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured, AppRegistryNotReady


def get_user_model():
    try:
        return django_apps.get_model(settings.AUTH_USER_MODEL)
    except ValueError:
        raise ImproperlyConfigured("AUTH_USER_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured("AUTH_USER_MODEL refers to model '%s' that has not been installed" % settings.AUTH_USER_MODEL)
    except AppRegistryNotReady:
        return getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


setattr(django.contrib.auth, 'get_user_model', get_user_model)