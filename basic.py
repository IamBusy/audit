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
from utils import db_helper, TABLE_COMPANY, TABLE_REPORT, TABLE_WORD_COUNTER


def process_reporters(dir):
    for root, dirs, files in os.walk(dir):
        for f in files:
            if '.pdf' not in f:
                continue
            if 'fee' in root:
                # fee_process_reporters(os.path.join(root, f))
                pass
            elif 'change' in root:
                change_process_reporters(os.path.join(root, f))
                pass
            elif 'opinion' in root:
                pass
            else:
                pass


def change_process_reporters(f):
    try:
        file_name = f.split('/')[-1]
        year = file_name[:4]
        df = tabula.read_pdf(f, pages='all')
        for index, row in df.iterrows():
            if '-' in date:
                date = utils.str_trim(row[2])
                code = str(utils.str_trim(row[0])).split(' ')[-1]
                company = db_helper.find(TABLE_COMPANY, {'code': code})
                if not company:
                    continue
                reporter = db_helper.find(TABLE_REPORT, {'company_id': company['id'], 'year': year})
                if not reporter:
                    continue
                db_helper.update(TABLE_REPORT, {'audit_change', 1}, {'id': reporter['id']})
    except Exception as e:
        pass


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
    col0_fields = list(filter(lambda x: len(x) > 0, str(row[0]).split(' ')))
    if len(col0_fields) > 1:
        code = col0_fields[1]
        if code == '600558':
            print(row)
        if len(col0_fields) > 2:
            name = col0_fields[2]
        elif not utils.str_is_nan(row[1]):
            name = utils.str_trim(row[1])
        elif not utils.str_is_nan(row[2]):
            name = utils.str_trim(row[2])
    else:
        col1 = str(row[1]).strip()
        code = col1 if len(col1) == 6 else col1.split(' ')[0]
        name = str(row[2]).strip() if len(col1) == 6 else None
        if name is None:
            name = ''
            for x in col1.split(' ')[1:]:
                name += x
    if code == '600558':
        print(row)
    res = {
        'code': code,
        'name': name,
        'date': row[3],
        'year': row[3][:4],
        'audit_name': str(row[4]).split(' ')[0] if len(str(row[4])) > 0 else '',
        'audit_fee': str(row[5]).replace('万', '')
    }
    if res['name'] == '':
        print(res)
    return res


def fee_process_reporters(f):
    try:
        df = tabula.read_pdf(f, pages='all')
        for index, row in df.iterrows():
            if fee_is_valid_row(row):
                fee_save_obj(fee_process_row(row))
    except Exception as e:
        pass


def fee_save_obj(obj):
    reporter = {
        'year': obj['year'],
        'auditor': obj['audit_name'],
        'audit_fee': obj['audit_fee']}

    companies = db_helper.select(utils.TABLE_COMPANY, {
        'code': obj['code'],

    })
    if len(companies) > 0:
        company_id = companies[0][0]
    else:
        res = db_helper.insert(utils.TABLE_COMPANY, {
            'code': obj['code'],
            'name': obj['name']
        })
        company_id = res.lastrowid
    reporter['company_id'] = company_id
    db_helper.insert(utils.TABLE_REPORT, reporter)
