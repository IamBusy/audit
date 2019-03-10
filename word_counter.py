#!/usr/bin/env python
# encoding: utf-8

"""
@author: william wei
@license: Apache Licence
@contact: weixiaole@baidu.com
@file: word_counter.py
@time: 2019/3/3 10:46 PM
"""
import os
import jieba
from utils import db_helper, TABLE_REPORT, TABLE_COMPANY, TABLE_WORD_COUNTER

mapper = {}


def count(code, name, year, file_name):
    word_counters = []
    companies = db_helper.select(TABLE_COMPANY, {'code', code})
    if len(companies) == 0:
        return
    company_id = companies[0]['id']
    reporters = db_helper.select(TABLE_REPORT, {'year': year, 'company_id': company_id})
    if len(reporters) == 0:
        return
    reporter_id = reporters[0]['id']

    include = mapper.keys()
    with open(file_name) as fp:
        cnt = fp.read()
        interested = analysis(cnt, include)
        for k in interested:
            db_helper.insert(TABLE_WORD_COUNTER, {
                'reporter_id': reporter_id,
                'word': k,
                'counter': interested[k]})


def analysis(content, included):
    words = jieba.lcut(content)
    res = {}
    for word in words:
        if word in included:
            res[word] = res.get(word, 0) + 1
    return res


def process_word_dim(f):
    with open(f) as fp:
        for line in fp:
            line = line.strip()
            words = line.split(',')
            if len(words) >= 2:
                mapper[words[1]] = words[0]


def is_valid_word(word):
    return word in mapper


def schedule(d, word_file):
    process_word_dim(word_file)
    for root, dirs, files in os.walk(d):
        for f in files:
            if '.txt' in f and '：' in f:
                name = f.split('：')[0]
                year = f.split('：')[1][:4]
                code = root.split('/')[-1]
                count(code, name, year, os.path.join(root, f))


