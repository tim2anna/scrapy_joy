#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms


class SubscribeForm(forms.Form):
    email = forms.EmailField(label=u'邮箱')