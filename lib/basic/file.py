# Author: sphong1
# Class: FILE


from flask import request
import os
import re
import time
from cbi.lib.basic.cfg import Cfg
from cbi.lib.basic.error import Error


class File:
    @classmethod
    def upload_file(cls, **kwargs):
        if 'upload_dir' not in kwargs:
            return Error.get_error('ERR_upload_dir_empty', 'The value of upload_dir is empty.')

        if 'service_dir' not in kwargs:
            return Error.get_error('ERR_service_dir_empty', 'The value of service_dir is empty.')

        if 'input_name' not in kwargs:
            return Error.get_error('ERR_input_name_empty', 'The value of input_name is empty.')

        if 'allowed_extensions' in kwargs:
            allowed_extensions = kwargs['allowed_extensions']
        else:
            allowed_extensions = ['csv', 'jpg', 'pdf', 'png', 'tgz']

        req_file = request.files[kwargs['input_name']]
        raw_file_name = req_file.filename
        if raw_file_name == '':
            return Error.get_error('ERR_filename_empty', 'The value of filename is empty.')

        lower_extension = cls.get_lower_extension(raw_file_name)
        if not cls.is_safe_extension(lower_extension, allowed_extensions):
            return Error.get_error('ERR_extension_not_allowed', 'The extension ' + lower_extension + ' is not allowed.')

        path_file_name, path_file_url = cls.get_path_file(kwargs['upload_dir'], kwargs['service_dir'], lower_extension)
        req_file.save(path_file_name)

        return {
            'path_file_name': path_file_name,
            'path_file_url': path_file_url,
            'raw_file_name': raw_file_name
        }


    @classmethod
    def get_lower_extension(cls, raw_file_name):
        if '.' in raw_file_name:
            lower_extension = raw_file_name.rsplit('.', 1)[1].lower()
        else:
            lower_extension = ''

        return lower_extension


    @classmethod
    def is_safe_extension(cls, lower_extension, allowed_extensions):
        ok = False
        for ext in allowed_extensions:
            ext = ext.lower()
            if lower_extension == ext:
                ok = True
                break

        return ok


    @classmethod
    def get_path_file(cls, upload_dir, service_dir, lower_extension):
        safe_file_name = cls.get_safe_file_name(lower_extension)
        day = safe_file_name[:8]
        dir_name = cls.get_mk_dir_name(upload_dir, service_dir, day)

        path_file_name = os.path.join(dir_name, safe_file_name)
        path_file_url = '/cbi/' + upload_dir + '/' + service_dir + '/' + day + '/' + safe_file_name

        return path_file_name, path_file_url


    @classmethod
    def get_safe_file_name(cls, lower_extension):
        fname1 = time.strftime('%Y%m%d%H%M%S')
        fname2 = os.urandom(16).hex()
        safe_file_name = fname1 + '_' + fname2 + '.' + lower_extension

        return safe_file_name


    @classmethod
    def get_safe_file_name_3(cls, lower_extension):
        remote_addr = request.remote_addr

        fname1 = time.strftime('%Y%m%d%H%M%S')
        fname2 = ''.join([ip.zfill(3) for ip in remote_addr.split('.')])
        fname3 = os.urandom(8).hex()
        safe_file_name = fname1 + '_' + fname2 + '_' + fname3 + '.' + lower_extension

        return safe_file_name


    @classmethod
    def get_mk_dir_name(cls, upload_dir, service_dir, day):
        # Only allow predefined directories for upload purpose.
        # Do not use arbitray directories as an argument.
        if upload_dir == 'pri':
          dname = Cfg.CBI_PRI_DIR
        else:
          dname = Cfg.CBI_PUB_DIR

        dir_name = os.path.join(dname, service_dir, day)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
            os.chmod(dir_name, 0o757)

        return dir_name
