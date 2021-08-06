# Author: sphong1
# Class: ConFiGuration


import configparser
import os


class Cfg:
    CBI_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    CBI_CFG_DIR = CBI_DIR + '/cfg'
    CBI_LOG_DIR = CBI_DIR + '/log'
    CBI_PRI_DIR = CBI_DIR + '/pri'
    CBI_PUB_DIR = CBI_DIR + '/pub'

    USR_DIR = os.path.dirname(CBI_DIR)

    CBI_APPAPI_URL = 'http://3.35.209.41/cbi/appapi'
    CBI_APPATH_URL = 'http://3.35.209.41/cbi/appath'
    CBI_APPMGR_URL = 'http://3.35.209.41/cbi/appmgr'


    @staticmethod
    def get_ini(filename, section, name=''):
        cfp = configparser.ConfigParser()
        cfp.read(Cfg.CBI_CFG_DIR + '/ini/' + filename)
        cfps = cfp[section]
        if name:
            return cfps[name]
        else:
            return cfps


    @staticmethod
    def get_headers_auth(app_id):
        return {'Authorization': 'Bearer ' + Cfg.get_access_token(app_id)}


    @staticmethod
    def get_access_token(app_id):
        token = Cfg.get_token(app_id)
        return token['access_token']


    @staticmethod
    def get_refresh_token(app_id):
        token = Cfg.get_token(app_id)
        return token['refresh_token']


    @staticmethod
    def get_token(app_id):
        cfp = configparser.ConfigParser()
        cfp.read(Cfg.CBI_PRI_DIR + '/oauth2/token_' + app_id + '.ini')
        token = cfp[app_id]
        return token
