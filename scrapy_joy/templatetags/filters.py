#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import locale
from decimal import Decimal
from django import template

register = template.Library()


@register.filter
def to_json(value):
    return json.dumps(value)


@register.filter
def to_abs(value):
    return abs(value)


@register.filter
def amount_split(value):
    """ 用逗号分隔数据 """
    return '{:,}'.format(float(value))
