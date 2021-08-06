# Author: sphong1
# Class: PAGING


import math
import re


class Paging:
    @classmethod
    def set_param(cls, req, param, **kwargs):
        param['ordby_col'] = cls.get_ordby_col(req, kwargs['ordby_col'])

        if 'ordby_adc' in kwargs:
            param['ordby_adc'] = cls.get_ordby_adc(req, kwargs['ordby_adc'])
        else:
            param['ordby_adc'] = cls.get_ordby_adc(req)

        if 'page_no' in kwargs:
            param['page_no'] = cls.get_page_no(req, kwargs['page_no'])
        else:
            param['page_no'] = cls.get_page_no(req)

        if 'page_size' in kwargs:
            param['page_size'] = cls.get_page_size(req, kwargs['page_size'])
        else:
            param['page_size'] = cls.get_page_size(req)


    @classmethod
    def get_ordby_col(cls, req, ordby_col_0):
        ordby_col = req.get('ordby_col')
        if ordby_col is None:
            ordby_col = ''
        ordby_col = re.sub('[^A-Za-z0-9_.]', '', ordby_col)
        ordby_col = ordby_col.lower()
        if ordby_col == '':
            ordby_col = ordby_col_0

        return ordby_col


    @classmethod
    def get_ordby_adc(cls, req, ordby_adc_0='DESC'):
        ordby_adc = req.get('ordby_adc')
        if ordby_adc is None:
            ordby_adc = ''
        ordby_adc = re.sub('[^A-Za-z]', '', ordby_adc)
        ordby_adc = ordby_adc.upper()
        if ordby_adc == '':
            ordby_adc = ordby_adc_0

        return ordby_adc


    @classmethod
    def get_page_no(cls, req, page_no_0=1):
        page_no = req.get('page_no')
        page_no = re.sub('\D', '', str(page_no))
        if page_no == '':
            page_no = page_no_0
        else:
            page_no = int(page_no)

        return page_no


    @classmethod
    def get_page_size(cls, req, page_size_0=20):
        page_size = req.get('page_size')
        page_size = re.sub('\D', '', str(page_size))
        if page_size == '':
            page_size = page_size_0
        else:
            page_size = int(page_size)

        return page_size


    @classmethod
    def add_result(cls, param, result):
        cls.add_ordby(param, result)
        cls.add_page_no_max(param, result)
        cls.add_page_nos(param, result)
        cls.add_page_sizes(param, result)


    @classmethod
    def add_ordby(cls, param, result):
        result['ordby_col'] = param['ordby_col']
        result['ordby_adc'] = param['ordby_adc']


    @classmethod
    def add_page_no_max(cls, param, result):
        if param['page_size'] > 0:
            result['page_no_max'] = math.ceil(result['row_no_max'] / param['page_size'])
        else:
            result['page_no_max'] = 0


    @classmethod
    def add_page_nos(cls, param, result):
        page_no_unit = 10
        page_no1 = math.floor((param['page_no'] - 1) / page_no_unit) * page_no_unit + 1
        page_no2 = page_no1 + page_no_unit - 1

        if page_no1 < 1:
            page_no1 = 1

        if page_no2 > result['page_no_max']:
            page_no2 = result['page_no_max']

        page_no_prev = page_no1 - 1
        page_no_next = page_no2 + 1

        result['page_nos'] = []
        for page_no in range(page_no1, page_no2 + 1):
            result['page_nos'].append(page_no)
        result['page_no_prev'] = page_no_prev
        result['page_no_next'] = page_no_next
        result['page_no'] = param['page_no']


    @classmethod
    def add_page_sizes(cls, param, result):
        result['page_size'] = param['page_size']
        if 'page_sizes' not in result:
            result['page_sizes'] = [20, 50, 100, 200]
