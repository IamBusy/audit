#!/usr/bin/env python
# encoding: utf-8

"""
@author: william wei
@license: Apache Licence
@contact: weixiaole@baidu.com
@file: main.py
@time: 2019/3/3 12:13 AM
"""

import utils
import basic
import sys
import word_counter

AUDIT_DIR = './resources/audit'


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'init':
        utils.db_helper.init_schema()
    else:
        utils.db_helper.init_schema()
        # basic.process_reporters(AUDIT_DIR)
        word_counter.schedule('./resources/report', './resources/wordmap.csv')


