# Author: sphong1
# Class: PostGreSQL


import configparser
import logging
import os
import psycopg2
import psycopg2.extras
from cbi.lib.basic.cfg import Cfg


class Pgsql:
    def __init__(self, db_id='', **kwargs):
        logging.info('__init__ called')
        self.db_id = db_id
        self.conn = None
        self.cursor = None
        if self.db_id:
            self.connect(**kwargs)


    def __del__(self):
        logging.info('__del__ called')
        self.close()


    def connect(self, **kwargs):
        cfp = configparser.ConfigParser()
        cfp.read(os.path.join(Cfg.SHP_CFG_DIR, 'ini', 'db.ini'))
        cf = cfp[self.db_id]
        for kw in kwargs:
            if isinstance(kwargs[kw], str):
                cf[kw] = kwargs[kw]
        if 'cursor_factory' not in kwargs:
            kwargs['cursor_factory'] = psycopg2.extras.DictCursor

        try:
            self.conn = psycopg2.connect(host=cf['host'], port=cf['port'], user=cf['user'], password=cf['password'], dbname=cf['dbname'])
        except Exception as err:
            logging.info('ERR_psycopg2_connect: ' + str(err))
            raise err

        self.cursor = self.conn.cursor(cursor_factory=kwargs['cursor_factory'])


    def close(self):
        if self.cursor:
            if not self.cursor.closed:
                self.cursor.close()
                logging.info('cursor.close called')
        if self.conn:
            if not self.conn.closed:
                self.conn.close()
                logging.info('conn.close called')


    def execute(self, query, param={}):
        try:
            self.cursor.execute(query, param)
        except Exception as err:
            logging.info('ERR_cursor_execute: ' + str(err) + self.cursor.query.decode())
            self.rollback()
            raise err


    def fetchall(self):
        return self.cursor.fetchall()


    def fetchone(self):
        return self.cursor.fetchone()


    def commit(self):
        self.conn.commit()


    def rollback(self):
        self.conn.rollback()


    def get_qryord(self, param):
        if 'ordby_col' in param and 'ordby_adc' in param:
            qryord = f"ORDER BY {param['ordby_col']} {param['ordby_adc']}"
        else:
            qryord = ''

        return qryord


    def get_qrylim(self, param):
        if 'page_no' in param and 'page_size' in param:
            offset = (param['page_no'] - 1) * param['page_size']
            qrylim = f"OFFSET {offset} LIMIT {param['page_size']}"
        else:
            qrylim = ''

        return qrylim
