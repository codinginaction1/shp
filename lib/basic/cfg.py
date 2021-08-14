# Author: sphong1
# Class: ConFiGuration


import configparser
import os


class Cfg:
    SHP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    SHP_CFG_DIR = SHP_DIR + '/cfg'
    SHP_LOG_DIR = SHP_DIR + '/log'
    SHP_PRI_DIR = SHP_DIR + '/pri'
    SHP_PUB_DIR = SHP_DIR + '/pub'

    USR_DIR = os.path.dirname(SHP_DIR)

    SHP_APPAPI_URL = 'http://3.35.209.41/shp/appapi'
    SHP_APPATH_URL = 'http://3.35.209.41/shp/appath'
    SHP_APPMGR_URL = 'http://3.35.209.41/shp/appmgr'


    @staticmethod
    def get_ini(filename, section, name=''):
        cfp = configparser.ConfigParser()
        cfp.read(Cfg.SHP_CFG_DIR + '/ini/' + filename)
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
        cfp.read(Cfg.SHP_PRI_DIR + '/oauth2/token_' + app_id + '.ini')
        token = cfp[app_id]
        return token
