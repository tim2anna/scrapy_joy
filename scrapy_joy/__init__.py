#!/usr/bin/python
# -*- coding: utf-8 -*-


##################################################
# add django-dynamic-scraper function：lambda处理器
##################################################

from dynamic_scraper.utils import processors


def lambda_str(text, loader_context):
    lam_str = loader_context.get('lambda_str', '')
    return eval(lam_str)(text)


if not hasattr(processors, 'lambda_str'):
    setattr(processors, 'lambda_str', lambda_str)


###############################################
# fix xadmin bug：启动时报AppRegistryNotReady错误
###############################################

from django.contrib import auth
from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, AppRegistryNotReady


def get_user_model():
    """
    Returns the User model that is active in this project.
    """
    try:
        return django_apps.get_model(settings.AUTH_USER_MODEL)
    except ValueError:
        raise ImproperlyConfigured("AUTH_USER_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL refers to model '%s' that has not been installed" % settings.AUTH_USER_MODEL
        )
    except AppRegistryNotReady:
        return getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

setattr(auth, 'get_user_model', get_user_model)