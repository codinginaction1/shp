# Author: sphong1


import base64
import configparser
from Crypto import Random
from Crypto.Cipher import AES
import os
from shp.lib.basic.cfg import Cfg


class Cipher:
    key = None


    @classmethod
    def init_config(cls):
        # In order to call functions like Cipher.encrypt and Cipher.decrypt for convenience without creating an instance
        # this function is needed instead of __init__.
        # This function is executed actually just once.
        if cls.key is None:
            cfp = configparser.ConfigParser()
            cfp.read(os.path.join(Cfg.SHP_CFG_DIR, 'ini', 'cipher.ini'))
            cf = cfp['cipher']
            # The length of key is 32 in case of AES256.
            cls.key = cf['key']


    @classmethod
    def encrypt(cls, msg, mode='b64'):
        cls.init_config()

        iv = Random.new().read(AES.block_size)
        aes = AES.new(cls.key, AES.MODE_CBC, iv)
        msg_enco = msg.encode() # necessary for multi-byte languages
        msg_enco_pad = cls.pad(msg_enco)
        msg_enco_pad_encr = aes.encrypt(msg_enco_pad)
        iv_msg_enco_pad_encr = iv + msg_enco_pad_encr
        if mode == 'hex':
            iv_msg_enco_pad_encr_ascii = iv_msg_enco_pad_encr.hex()
        else:
            iv_msg_enco_pad_encr_ascii = base64.b64encode(iv_msg_enco_pad_encr).decode()

        return iv_msg_enco_pad_encr_ascii


    @classmethod
    def decrypt(cls, iv_msg_enco_pad_encr_ascii, mode='b64'):
        cls.init_config()

        if mode == 'hex':
            iv_msg_enco_pad_encr = bytes.fromhex(iv_msg_enco_pad_encr_ascii)
        else:
            iv_msg_enco_pad_encr = base64.b64decode(iv_msg_enco_pad_encr_ascii.encode())
        iv = iv_msg_enco_pad_encr[:AES.block_size]
        msg_enco_pad_encr = iv_msg_enco_pad_encr[AES.block_size:]
        aes = AES.new(cls.key, AES.MODE_CBC, iv)
        msg_enco_pad = aes.decrypt(msg_enco_pad_encr)
        msg_enco = cls.unpad(msg_enco_pad)
        msg = msg_enco.decode()

        return msg


    @classmethod
    def pad(cls, msg):
        pad_cnt = AES.block_size - len(msg) % AES.block_size

        return msg + pad_cnt * chr(pad_cnt).encode()


    @classmethod
    def unpad(cls, msg):
        return msg[:-ord(msg[len(msg) - 1:])]
