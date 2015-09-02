#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
自定义的数据处理器
"""


def convert_amount(value):
    return float(value.replace(',', ''))