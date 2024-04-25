# -*- coding: utf-8 -*-

import time
import base64
import hashlib
import traceback
import random


class AuthUtil(object):
    def __init__(self):
        self.secret = '3E5D4C94-A9FE-4690-BEF4-76C40EAE44AB'
        self.user_id = 'qapm'

    def set_secret(self, secret):
        self.secret = secret

    def gen_token(self, expire_sec=3600*24*7):
        user_id = self.user_id
        expire_stamp = str(int(time.time()) + expire_sec)
        rand = random.randint(10000000, 99999999)
        v = "%s||%s%8d%s" % (user_id, expire_stamp, rand, self.secret)
        md5_value = hashlib.md5(v.encode('utf-8')).hexdigest()
        # print "stamp: %s, rand: %s, md5_value: %s" % (stamp, rand, md5_value)
        raw = "%s||%s%8d%s" % (user_id, expire_stamp, rand, md5_value)
        return base64.b64encode(raw.encode('utf-8')).decode('utf-8')


if __name__ == '__main__':
    a = AuthUtil()
    print(a.gen_token())
