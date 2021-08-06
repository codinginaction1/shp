# Author: sphong1


class Error:
    @staticmethod
    def get_error(code, message):
        return {'error': {'code': code, 'message': message}}


    @staticmethod
    def get_error_500():
        return Error.get_error('ERR_HTTP_500', 'internal server error')
