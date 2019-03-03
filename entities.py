#!/usr/bin/env python
# encoding: utf-8

"""
@author: william wei
@license: Apache Licence
@contact: weixiaole@baidu.com
@file: entities.py
@time: 2019/3/3 3:03 PM
"""
class Company:
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self._name = kwargs['name']
        if 'code' in kwargs:
            pass