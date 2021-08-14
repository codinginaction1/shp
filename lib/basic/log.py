# Author: sphong1


from flask import request
import logging
import os
import re
import time
from cbi.lib.basic.cfg import Cfg


class Log:
    @staticmethod
    def set_logger(name=''):
        if name == '':
            if request:
                # 너무 하위 경로로 구분하지 않고 상위 경로 두 레벨까지만 사용한다.
                path = re.sub('^(/\w+/\w+).*$', '\\1', request.path)
                name = request.script_root + path
                if name[-1:] == '/':
                    name += 'index'
            else:
                name = __file__
                name = name.replace(Cfg.USR_DIR, '')
        else:
            name = os.path.abspath(name)
            name = name.replace(Cfg.USR_DIR, '')
        name = name.lstrip('/')
        name = re.sub('\.py$', '', name)
        name = name.replace('/', '.')

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        dir_name = os.path.join(Cfg.SHP_LOG_DIR, time.strftime('%Y%m%d'))
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
            os.chmod(dir_name, 0o757)
        file_name = os.path.join(dir_name, name + '.log')
        fh = logging.FileHandler(file_name)
        where = '%(remote_addr)s' if request else 'cli'
        fmt = '%(asctime)s ' + where + ' [%(process)d:%(thread)d %(processName)s:%(threadName)s] [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
        if request:
            fmtr = RequestFormatter(fmt)
        else:
            fmtr = logging.Formatter(fmt)
        fh.setFormatter(fmtr)
        logger.addHandler(fh)


    @staticmethod
    def unset_logger():
        logger = logging.getLogger()
        for handler in logger.handlers:
            logger.removeHandler(handler)


    @staticmethod
    def logging_access():
        logging.info('')


    @staticmethod
    def logging_begin():
        logging.info('--- begin ---')


    @staticmethod
    def logging_end():
        logging.info('--- end ---')


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.remote_addr = request.remote_addr
        return super(RequestFormatter, self).format(record)
