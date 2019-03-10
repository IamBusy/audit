#!/usr/bin/env python
# encoding: utf-8

"""
@author: william wei
@license: Apache Licence
@contact: weixiaole@baidu.com
@file: utils.py
@time: 2019/3/3 2:51 PM
"""
import sqlite3
DB_NAME = 'audit.db'

TABLE_COMPANY = 'companies'
TABLE_REPORT = 'reports'
TABLE_WORD_COUNTER = 'word_counters'


class DBHelper:
    def __init__(self):
        self._conn = sqlite3.connect(DB_NAME)

    def init_schema(self):
        sqls = []
        sqls.append('''
                drop table if exists {0};
                create table {0} (
                  id integer primary key AUTOINCREMENT,
                  code varchar ,
                  name varchar 
                )
                '''.format(TABLE_COMPANY))

        sqls.append('''
                drop table if exists {0};
                create table {0} (
                  id integer primary key AUTOINCREMENT,
                  year  varchar,
                  company_id varchar, 
                  size varchar,
                  audit_fee varchar,
                  auditor varchar,
                  audit_change integer,
                  audit_opinion varchar
                )
                '''.format(TABLE_REPORT))

        sqls.append('''
                        drop table if exists {0};
                        create table {0} (
                          id integer primary key AUTOINCREMENT,
                          report_id integer,
                          word varchar,
                          counter integer
                        )
                        '''.format(TABLE_WORD_COUNTER))
        c = self._conn.cursor()
        for sql in sqls:
            for s in sql.split(';'):
                c.execute(s)
        c.close()
        self._conn.commit()

    @staticmethod
    def _parse_query(d):
        res = ''
        if type(d) == dict:
            for k in d:
                res = res + " and %s='%s'" % (k, d[k])
        return res

    def select(self, table, query):
        '''
        :param table:
        :param query:
        :return:
        '''
        c = self._conn.cursor()
        c.execute('select * from {0} where 1=1 {1}'.format(table, self._parse_query(query)))
        res = c.fetchall()
        c.close()
        self._conn.commit()
        return res

    def find(self, table, query):
        c = self._conn.cursor()
        c.execute('select * from {0} where 1=1 {1} limit 1'.format(table, self._parse_query(query)))
        res = c.fetchone()
        c.close()
        self._conn.commit()
        return res

    def insert(self, table, obj):
        '''
        :param table:
        :type table str
        :param obj:
        :type obj: dict
        :return:
        '''
        c = self._conn.cursor()
        values = ','.join(map(lambda k: "'%s'" % obj[k], obj.keys()))
        res = c.execute('insert into {0} ({1}) values ({2})'.format(table, ','.join(obj.keys()), values))
        c.close()
        self._conn.commit()
        return res

    def update(self, table, obj, query):
        '''
        :param table:
        :param obj:
        :type obj: dict
        :param query:
        :type query: dict
        :return:
        '''
        c = self._conn.cursor()
        values = ','.join(map(lambda k: " %s='%s' " % (k, obj[k]), obj.keys()))
        # print('update {0} set {1} where {2};'.format(table, values, self._parse_query(query)))
        res = c.execute('update {0} set {1} where 1=1 {2};'.format(table, values, self._parse_query(query)))

        c.close()
        self._conn.commit()
        return res

    def delete(self, table, query):
        c = self._conn.cursor()
        c.execute('delete from {0} where 1=1 {1}'.format(table, self._parse_query(query)))
        c.close()
        self._conn.commit()


def str_trim(s):
    return str(s).strip()


def str_is_nan(s):
    s = str(s).strip()
    return len(s) == 0 or s == 'NaN' or s == 'nan'


db_helper = DBHelper()
