#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from django import template

register = template.Library()


@register.filter
def to_json(value):
    return json.dumps(value)