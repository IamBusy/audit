#!/usr/bin/env python
# encoding: utf-8

"""
@author: william wei
@license: Apache Licence
@contact: weixiaole@baidu.com
@file: main.py
@time: 2019/3/3 12:13 AM
"""

import tabula
import os

AUDIT_DIR = '/Users/william/Desktop/'


def is_valid_row(row):
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


def process_row(row):
    return {
        'code': row[1],
        'name': row[2],
        'date': row[3],
        'year': row[3][:4],
        'audit_name': row[4].split(' ')[0] if len(row[4]) > 0 else '',
        'audit_fee': str(row[5]).replace('万', '')
    }


def process_fee_file(f):
    df = tabula.read_pdf('/Users/william/Desktop/2017_audit.pdf', pages=100)
    reporters = []
    for index, row in df.iterrows():
        if is_valid_row(row):
            reporters.append(process_row(row))


if __name__ == '__main__':
    for root, dirs, files in os.walk(AUDIT_DIR):
        if 'fee' in root:
            for f in files:
                pass

    # Read pdf into DataFrame

    df = tabula.read_pdf('/Users/william/Desktop/2017_audit.pdf', pages=[24])
    print(df)
    reporters = []
    for index, row in df.iterrows():
        if is_valid_row(row):
            print(process_row(row))
            reporters.append(process_row(row))
    print(len(reporters))
    print(reporters)
    #
    #
    # # Read remote pdf into DataFrame
    # df2 = tabula.read_pdf(
    #     "https://github.com/tabulapdf/tabula-java/raw/master/src/test/resources/technology/tabula/arabic.pdf")
    #
    # # convert PDF into CSV
    # tabula.convert_into("test.pdf", "output.csv", output_format="csv")
    #
    # # convert all PDFs in a directory
    # tabula.convert_into_by_batch("input_directory", output_format='csv')

