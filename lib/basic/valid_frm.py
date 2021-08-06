# Author: sphong1
# Class: VALIDate FoRM


from wtforms import validators


class Valid_frm:
    @staticmethod
    def is_required():
        return validators.InputRequired(message='필수 입력 항목입니다.')


    @staticmethod
    def is_digit():
        # type이 str일 떄 숫자(0~9) 패턴인지 확인
        return validators.Regexp('^\d+$|^$', message='값에 숫자(0~9)만 허용됩니다.')


    @staticmethod
    def is_int():
        # type이 str일 떄 정수 패턴인지 확인
        return validators.Regexp('^[\-+]?\d+$|^$', message='값에 정수만 허용됩니다.')


    @staticmethod
    def is_month():
        return validators.Regexp('^\d{4}[\-.]?\d{2}$|^$', message='네 자리 연도와 두 자리 월의 모양(YYYYMM, YYYY-MM, YYYY.MM)만 허용됩니다.')


    @staticmethod
    def is_word():
        return validators.Regexp('^[A-Za-z0-9_]+$|^$', message='영문자, 숫자, 밑줄만 허용됩니다.')


    @staticmethod
    def get_error(form):
        error = {'error': {'code': 'ERR_FORM', 'message': 'Invalid form values.', 'detail': form.errors}}
        return error

