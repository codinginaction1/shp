# Author: sphong1
# Class: VALIDate ScheMA


from marshmallow import validate


class Valid_sma:
    error_messages_int = {'invalid': 'Both the type and the value must be int.'}


    @staticmethod
    def is_dashword():
        return validate.Regexp('^[A-Za-z0-9_\-]+$|^$', error='Only alphabets, digits, underscores, and dashes are allowed.')


    @staticmethod
    def is_digit():
        # type이 str일 떄 숫자(0~9) 패턴인지 확인
        return validate.Regexp('^\d+$|^$', error='Only digits are allowd in the string. (0~9)')


    @staticmethod
    def is_int():
        # type이 str일 떄 정수 패턴인지 확인
        return validate.Regexp('^[\-+]?\d+$|^$', error='Only integer is allowd in the string.')


    @staticmethod
    def is_month():
        return validate.Regexp('^\d{4}[\-.]?\d{2}$|^$', error='Only four-digit year followed by two-digit month is allowed. (YYYYMM, YYYY-MM, YYYY.MM)')


    @staticmethod
    def is_word():
        return validate.Regexp('^[A-Za-z0-9_]+$|^$', error='Only alphabets, digits, and underscores are allowed.')


    @staticmethod
    def get_error(err):
        error = {'error': {'code': 'ERR_SCHEMA', 'message': 'Invalid schema values.', 'detail': err.messages}}
        return error
