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


def url_hour_arg(text, loader_context):
    """ 加上小时的时间戳 """
    from datetime import datetime
    url = loader_context.get('url_hour_arg', '')
    return url + '#' + datetime.now().strftime('%Y%m%d%H')

if not hasattr(processors, 'url_hour_arg'):
    setattr(processors, 'url_hour_arg', url_hour_arg)



try:
    from dynamic_scraper import migrations
    import shutil
    shutil.rmtree(migrations.__dict__['__path__'][0])
    print '######', u'删除migrations'
except:
    pass


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


################################################################
# fix xadmin bug：AuthenticationForm没有check_for_test_cookie方法
################################################################
from django.contrib.auth.forms import AuthenticationForm


def check_for_test_cookie(self):
    pass

setattr(AuthenticationForm, 'check_for_test_cookie', check_for_test_cookie)


from django.http import HttpResponse


def __init__(self, content=b'', *args, **kwargs):
    if 'mimetype' in kwargs:
        mimetype = kwargs.pop('mimetype')
        kwargs['content_type'] = mimetype
    super(HttpResponse, self).__init__(*args, **kwargs)
    self.content = content

setattr(HttpResponse, '__init__', __init__)



