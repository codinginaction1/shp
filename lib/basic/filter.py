# Author: sphong1
# Class: FILTER


import re


class Filter:
    @staticmethod
    def get_digit(string):
        return re.sub('\D', '', string)


    @staticmethod
    def get_word(string):
        return re.sub('[^A-Za-z0-9_]', '', string)
