#!/usr/bin/env python
# encoding: utf-8

"""
@author: william wei
@license: Apache Licence
@contact: weixiaole@baidu.com
@file: basic.py
@time: 2019/3/3 10:20 PM
"""
import os
import tabula
import utils

db_helper = utils.DBHelper()


def process_reporters(dir):
    for root, dirs, files in os.walk(dir):
        for f in files:
            if 'fee' in root:
                fee_process_reporters(f)


def fee_is_valid_row(row):
    '''
    :param row:
    :return:
    :exapmle
    NaN        NaN        NaN  2019-05-23         带强调事项段的        NaN    NaN
     38     000886       海南高速  2019-05-23             立信         65     65
    NaN        NaN        NaN  2019-05-23           无保留意见        NaN    NaN
     39     000976       华铁股份  2019-05-23      大华 标准无保留意见        155    170
    '''
    if type(row[3]) == str and len(row[3]) > 0 and '-' in row[3] and row[0] != 'NaN' and row[1] != 'NaN':
        return True
    return False


def fee_process_row(row):
    return {
        'code': row[1],
        'name': row[2],
        'date': row[3],
        'year': row[3][:4],
        'audit_name': row[4].split(' ')[0] if len(row[4]) > 0 else '',
        'audit_fee': str(row[5]).replace('万', '')
    }


def fee_process_reporters(f):
    df = tabula.read_pdf(f, pages=100)
    for index, row in df.iterrows():
        if fee_is_valid_row(row):
            fee_save_obj(fee_process_row(row))


def fee_save_obj(obj):
    company = {'code': obj['code'], 'name': obj['name']}

    # TODO
    reporter = {'year': obj['year']}

    companies = db_helper.select(utils.TABLE_COMPANY, company)
    if len(companies) > 0:
        company_id = companies[0][0]
    else:
        res = db_helper.insert(utils.TABLE_COMPANY, company)
        company_id = res.lastrowid
    reporter['company_id'] = company_id
    res = db_helper.insert(utils.TABLE_REPORT, reporter)
    print(res)