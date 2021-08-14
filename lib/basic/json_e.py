# Author: sphong1
# Class: JSON Error


import json
from shp.lib.basic.error import Error


class Json_e:
    @staticmethod
    def loads(text):
        try:
            res = json.loads(text)
        except:
            res = Error.get_error_500()
        return res
