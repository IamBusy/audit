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
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, ProcessPoolExecutor
import jieba
from utils import db_helper, TABLE_REPORT, TABLE_COMPANY, TABLE_WORD_COUNTER, DBHelper

mapper = {}


def count(code, name, year, file_name):
    word_counters = []
    # companies = db_helper.select(TABLE_COMPANY, {'code', code})
    # if len(companies) == 0:
    #     return
    # company_id = companies[0][0]
    # reporters = db_helper.select(TABLE_REPORT, {'year': year, 'company_id': company_id})
    # if len(reporters) == 0:
    #     return
    # reporter_id = reporters[0][0]
    db = DBHelper()
    try:
        include = mapper.keys()
        with open(file_name) as fp:
            cnt = fp.read()
            interested = analysis(cnt, include)
            for k in interested:
                db.insert(TABLE_WORD_COUNTER, {
                    'report_id': -1,
                    'word': k,
                    'counter': interested[k],
                    'code': code,
                    'year': year,
                    'name': name,
                    'group_name': mapper[k]
                })
    except Exception as e:
        print(e)


def analysis(content, included):
    words = jieba.lcut(content)
    res = {}
    for word in words:
        if word in included:
            res[word] = res.get(word, 0) + 1
            # k = mapper[word]
            # res[k] = res.get(k, 0) + 1
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
    # executor = ThreadPoolExecutor(max_workers=10)
    executor = ProcessPoolExecutor(max_workers=4)
    all_tasks = []
    for root, dirs, files in os.walk(d):
        for f in files:
            if '.txt' in f and '：' in f:
                name = f.split('：')[0]
                year = f.split('：')[1][:4]
                code = root.split('/')[-2]
                if len(all_tasks) % 1000 == 0:
                    print("Task %d\n" % len(all_tasks))
                all_tasks.append(executor.submit(count, code, name, year, os.path.join(root, f)))
    wait(all_tasks, return_when=ALL_COMPLETED)

